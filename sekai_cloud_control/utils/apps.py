"""App lookup utilities for finding docker apps in cache."""

import json
from pathlib import Path

from .hosts import CACHE_FILE


def find_app(app_name: str, hostname: str | None = None) -> dict | None:
    """Find a single app by name, optionally filtered by hostname.

    Returns the app dict if found and unique, None otherwise.
    Prints error messages if no app or multiple apps are found.
    """
    if not CACHE_FILE.exists():
        print("No cache found. Run 'main.py sync' first.")
        return None

    with open(CACHE_FILE) as f:
        cache = json.load(f)

    apps = cache.get("apps", [])
    matching_apps = [app for app in apps if app["name"] == app_name]
    if hostname:
        matching_apps = [app for app in matching_apps if hostname in app["remote"]]

    if not matching_apps:
        print(f"No app found with name: {app_name}")
        return None

    if len(matching_apps) > 1:
        print(
            f"Multiple apps found with name: {app_name}. Perhaps add --H/--hostname filter?"
        )
        return None

    return matching_apps[0]


def get_app_host_folder(app: dict) -> tuple[str, str]:
    """Extract host and folder from app remote string.

    Returns tuple of (host, folder).
    """
    host = app["remote"].split(":")[0]
    folder = app["remote"].split(":")[1]
    return host, folder
