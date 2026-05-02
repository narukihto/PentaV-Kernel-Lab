# PentaV-Kernel-Lab/src/power_efficiency.py

import time
import psutil
import penta_v_kernel as pvk

class EfficiencyTracker:
    """
    متتبع الكفاءة: يقيس مدى اقتصادية النواة في استهلاك موارد النظام.
    الهدف: إثبات أن منطق الـ ASIC يقلل من "الحمل الضائع" (Overhead).
    """

    def __init__(self):
        self.process = psutil.Process()

    def track_resource_impact(self, workload=1_000_000):
        print(f"🔋 Analyzing Power Efficiency Proxy for {workload:,} ops...")
        
        # الحالة الصفرية (Baseline)
        initial_mem = self.process.memory_info().rss
        initial_cpu_times = self.process.cpu_times()
        
        start_time = time.perf_counter()
        
        # تشغيل النواة
        pvk.run_core_logic(workload)
        
        end_time = time.perf_counter()
        
        # القياس بعد التنفيذ
        final_mem = self.process.memory_info().rss
        final_cpu_times = self.process.cpu_times()
        
        duration = end_time - start_time
        self._report_efficiency(initial_cpu_times, final_cpu_times, initial_mem, final_mem, duration)

    def _report_efficiency(self, cpu_start, cpu_end, mem_start, mem_final, duration):
        # حساب وقت المعالج الحقيقي (User + System time)
        user_time = cpu_end.user - cpu_start.user
        system_time = cpu_end.system - cpu_start.system
        total_cpu_time = user_time + system_time
        
        # كفاءة التنفيذ: نسبة الوقت الذي قضاه المعالج فعلياً في الكود مقابل وقت الانتظار
        efficiency_ratio = (total_cpu_time / duration) * 100 if duration > 0 else 0
        mem_delta = mem_final - mem_start

        print("\n" + "🍃" + " RESOURCE EFFICIENCY REPORT " + "🍃")
        print("="*40)
        print(f"⏱️  Real CPU Work Time : {total_cpu_time:.6f} s")
        print(f"📉 System Overhead    : {system_time:.6f} s")
        print(f"💾 Memory Pressure    : {mem_delta / 1024:.2f} KB")
        print(f"⚡ CPU Utilization    : {efficiency_ratio:.2f}%")
        
        # التقييم التقني
        if system_time < (user_time * 0.1):
            print("\n✅ Verdict: Ultra-efficient. Minimal OS intervention (Pure Logic).")
        else:
            print("\n⚠️  Verdict: High System Overhead. Kernel is fighting with the OS.")
        print("="*40)

if __name__ == "__main__":
    tracker = EfficiencyTracker()
    tracker.track_resource_impact(workload=5_000_000)
