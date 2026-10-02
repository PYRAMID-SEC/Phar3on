# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

from ..core import BaseSensor, make_event


class SSHTrapSensor(BaseSensor):
    def __init__(self, event_bus=None, bind='127.0.0.1', port=2022) -> None:
        super().__init__('ssh', event_bus)
        self.bind = bind
        self.port = port

    async def start(self):
        self._started = True
        return self

    async def handle_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        ip = addr[0] if addr else '127.0.0.1'
        port = addr[1] if addr else None
        writer.write(b'SSH-2.0-fake sshd\r\n')
        await writer.drain()
        data = await reader.read(4096)
        self.on_event(make_event(source_ip=ip, source_port=port, sensor='ssh', event_type='credential_bruteforce', severity='HIGH', details={'payload': data.decode('utf-8', errors='replace')[:256], 'username': 'root'}, mitre_ids=['T1110']))
        writer.close()
