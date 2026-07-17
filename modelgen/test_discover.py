"""Discover EA COM API Element properties."""
import sys, os, inspect

QEA = r"M:\EAxCRM\models\EAxCRM.qea"

try:
    import win32com.client
    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(QEA)

    root = repo.Models.GetAt(0)
    app_arch = root.Packages.GetAt(0)
    for i in range(root.Packages.Count):
        p = root.Packages.GetAt(i)
        if p.Name == "Application Architecture":
            app_arch = p

    eax_pkg = app_arch.Packages.GetAt(0)  # EAxCRM

    # Get an existing element
    el = eax_pkg.Elements.GetAt(0)
    print(f"Element: '{el.Name}'")
    print(f"  Type: {el.Type}")
    print(f"  StereotypeEx: {el.StereotypeEx}")
    print(f"  Stereotype: {el.Stereotype}")
    print(f"  ObjectType: {el.ObjectType}")

    # List all accessible properties
    print("\nAll properties via dir:")
    for attr in sorted(dir(el)):
        if not attr.startswith('_') and not attr.startswith('__'):
            try:
                val = getattr(el, attr)
                if not callable(val):
                    print(f"  {attr} = {val}")
            except:
                print(f"  {attr} = <error>")

    repo.CloseFile()
except Exception as e:
    print(f"FAIL: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)
