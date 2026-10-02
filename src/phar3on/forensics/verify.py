# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

from pathlib import Path

from ..chainlog import ChainLog


def verify_log(path: str | Path) -> tuple[bool, list[str]]:
    return ChainLog(path).verify()
