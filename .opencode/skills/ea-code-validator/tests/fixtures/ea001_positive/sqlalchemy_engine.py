"""Fixture: violates EA001 by creating a SQLAlchemy engine on the EA repo."""
from ea_session import ea_repository  # noqa: F401

import sqlalchemy


def open_engine():
    return sqlalchemy.create_engine("sqlite:///repo.qea")
