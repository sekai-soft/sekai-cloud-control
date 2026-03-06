"""Upgrade command - Pull and update docker compose apps via SSH."""

from .utils.apps import find_app
from .utils.ssh import run_ssh_command


def cmd_upgrade(app_name: str, hostname: str | None) -> None:
    """Upgrade a docker compose app via SSH."""
    matching_app = find_app(app_name, hostname)
    if not matching_app:
        return

    host, folder = (
        matching_app["remote"].split(":")[0],
        matching_app["remote"].split(":")[1],
    )
    upgrade_command = f"cd {app_name} && docker compose pull && docker compose up -d"
    run_ssh_command(host, folder, upgrade_command, interactive=True)
