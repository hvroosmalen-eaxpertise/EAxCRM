"""Reproduces the shape of the original test_archimate.py bug."""
import sys
import win32com.client

QEA = r"M:\some.qea"

try:
    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(QEA)
    print("OK")
    repo.CloseFile()
except Exception as e:
    print(f"FAIL: {e}")
    sys.exit(1)
