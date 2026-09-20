import logging
import time
from typing import List
import re

def setup_logging(level: str) -> None:
    """Configure the root logger.
    
    Args:
        level: Logging level name, e.g. "INFO".
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logging.basicConfig(level=numeric_level, format="[%(levelname)s] %(message)s")

def timer() -> float:
    """Return a high‑resolution timestamp (seconds)."""
    return time.perf_counter()

def parse_ports(port_str: str) -> List[int]:
    """Parse a port specification string.
    
    Supported formats:
        "80"               -> [80]
        "22,80,443"        -> [22, 80, 443]
        "1-1024"           -> list(range(1, 1025))
        "22,80-85,443"     -> combined list.
    
    Args:
        port_str: The raw string from the CLI.
    
    Returns:
        Sorted list of unique port numbers.
    
    Raises:
        ValueError: If any part is invalid or out of range.
    """
    ports: set[int] = set()
    parts = [p.strip() for p in port_str.split(',') if p.strip()]
    for part in parts:
        if '-' in part:
            start_str, end_str = part.split('-', 1)
            try:
                start = int(start_str)
                end = int(end_str)
            except ValueError:
                raise ValueError(f"Invalid range '{part}'.")
            if not (1 <= start <= 65535 and 1 <= end <= 65535):
                raise ValueError(f"Port numbers must be between 1 and 65535: '{part}'.")
            if start > end:
                raise ValueError(f"Range start greater than end in '{part}'.")
            ports.update(range(start, end + 1))
        else:
            try:
                p = int(part)
            except ValueError:
                raise ValueError(f"Invalid port '{part}'.")
            if not (1 <= p <= 65535):
                raise ValueError(f"Port number must be between 1 and 65535: {p}.")
            ports.add(p)
    return sorted(ports)
