import asyncio
import fastapi_jsonrpc as jsonrpc
from fastapi import Depends
from loguru import logger

from core.tree import *
from core.errors import *
from core.authorizer import *

# JSON-RPC entrypoint
api_v1 = jsonrpc.Entrypoint('/api/v1')

# Server singletons
merkle_tree = Tree()
auth = Authorizer()

# RPC Methods

@api_v1.method(errors=[ChecksumFormatError, AuthorizationError])
def submit(api_key:str, checksum:str) -> bool:
    """Expect a bytestring in hexadecimal representing the hash digest of the file you want to timestamp. The response will be a boolean indicating if the submission was accepted by the calendar (but the proof of existence is assumed incomplete). Digests submitted this block are idempotent - meaning that you can only timestamp a file once per block."""
    logger.info("Checksum {} submitted for inclusion", checksum)
    if(Authorizer.contains(api_key)):
        return merkle_tree.stamp(checksum)
    else:
         raise AuthorizationError


@api_v1.method(errors=[ChecksumFormatError, ChecksumNotFoundError, AuthorizationError])
def proof(api_key: str, checksum:str) -> dict:
    """Expects a bytestring already submitted. The response will be an existing proof upgraded to its latest commitment.Or an error indicating the checksum must be submitted first. This endpoint should be polled by submitters of incomplete timestamps for proofs that include the complete anchor.""" 
    logger.info("Checksum {} submitted for inclusion", checksum)
    if(Authorizer.contains(api_key)):
        return merkle_tree.proofFor(checksum)
    else:
         raise AuthorizationError


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
