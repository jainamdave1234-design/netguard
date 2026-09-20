import socket as _socket
# expose socket under the expected name for tests
socket = _socket
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import List
import concurrent.futures
import logging

from .service import lookup_service

# Preserve the real timeout exception class before any monkey‑patching.
REAL_TIMEOUT = socket.timeout

logger = logging.getLogger(__name__)

class PortState(Enum):
    OPEN = auto()
    CLOSED = auto()
    TIMEOUT = auto()
    ERROR = auto()

@dataclass
class PortResult:
    port: int
    state: PortState
    service: str
    elapsed: float | None  # Seconds; None for non‑open ports

def scan_port(target: str, port: int, timeout: float) -> PortResult:
    """Attempt a TCP connect to *target*:*port*.

    Returns a :class:`PortResult` with detailed state.
    """
    start = time.perf_counter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((target, port))
        elapsed = time.perf_counter() - start
        service_name = lookup_service(port)
        logger.debug("Port %s open (service=%s, time=%fs)", port, service_name, elapsed)
        return PortResult(port=port, state=PortState.OPEN, service=service_name, elapsed=elapsed)
    except REAL_TIMEOUT:
        logger.debug("Port %s timeout after %fs", port, timeout)
        return PortResult(port=port, state=PortState.TIMEOUT, service="UNKNOWN", elapsed=None)
    except ConnectionRefusedError:
        logger.debug("Port %s connection refused", port)
        return PortResult(port=port, state=PortState.CLOSED, service="UNKNOWN", elapsed=None)
    except OSError as e:
        logger.debug("Port %s error: %s", port, e)
        return PortResult(port=port, state=PortState.ERROR, service="UNKNOWN", elapsed=None)
    finally:
        s.close()

def run_scan(target: str, ports: List[int], timeout: float = 1.0, max_workers: int = 50) -> List[PortResult]:
    """Scan *ports* on *target* concurrently.

    Returns a list of :class:`PortResult` objects preserving the input order.
    """
    results: List[PortResult] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, target, port, timeout): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            try:
                result = future.result()
            except Exception as exc:
                port = future_to_port[future]
                logger.error("Unexpected error scanning port %s: %s", port, exc)
                result = PortResult(port=port, state=PortState.ERROR, service="UNKNOWN", elapsed=None)
            results.append(result)
    results.sort(key=lambda r: r.port)
    return results
