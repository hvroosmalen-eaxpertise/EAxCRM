"""Negative fixture: SQL passed to Repository.SQLQuery is allowed."""
from ea_session import ea_repository  # noqa: F401


def read_element(repo, guid):
    return repo.SQLQuery("SELECT ea_guid FROM t_object WHERE ea_guid=?", [guid])
