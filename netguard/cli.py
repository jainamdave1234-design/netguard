import argparse
import logging
import sys
from typing import List

from netguard import scanner, utils, report

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NetGuard v1 - Educational TCP port scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Port(s) to scan. Formats: 80,1-1024,22,8080. If omitted, defaults to common ports.")
    parser.add_argument("-T", "--timeout", type=float, default=1.0, help="Connection timeout in seconds (default: 1)")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Maximum number of concurrent worker threads (default: 50)")
    parser.add_argument("--json", metavar="PATH", help="Write JSON report to the specified file")
    parser.add_argument("--csv", metavar="PATH", help="Write CSV report to the specified file")
    parser.add_argument("--log-level", default="WARNING", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Logging verbosity (default: WARNING)")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    utils.setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    # Resolve ports
    if args.ports:
        try:
            ports = utils.parse_ports(args.ports)
        except ValueError as e:
            logger.error("Invalid ports specification: %s", e)
            sys.exit(1)
    else:
        # Default small set of common ports
        ports = [22, 80, 443, 445, 3389]

    logger.info("Scanning target %s on %d ports", args.target, len(ports))
    start_time = utils.timer()
    results = scanner.run_scan(args.target, ports, timeout=args.timeout, max_workers=args.workers)
    total_time = utils.timer() - start_time

    # Output table
    print(report.format_table(results))

    # Statistics
    open_cnt = sum(1 for r in results if r.state == scanner.PortState.OPEN)
    closed_cnt = sum(1 for r in results if r.state == scanner.PortState.CLOSED)
    timeout_cnt = sum(1 for r in results if r.state == scanner.PortState.TIMEOUT)
    error_cnt = sum(1 for r in results if r.state == scanner.PortState.ERROR)
    print("\n--- Scan Statistics ---")
    print(f"Target: {args.target}")
    print(f"Ports scanned: {len(ports)}")
    print(f"Open ports: {open_cnt}")
    print(f"Closed ports: {closed_cnt}")
    print(f"Timeout/filtered: {timeout_cnt}")
    print(f"Errors: {error_cnt}")
    print(f"Total scan time: {total_time:.4f}s")

    # Optional reports
    if args.json:
        try:
            report.write_json(results, args.json)
            logger.info("JSON report written to %s", args.json)
        except Exception as e:
            logger.error("Failed to write JSON report: %s", e)
    if args.csv:
        try:
            report.write_csv(results, args.csv)
            logger.info("CSV report written to %s", args.csv)
        except Exception as e:
            logger.error("Failed to write CSV report: %s", e)

if __name__ == "__main__":
    main()
