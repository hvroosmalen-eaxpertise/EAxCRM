"""Reproduces the shape of the original cleanup.py bug."""
import sys
import ea_session

QEA = r"M:\some.qea"

try:
    with ea_session.ea_repository(QEA) as repo:
        root = repo.Models.GetAt(0)
        print(root.Name)
except Exception as e:
    print(f"FAIL: {e}")
    sys.exit(1)
