# PentaV-Kernel-Lab/src/latency_check.py

import time
import numpy as np
import penta_v_kernel as pvk
import inspect

class LatencyMonitor:
    """
    مراقب التأخير المحدث: يقيس استقرار التوقيت (Determinism) 
    عبر اكتشاف دوال النواة تلقائياً وتحليل الانحراف المعياري بالنانو ثانية.
    """

    def __init__(self, sample_size=5000):
        self.sample_size = sample_size
        self.kernel_fn = self._discover_kernel_function()

    def _discover_kernel_function(self):
        """الرادار التقني: العثور على الدالة القابلة للتنفيذ داخل النواة"""
        for name, func in inspect.getmembers(pvk, inspect.isbuiltin):
            if not name.startswith('_'):
                return func
        for name, func in inspect.getmembers(pvk, inspect.isroutine):
            if not name.startswith('_'):
                return func
        return None

    def measure_precision(self):
        if not self.kernel_fn:
            print("❌ Latency Analysis Failed: Target logic not found.")
            return

        print(f"⏱️  Starting Nano-latency Analysis ({self.sample_size} samples)...")
        print(f"⚙️  Profiling Target: {self.kernel_fn.__name__}")
        
        latencies = []

        # تسخين المعالج (Warm-up) لضمان استقرار التردد ومنع الـ CPU Throttling
        try:
            try:
                self.kernel_fn(1000)
            except TypeError:
                for _ in range(100): self.kernel_fn()
        except:
            pass

        # حلقة القياس الدقيقة
        for _ in range(self.sample_size):
            t1 = time.perf_counter_ns()
            
            try:
                # تنفيذ أصغر وحدة عمل ممكنة
                self.kernel_fn() if hasattr(self.kernel_fn, '__call__') else None
            except TypeError:
                self.kernel_fn(1) # بعض الدوال تتطلب وسيطاً عددياً
            
            t2 = time.perf_counter_ns()
            latencies.append(t2 - t1)

        if latencies:
            self._analyze_latencies(latencies)

    def _analyze_latencies(self, data):
        # حساب الإحصائيات الحيوية للـ ASIC Logic
        min_lat = np.min(data)
        max_lat = np.max(data)
        avg_lat = np.mean(data)
        std_dev = np.std(data) # الانحراف المعياري (العدو الأول للـ ASIC)
        jitter = max_lat - min_lat

        print("\n" + "🎯" + " LATENCY & JITTER ANALYSIS " + "🎯")
        print("="*40)
        print(f"🔹 Min Latency      : {min_lat} ns")
        print(f"🔹 Max Latency      : {max_lat} ns")
        print(f"🔹 Avg Latency      : {avg_lat:.2f} ns")
        print(f"🔹 Standard Dev     : {std_dev:.2f} ns")
        print(f"🔹 Total Jitter     : {jitter} ns")
        
        # الحكم الهندسي (Verdict)
        if std_dev < 150:
            print("\n✅ Verdict: Ultra-stable Logic. Matches ASIC-level determinism.")
        elif std_dev < 1000:
            print("\nℹ️  Verdict: High-performance software execution.")
        else:
            print("\n⚠️  Verdict: Jitter detected. System noise is affecting the kernel.")
        print("="*40)

if __name__ == "__main__":
    monitor = LatencyMonitor(sample_size=10000)
    monitor.measure_precision()
