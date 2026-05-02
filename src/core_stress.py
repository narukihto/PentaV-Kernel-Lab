# PentaV-Kernel-Lab/src/core_stress.py

import time
import psutil
import penta_v_kernel as pvk
import inspect

class CoreStressTester:
    """
    مختبر الضغط الجوهري المحدث: يكتشف دوال النواة تلقائياً ويقيس أداء السيليكون.
    """

    def __init__(self, default_iterations=1_000_000):
        self.default_iterations = default_iterations
        self.process = psutil.Process()
        self.kernel_fn = self._discover_kernel_function()

    def _discover_kernel_function(self):
        """يبحث عن الدالة القابلة للاستدعاء داخل المكتبة"""
        # استبعاد الدوال الداخلية (التي تبدأ بـ _) والبحث عن أول دالة متاحة
        for name, func in inspect.getmembers(pvk, inspect.isbuiltin):
            if not name.startswith('_'):
                return func
        for name, func in inspect.getmembers(pvk, inspect.isroutine):
            if not name.startswith('_'):
                return func
        return None

    def run_benchmark(self, iterations=None):
        iters = iterations if iterations else self.default_iterations
        
        if not self.kernel_fn:
            print("❌ Error: No executable function found in penta_v_kernel!")
            return None

        print(f"🔥 Initializing Core Stress Test: {iters:,} operations...")
        print(f"⚙️  Detected Function: {self.kernel_fn.__name__}")

        # تسجيل الحالة الأولية
        cpu_before = psutil.cpu_percent(interval=None)
        mem_before = self.process.memory_info().rss / 1024**2
        
        start_time = time.perf_counter()

        try:
            # تنفيذ الدالة المكتشفة تلقائياً
            # إذا كانت الدالة لا تقبل الوسيط 'iters'، سنقوم بتكرارها يدوياً
            try:
                self.kernel_fn(iters)
            except TypeError:
                for _ in range(iters):
                    self.kernel_fn()
            
            end_time = time.perf_counter()
            duration = end_time - start_time
            
            # تسجيل الحالة النهائية
            mem_after = self.process.memory_info().rss / 1024**2
            cpu_after = psutil.cpu_percent(interval=None)

            self._display_results(iters, duration, mem_before, mem_after, cpu_after)
            return duration

        except Exception as e:
            print(f"❌ Core Stress Failure: {e}")
            return None

    def _display_results(self, iters, duration, m_init, m_final, cpu_usage):
        # منع القسمة على صفر في حال كان التنفيذ فائق السرعة
        safe_duration = max(duration, 0.000001)
        ops_per_sec = iters / safe_duration
        
        print("\n" + "🚀" + " CORE PERFORMANCE DATA " + "🚀")
        print("="*40)
        print(f"⏱️  Total Duration    : {duration:.6f} seconds")
        print(f"⚙️  Processing Speed  : {ops_per_sec:,.0f} ops/sec")
        print(f"💾 Memory Stability  : {m_final - m_init:.4f} MB Delta")
        print(f"📈 CPU Load Observed : {cpu_usage}%")
        
        if ops_per_sec > 1_000_000:
            print("\n✅ Verdict: High-Efficiency Silicon Logic. Native-level speed.")
        else:
            print("\n⚠️ Verdict: Sub-optimal throughput.")
        print("="*40)

if __name__ == "__main__":
    tester = CoreStressTester()
    tester.run_benchmark(iterations=2_000_000)
