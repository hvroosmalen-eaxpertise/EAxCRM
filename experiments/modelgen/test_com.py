"""Minimal EA COM test."""
import sys, os

QEA = r"M:\EAxCRM\models\EAxCRM.qea"

try:
    import win32com.client
    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(QEA)
    print(f"OK: Connected to {repo.ConnectionString}")
    root = repo.Models.GetAt(0)
    print(f"Root: '{root.Name}' ({root.PackageID})")
    for i in range(root.Packages.Count):
        c = root.Packages.GetAt(i)
        print(f"  Child: '{c.Name}' ({c.PackageID})")
    repo.CloseFile()
except Exception as e:
    print(f"FAIL: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)
