"""Restart command - Restart a docker compose app via SSH."""

from .utils.apps import find_app
from .utils.ssh import run_ssh_command


def cmd_restart(app_name: str, hostname: str | None) -> None:
    """Restart a docker compose app via SSH."""
    matching_app = find_app(app_name, hostname)
    if not matching_app:
        return

    host, folder = (
        matching_app["remote"].split(":")[0],
        matching_app["remote"].split(":")[1],
    )
    restart_command = f"cd {app_name} && docker compose down && docker compose up -d"
    run_ssh_command(host, folder, restart_command, interactive=True)
