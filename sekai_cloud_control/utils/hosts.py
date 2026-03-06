"""Host configuration and cache file paths."""

from pathlib import Path

HOSTS_FILE = Path(__file__).parent.parent.parent / "hosts.txt"
CACHE_FILE = Path(__file__).parent.parent.parent / "cache.json"


def parse_hosts_file() -> list[dict[str, str]]:
    """Parse hosts.txt into list of host configs."""
    hosts = []
    with open(HOSTS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            host = parts[0]
            folder = parts[1] if len(parts) > 1 else "."
            username, hostname = host.split("@")
            hosts.append(
                {
                    "host": host,
                    "folder": folder,
                    "username": username,
                    "hostname": hostname,
                }
            )
    return hosts
