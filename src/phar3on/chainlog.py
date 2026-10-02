# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class ChainLog:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text('', encoding='utf-8')

    def _hash_record(self, payload: dict[str, Any], prev_hash: str) -> str:
        record = dict(payload)
        record['prev_hash'] = prev_hash
        encoded = json.dumps(record, sort_keys=True, separators=(',', ':')).encode('utf-8')
        return hashlib.sha256(encoded).hexdigest()

    def append(self, payload: dict[str, Any]) -> str:
        prev_hash = self.last_hash()
        record = dict(payload)
        record['prev_hash'] = prev_hash
        record['hash'] = self._hash_record(record, prev_hash)
        with self.path.open('a', encoding='utf-8') as fh:
            fh.write(json.dumps(record, sort_keys=True) + '\n')
        return record['hash']

    def last_hash(self) -> str:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return '0' * 64
        with self.path.open('r', encoding='utf-8') as fh:
            lines = [line.strip() for line in fh if line.strip()]
        if not lines:
            return '0' * 64
        return str(json.loads(lines[-1]).get('hash', '0' * 64))

    def verify(self) -> tuple[bool, list[str]]:
        problems: list[str] = []
        previous_hash = '0' * 64
        if not self.path.exists() or self.path.stat().st_size == 0:
            return True, problems
        with self.path.open('r', encoding='utf-8') as fh:
            lines = [line.strip() for line in fh if line.strip()]
        for index, line in enumerate(lines, start=1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f'Record {index} is not valid JSON')
                continue
            actual_prev = record.get('prev_hash', '0' * 64)
            if actual_prev != previous_hash:
                problems.append(f'Tampering detected at record {index}: previous_hash mismatch')
                break
            computed = self._hash_record({k: v for k, v in record.items() if k != 'hash'}, previous_hash)
            if record.get('hash') != computed:
                problems.append(f'Tampering detected at record {index}: hash mismatch')
                break
            previous_hash = record.get('hash', '0' * 64)
        return not problems, problems
