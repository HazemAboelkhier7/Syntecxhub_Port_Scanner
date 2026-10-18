# Syntecxhub Port Scanner

A Python-based TCP port scanner developed as part of the Syntecxhub Cybersecurity Internship.

## Features

- Scan a single authorized host.
- Specify a custom TCP port range.
- Use multithreading to scan multiple ports concurrently.
- Handle connection errors and timeouts.
- Save scan results to `scan_results.txt`.

## Requirements

- Python 3.10 or later

## Usage

### Basic Scan

Scan TCP ports 1–100 on your local machine:

```powershell
python port_scanner.py 127.0.0.1 --start 1 --end 100
```

### Advanced Scan

Customize the port range, connection timeout, and number of concurrent workers:

```powershell
python port_scanner.py 127.0.0.1 --start 1 --end 1024 --timeout 1.0 --workers 100
```

### Available Options

| Option | Description | Default |
|---|---|---|
| `host` | Target hostname or IP address | Required |
| `--start` | First port to scan | `1` |
| `--end` | Last port to scan | `1024` |
| `--timeout` | Connection timeout in seconds | `0.5` |
| `--workers` | Maximum concurrent workers | `50` |

## Output

The scanner displays discovered open ports and other non-closed results in the terminal. It also saves the scan results to `scan_results.txt`.

## Responsible Use

Only scan systems you own or have explicit permission to test.