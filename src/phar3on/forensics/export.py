# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def export_report(events: list[dict], *, fmt: str = 'html', output: str | None = None) -> str:
    payload = {'events': events, 'generated_at': datetime.now(timezone.utc).isoformat()}
    if fmt == 'json':
        text = json.dumps(payload, indent=2)
    elif fmt == 'html':
        text = f"<html><body><h1>Phar3on Incident Report</h1><pre>{json.dumps(payload, indent=2)}</pre></body></html>"
    elif fmt == 'md':
        text = '# Phar3on Incident Report\n\n```json\n' + json.dumps(payload, indent=2) + '\n```\n'
    elif fmt == 'stix':
        bundle = {'type': 'bundle', 'id': 'bundle--phar3on', 'objects': [{'type': 'indicator', 'id': 'indicator--1', 'pattern': 'file.name:*', 'pattern_type': 'stix'}]}
        text = json.dumps(bundle, indent=2)
    else:
        text = json.dumps(payload, indent=2)
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    text = text + f'\n\n<!-- SHA256: {digest} -->\n'
    if output:
        Path(output).write_text(text, encoding='utf-8')
    return text
