"""Main Application"""
# pylint: disable=redefined-builtin,unused-argument
from flask import Response, abort, jsonify, redirect, render_template, request, url_for
from future_router import Router, ResourceDummy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from db.url import URLEntry
from errors import ValidationError

from .utils import validate_request, validate_update

limiter = Limiter(get_remote_address,
                  default_limits=['60/minute', "500/day"],
                  #   storage_uri="memcached://localhost:11211"
                  )
route = Router()


@route.resource("/url")
class Main(ResourceDummy):
    """Main resource class"""

    @staticmethod
    def index() -> str:
        """Return index.html"""
        return render_template("index.html")

    @staticmethod
    def create() -> str:
        """Show the user/form response"""
        return abort(404)

    @limiter.limit("5/minute")
    @staticmethod
    def store() -> Response:
        """Store user request"""
        data = validate_update(request)
        # print(data)
        entry = URLEntry.create(data['target'])
        return jsonify({
            "message": "Successfully shortened URL",
            "status": "success",
            "url": f"/u/{entry.bind}"
        })

    @staticmethod
    def edit(id) -> str:
        """Show user edit form response."""
        return 404

    @limiter.limit("5/minute")
    @staticmethod
    def update(id) -> Response:
        """Update user request"""
        try:
            data = validate_request(request)
        except ValidationError:
            data = validate_update(request)
        URLEntry.fetch(id).update(data['target'])
        return redirect('/')

    @limiter.limit("5/minute")
    @staticmethod
    def destroy(id) -> Response:
        """Delete user request"""
        URLEntry.fetch(id).destroy()
        return redirect("/")

    @staticmethod
    def show(id) -> Response:
        """Return redirect to target"""
        return redirect(URLEntry.fetch(id).target)
