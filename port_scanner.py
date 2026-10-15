
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def scan_port(host, port, timeout):
    """Check one TCP port on an authorized target."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))

        if result == 0:
            return port, "OPEN"
        return port, "CLOSED"

    except socket.timeout:
        return port, "TIMEOUT"
    except OSError as exc:
        return port, f"ERROR: {exc}"


def main():
    parser = argparse.ArgumentParser(
        description="Simple threaded TCP port scanner"
    )
    parser.add_argument("host", help="Hostname or IP you are authorized to scan")
    parser.add_argument("--start", type=int, default=1, help="First port")
    parser.add_argument("--end", type=int, default=1024, help="Last port")
    parser.add_argument("--timeout", type=float, default=0.5)
    parser.add_argument("--workers", type=int, default=50)
    args = parser.parse_args()

    if not (1 <= args.start <= args.end <= 65535):
        parser.error("Ports must satisfy 1 <= start <= end <= 65535")
    if args.timeout <= 0 or not (1 <= args.workers <= 200):
        parser.error("Timeout must be positive and workers must be 1-200")

    try:
        target_ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        parser.error("Could not resolve the target hostname")

    print(f"Target: {args.host} ({target_ip})")
    print(f"Started: {datetime.now().isoformat(timespec='seconds')}")
    print(f"Scanning ports {args.start}-{args.end} ...")

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(scan_port, target_ip, port, args.timeout): port
            for port in range(args.start, args.end + 1)
        }

        for future in as_completed(futures):
            port, status = future.result()
            results.append((port, status))
            if status != "CLOSED":
                print(f"{port:5}  {status}")

    results.sort()
    with open("scan_results.txt", "w", encoding="utf-8") as log:
        log.write(f"Target: {args.host} ({target_ip})\n")
        for port, status in results:
            log.write(f"{port}\t{status}\n")

    print(f"Finished. Results saved to scan_results.txt")


if __name__ == "__main__":
    main()
