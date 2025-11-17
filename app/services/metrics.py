from time import perf_counter
from statistics import mean
from typing import List


class MetricsCollector:
    def __init__(self):
        self.latencies: List[float] = []
        self.total_requests: int = 0
        self.failed_requests: int = 0

    def record_request(self, latency: float, success: bool):
        self.latencies.append(latency)
        self.total_requests += 1
        if not success:
            self.failed_requests += 1

    def report(self):
        if not self.latencies:
            return {"p50_ms": None, "p95_ms": None, "failure_rate": 0.0, "total": 0}
        sorted_lats = sorted(self.latencies)
        p50 = sorted_lats[int(0.5 * len(sorted_lats))] * 1000
        p95 = sorted_lats[int(0.95 * len(sorted_lats)) - 1] * 1000 if len(sorted_lats) > 1 else p50
        return {
            "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2),
            "failure_rate": round(self.failed_requests / self.total_requests, 3) if self.total_requests else 0.0,
            "total": self.total_requests,
        }


class Timed:
    def __enter__(self):
        from time import perf_counter
        self._start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        from time import perf_counter
        self.elapsed = perf_counter() - self._start