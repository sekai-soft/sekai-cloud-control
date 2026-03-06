"""Logs command - Stream logs for a docker compose app via SSH."""

import json
from pathlib import Path

from .utils.hosts import CACHE_FILE
from .utils.ssh import run_ssh_command


def cmd_logs(app_name: str, hostname: str | None) -> None:
    """Stream logs for a docker compose app via SSH."""
    if not CACHE_FILE.exists():
        print("No cache found. Run 'main.py sync' first.")
        return

    with open(CACHE_FILE) as f:
        cache = json.load(f)

    apps = cache.get("apps", [])
    matching_apps = [app for app in apps if app["name"] == app_name]
    if hostname:
        matching_apps = [app for app in matching_apps if hostname in app["remote"]]

    if not matching_apps:
        print(f"No app found with name: {app_name}")
        return

    if len(matching_apps) > 1:
        print(
            f"Multiple apps found with name: {app_name}. Perhaps add --H/--hostname filter?"
        )
        return

    matching_app = matching_apps[0]

    host = matching_app["remote"].split(":")[0]
    folder = matching_app["remote"].split(":")[1]
    logs_command = f"cd {app_name} && docker compose logs {app_name} -n 100 -f"
    run_ssh_command(host, folder, logs_command, interactive=True)
