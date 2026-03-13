"""Down command - Stop docker compose apps via SSH."""

from .utils.apps import find_app
from .utils.ssh import run_ssh_command


def cmd_down(app_name: str, hostname: str | None) -> None:
    """Stop docker compose apps via SSH."""
    matching_app = find_app(app_name, hostname)
    if not matching_app:
        return

    host, folder = (
        matching_app["remote"].split(":")[0],
        matching_app["remote"].split(":")[1],
    )
    down_command = f"cd {folder}/{app_name} && docker compose down"
    run_ssh_command(host, folder, down_command, interactive=True)
