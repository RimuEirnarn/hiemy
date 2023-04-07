"""URL Model"""
from secrets import choice
from typing import NamedTuple
from string import ascii_lowercase, ascii_uppercase

from sqlite_database import op

from errors import ValidationError
from utils import validate_url
from . import database
from .create import init

if not database.check_table('url'):
    init()

mapped_char = ascii_uppercase + ascii_lowercase
url_table = database.table("url")


class URLEntry(NamedTuple):
    """Base URL Model."""
    bind: str
    target: str

    @classmethod
    def _create(cls, bind: str, target: str):
        """Create and push data to table"""
        if not validate_url(target):
            raise ValidationError("Target malformed.")
        url_table.insert({
            "bind": bind,
            "target": target
        })
        return cls(bind, target)

    @staticmethod
    def create(target: str):
        """Create and push data to table, except without bind parameter."""
        bind = ''.join(choice(mapped_char) for _ in range(6))
        return URLEntry._create(bind, target)

    def destroy(self):
        """Destroy current data from table"""
        try:
            url_table.delete_one({
                "bind": op == self.bind
            })
            return True
        except Exception:
            return False

    def update(self, target: str):
        """Update current target."""
        try:
            return any([url_table.update({"target": target}, {'bind': op == self.bind})])
        except Exception:
            return False

    @classmethod
    def fetch(cls, bind: str):
        """Fetch from bind"""
        return cls(**url_table.select_one({
            "bind": op == bind
        }))
