"""Main database entry"""
from sqlite_database import Database
from env import environ

PATH = environ.get("SQLITE_PATH", ":memory:")

database = Database(PATH)

__all__ = ['database']
