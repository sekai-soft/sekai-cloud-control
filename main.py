import sys
from pathlib import Path

from sekai_cloud_control import (
    cmd_apps,
    cmd_logs,
    cmd_ps,
    cmd_restart,
    cmd_sync,
    cmd_upgrade,
)

CACHE_FILE = Path(__file__).parent / "cache.json"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sekai Cloud Control CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parser_apps = subparsers.add_parser("apps", help="List all cached docker apps")
    parser_apps.set_defaults(func=cmd_apps)
    parser_logs = subparsers.add_parser("logs", help="Stream logs for a docker app")
    parser_logs.add_argument("app_name", help="Name of the docker app")
    parser_logs.add_argument(
        "-H",
        "--hostname",
        dest="hostname",
        help="Filter by hostname for duplicate apps",
    )
    parser_ps = subparsers.add_parser(
        "ps", help="Show container status for a docker app"
    )
    parser_ps.add_argument("app_name", help="Name of the docker app")
    parser_ps.add_argument(
        "-H",
        "--hostname",
        dest="hostname",
        help="Filter by hostname for duplicate apps",
    )
    parser_restart = subparsers.add_parser("restart", help="Restart a docker app")
    parser_restart.add_argument("app_name", help="Name of the docker app")
    parser_restart.add_argument(
        "-H",
        "--hostname",
        dest="hostname",
        help="Filter by hostname for duplicate apps",
    )
    parser_sync = subparsers.add_parser("sync", help="Sync docker apps from all hosts")
    parser_sync.add_argument(
        "-H",
        "--hostname",
        dest="hostname",
        help="Filter by hostname to sync only that host",
    )

    parser_upgrade = subparsers.add_parser(
        "upgrade", help="Upgrade a docker compose app"
    )
    parser_upgrade.add_argument("app_name", help="Name of the docker app")
    parser_upgrade.add_argument(
        "-H",
        "--hostname",
        dest="hostname",
        help="Filter by hostname for duplicate apps",
    )

    args = parser.parse_args()

    if args.command == "apps":
        cmd_apps()
    elif args.command == "logs":
        cmd_logs(args.app_name, args.hostname)
    elif args.command == "ps":
        cmd_ps(args.app_name, args.hostname)
    elif args.command == "restart":
        cmd_restart(args.app_name, args.hostname)
    elif args.command == "sync":
        cmd_sync(args.hostname)
    elif args.command == "upgrade":
        cmd_upgrade(args.app_name, args.hostname)
    else:
        print(
            "Usage: python main.py <command> [options]\nCommands: apps, logs, ps, restart, sync, upgrade"
        )
        sys.exit(1)
