import json

import pytest

from app.api import crud



def test_create_stamp(test_app):
    response = test_app.post("/api/v1/submit", json={
  "jsonrpc": "2.0",
  "id": 0,
  "method": "submit",
  "params": {
    "checksum": "3c7ecd612d792941b9e4e341ab01ef4cac6cee40ed0c0ef912a7c5dc380d5865"
  }
})
    assert response.status_code == 200

def test_reject_bad_hash(test_app):
    response = test_app.post("/api/v1/submit", json={
  "jsonrpc": "2.0",
  "id": 0,
  "method": "submit",
  "params": {
    "checksum": "badhash"
  }
})
    assert response.status_code == 200
    assert response.json =={
  "error": {
    "code": 6000,
    "message": "Checksum improperly formed error"
  },
  "jsonrpc": "2.0",
  "id": 0
}

def test_valid_proof(test_app):
    pass

def test_proof_upgrade(test_app):
    pass



def test_consistency(test_app):
    """demonstrate that the service can prove a new merkle root has a specific anscestor"""
    pass
