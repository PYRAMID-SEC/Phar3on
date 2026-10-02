# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import json
import sqlite3
from typing import Any

from .config import Phar3onConfig
from .utils import iso_now


class Storage:
    def __init__(self, config: Phar3onConfig | None = None) -> None:
        self.config = config or Phar3onConfig.load()
        self.config.data_dir.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.config.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                source_ip TEXT,
                source_port INTEGER,
                sensor TEXT,
                event_type TEXT,
                severity TEXT,
                details TEXT,
                mitre_ids TEXT
            )'''
        )
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS decoys (
                id TEXT PRIMARY KEY,
                path TEXT,
                decoy_type TEXT,
                created_at TEXT,
                last_seen TEXT,
                status TEXT DEFAULT 'active'
            )'''
        )
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                source_ip TEXT,
                score INTEGER,
                label TEXT,
                summary TEXT,
                created_at TEXT
            )'''
        )
        self.conn.commit()

    def add_event(self, event: dict[str, Any]) -> None:
        self.conn.execute(
            'INSERT OR REPLACE INTO events (id, timestamp, source_ip, source_port, sensor, event_type, severity, details, mitre_ids) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                event.get('id'),
                event.get('timestamp', iso_now()),
                event.get('source_ip', 'unknown'),
                event.get('source_port'),
                event.get('sensor', 'unknown'),
                event.get('event_type', 'generic'),
                event.get('severity', 'LOW'),
                json.dumps(event.get('details', {})),
                json.dumps(event.get('mitre_ids', [])),
            ),
        )
        self.conn.commit()

    def add_decoy(self, decoy_id: str, path: str, decoy_type: str) -> None:
        self.conn.execute(
            'INSERT OR REPLACE INTO decoys (id, path, decoy_type, created_at, last_seen, status) VALUES (?, ?, ?, ?, ?, ?)',
            (decoy_id, path, decoy_type, iso_now(), iso_now(), 'active'),
        )
        self.conn.commit()

    def list_decoys(self) -> list[sqlite3.Row]:
        return self.conn.execute('SELECT * FROM decoys ORDER BY created_at DESC').fetchall()

    def get_events(self, source_ip: str | None = None) -> list[sqlite3.Row]:
        if source_ip:
            return self.conn.execute('SELECT * FROM events WHERE source_ip = ? ORDER BY timestamp', (source_ip,)).fetchall()
        return self.conn.execute('SELECT * FROM events ORDER BY timestamp').fetchall()

    def close(self) -> None:
        self.conn.close()
