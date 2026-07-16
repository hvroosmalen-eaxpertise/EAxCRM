"""Fixture: violates EA001 by opening the .qea file via sqlite3."""
from ea_session import ea_repository  # noqa: F401  — forces EA-touching scope

import sqlite3


def read_elements(qea_path):
    conn = sqlite3.connect(qea_path)
    cur = conn.cursor()
    cur.execute("SELECT ea_guid FROM t_object")
    return cur.fetchall()
