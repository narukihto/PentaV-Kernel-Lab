# PentaV-Kernel-Lab/src/__init__.py

"""
Penta-V Kernel Lab: High-Performance Processor Logic Evaluation
--------------------------------------------------------------
مختبر تقييم الأداء لنواة المعالج المعتمدة على منطق الهندسة والرياضيات.
يركز هذا المختبر على قياس سرعة المعالجة (Throughput) واستقرار التوقيت (Jitter).
"""

__version__ = "2.0.0"  # نسخة المعالج
__author__ = "Issaclex System Analyst"

# استدعاء الكلاسات الرئيسية من الملفات الفرعية لسهولة الاستخدام من خارج المجلد
from .core_stress import CoreStressTester
from .latency_check import LatencyMonitor
from .power_efficiency import EfficiencyTracker

# تحديد ما سيتم تصديره عند استخدام (from src import *)
__all__ = [
    "CoreStressTester",
    "LatencyMonitor",
    "EfficiencyTracker"
]

def get_lab_status():
    """دالة برمجية للتأكد من جاهزية بيئة الاختبار"""
    return f"🛡️ Penta-V Lab is active. Logic Engine: pvk (Rust/ASIC-Based)"

# طباعة رسالة ترحيبية عند التهيئة (اختياري)
print(get_lab_status())
