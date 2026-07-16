"""Negative: PowerShell 'Select-Object' identifier must not match SELECT."""
from ea_session import ea_repository  # noqa: F401

import subprocess


def get_ea_pids():
    out = subprocess.check_output(
        ["powershell", "-command",
         "Get-Process -Name 'EA' -ErrorAction SilentlyContinue "
         "| Select-Object -ExpandProperty Id"],
        text=True,
    )
    return out
