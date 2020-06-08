"""This script has all the essential functions to access the timestamping functions of a Data-Timestamp calendar server."""
import hashlib
import requests
import json

import pymerkle

submit_route="http://localhost:5000/api/v1/submit"
proof_route="http://localhost:5000/api/v1/proof"
m = hashlib.sha256()
m.update(b"a random string")


submit_payload = {
  "jsonrpc": "2.0",
  "id": 0,
  "method": "submit",
  "params": {
    "checksum": m.hexdigest()
  }
}

proof_payload = {
  "jsonrpc": "2.0",
  "id": 0,
  "method": "proof",
  "params": {
    "checksum": m.hexdigest()
  }
}
    

if __name__ == '__main__':

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