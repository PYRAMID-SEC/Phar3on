# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import html
import re

ANSI_RE = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')


def strip_ansi(value: str) -> str:
    return ANSI_RE.sub('', value)


def sanitize_text(value: object) -> str:
    text = '' if value is None else str(value)
    text = strip_ansi(text)
    text = html.unescape(text)
    text = re.sub(r'(?is)<script.*?>.*?</script>', ' ', text)
    text = re.sub(r'(?is)<[^>]+>', ' ', text)
    text = text.replace('\r', '\\r').replace('\n', '\\n')
    text = ''.join(ch if ch.isprintable() and ch not in {'\x00', '\x1f', '\x7f'} else ' ' for ch in text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def html_escape(value: object) -> str:
    text = '' if value is None else str(value)
    return html.escape(text, quote=True)


def redact_secret(value: str, show_tail: int = 4) -> str:
    if not value or len(value) <= max(4, show_tail):
        return '***'
    return f"{value[:2]}***{value[-show_tail:]}"


def safe_error_message(value: object) -> str:
    return sanitize_text(html_escape(value))
