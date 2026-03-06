"""Apps command - List all cached docker apps."""

import json
from pathlib import Path

from .utils.hosts import CACHE_FILE


def cmd_apps() -> None:
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
