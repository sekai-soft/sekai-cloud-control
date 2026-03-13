"""SSH utility functions for running remote commands."""

import signal
import subprocess
import sys
from typing import Any


def handle_interrupt(signum, frame):
    print("\nInterrupted")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_interrupt)
signal.signal(signal.SIGTERM, handle_interrupt)


def run_ssh_command(
    host: str, folder: str, command: str, interactive: bool = False
) -> str:
    """Run a command on a remote host via SSH."""
    cmd = f"ssh {host} 'cd {folder} && {command}'"
    if interactive:
        result = subprocess.run(
            cmd,
            shell=True,
            executable="/bin/sh",
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=False,
        )
        return ""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def has_compose_yml(host: str, folder: str, app_name: str) -> bool:
    """Check if an app folder contains a compose.yml or compose.yaml file."""
    result = subprocess.run(
        f"ssh {host} 'test -f {folder}/{app_name}/compose.yml || test -f {folder}/{app_name}/compose.yaml'",
        shell=True,
        capture_output=True,
    )
    return result.returncode == 0


def get_docker_apps(host: str, folder: str) -> list[dict[str, Any]]:
    """Fetch docker compose apps from a host's folder."""
    output = run_ssh_command(host, folder, "ls -1")
    apps = []
    for line in output.strip().split("\n"):
        if line:
            if has_compose_yml(host, folder, line):
                apps.append({"name": line, "path": line, "remote": f"{host}:{folder}"})
    return apps
