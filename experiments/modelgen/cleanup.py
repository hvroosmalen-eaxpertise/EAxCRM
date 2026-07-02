"""Clean up test elements."""
import sys
import ea_session

QEA = r"M:\EAxCRM\models\EAxCRM.qea"

try:
    with ea_session.ea_repository(QEA) as repo:
        root = ea_session.get_model_root(repo)
        app_arch = None
        for i in range(root.Packages.Count):
            p = root.Packages.GetAt(i)
            if p.Name == "Application Architecture":
                app_arch = p
                break

        pkgs = []
        for i in range(app_arch.Packages.Count):
            p = app_arch.Packages.GetAt(i)
            if p.Name == "EAxCRM":
                pkgs.append(p)

        if not pkgs:
            print("No EAxCRM packages found.")
        else:
            for pkg in pkgs:
                n = pkg.Elements.Count
                for j in range(n - 1, -1, -1):
                    e = pkg.Elements.GetAt(j)
                    print(f"  Delete elem [{j}]: '{e.Name}' (ID={e.ElementID})")
                    pkg.Elements.Delete(j)
                    pkg.Update()
                pkg.Update()
                print(f"  Deleted {n} elements from package ID={pkg.PackageID}")

    print("Done.")

except Exception as e:
    print(f"FAIL: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)
