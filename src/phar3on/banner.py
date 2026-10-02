# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations


def ansi(text: str, *, color: str | None = None, bold: bool = False) -> str:
    if color is None and not bold:
        return text
    colors = {'cyan': '36', 'gold': '33', 'red': '31', 'green': '32'}
    codes: list[str] = []
    if bold:
        codes.append('1')
    if color:
        codes.append(colors.get(color, '0'))
    return f"\033[{';'.join(codes)}m{text}\033[0m" if codes else text


def build_banner(version: str = '0.1.0', *, no_color: bool = False, no_banner: bool = False) -> str:
    if no_banner:
        return ''
    lines = [
        'Phar3on ' + version,
        'Built by Ahmed Tarek Salah',
        'MIT License',
        'Guard the tomb. Trap the thief.',
    ]
    if no_color:
        return '\n'.join(lines)
    return '\n'.join(ansi(line, color='cyan', bold=True) for line in lines)
