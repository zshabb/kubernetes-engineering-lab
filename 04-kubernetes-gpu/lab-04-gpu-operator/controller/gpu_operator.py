"""Educational GPUWorkload operator: create missing Jobs, report drift, never delete."""
import logging
import os
import time
from kubernetes import client, config, watch
from kubernetes.client.exceptions import ApiException

LOG = logging.getLogger("gpu-operator")
GROUP = "training.example.com"
VERSION = "v1"
PLURAL = "gpuworkloads"
NAMESPACE = os.environ.get("WATCH_NAMESPACE", "default")
RESYNC_SECONDS = 30


def desired_job(workload):
    name = workload["metadata"]["name"]
    uid = workload["metadata"]["uid"]
    spec = workload["spec"]
    return client.V1Job(
        metadata=client.V1ObjectMeta(
            name=f"{name}-job",
            owner_references=[client.V1OwnerReference(
                api_version=f"{GROUP}/{VERSION}", kind="GPUWorkload",
                name=name, uid=uid, controller=True, block_owner_deletion=True,
            )],
            labels={"app.kubernetes.io/managed-by": "gpuworkload-operator"},
        ),
        spec=client.V1JobSpec(
            backoff_limit=1,
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    restart_policy="Never",
                    containers=[client.V1Container(
                        name="gpu-worker", image=spec["image"],
                        command=["sh", "-c", "echo GPU workload started; sleep 60"],
                        resources=client.V1ResourceRequirements(
                            limits={"nvidia.com/gpu": str(spec["gpuCount"])}
                        ),
                    )],
                )
            ),
        ),
    )


def job_owned_by(job, workload):
    return any(
        ref.uid == workload["metadata"]["uid"]
        and ref.name == workload["metadata"]["name"]
        and ref.kind == "GPUWorkload"
        and ref.api_version == f"{GROUP}/{VERSION}"
        and ref.controller is True
        for ref in (job.metadata.owner_references or [])
    )


def job_matches(job, desired):
    current = job.spec.template.spec.containers[0]
    target = desired.spec.template.spec.containers[0]
    limits = current.resources.limits if current.resources else {}
    return (current.image == target.image and
            str((limits or {}).get("nvidia.com/gpu", "")) ==
            str(target.resources.limits["nvidia.com/gpu"]))


def reconcile(batch_api, workload):
    name = workload["metadata"]["name"]
    desired = desired_job(workload)
    job_name = desired.metadata.name
    try:
        existing = batch_api.read_namespaced_job(job_name, NAMESPACE)
    except ApiException as exc:
        if exc.status != 404:
            raise
        try:
            batch_api.create_namespaced_job(NAMESPACE, desired)
            LOG.info("Created Job %s for GPUWorkload %s", job_name, name)
        except ApiException as create_exc:
            if create_exc.status != 409:
                raise
            LOG.info("Job %s was created concurrently; will recheck", job_name)
        return
    if not job_owned_by(existing, workload):
        LOG.error("Ownership mismatch for %s; refusing modification", job_name)
    elif not job_matches(existing, desired):
        LOG.warning("Drift detected for %s; manual replacement required", job_name)
    else:
        LOG.info("Job %s synchronized", job_name)


def reconcile_all(custom_api, batch_api):
    result = custom_api.list_namespaced_custom_object(
        GROUP, VERSION, NAMESPACE, PLURAL
    )
    for workload in result.get("items", []):
        try:
            reconcile(batch_api, workload)
        except Exception:
            LOG.exception("Reconciliation failed for %s", workload["metadata"]["name"])


def run():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        config.load_incluster_config()
        LOG.info("Using in-cluster Kubernetes credentials")
    except config.ConfigException:
        config.load_kube_config()
        LOG.info("Using local kubeconfig")
    custom_api = client.CustomObjectsApi()
    batch_api = client.BatchV1Api()
    while True:
        try:
            reconcile_all(custom_api, batch_api)
            stream = watch.Watch()
            try:
                for event in stream.stream(
                    custom_api.list_namespaced_custom_object,
                    GROUP, VERSION, NAMESPACE, PLURAL,
                    timeout_seconds=RESYNC_SECONDS,
                ):
                    if event["type"] in ("ADDED", "MODIFIED"):
                        reconcile(batch_api, event["object"])
                    # Deleted resources are garbage-collected via owner references.
            finally:
                stream.stop()
        except Exception:
            LOG.exception("Watch/reconcile error; retrying in 5 seconds")
            time.sleep(5)


if __name__ == "__main__":
    run()
