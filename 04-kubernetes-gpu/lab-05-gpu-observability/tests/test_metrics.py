import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'simulator'))
from metrics import render_metrics

class TestMetrics(unittest.TestCase):
    def test_gpu_utilization_range(self):
        for t in (0, 100, 500, 10000):
            output = render_metrics(t)
            line = next(line for line in output.splitlines() if line.startswith('DCGM_FI_DEV_GPU_UTIL{'))
            self.assertLessEqual(float(line.split()[-1]), 100)
            self.assertGreaterEqual(float(line.split()[-1]), 0)
    def test_memory_totals(self):
        output = render_metrics(200)
        used = next(float(x.split()[-1]) for x in output.splitlines() if x.startswith('DCGM_FI_DEV_FB_USED{'))
        free = next(float(x.split()[-1]) for x in output.splitlines() if x.startswith('DCGM_FI_DEV_FB_FREE{'))
        self.assertEqual(used+free, 81920)
    def test_exposes_expected_metrics(self):
        output = render_metrics(0)
        for metric in ('DCGM_FI_DEV_GPU_UTIL','DCGM_FI_DEV_FB_USED','DCGM_FI_DEV_FB_FREE','DCGM_FI_DEV_GPU_TEMP','gpu_simulator_up'):
            self.assertIn(metric,output)

if __name__ == '__main__': unittest.main()
