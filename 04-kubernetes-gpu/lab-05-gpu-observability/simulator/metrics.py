"""Educational DCGM-like Prometheus exporter; NOT actual NVIDIA measurements."""
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "9400"))
START = time.monotonic()

def render_metrics(elapsed):
    # Deterministic values allow predictable tests and alert exercises.
    util = 60 + int(elapsed / 10) % 35
    used = 20_000 + (int(elapsed / 20) % 15) * 1000
    temp = 55 + int(elapsed / 15) % 25
    return ("# HELP DCGM_FI_DEV_GPU_UTIL Simulated GPU utilization percentage\n"
            "# TYPE DCGM_FI_DEV_GPU_UTIL gauge\n"
            f'DCGM_FI_DEV_GPU_UTIL{{gpu="0",UUID="SIMULATED-H100",device="nvidia0"}} {util}\n'
            "# HELP DCGM_FI_DEV_FB_USED Simulated framebuffer used in MiB\n"
            "# TYPE DCGM_FI_DEV_FB_USED gauge\n"
            f'DCGM_FI_DEV_FB_USED{{gpu="0",UUID="SIMULATED-H100",device="nvidia0"}} {used}\n'
            "# HELP DCGM_FI_DEV_FB_FREE Simulated framebuffer free in MiB\n"
            "# TYPE DCGM_FI_DEV_FB_FREE gauge\n"
            f'DCGM_FI_DEV_FB_FREE{{gpu="0",UUID="SIMULATED-H100",device="nvidia0"}} {81920-used}\n'
            "# HELP DCGM_FI_DEV_GPU_TEMP Simulated GPU temperature in Celsius\n"
            "# TYPE DCGM_FI_DEV_GPU_TEMP gauge\n"
            f'DCGM_FI_DEV_GPU_TEMP{{gpu="0",UUID="SIMULATED-H100",device="nvidia0"}} {temp}\n'
            "# HELP gpu_simulator_up Simulator liveness gauge\n"
            "# TYPE gpu_simulator_up gauge\n"
            'gpu_simulator_up 1\n')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            body = b'ok\n'; code=200; kind='text/plain'
        elif self.path == '/metrics':
            body = render_metrics(time.monotonic()-START).encode(); code=200; kind='text/plain; version=0.0.4; charset=utf-8'
        else:
            body=b'not found\n'; code=404; kind='text/plain'
        self.send_response(code)
        self.send_header('Content-Type',kind)
        self.send_header('Content-Length',str(len(body)))
        self.end_headers();self.wfile.write(body)

if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
