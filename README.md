# Treezy: A simple sidetree RPC server for Zilliqa 

There are many cases where a blockchain transaction is not required to achieve the benefit of a public ledger. Zilliqa offers several unique properties that make it a valuable target for a [SideTree protocol]](https://github.com/decentralized-identity/sidetree/blob/master/docs/protocol.md) implementation, such as fast finality and cheap transactions. To achieve a practical variant of the Sidetree implementation for the Zilliqa community is a one-off task that could yield value through many forks. We do not concern ourselves with some of the standards compliance components, and our merkle tree implementation was selected for the succint proofs it creates for long-running trees. The sidetree protocol documentation can be used for guidance in future developments, which may include an on-chain proof gadget that allows for arbitrary oracles.

Our SideTree implementation is modified to make full use of PyMerkle's efficient tree encoding strategy. It relies on a Redis Cache to act as the mempool, and is ready to act as the datastructure for a sidechain - just add consensus. 
In comparison with SideTree, which has a more general form, our service can offer updates with an interval of 30s (roughly the current Zilliqa blocktime) and finality in at most 2 minutes. Bitcoin's Nakamoto consensus and long unreliable blocktime mean that any off-chain forwarding merkle tree client must wait hours to a full day before they can be confident a merkle root is truly anchored on the new mainchain. 

Beyond that, Bitcoin's facility for native smart contracts is limited, while Zilliqa is a smart contract platform. The greatest potential benefit for having a real-world oracle that exposes trustworthy proofs of inclusion on-chain is in its flexibility.


## System
This system is a JSON-RPC 2.0 Server implemented in FastAPI, which keeps a persistent merkle tree in sync with a file-backed log and periodic on-chain anchor updates. The on-chain updates serve to anchor the merkle tree's state to the Zilliqa blockchain so that data availability is backed by the entire hashpower of the Zilliqa mainnet.

Docker-Swarm and Docker Secrets relied on heavily to manage the system and provide safe handling of keys. The implementation is intended to be cloud-portable in Docker containers, but only AWS will be tested in production by the developers.
 
### RPC Service
We use JSON-RPC 2.0 for several reasons. Mainly, because of the nature of merkle proofs we will always provide create-or-update functionality from the same endpoing, JSON-RPC defines itself around method calls to POST endpoint(s), so the remaining functionality of REST is not needed. Additionally, this is more typical for IoT and service meshes, since RPC is message-oriented knowing the system is sufficient. Finally, Zilliqa's interactions are all defined as a JSON-RPC 2.0 service so familiarity and compatibility will benefit any developers looking to fork the project as the basis for their own dapp. 

### Smart Contracts

The anchor contract is included here, along with deployment and testing scripts targeting the Zilliqa Testnet. It may be useful to add access control to your contract, but that is left out for this implementation. See the BookStore.scilla official example for a more complete CRUD solution.

### Client-side digest generation, privacy features.
The `client.py` example demonstrates the interaction pattern, but any merkle tree library should be able to import and check the provided proofs if they are able to ingest the path embedded in the response JSON. PyMerkle has tree management properties unique to its implementation, but once the merkle proof is generated it should be universal.

## Development

To learn the basics of our development approach, this [guide](https://testdriven.io/blog/fastapi-crud/) may be helpful.
To first build the platform in containers run `docker-compose up -d` or `.src/build.sh`, go to 
[http://localhost:8002/docs](http://localhost:8002/docs) to easily interact with the system.
If you have to rebuild the container during development you might find that running `docker-compose up --force-recreate` will save you headaches from the cached builds.

## Modifying for your needs

If you wish to use this service in your existing authenticated infrastructure, the easiest way would be to enable the JWT authentication commented out in `main.py`, and adding it as middleware to the endpoints you wish to have authentication guards for. It can be left open access by leaving the JWT commented out.

## Security

In order to fully secure your service, you need to figure out how to store the private key for this forwarding server. If you are already using Kubernetes, then you probably know what that means. If you have a DevOps team, then you could use [Consul](https://www.consul.io/). This repo provides an example of using Docker Secrets to store this key, in hopes that it will be sufficiently simple for the Zilliqa community to adopt it as a standard practice, replacing the .env files that have been used by the Ethereum community to store keys.


run your pytests in the container with `./src/test.sh`