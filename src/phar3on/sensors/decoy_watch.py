# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

from pathlib import Path

from ..core import BaseSensor


class DecoyWatchSensor(BaseSensor):
    def __init__(self, event_bus=None) -> None:
        super().__init__('decoy_watch', event_bus)

    def watch(self, folder: str) -> list[dict]:
        root = Path(folder)
        return [{'path': str(file), 'size': file.stat().st_size} for file in sorted(root.rglob('*')) if file.is_file()]
