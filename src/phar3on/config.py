# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Phar3onConfig:
    data_dir: Path = field(default_factory=lambda: Path.home() / '.phar3on')
    db_path: Path = field(default_factory=lambda: Path.home() / '.phar3on' / 'events.db')
    config_path: Path = field(default_factory=lambda: Path.home() / '.phar3on' / 'config.json')
    evidence_path: Path = field(default_factory=lambda: Path.home() / '.phar3on' / 'evidence.jsonl')
    log_file: str | None = None
    verbose: bool = False
    quiet: bool = False
    bind: str = '127.0.0.1'
    capture_secrets: bool = False
    max_connections: int = 64
    rate_limit: int = 20
    max_bytes_read: int = 4096
    idle_timeout: int = 30
    max_log_size: int = 1048576
    tarpit: float = 0.0
    min_severity: str = 'LOW'

    @classmethod
    def load(cls, path: str | None = None) -> 'Phar3onConfig':
        config_path = Path(path) if path else Path.home() / '.phar3on' / 'config.json'
        config = cls()
        if config_path.exists():
            with config_path.open('r', encoding='utf-8') as fh:
                try:
                    data = json.load(fh)
                except json.JSONDecodeError:
                    data = {}
            for key, value in data.items():
                if hasattr(config, key):
                    setattr(config, key, value)
        config.data_dir.mkdir(parents=True, exist_ok=True)
        config.db_path = config.data_dir / 'events.db'
        config.evidence_path = config.data_dir / 'evidence.jsonl'
        config.config_path = config_path
        return config

    def save(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            'bind': self.bind,
            'capture_secrets': self.capture_secrets,
            'max_connections': self.max_connections,
            'rate_limit': self.rate_limit,
            'max_bytes_read': self.max_bytes_read,
            'idle_timeout': self.idle_timeout,
            'max_log_size': self.max_log_size,
            'tarpit': self.tarpit,
            'min_severity': self.min_severity,
            'log_file': self.log_file,
            'verbose': self.verbose,
            'quiet': self.quiet,
        }
        with self.config_path.open('w', encoding='utf-8') as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
