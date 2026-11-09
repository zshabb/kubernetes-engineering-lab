import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "k8s"


def load_docs(name):
    return [doc for doc in yaml.safe_load_all((ROOT / name).read_text()) if doc]


class ManifestTests(unittest.TestCase):
    def test_tenant_namespaces(self):
        docs = load_docs("01-namespaces.yaml")
        self.assertEqual({d["metadata"]["name"] for d in docs}, {"ai-team-a", "ai-team-b"})

    def test_gpu_quota_separation(self):
        docs = load_docs("02-quotas.yaml")
        budgets = {d["metadata"]["namespace"]: d["spec"]["hard"]["requests.nvidia.com/gpu"] for d in docs}
        self.assertEqual(budgets, {"ai-team-a": "2", "ai-team-b": "1"})

    def test_priority_order(self):
        docs = load_docs("00-priorityclasses.yaml")
        priorities = {d["metadata"]["name"]: d["value"] for d in docs}
        self.assertGreater(priorities["ai-interactive"], priorities["ai-batch"])

    def test_gpu_pod_request_matches_limit(self):
        pod = load_docs("05-gpu-workloads.yaml")[0]
        container = pod["spec"]["containers"][0]
        self.assertEqual(container["resources"]["requests"]["nvidia.com/gpu"], container["resources"]["limits"]["nvidia.com/gpu"])

    def test_cpu_workloads_have_priority(self):
        docs = load_docs("04-cpu-workloads.yaml")
        classes = {d["metadata"]["namespace"]: d["spec"]["template"]["spec"]["priorityClassName"] for d in docs}
        self.assertEqual(classes, {"ai-team-a": "ai-interactive", "ai-team-b": "ai-batch"})


if __name__ == "__main__":
    unittest.main()
