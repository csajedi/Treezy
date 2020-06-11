"""This singleton issues new API secrets and keeps the digests for valid API secrets in a Redis Instance"""
from walrus import *
import hashlib
import secrets

class Authorizer:
    """Authorizer class should be treated as a singleton that allows for quick search of a submitted API key's SHA256 hash against the approved list of keys"""
    def __init__(self, db):
        self.store = db.Set('acess_tokens')

    def generate_key(self):
        """returns a newly generated API key and adds it to the set of authorized keys"""
        key = secrets.token_hex(16)
        self.add(key)
        return key


    def add(self, api_key):
        """add a raw API key to the database, do not add hashed keys here."""
        hashed_key = hashlib.sha256(api_key)
        self.store.add(hashed_key)

    def contains(self, api_key):
        hashed_key = hashlib.sha256(api_key)
        return self.store.contains(hashed_key)