"""This script has all the essential functions to access the timestamping functions of a Data-Timestamp calendar server."""
import hashlib
import requests
import json

import pymerkle

if __name__ == '__main__':

  submit_route="http://localhost:5000/api/v1/submit"
  proof_route="http://localhost:5000/api/v1/proof"
  key_route="http://localhost:5000/api/v1/generate_key"
  m = hashlib.sha256()
  m.update(b"a random string")

  key_payload = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "generate_key",
    "params": {}
  }
  # get an API key to use for our requests
  key_resp = requests.post(key_route, data=json.dumps(key_payload))
  api_key = json.loads(key_resp.text)["result"]
  print("API key for the client: {}", api_key)


    
  submit_payload = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "submit",
    "params": {
      "api_key": api_key,
      "checksum": m.hexdigest()
    }
  }

  proof_payload = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "proof",
    "params": {
      "api_key": api_key,
      "checksum": m.hexdigest()
    }
  }

  # Submits a file by digest to the calendar server for timestamping. Caches the UUID response object to use later for requesting the proof
  r = requests.post(submit_route, data=json.dumps(submit_payload))
  print(r.text)

  # Gets the Proof based on the UUID response
  proof_resp = requests.post(proof_route, data=json.dumps(proof_payload))
  proof_json = json.loads(proof_resp.text)["result"]
  print(proof_json)

  # Reconstructs the tree from the recieved proof to check it is valid
  print("Validating proof...")

  Proof_obj = pymerkle.Proof.deserialize(proof_json)
  if pymerkle.validateProof(Proof_obj):
      print("Proof is valid given parameters")
  else:
      print("invalid proof")