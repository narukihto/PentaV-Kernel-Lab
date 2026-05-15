"""
Performance benchmarks for the Penta-V Kernel.

These benchmarks measure the core `calculate_impact` function from
penta_v_kernel across a range of input scenarios representative of
real workloads.
"""

import pytest
import penta_v_kernel as pvk


# ---------------------------------------------------------------------------
# Single-call benchmarks — exercise the kernel with representative inputs
# ---------------------------------------------------------------------------


def test_bench_calculate_impact_balanced(benchmark):
    """Balanced deficit/immunity values (typical workload)."""
    benchmark(pvk.calculate_impact, deficit=1.0, immunity=1.0)


def test_bench_calculate_impact_low_deficit(benchmark):
    """Low deficit with moderate immunity."""
    benchmark(pvk.calculate_impact, deficit=0.001, immunity=0.999)


def test_bench_calculate_impact_high_deficit(benchmark):
    """High deficit against high immunity."""
    benchmark(pvk.calculate_impact, deficit=100.0, immunity=50.0)


def test_bench_calculate_impact_zero_deficit(benchmark):
    """Zero deficit edge case."""
    benchmark(pvk.calculate_impact, deficit=0.0, immunity=1.0)


def test_bench_calculate_impact_fractional(benchmark):
    """Fractional inputs simulating fine-grained analysis."""
    benchmark(pvk.calculate_impact, deficit=0.5, immunity=0.8)


# ---------------------------------------------------------------------------
# Batch benchmarks — simulate throughput-oriented workloads
# ---------------------------------------------------------------------------


def _batch_uniform(n):
    """Run calculate_impact n times with uniform parameters."""
    fn = pvk.calculate_impact
    for _ in range(n):
        fn(deficit=1.0, immunity=1.0)


def _batch_varying(n):
    """Run calculate_impact n times with varying parameters."""
    fn = pvk.calculate_impact
    for i in range(1, n + 1):
        fn(deficit=float(i), immunity=float(n - i + 1))


def test_bench_batch_1k_uniform(benchmark):
    """1 000 uniform calls — measures raw throughput."""
    benchmark(_batch_uniform, 1_000)


def test_bench_batch_1k_varying(benchmark):
    """1 000 calls with varying inputs — measures throughput under input diversity."""
    benchmark(_batch_varying, 1_000)


def test_bench_batch_10k_uniform(benchmark):
    """10 000 uniform calls — sustained throughput."""
    benchmark(_batch_uniform, 10_000)
