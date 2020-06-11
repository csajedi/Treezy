import json
import os

import pytest
from walrus import *

# CONN_URL = os.getenv("REDIS_URL")

def test_connection():
    """Simply check that the server can send then retrieve data from Redis"""
    db = Database(host='redis', port=6379, db=0)
    db['walrus'] = b'tusk'
    assert db['walrus'] == b'tusk'