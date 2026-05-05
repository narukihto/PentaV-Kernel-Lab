# PentaV-Kernel-Lab

[![CodSpeed](https://img.shields.io/endpoint?url=https://codspeed.io/badge.json)](https://codspeed.io/narukihto/PentaV-Kernel-Lab?utm_source=badge)

High-performance processor logic evaluation lab. Measures throughput, latency consistency, and resource efficiency of the Penta-V kernel engine.

## Setup

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
python scripts/run_all_tests.py
```

## Benchmarks

Performance benchmarks are located in `tests/test_benchmarks.py` and are tracked continuously with [CodSpeed](https://codspeed.io).

To run benchmarks locally:

```bash
pip install pytest pytest-codspeed
pytest tests/test_benchmarks.py
```
