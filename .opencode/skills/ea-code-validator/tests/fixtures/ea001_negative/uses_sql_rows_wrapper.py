"""Negative fixture: ea_session.sql_rows is the blessed SQLQuery wrapper."""
from ea_session import sql_rows  # noqa: F401
import ea_session


def read_elements(repo, pkg_id):
    return ea_session.sql_rows(repo, f"""
        SELECT Object_ID, Name FROM t_object
        WHERE Package_ID = {pkg_id}
    """)


def read_via_bare_import(repo):
    return sql_rows(repo, "SELECT ea_guid FROM t_object")
