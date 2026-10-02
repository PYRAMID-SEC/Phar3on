# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

from ..core import BaseSensor, make_event


class FTPTrapSensor(BaseSensor):
    def __init__(self, event_bus=None, bind='127.0.0.1', port=2021) -> None:
        super().__init__('ftp', event_bus)
        self.bind = bind
        self.port = port

    async def start(self):
        self._started = True
        return self

    async def handle_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        ip = addr[0] if addr else '127.0.0.1'
        port = addr[1] if addr else None
        data = await reader.read(4096)
        msg = data.decode('utf-8', errors='replace')
        self.on_event(make_event(source_ip=ip, source_port=port, sensor='ftp', event_type='credential_bruteforce', severity='HIGH', details={'payload': msg[:256]}, mitre_ids=['T1110']))
        writer.write(b'220 fake FTP server ready\r\n')
        await writer.drain()
        writer.close()
