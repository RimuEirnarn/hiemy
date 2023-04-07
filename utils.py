"""Universal utility"""
from urllib.parse import urlparse


def validate_url(url: str):
    """Validate url"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
