"""Create database entry"""
from sqlite_database import text

from . import database


def init():
    """Initialise database creation"""
    database.reset_table("url", [
        text("bind").primary(),
        text('target')
    ])
    return True
