# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

from ipaddress import ip_address


def build_blocklist(ip_scores: dict[str, int], *, min_score: int = 70, fmt: str = 'txt') -> list[str]:
    items: list[str] = []
    for ip, score in sorted(ip_scores.items()):
        try:
            parsed = ip_address(ip)
        except ValueError:
            continue
        if score < min_score:
            continue
        if parsed.is_private or parsed.is_loopback:
            continue
        if fmt == 'json':
            items.append(f'{ip}:{score}')
        else:
            items.append(f'{ip} {score}')
    return items
