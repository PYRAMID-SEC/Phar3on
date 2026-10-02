# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

from ..core import BaseSensor, make_event


class HTTPTrapSensor(BaseSensor):
    def __init__(self, event_bus=None, bind='127.0.0.1', port=2080) -> None:
        super().__init__('http', event_bus)
        self.bind = bind
        self.port = port

    async def start(self):
        self._started = True
        return self

    async def handle_request(self, reader, writer):
        addr = writer.get_extra_info('peername')
        ip = addr[0] if addr else '127.0.0.1'
        port = addr[1] if addr else None
        request = await reader.read(4096)
        text = request.decode('utf-8', errors='replace')
        parts = text.split()
        path = parts[1] if len(parts) >= 2 else '/'
        self.on_event(make_event(source_ip=ip, source_port=port, sensor='http', event_type='web_probe', severity='MEDIUM', details={'path': path}, mitre_ids=['T1190']))
        writer.write(b'HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n<html><body>Forbidden</body></html>')
        await writer.drain()
        writer.close()
