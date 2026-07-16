"""Fixture: reflows existing DiagramObjects — violates EA003."""
from ea_session import ea_repository  # noqa: F401


def reflow(diagram):
    for i in range(diagram.DiagramObjects.Count):
        dobj = diagram.DiagramObjects.GetAt(i)
        dobj.left = i * 200
        dobj.top = 100
        dobj.right = dobj.left + 150
        dobj.bottom = 300
        dobj.Update()
