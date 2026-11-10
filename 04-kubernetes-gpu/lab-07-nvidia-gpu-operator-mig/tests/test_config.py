import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class ConfigurationTests(unittest.TestCase):
    def test_mig_reference_has_safe_annotation(self):
        text = (ROOT / 'configs/mig-strategy.yaml').read_text()
        self.assertIn('reference-only: "true"', text)
        self.assertIn('mig-enabled: true', text)
        self.assertIn('mig-enabled: false', text)

    def test_timeslicing_not_mig(self):
        text = (ROOT / 'configs/time-slicing-reference.yaml').read_text()
        self.assertIn('migStrategy: none', text)
        self.assertIn('replicas: 4', text)
        self.assertIn('renameByDefault: true', text)

    def test_pod_requests_gpu(self):
        text = (ROOT / 'examples/gpu-pod.yaml').read_text()
        self.assertIn('nvidia.com/gpu: 1', text)
        self.assertIn('name: lab07-gpu-request', text)

    def test_verify_script_guards_kind(self):
        text = (ROOT / 'scripts/verify.sh').read_text()
        self.assertIn('kind-*', text)
        self.assertIn('Pending', text)

if __name__ == '__main__':
    unittest.main()
