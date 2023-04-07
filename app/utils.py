"""App-specific utility"""

from flask import Request

from errors import ValidationError
from utils import validate_url


def validate_request(request: Request):
    """Validate current request"""
    bind = request.form.get("bind", "-")
    target = request.form.get("target", '-')

    if bind == "-" or target == '-':
        raise ValidationError("Request failed, not enough arguments")
    if validate_url(target) is False:
        raise ValidationError("Request failed, url mismatch.")
    return {
        "bind": bind,
        "target": target
    }


def validate_update(request: Request):
    """Validate current request for update."""
    target = request.form.get('target', '-')

    if target == '-':
        raise ValidationError("Request failed, not enough arguments")
    if validate_url(target) is False:
        raise ValidationError("Request failed, url mismatch.")
    return {'target': target}
