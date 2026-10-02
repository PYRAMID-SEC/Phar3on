# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / 'data' / 'scoring_rules.json'
with DATA_FILE.open('r', encoding='utf-8') as fh:
    RULES = json.load(fh)


def score_session(session_events: list[dict]) -> tuple[int, str, list[str], str]:
    score = 0
    reasons: list[str] = []
    for event in session_events:
        event_type = event.get('event_type', '')
        if 'port_scan' in event_type:
            score += RULES.get('port_scan', 0)
            reasons.append('port_scan')
        if 'credential_bruteforce' in event_type:
            score += RULES.get('credential_bruteforce', 0)
            reasons.append('credential_bruteforce')
        if 'web_probe' in event_type:
            score += RULES.get('web_probe', 0)
            reasons.append('web_probe')
        if 'bait_access' in event_type:
            score += RULES.get('bait_access', 0)
            reasons.append('bait_access')
    if len({e.get('event_type', '') for e in session_events}) >= 3:
        score += RULES.get('multistage', 0)
        reasons.append('multistage')
    score = max(0, min(100, score))
    if score >= 80:
        label = 'CRITICAL'
        stage = 'Collection'
    elif score >= 60:
        label = 'HIGH'
        stage = 'Credential Access'
    elif score >= 35:
        label = 'MEDIUM'
        stage = 'Recon'
    else:
        label = 'LOW'
        stage = 'Recon'
    return score, label, reasons, stage
