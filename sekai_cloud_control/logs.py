"""Logs command - Stream logs for a docker compose app via SSH."""

from .utils.apps import find_app
from .utils.ssh import run_ssh_command


def cmd_logs(app_name: str, hostname: str | None) -> None:
    """Stream logs for a docker compose app via SSH."""
    matching_app = find_app(app_name, hostname)
    if not matching_app:
        return

    host, folder = (
        matching_app["remote"].split(":")[0],
        matching_app["remote"].split(":")[1],
    )
    logs_command = f"cd {app_name} && docker compose logs {app_name} -n 100 -f"
    run_ssh_command(host, folder, logs_command, interactive=True)
