# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / 'data' / 'mitre_map.json'


def load_mitre_map() -> dict[str, dict[str, str]]:
    with DATA_FILE.open('r', encoding='utf-8') as fh:
        return json.load(fh)
