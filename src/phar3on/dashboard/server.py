# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

INDEX_HTML = (Path(__file__).resolve().parent / 'static' / 'index.html').read_text(encoding='utf-8')


class DashboardHandler(BaseHTTPRequestHandler):
    token = ''
    live_events: list[dict[str, Any]] = []
    latest_score = 0
    latest_ip = 'N/A'
    latest_mitre: list[str] = []

    def do_GET(self) -> None:
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline';")
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode('utf-8'))
            return
        if self.path == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            payload = {'events': self.live_events[-10:], 'score': self.latest_score, 'ip': self.latest_ip, 'mitre': self.latest_mitre}
            self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode('utf-8'))
            return
        self.send_error(404)

    def log_message(self, format: str, *args: Any) -> None:
        return


def start_dashboard(port: int = 8765, bind_host: str = '127.0.0.1') -> tuple[ThreadingHTTPServer, str]:
    token = secrets.token_urlsafe(24)
    dashboard = ThreadingHTTPServer((bind_host, port), DashboardHandler)
    dashboard.timeout = 1
    DashboardHandler.token = token
    return dashboard, token
