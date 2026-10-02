# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations


def generate_activity(scenario: str = 'all') -> list[dict]:
    scenarios = {
        'port_scan': [
            {'event_type': 'port_scan', 'source_ip': '127.0.0.1', 'details': {'ports': [22, 80, 443]}},
            {'event_type': 'port_scan', 'source_ip': '127.0.0.1', 'details': {'ports': [21, 25, 8080]}},
        ],
        'brute_force': [
            {'event_type': 'credential_bruteforce', 'source_ip': '127.0.0.1', 'details': {'username': 'root'}},
        ],
        'web_probe': [
            {'event_type': 'web_probe', 'source_ip': '127.0.0.1', 'details': {'path': '/wp-login.php'}},
        ],
        'bait_access': [
            {'event_type': 'bait_access', 'source_ip': '127.0.0.1', 'details': {'path': 'passwords.txt'}},
        ],
        'all': ['port_scan', 'brute_force', 'web_probe', 'bait_access'],
    }
    chosen = scenarios.get(scenario, scenarios['all'])
    if isinstance(chosen, list) and all(isinstance(item, dict) for item in chosen):
        return chosen
    result: list[dict] = []
    for item in chosen:
        result.extend(generate_activity(item))
    return result
