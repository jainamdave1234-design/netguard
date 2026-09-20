# netguard.py - entry point for the NetGuard scanner

"""NetGuard v1

Educational TCP port scanner CLI.

Run with::
    python netguard.py --target 127.0.0.1 --ports 1-1024
"""

from netguard import cli

if __name__ == "__main__":
    cli.main()
