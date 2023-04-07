"""Environ"""
from os.path import exists
from os import environ
from dotenv import load_dotenv

DOTENV = ".env"

if exists(DOTENV):
    load_dotenv(DOTENV)

__all__ = ["environ"]
