# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations


def replay_session(session_id: str, events: list[dict], speed: int = 5) -> list[str]:
    lines: list[str] = []
    for event in events:
        lines.append(f"[{event.get('timestamp', 'unknown')}] {session_id} {event.get('event_type', 'unknown')}")
    return lines
