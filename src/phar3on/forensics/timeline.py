# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations


def build_timeline(events: list[dict]) -> list[dict]:
    return sorted(events, key=lambda item: item.get('timestamp', ''))
