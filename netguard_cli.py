#!/usr/bin/env python
"""Entry point for NetGuard CLI.
Run with:
    python netguard_cli.py --target 127.0.0.1 --ports 1-1024
"""

from netguard import cli

if __name__ == "__main__":
    cli.main()
