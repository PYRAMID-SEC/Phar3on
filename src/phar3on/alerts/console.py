# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations


def emit_console_alert(message: str, *, severity: str = 'INFO') -> None:
    print(f'[{severity}] {message}')
