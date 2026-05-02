# PentaV-Kernel-Lab/src/power_efficiency.py

import time
import psutil
import penta_v_kernel as pvk
import inspect

class EfficiencyTracker:
    """
    متتبع الكفاءة المحدث: يكتشف دوال النواة تلقائياً ويقيس مدى 
    اقتصادية المنطق الهندسي في استهلاك موارد النظام.
    """

    def __init__(self):
        self.process = psutil.Process()
        self.kernel_fn = self._discover_kernel_function()

    def _discover_kernel_function(self):
        """اكتشاف الدالة الأساسية للنواة برمجياً"""
        # البحث في الدوال المدمجة (Built-in) أو الروتينية
        for name, func in inspect.getmembers(pvk, inspect.isbuiltin):
            if not name.startswith('_'):
                return func
        for name, func in inspect.getmembers(pvk, inspect.isroutine):
            if not name.startswith('_'):
                return func
        return None

    def track_resource_impact(self, workload=1_000_000):
        if not self.kernel_fn:
            print("❌ Efficiency Track Failed: No executable function found.")
            return

        print(f"🔋 Analyzing Power Efficiency Proxy for {workload:,} ops...")
        print(f"⚙️  Testing Logic: {self.kernel_fn.__name__}")
        
        # الحالة الصفرية (Baseline)
        initial_mem = self.process.memory_info().rss
        initial_cpu_times = self.process.cpu_times()
        
        start_time = time.perf_counter()
        
        try:
            # محاولة التنفيذ المباشر أو التكراري حسب نوع الدالة
            try:
                self.kernel_fn(workload)
            except TypeError:
                for _ in range(workload):
                    self.kernel_fn()
                    
            end_time = time.perf_counter()
            
            # القياس بعد التنفيذ
            final_mem = self.process.memory_info().rss
            final_cpu_times = self.process.cpu_times()
            
            duration = end_time - start_time
            self._report_efficiency(initial_cpu_times, final_cpu_times, initial_mem, final_mem, duration)

        except Exception as e:
            print(f"❌ Efficiency Trace Interrupted: {e}")

    def _report_efficiency(self, cpu_start, cpu_end, mem_start, mem_final, duration):
        # حساب وقت المعالج الحقيقي (User + System time)
        user_time = max(cpu_end.user - cpu_start.user, 0.0)
        system_time = max(cpu_end.system - cpu_start.system, 0.0)
        total_cpu_time = user_time + system_time
        
        # كفاءة التنفيذ
        safe_duration = max(duration, 0.000001)
        efficiency_ratio = (total_cpu_time / safe_duration) * 100
        mem_delta = mem_final - mem_start

        print("\n" + "🍃" + " RESOURCE EFFICIENCY REPORT " + "🍃")
        print("="*40)
        print(f"⏱️  Real CPU Work Time : {total_cpu_time:.6f} s")
        print(f"📉 System Overhead    : {system_time:.6f} s")
        print(f"💾 Memory Pressure    : {mem_delta / 1024:.2f} KB")
        print(f"⚡ CPU Utilization    : {min(efficiency_ratio, 100.0):.2f}%")
        
        # التقييم التقني بناءً على تدخل النظام
        if system_time < (user_time * 0.15) or system_time < 0.001:
            print("\n✅ Verdict: Ultra-efficient. Minimal OS intervention (Pure Logic).")
        else:
            print("\n⚠️  Verdict: Moderate Overhead. Potential OS context switching.")
        print("="*40)

if __name__ == "__main__":
    tracker = EfficiencyTracker()
    tracker.track_resource_impact(workload=5_000_000)
