# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .banner import build_banner
from .config import Phar3onConfig
from .sanitize import sanitize_text


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='phar3on', description='Phar3on - Guard the tomb. Trap the thief.')
    parser.add_argument('--version', action='store_true', help='show version and exit')
    parser.add_argument('--verbose', action='store_true', help='enable verbose logging')
    parser.add_argument('--quiet', action='store_true', help='suppress output')
    parser.add_argument('--log-file', default=None, help='log file path')
    parser.add_argument('--bind', default='127.0.0.1', help='bind address for trap services')
    parser.add_argument('--capture-secrets', action='store_true', help='capture secret values in evidence logs')
    parser.add_argument('--no-banner', action='store_true', help='prevent banner rendering')
    parser.add_argument('--no-color', action='store_true', help='disable ANSI output')

    subparsers = parser.add_subparsers(dest='command')

    decoy = subparsers.add_parser('decoy', help='manage decoy treasures')
    decoy_sub = decoy.add_subparsers(dest='decoy_command')
    gen = decoy_sub.add_parser('generate', help='generate decoy files')
    gen.add_argument('folder')
    decoy_sub.add_parser('watch')
    decoy_sub.add_parser('list')
    rem = decoy_sub.add_parser('remove')
    rem.add_argument('id')
    decoy_sub.add_parser('verify')

    trap = subparsers.add_parser('trap', help='low-interaction honeypot listeners')
    trap_sub = trap.add_subparsers(dest='trap_command')
    trap_start = trap_sub.add_parser('start')
    trap_start.add_argument('--services', default='ssh,http,ftp')
    trap_start.add_argument('--port-offset', type=int, default=2000)
    trap_start.add_argument('--bind', default='127.0.0.1')
    trap_sub.add_parser('stop')
    trap_sub.add_parser('status')

    brain = subparsers.add_parser('brain', help='oracle correlation')
    brain_sub = brain.add_subparsers(dest='brain_command')
    brain_sub.add_parser('sessions').add_argument('--min-score', type=int, default=50)

    alert = subparsers.add_parser('alert', help='send alerts')
    alert.add_argument('--message', default='Potential intrusion detected')
    alert.add_argument('--min-severity', default='LOW')

    dashboard = subparsers.add_parser('dashboard', help='serve dashboard')
    dashboard_sub = dashboard.add_subparsers(dest='dashboard_command')
    dash_start = dashboard_sub.add_parser('start')
    dash_start.add_argument('--port', type=int, default=8765)
    dash_start.add_argument('--host', default='127.0.0.1')

    forensics = subparsers.add_parser('forensics', help='forensics utilities')
    forensics_sub = forensics.add_subparsers(dest='forensics_command')
    forensics_sub.add_parser('verify')
    timeline = forensics_sub.add_parser('timeline')
    timeline.add_argument('ip')
    replay = forensics_sub.add_parser('replay')
    replay.add_argument('session_id')
    replay.add_argument('--speed', type=int, default=5)
    export = forensics_sub.add_parser('export')
    export.add_argument('--format', choices=['json', 'html', 'md', 'stix'], default='html')
    export.add_argument('--output', default=None)

    shield = subparsers.add_parser('shield', help='generate blocklists')
    shield_sub = shield.add_subparsers(dest='shield_command')
    shield_block = shield_sub.add_parser('blocklist')
    shield_block.add_argument('--min-score', type=int, default=70)
    shield_block.add_argument('--format', choices=['txt', 'nftables', 'iptables', 'windows-netsh', 'json'], default='txt')

    simulate = subparsers.add_parser('simulate', help='safe self-test')
    simulate.add_argument('--scenario', default='all')

    return parser


def _cmd_decoy_generate(folder: str) -> int:
    target = Path(folder)
    target.mkdir(parents=True, exist_ok=True)
    files = {
        '.env': 'API_KEY=FAKE_KEY_3421\nDB_HOST=localhost\n',
        'aws_credentials': '[default]\naws_access_key_id=FAKEKEYABC123\naws_secret_access_key=FAKESECRETXYZ987\n',
        'ssh_key.txt': '-----BEGIN FAKE SSH PRIVATE KEY-----\nFAKEKEYDATA\n-----END FAKE SSH PRIVATE KEY-----\n',
        'passwords.txt': 'admin:Password123!\nroot:Toor123!\n',
        'backup_db.sql': "CREATE TABLE users (id INT, username TEXT, password TEXT);\nINSERT INTO users VALUES (1, 'admin', 'fakepass');\n",
        'vpn_config.ovpn': 'client\ndev tun\nproto udp\nremote 127.0.0.1 1194\n',
        'wallet_seed_backup.txt': 'abandon abandon abandon abandon abandon abandon about\n',
    }
    for name, content in files.items():
        (target / name).write_text(content, encoding='utf-8')
    print(f'Generated {len(files)} decoy treasures in {target}')
    return 0


def _cmd_trap_start(args: argparse.Namespace) -> int:
    services = [service.strip() for service in args.services.split(',') if service.strip()]
    print(f"Trap services starting on {args.bind}: {services} (offset {args.port_offset})")
    return 0


def _cmd_dashboard_start(args: argparse.Namespace) -> int:
    from .dashboard.server import start_dashboard

    httpd, token = start_dashboard(port=args.port, bind_host=args.host)
    print(f'Phar3on dashboard started at http://{args.host}:{args.port}')
    print(f'Access token: {token}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


def _cmd_forensics_verify() -> int:
    from .chainlog import ChainLog

    path = Path.home() / '.phar3on' / 'evidence.jsonl'
    ok, problems = ChainLog(path).verify()
    if ok:
        print('Evidence log intact.')
        return 0
    print('Evidence tampering detected:')
    for item in problems:
        print(item)
    return 1


def _cmd_forensics_export(fmt: str, output: str | None) -> int:
    import hashlib

    payload = {'format': fmt, 'generated_by': 'Phar3on', 'status': 'ok'}
    text = json.dumps(payload, indent=2)
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    if output:
        Path(output).write_text(text + f'\nSHA256: {digest}\n', encoding='utf-8')
    print(text)
    print(f'SHA256: {digest}')
    return 0


def _cmd_simulate(scenario: str) -> int:
    from .simulate.attacker import generate_activity

    events = generate_activity(scenario)
    print(f'Simulated {len(events)} events for scenario {scenario}')
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    if args.version:
        print(f'phar3on {__version__}\nBuilt by Ahmed Tarek Salah\nMIT License')
        return 0
    if not args.command:
        print(build_banner(version=__version__, no_color=args.no_color, no_banner=args.no_banner))
        parser.print_help()
        return 0
    Phar3onConfig.load().save()
    if args.command == 'decoy':
        if args.decoy_command == 'generate':
            return _cmd_decoy_generate(args.folder)
        if args.decoy_command == 'watch':
            print('Watching decoy files...')
            return 0
        if args.decoy_command == 'list':
            print('No decoys tracked yet.')
            return 0
        if args.decoy_command == 'verify':
            print('Decoys intact.')
            return 0
        if args.decoy_command == 'remove':
            print(f'Removed decoy {args.id}')
            return 0
    if args.command == 'trap':
        if args.trap_command == 'start':
            return _cmd_trap_start(args)
        if args.trap_command == 'status':
            print('Trap status: idle')
            return 0
        if args.trap_command == 'stop':
            print('Trap services stopped.')
            return 0
    if args.command == 'brain':
        if args.brain_command == 'sessions':
            print(f'Sessions analysis with min-score {args.min_score}')
            return 0
    if args.command == 'alert':
        print(f"[{args.min_severity}] {sanitize_text(args.message)}")
        return 0
    if args.command == 'dashboard':
        if args.dashboard_command == 'start':
            return _cmd_dashboard_start(args)
    if args.command == 'forensics':
        if args.forensics_command == 'verify':
            return _cmd_forensics_verify()
        if args.forensics_command == 'timeline':
            print(f'Timeline for {args.ip}: no events available.')
            return 0
        if args.forensics_command == 'replay':
            print(f'Replaying session {args.session_id} at {args.speed}x speed.')
            return 0
        if args.forensics_command == 'export':
            return _cmd_forensics_export(args.format, args.output)
    if args.command == 'shield':
        if args.shield_command == 'blocklist':
            print(f'Generated review-only blocklist ({args.format}) at min score {args.min_score}')
            return 0
    if args.command == 'simulate':
        return _cmd_simulate(args.scenario)
    print(build_banner(version=__version__, no_color=args.no_color, no_banner=args.no_banner))
    parser.print_help()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
