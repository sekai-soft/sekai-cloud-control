"""Sync command - Sync docker apps from all hosts and cache locally."""

import json
from datetime import datetime
from pathlib import Path

from .utils.hosts import HOSTS_FILE, CACHE_FILE, parse_hosts_file
from .utils.ssh import get_docker_apps


def cmd_sync(hostname: str | None = None) -> None:
    """Sync docker apps from all hosts and cache locally."""
    hosts = parse_hosts_file()

    if hostname:
        matching_hosts = [h for h in hosts if h["hostname"] == hostname]
        if not matching_hosts:
            print(f"No host found with hostname: {hostname}")
            return

        try:
            with open(CACHE_FILE) as f:
                cache: dict = json.load(f)
        except FileNotFoundError:
            cache = {"apps": []}

        cache["apps"] = [
            a
            for a in cache.get("apps", [])
            if a["remote"].split("@")[1].split(":")[0] != hostname
        ]

        all_apps = cache.get("apps", [])

        for h in matching_hosts:
            apps = get_docker_apps(h["host"], h["folder"])
            all_apps.extend(apps)
            print(f"Synced {len(apps)} apps from {h['host']}")

        cache["last_updated"] = datetime.now().isoformat()
        cache["apps"] = all_apps
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)

        print(f"\nCached {len(all_apps)} total apps to {CACHE_FILE}")
    else:
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
