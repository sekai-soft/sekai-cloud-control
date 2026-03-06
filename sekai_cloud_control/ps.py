"""PS command - Show container status for a docker compose app via SSH."""

from .utils.apps import find_app
from .utils.ssh import run_ssh_command


def cmd_ps(app_name: str, hostname: str | None) -> None:
    """Show container status for a docker compose app via SSH."""
    matching_app = find_app(app_name, hostname)
    if not matching_app:
        return

    host, folder = (
        matching_app["remote"].split(":")[0],
        matching_app["remote"].split(":")[1],
    )
    ps_command = f"cd {app_name} && docker compose ps"
    run_ssh_command(host, folder, ps_command, interactive=True)
