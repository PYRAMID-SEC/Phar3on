# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

from collections import defaultdict


def group_sessions(events: list[dict], window_seconds: int = 300) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for event in events:
        groups[event.get('source_ip', 'unknown')].append(event)
    return dict(groups)
