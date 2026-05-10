"""Habilita coverage automaticamente em subprocess (testes que invocam bin/visa).

Pyproject.toml configurou parallel=true e concurrency=multiprocessing.
Este arquivo é importado automaticamente pelo Python em todo subprocess
quando COVERAGE_PROCESS_START aponta para o pyproject.toml.
"""
import os

if os.environ.get("COVERAGE_PROCESS_START"):
    try:
        import coverage
        coverage.process_startup()
    except ImportError:
        pass
