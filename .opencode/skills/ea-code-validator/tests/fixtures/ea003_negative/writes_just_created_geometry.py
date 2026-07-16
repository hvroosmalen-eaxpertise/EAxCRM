"""Negative: first-time DiagramObject creation may set geometry."""
from ea_session import ea_repository  # noqa: F401


def place_new(diagram, elem_id):
    dobj = diagram.DiagramObjects.AddNew("", "")
    dobj.left = 100
    dobj.top = 100
    dobj.right = 300
    dobj.bottom = 200
    dobj.Update()


def place_via_create(diagram, elem):
    dobj = diagram.CreateDiagramObject(elem)
    dobj.left = 50
    dobj.top = 50
    dobj.right = 250
    dobj.bottom = 150
    dobj.Update()
