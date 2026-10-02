# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import json
import urllib.request


def post_webhook(url: str, payload: dict) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return True, response.read().decode('utf-8', errors='replace')
    except Exception as exc:  # pragma: no cover
        return False, str(exc)
