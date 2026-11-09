import unittest
from unittest.mock import Mock
from kubernetes import client
from gpu_operator import desired_job, job_matches, job_owned_by

WORKLOAD = {"metadata": {"name": "example", "uid": "test-uid"},
            "spec": {"gpuCount": 2, "image": "ubuntu:24.04"}}


class OperatorTests(unittest.TestCase):
    def test_job_gpu_request(self):
        job = desired_job(WORKLOAD)
        container = job.spec.template.spec.containers[0]
        self.assertEqual(container.resources.limits["nvidia.com/gpu"], "2")
        self.assertEqual(container.image, "ubuntu:24.04")

    def test_owner_reference(self):
        job = desired_job(WORKLOAD)
        self.assertTrue(job_owned_by(job, WORKLOAD))

    def test_detect_drift(self):
        job = desired_job(WORKLOAD)
        self.assertTrue(job_matches(job, desired_job(WORKLOAD)))
        job.spec.template.spec.containers[0].image = "ubuntu:22.04"
        self.assertFalse(job_matches(job, desired_job(WORKLOAD)))


if __name__ == "__main__":
    unittest.main()
