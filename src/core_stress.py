# PentaV-Kernel-Lab/src/core_stress.py

import time
import psutil
import penta_v_kernel as pvk

class CoreStressTester:
    """
    مختبر الضغط الجوهري: يركز على قياس الـ Throughput (الإنتاجية) 
    للمعالج عند تنفيذ ملايين العمليات الرياضية والهندسية.
    """

    def __init__(self, default_iterations=1_000_000):
        self.default_iterations = default_iterations
        self.process = psutil.Process()

    def run_benchmark(self, iterations=None):
        """
        ينفذ اختبار الضغط ويسجل البيانات التقنية للأداء.
        """
        iters = iterations if iterations else self.default_iterations
        print(f"🔥 Initializing Core Stress Test: {iters:,} operations...")

        # تسجيل استهلاك الموارد قبل البدء
        cpu_before = psutil.cpu_percent(interval=None)
        mem_before = self.process.memory_info().rss / 1024**2
        
        start_time = time.perf_counter()

        try:
            # تشغيل منطق النواة (الذي يفترض أنه مترجم من HDL لـ Rust)
            # استبدل 'run_core_logic' بالدالة الأساسية في المكتبة
            pvk.run_core_logic(iters)
            
            end_time = time.perf_counter()
            duration = end_time - start_time
            
            # تسجيل الاستهلاك بعد الاختبار
            mem_after = self.process.memory_info().rss / 1024**2
            cpu_after = psutil.cpu_percent(interval=None)

            self._display_results(iters, duration, mem_before, mem_after, cpu_after)
            return duration

        except Exception as e:
            print(f"❌ Core Stress Failure: {e}")
            return None

    def _display_results(self, iters, duration, m_init, m_final, cpu_usage):
        ops_per_sec = iters / duration
        print("\n" + "🚀" + " CORE PERFORMANCE DATA " + "🚀")
        print("="*40)
        print(f"⏱️  Total Duration    : {duration:.6f} seconds")
        print(f"⚙️  Processing Speed  : {ops_per_sec:,.0f} ops/sec")
        print(f"💾 Memory Stability  : {m_final - m_init:.4f} MB Delta")
        print(f"📈 CPU Load Observed : {cpu_usage}%")
        
        # التقييم بناءً على معايير الـ ASIC
        if ops_per_sec > 1_000_000:
            print("\n✅ Verdict: High-Efficiency Silicon Logic. Native-level speed.")
        else:
            print("\n⚠️ Verdict: Sub-optimal throughput for ASIC logic.")
        print("="*40)

if __name__ == "__main__":
    # تجربة افتراضية بـ 2 مليون عملية
    tester = CoreStressTester()
    tester.run_benchmark(iterations=2_000_000)
