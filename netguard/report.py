import csv
import json
from typing import List
from .scanner import PortResult, PortState

def format_table(results: List[PortResult]) -> str:
    """Return a formatted string table of scan results.

    Columns: PORT, STATE, SERVICE, TIME
    TIME is shown in seconds with 4 decimal places for OPEN ports, otherwise '-'.
    """
    header = f"{'PORT':<6} {'STATE':<8} {'SERVICE':<15} {'TIME'}"
    lines = [header]
    for r in results:
        time_str = f"{r.elapsed:.4f}s" if r.state == PortState.OPEN and r.elapsed is not None else "-"
        lines.append(f"{r.port:<6} {r.state.name:<8} {r.service:<15} {time_str}")
    return "\n".join(lines)

def _result_to_dict(r: PortResult) -> dict:
    return {
        "port": r.port,
        "state": r.state.name,
        "service": r.service,
        "time": r.elapsed,
    }

def write_json(results: List[PortResult], path: str) -> None:
    """Write results to *path* as JSON array."""
    data = [_result_to_dict(r) for r in results]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def write_csv(results: List[PortResult], path: str) -> None:
    """Write results to *path* as CSV.

    Columns: port,state,service,time
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["port", "state", "service", "time"])
        for r in results:
            writer.writerow([r.port, r.state.name, r.service, r.elapsed])
