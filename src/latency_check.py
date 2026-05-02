# PentaV-Kernel-Lab/src/latency_check.py

import time
import numpy as np
import penta_v_kernel as pvk
import inspect

class LatencyMonitor:
    """
    Updated Latency Monitor: Measures timing consistency (determinism) 
    by auto-discovering kernel functions and analyzing nanosecond-level jitter.
    """

    def __init__(self, sample_size=5000):
        self.sample_size = sample_size
        self.kernel_fn = self._discover_kernel_function()

    def _discover_kernel_function(self):
        """Technical Radar: Locates the executable kernel function within the library."""
        for name, func in inspect.getmembers(pvk, inspect.isbuiltin):
            if not name.startswith('_'):
                return func
        for name, func in inspect.getmembers(pvk, inspect.isroutine):
            if not name.startswith('_'):
                return func
        return None

    def measure_precision(self):
        """Executes high-precision latency benchmarks and handles dynamic signatures."""
        if not self.kernel_fn:
            print("❌ Latency Analysis Failed: Target logic not found.")
            return

        print(f"⏱️  Starting Nano-latency Analysis ({self.sample_size} samples)...")
        print(f"⚙️  Profiling Target: {self.kernel_fn.__name__}")
        
        latencies = []

        # Warm-up phase: Stabilize CPU frequency and minimize initial throttling
        try:
            # Try passing positional arguments first (for logic like calculate_impact)
            self.kernel_fn(deficit=1.0, immunity=1.0)
        except TypeError:
            try:
                self.kernel_fn()
            except:
                pass

        # Precision measurement loop
        for _ in range(self.sample_size):
            t1 = time.perf_counter_ns()
            
            try:
                # Attempt call with expected Penta-V parameters
                self.kernel_fn(deficit=1.0, immunity=1.0)
            except TypeError:
                # Fallback for parameterless or standard functions
                try:
                    self.kernel_fn()
                except:
                    continue # Skip failed iterations to avoid skewing data
            
            t2 = time.perf_counter_ns()
            latencies.append(t2 - t1)

        if latencies:
            self._analyze_latencies(latencies)

    def _analyze_latencies(self, data):
        """Analyzes collected latency data to determine silicon-level stability."""
        min_lat = np.min(data)
        max_lat = np.max(data)
        avg_lat = np.mean(data)
        std_dev = np.std(data) # Standard Deviation: The primary enemy of determinism
        jitter = max_lat - min_lat

        print("\n" + "🎯" + " LATENCY & JITTER ANALYSIS " + "🎯")
        print("="*40)
        print(f"🔹 Min Latency      : {min_lat} ns")
        print(f"🔹 Max Latency      : {max_lat} ns")
        print(f"🔹 Avg Latency      : {avg_lat:.2f} ns")
        print(f"🔹 Standard Dev     : {std_dev:.2f} ns")
        print(f"🔹 Total Jitter     : {jitter} ns")
        
        # Engineering Verdict
        if std_dev < 150:
            print("\n✅ Verdict: Ultra-stable Logic. Matches ASIC-level determinism.")
        elif std_dev < 1000:
            print("\nℹ️  Verdict: High-performance software execution.")
        else:
            print("\n⚠️  Verdict: Jitter detected. System noise is affecting the kernel.")
        print("="*40)

if __name__ == "__main__":
    # Standard monitor run with 10,000 samples for statistical significance
    monitor = LatencyMonitor(sample_size=10000)
    monitor.measure_precision()
