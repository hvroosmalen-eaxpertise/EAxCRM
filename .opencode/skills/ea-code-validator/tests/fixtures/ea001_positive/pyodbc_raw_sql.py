"""Fixture: violates EA001 by using pyodbc with raw SQL against t_object."""
from ea_session import ea_repository  # noqa: F401

import pyodbc


def touch():
    with pyodbc.connect("DRIVER={SQLite3};Database=repo.qea") as conn:
        conn.execute("UPDATE t_object SET note='x' WHERE ea_guid='X'")
