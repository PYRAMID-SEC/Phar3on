# Phar3on

Phar3on is a local deception-defense framework. The idea is simple: create believable decoys and traps that no legitimate user should touch, then treat any contact as a high-confidence signal of intrusion.

Tagline: "Guard the tomb. Trap the thief."

![Phar3on banner](phar3on/assets/banner.svg)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

## What is deception defense?

Instead of only scanning for vulnerabilities, Phar3on creates fake credentials, fake services, and bait files that appear realistic but are harmless. When an attacker touches one, the system knows the event is highly likely malicious.

## Features

- Treasures: bait files such as fake `.env`, AWS credentials, SSH key-like files, password stores, SQL backups, VPN config, wallet seed backup.
- Tomb Gates: low-interaction honeypot listeners for SSH, HTTP, FTP, Telnet, and MySQL-style banners.
- Oracle: correlation and MITRE ATT&CK mapping from telemetry.
- Shield of Ra: review-only blocklist generator.
- Dashboard: local SSE dashboard with a clean dark theme.
- Forensics: hash-chained tamper-evident JSONL logging.

## Installation

```bash
python -m pip install -e .
```

## Quick start

```bash
python -m phar3on --version
python -m phar3on decoy generate ./bait
python -m phar3on trap start --services ssh,http,ftp --port-offset 2000
python -m phar3on dashboard start --port 8765
python -m phar3on simulate --scenario all
```

## Command cheat-sheet

```bash
python -m phar3on --version
python -m phar3on decoy generate ./bait
python -m phar3on decoy watch
python -m phar3on trap start --services ssh,http,ftp --port-offset 2000
python -m phar3on dashboard start --port 8765
python -m phar3on simulate --scenario brute-force
python -m phar3on brain sessions --min-score 50
python -m phar3on forensics verify
python -m phar3on forensics replay <session-id> --speed 5
python -m phar3on forensics export --format html --output incident.html
python -m phar3on shield blocklist --min-score 70 --format nftables
```

## Safety design

- Bind to `127.0.0.1` by default.
- No command execution or shell relays.
- No outbound connection except an optional user-configured webhook.
- All attacker data is sanitized before logging and display.
- Firewall rules are generated as review-only text.

## Legal and ethical disclaimer

Use Phar3on only on systems you own or are authorized to defend. This project is intended for lawful defensive testing and local monitoring.

## Roadmap

- Stronger emulated service coverage
- Better session correlation models
- More threat scoring and export formats

## License & Author

Built by Ahmed Tarek Salah. Released under the MIT License. See LICENSE.
