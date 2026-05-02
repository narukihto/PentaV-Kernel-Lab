# PentaV-Kernel-Lab/src/latency_check.py

import time
import numpy as np
import penta_v_kernel as pvk

class LatencyMonitor:
    """
    مراقب التأخير: يقيس استقرار التوقيت (Timing Consistency) 
    ودقة الاستجابة للعمليات الفردية بنظام النانو ثانية.
    """

    def __init__(self, sample_size=5000):
        self.sample_size = sample_size

    def measure_precision(self):
        print(f"⏱️  Starting Nano-latency Analysis ({self.sample_size} samples)...")
        
        latencies = []

        # تسخين المعالج (Warm-up) لضمان استقرار التردد
        pvk.run_core_logic(1000)

        for _ in range(self.sample_size):
            t1 = time.perf_counter_ns()  # قياس بدقة النانو ثانية
            
            # تنفيذ عملية واحدة صغرى (Atomic Operation)
            pvk.run_core_logic(1) 
            
            t2 = time.perf_counter_ns()
            latencies.append(t2 - t1)

        self._analyze_latencies(latencies)

    def _analyze_latencies(self, data):
        # حساب الإحصائيات الحيوية للـ ASIC Logic
        min_lat = np.min(data)
        max_lat = np.max(data)
        avg_lat = np.mean(data)
        std_dev = np.std(data) # الانحراف المعياري
        jitter = max_lat - min_lat

        print("\n" + "🎯" + " LATENCY & JITTER ANALYSIS " + "🎯")
        print("="*40)
        print(f"🔹 Min Latency      : {min_lat} ns")
        print(f"🔹 Max Latency      : {max_lat} ns")
        print(f"🔹 Avg Latency      : {avg_lat:.2f} ns")
        print(f"🔹 Standard Dev     : {std_dev:.2f} ns")
        print(f"🔹 Total Jitter     : {jitter} ns")
        
        # الحكم التقني (Verdict)
        if std_dev < 100:
            print("\n✅ Verdict: Ultra-stable Logic. This matches ASIC-level determinism.")
        elif std_dev < 500:
            print("\nℹ️  Verdict: High-performance software timing.")
        else:
            print("\n⚠️  Verdict: High jitter detected. OS interrupts are affecting the kernel.")
        print("="*40)

if __name__ == "__main__":
    monitor = LatencyMonitor(sample_size=10000)
    monitor.measure_precision()
