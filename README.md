# NetGuard v1

## Project Overview
NetGuard is an **educational** Python‑based TCP port scanner designed as a portfolio project. It demonstrates basic network probing techniques, threading/concurrency, and report generation in JSON and CSV formats.

## Motivation
The goal is to provide a lightweight, easy‑to‑understand example of how a security‑oriented command‑line tool can be built from scratch. It is **not** intended for production use or as a replacement for full‑featured scanners such as Nmap.

## Features
- Scan a single host or hostname.
- Specify individual ports, comma‑separated lists, or ranges (e.g., `1-1024`).
- Concurrent scanning with a configurable thread pool (default 50 workers).
- Per‑connection timeout (default 1 second).
- Plain‑text, JSON, and CSV reporting.
- Service name lookup via the OS `socket.getservbyport` database.
- Simple CLI with short (`-t`, `-p`, `-T`, `-w`) and long options.

## Architecture
```
netguard/
├─ cli.py          # argparse handling, validation, entry point
├─ scanner.py      # Core ThreadPoolExecutor scan logic, port classification
├─ service.py      # Service‑name resolution helper
├─ report.py       # Formatting for table, JSON, CSV output
└─ utils.py        # Shared utilities (port parsing, logging)
```
The scanner module exposes a `scan_target(target, ports, timeout, workers)` function that returns a list of result dictionaries. The CLI simply collects arguments, calls the scanner, and forwards the results to the reporter.

## Installation
```bash
# Clone the repository
git clone https://github.com/jainamdave/netguard.git
cd netguard

# (Optional) create a virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # PowerShell

# No external dependencies – standard library only
```

## Usage
```bash
# Basic scan (default common ports)
python netguard_cli.py -t 127.0.0.1

# Scan specific ports
python netguard_cli.py -t 127.0.0.1 -p 22,80,443

# Scan a range
python netguard_cli.py -t 127.0.0.1 -p 135-445

# Change timeout and workers
python netguard_cli.py -t 127.0.0.1 -p 1-1024 -T 2 -w 30

# Export JSON and CSV reports
python netguard_cli.py -t 127.0.0.1 -p 1-1024 \
    --json scan.json --csv scan.csv
```
### Example Output (plain‑text)
```
PORT   STATE    SERVICE          TIME
22     CLOSED   UNKNOWN          -
80     CLOSED   UNKNOWN          -
443    CLOSED   UNKNOWN          -

--- Scan Statistics ---
Target: 127.0.0.1
Ports scanned: 3
Open ports: 0
Closed ports: 3
Timeout/filtered: 0
Errors: 0
Total scan time: 0.012s
```

## Testing
```bash
python -m unittest discover -v
```
All unit tests should pass (17 tests). The test suite covers:
- Port string parsing (`tests/test_port_parsing.py`)
- Service lookup (`tests/test_service_lookup.py`
- Scanner classification of OPEN, CLOSED, TIMEOUT, ERROR (`tests/test_scanner_classification.py`)
- CLI validation and error handling (`tests/test_cli_errors.py`)

## Limitations
- **No stealth or evasion** – pure TCP connect attempts.
- **No UDP, SYN, or version detection**.
- **Timeouts are reported as `TIMEOUT`**, not “filtered”.
- Only a single target per execution.
- No authentication handling; scanner only works on hosts you are authorized to probe.

## Security / Authorization Note
Use NetGuard **only on systems you own or have explicit permission to scan**. Unauthorized scanning may violate laws or policies.

## Future Improvements (optional)
- Add banner grabbing / service version detection.
- Support multiple targets from a file.
- Implement rate‑limiting and polite scanning flags.
- Provide richer output formats (HTML, XML).
- Add OS‑specific enhancements (e.g., raw sockets for SYN scans).

---
*NetGuard v1 is released under the MIT License.*
