"""This singleton issues new API secrets and keeps the digests for valid API secrets in a Redis Instance"""
from walrus import *
import hashlib
import secrets

from .errors import *

class Authorizer:
    """Authorizer class should be treated as a singleton that allows for quick search of a submitted API key's SHA256 hash against the approved list of keys"""
    def __init__(self, db):
        self.store = db.Set('acess_tokens')

    def generate_key(self):
        """returns a newly generated API key and adds it to the set of authorized keys"""
        key = str.encode(secrets.token_hex(16))
        self.add(key)
        return key


    def add(self, api_key=None):
        """add a raw API key to the database, do not add hashed keys here."""
        if api_key is None:
            return AuthorizationError
        hashed_key = hashlib.sha256(api_key).hexdigest()
        self.store.add(str.encode(hashed_key))

    def contains(self, api_key=None):
        if api_key is None:
            return AuthorizationError
        hashed_key = hashlib.sha256(str.encode(api_key)).hexdigest()
        return hashed_key in self.store