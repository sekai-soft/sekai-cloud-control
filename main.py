import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

HOSTS_FILE = Path(__file__).parent / "hosts.txt"
CACHE_FILE = Path(__file__).parent / "cache.json"


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


def run_ssh_command(host: str, folder: str, command: str) -> str:
    """Run a command on a remote host via SSH."""
    cmd = f"ssh {host} 'cd {folder} && {command}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def has_compose_yml(host: str, folder: str, app_name: str) -> bool:
    """Check if an app folder contains a compose.yml file."""
    result = subprocess.run(
        f"ssh {host} test -f {folder}/{app_name}/compose.yml",
        shell=True,
        capture_output=True,
    )
    return result.returncode == 0


def get_docker_apps(host: str, folder: str) -> list[dict[str, Any]]:
    """Fetch docker compose apps from a host's folder."""
    output = run_ssh_command(host, folder, "ls -1")
    apps = []
    for line in output.strip().split("\n"):
        if line:
            if has_compose_yml(host, folder, line):
                apps.append({"name": line, "path": line, "remote": f"{host}:{folder}"})
    return apps


def cmd_sync() -> None:
    """Sync docker apps from all hosts and cache locally."""
    hosts = parse_hosts_file()
    all_apps = []

    for h in hosts:
        apps = get_docker_apps(h["host"], h["folder"])
        all_apps.extend(apps)
        print(f"Synced {len(apps)} apps from {h['host']}")

    last_updated = datetime.now().isoformat()
    cache = {"last_updated": last_updated, "hosts": hosts, "apps": all_apps}
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    print(f"\nCached {len(all_apps)} total apps to {CACHE_FILE}")


def cmd_app() -> None:
    """List all cached docker apps."""
    if not CACHE_FILE.exists():
        print("No cache found. Run 'main.py sync' first.")
        return

    with open(CACHE_FILE) as f:
        cache = json.load(f)

    def get_app_hostname(app: dict) -> str:
        """Extract hostname from app remote string."""
        return app["remote"].split(":")[0].split("@")[1]

    # Count app occurrences to identify duplicates
    app_counts: dict[str, int] = {}
    for app in cache.get("apps", []):
        name = app["name"]
        app_counts[name] = app_counts.get(name, 0) + 1

    # Sort by app name
    sorted_apps = sorted(cache.get("apps", []), key=lambda x: x["name"])

    for app in sorted_apps:
        hostname = get_app_hostname(app)
        if app_counts[app["name"]] > 1:
            print(f"{app['name']} ({hostname})")
        else:
            print(app["name"])


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py <command>\nCommands: sync, apps")
        sys.exit(1)

    command = sys.argv[1]

    if command == "sync":
        cmd_sync()
    elif command == "apps":
        cmd_app()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
