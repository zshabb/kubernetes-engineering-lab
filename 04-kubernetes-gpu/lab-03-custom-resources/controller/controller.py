
import argparse
import time

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

GROUP = "training.example.com"
VERSION = "v1"
PLURAL = "gpuworkloads"
NAMESPACE = "default"
WORKLOAD_NAME = "h100-inference"

DELETE_TIMEOUT = 60


def get_workload(custom_api):
    return custom_api.get_namespaced_custom_object(
        group=GROUP,
        version=VERSION,
        namespace=NAMESPACE,
        plural=PLURAL,
        name=WORKLOAD_NAME,
    )


def owns_job(job, workload_uid):
    owners = job.metadata.owner_references or []

    return any(
        owner.uid == workload_uid
        and owner.kind == "GPUWorkload"
        and owner.name == WORKLOAD_NAME
        and owner.api_version == f"{GROUP}/{VERSION}"
        and owner.controller is True
        for owner in owners
    )


def create_job(batch_api, workload):
    spec = workload["spec"]
    gpu_count = spec["gpuCount"]
    image = spec["image"]
    workload_uid = workload["metadata"]["uid"]

    job_name = f"{WORKLOAD_NAME}-job"

    container = client.V1Container(
        name="gpu-worker",
        image=image,
        command=[
            "sh", "-c",
            "echo GPU workload started; sleep 60"
        ],
        resources=client.V1ResourceRequirements(
            limits={"nvidia.com/gpu": str(gpu_count)}
        ),
    )

    pod_spec = client.V1PodSpec(
        restart_policy="Never",
        containers=[container],
    )

    owner_reference = client.V1OwnerReference(
        api_version=f"{GROUP}/{VERSION}",
        kind="GPUWorkload",
        name=WORKLOAD_NAME,
        uid=workload_uid,
        controller=True,
        block_owner_deletion=True,
    )

    job = client.V1Job(
        metadata=client.V1ObjectMeta(
            name=job_name,
            owner_references=[owner_reference],
        ),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=pod_spec
            ),
            backoff_limit=1,
        ),
    )

    batch_api.create_namespaced_job(
        namespace=NAMESPACE,
        body=job,
    )

    print(f"Created Kubernetes Job: {job_name}")


def get_job_pods(core_api, job):
    return core_api.list_namespaced_pod(
        namespace=NAMESPACE,
        label_selector=(
            f"batch.kubernetes.io/controller-uid={job.metadata.uid}"
        ),
    ).items


def replacement_eligible(job, pods):
    if job.metadata.deletion_timestamp:
        print("BLOCKED: Job is already terminating")
        return False

    if job.status.conditions:
        print("BLOCKED: Job has lifecycle conditions")
        return False

    if not pods:
        print("BLOCKED: No Pods found")
        return False

    for pod in pods:
        phase = pod.status.phase

        print(f"Pod {pod.metadata.name}: {phase}")

        if phase != "Pending":
            print("BLOCKED: Pod is not Pending")
            return False

        if pod.spec.node_name:
            print("BLOCKED: Pod is assigned to a node")
            return False

        if pod.metadata.deletion_timestamp:
            print("BLOCKED: Pod is terminating")
            return False

        owners = pod.metadata.owner_references or []

        if not any(
            owner.uid == job.metadata.uid
            and owner.kind == "Job"
            for owner in owners
        ):
            print("BLOCKED: Pod ownership mismatch")
            return False

    return True


def delete_job_and_wait(batch_api, core_api, job):
    job_name = job.metadata.name
    job_uid = job.metadata.uid

    print(f"Deleting Job: {job_name}")

    batch_api.delete_namespaced_job(
        name=job_name,
        namespace=NAMESPACE,
        body=client.V1DeleteOptions(
            propagation_policy="Foreground",
            preconditions=client.V1Preconditions(
                uid=job_uid,
            ),
        ),
    )

    deadline = time.monotonic() + DELETE_TIMEOUT

    while time.monotonic() < deadline:
        try:
            batch_api.read_namespaced_job(
                name=job_name,
                namespace=NAMESPACE,
            )
        except ApiException as error:
            if error.status == 404:
                remaining = get_job_pods(core_api, job)

                if not remaining:
                    print("Old Job and Pods deleted")
                    return

            else:
                raise

        time.sleep(2)

    raise TimeoutError(
        f"Timed out waiting for deletion of {job_name}"
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--approve-replacement",
        action="store_true",
        help="Approve replacement of an eligible Pending Job",
    )

    args = parser.parse_args()

    config.load_kube_config()

    custom_api = client.CustomObjectsApi()
    batch_api = client.BatchV1Api()
    core_api = client.CoreV1Api()

    workload = get_workload(custom_api)

    spec = workload["spec"]
    desired_gpu_count = spec["gpuCount"]
    desired_image = spec["image"]
    workload_uid = workload["metadata"]["uid"]

    job_name = f"{WORKLOAD_NAME}-job"

    print(f"GPUWorkload: {WORKLOAD_NAME}")
    print(f"Desired GPUs: {desired_gpu_count}")
    print(f"Desired image: {desired_image}")

    try:
        existing_job = batch_api.read_namespaced_job(
            name=job_name,
            namespace=NAMESPACE,
        )

    except ApiException as error:
        if error.status != 404:
            raise

        print("No existing Job found")
        create_job(batch_api, workload)
        return

    if not owns_job(existing_job, workload_uid):
        print("SAFETY BLOCK: Job ownership mismatch")
        print("Refusing to modify an unowned Job")
        return

    container = existing_job.spec.template.spec.containers[0]

    actual_gpu_count = int(
        container.resources.limits.get("nvidia.com/gpu", 0)
    )

    actual_image = container.image

    gpu_drift = actual_gpu_count != desired_gpu_count
    image_drift = actual_image != desired_image

    if not gpu_drift and not image_drift:
        print("Job is synchronized")
        return

    print("CONFIGURATION DRIFT DETECTED")
    print(
        f"GPU count: {actual_gpu_count} -> {desired_gpu_count}"
    )
    print(
        f"Image: {actual_image} -> {desired_image}"
    )

    pods = get_job_pods(core_api, existing_job)

    if not replacement_eligible(existing_job, pods):
        print("Replacement denied by safety checks")
        return

    if not args.approve_replacement:
        print("Replacement requires --approve-replacement")
        return

    print("Replacement approved")

    # Recheck the Job UID and Pod state immediately before deletion.
    latest_job = batch_api.read_namespaced_job(
        name=job_name,
        namespace=NAMESPACE,
    )

    if latest_job.metadata.uid != existing_job.metadata.uid:
        print("BLOCKED: Job changed during reconciliation")
        return

    if not owns_job(latest_job, workload_uid):
        print("BLOCKED: Job ownership changed")
        return

    latest_pods = get_job_pods(core_api, latest_job)

    if not replacement_eligible(latest_job, latest_pods):
        print("BLOCKED: Pod state changed")
        return

    latest_workload = get_workload(custom_api)

    if (
        latest_workload["metadata"]["uid"] != workload_uid
        or latest_workload["metadata"]["generation"]
        != workload["metadata"]["generation"]
    ):
        print("BLOCKED: GPUWorkload changed during reconciliation")
        return

    delete_job_and_wait(batch_api, core_api, latest_job)

    # Avoid recreating a Job if the custom resource changed
    # while deletion was in progress.
    final_workload = get_workload(custom_api)

    if (
        final_workload["metadata"]["uid"] != workload_uid
        or final_workload["metadata"]["generation"]
        != workload["metadata"]["generation"]
    ):
        print("GPUWorkload changed; skipping Job recreation")
        return

    create_job(batch_api, final_workload)

    print("Reconciliation complete")


if __name__ == "__main__":
    main()
