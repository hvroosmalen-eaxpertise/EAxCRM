"""Test ArchiMate3 element creation - fixed COM API usage."""
import sys, os

QEA = r"M:\EAxCRM\models\EAxCRM.qea"

try:
    import win32com.client
    repo = win32com.client.Dispatch("EA.Repository")
    repo.OpenFile(QEA)
    print("=== Testing ArchiMate3 element creation ===")

    root = repo.Models.GetAt(0)
    # Application Architecture is Package_ID=2
    app_arch = root.Packages.GetAt(0)
    for i in range(root.Packages.Count):
        p = root.Packages.GetAt(i)
        print(f"  Root child: '{p.Name}' (ID={p.PackageID})")
        if p.Name == "Application Architecture":
            app_arch = p
    print(f"Using package: '{app_arch.Name}' (ID={app_arch.PackageID})")

    # Get or create EAxCRM sub-package
    eax_pkg = None
    for i in range(app_arch.Packages.Count):
        p = app_arch.Packages.GetAt(i)
        if p.Name == "EAxCRM":
            eax_pkg = p
            break
    if not eax_pkg:
        eax_pkg = app_arch.Packages.AddNew("EAxCRM", "Package")
        eax_pkg.Update()
        app_arch.Update()
        print(f"  Created EAxCRM package (ID={eax_pkg.PackageID})")
    else:
        print(f"  Found EAxCRM package (ID={eax_pkg.PackageID})")

    # Create element
    elem = eax_pkg.Elements.AddNew("Test Business Actor", "Class")
    elem.StereotypeEx = "ArchiMate3::ArchiMate_BusinessActor"
    elem.Notes = "Test element for ArchiMate3 COM API verification"
    elem.Update()

    # After Update(), fetch from collection by ID
    eax_pkg.Elements.Refresh()
    for i in range(eax_pkg.Elements.Count):
        e = eax_pkg.Elements.GetAt(i)
        if e.ElementID == elem.ElementID:
            print(f"\nCreated element ID={e.ElementID}")
            print(f"  Name: {e.Name}")
            print(f"  StereotypeEx: {e.StereotypeEx}")
            print(f"  Stereotype: {e.Stereotype}")
            print(f"  ObjectType: {e.ObjectType}")
            print(f"  ea_guid: {e.ea_guid}")

            # Store AMEFF identifier as tagged value
            tv = e.TaggedValues.AddNew("ameff_id", "e-test-actor")
            tv.Update()
            e.Update()
            e.TaggedValues.Refresh()
            print("  Tagged values:")
            for j in range(e.TaggedValues.Count):
                tv2 = e.TaggedValues.GetAt(j)
                print(f"    {tv2.Name} = {tv2.Value}")
            break

    # Test diagram
    diag = None
    for i in range(eax_pkg.Diagrams.Count):
        d = eax_pkg.Diagrams.GetAt(i)
        if d.Name == "EAxCRM ArchiMate":
            diag = d
            break
    if not diag:
        diag = eax_pkg.Diagrams.AddNew("EAxCRM ArchiMate", "Application Layer")
        diag.Update()
        eax_pkg.Update()
        print(f"\nCreated diagram: '{diag.Name}'")
        print(f"  Stereotype: {diag.Stereotype}")
        print(f"  DiagramType: {diag.DiagramType}")
    else:
        print(f"\nFound diagram: '{diag.Name}'")

    repo.SaveAndClose()
    print("\nOK: Test completed. Check .qea in Sparx EA.")

except Exception as e:
    print(f"FAIL: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)
