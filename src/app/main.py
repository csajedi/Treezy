
import fastapi_jsonrpc as jsonrpc
from fastapi import Depends
from loguru import logger

from core.tree import *
from core.errors import *

# JSON-RPC entrypoint
api_v1 = jsonrpc.Entrypoint('/api/v1/')

# Server singletons
merkle_tree = Tree()


# RPC Methods

@api_v1.method(errors=[ChecksumFormatError])
def submit(checksum:bytes) -> bool:
    """Expect a bytestring in hexadecimal representing the hash digest of the file you want to timestamp. The response will be a boolean indicating if the submission succeeded. Note if you a re-submitting a digest that is the same, the proof method will still return the oldest checksum's proof."""
    return merkle_tree.stamp(checksum)


@api_v1.method(errors=[ChecksumFormatError, ChecksumNotFoundError])
def proof(checksum:bytes) -> dict:
    """Expects a bytestring already submitted. The response will be an existing proof upgraded to its latest commitment.Or an error indicating the checksum must be submitted first""" 
    return merkle_tree.proofFor(checksum)

@api_v1.method()
def consistency(past_root:str) -> dict:
    """This method calls the merkle tree's consistency proof - demonstrating a given merkle root is an ancestor of the present one. If nothing is passed as parameter, the present merkle root is returned."""
    if past_root is None:
        return merkle_tree.current_root()
    else:
        return merkle_tree.consistency_proof(past_root)


@api_v1.method()
def validate(proof:dict) -> dict:
    """This method validates the serialized proof against its local merkle tree. It does not indicate that the proof is anchored, only that its checksum exists and the proof is well-formed. It is not recommended over the client validate, as the client can check the mainchain for valid anchoring"""
    return merkle_tree.validate(proof)


# entrypoint: ./api/v1/... methods=stamp, tree, validate
app = jsonrpc.API()
app.bind_entrypoint(api_v1)


# configure logger session
@app.on_event("startup")
async def startup():
    logger.add("file_{time}.log")
    logger.info("Service is Spinning Up")

# Dump the logs if a shutdown is occuring.
@app.on_event("shutdown")
async def shutdown():
    # ideally you'd put this backup in a docker volume, S3 or Grafana-compatible store.
    merkle_tree.export()
    logger.info("Service is Shutting Down")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=5000, debug=True, access_log=False)
