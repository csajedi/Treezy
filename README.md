# Chronos: A public  timestamping service for Zilliqa 

There are many cases where a blockchain transaction is not required to achieve the benefit of a public ledger. A well-known example being a timestamp or other time artifact that can serve as a proof of existance prior to a certain point in time. Many examples exist for Bitcoin and other public ledgers, including BTStamp, OpenTimestamps and The Ethereum Chronos project. Zilliqa offers several unique properties that make timestamping against its pool of hashpower particularly attractive.
In comparison with OpenTimeStamps, which forwards to Bitcoin, our service can offer timestamps with an interval of 30s (the current Zilliqa blockchain) and finality in at most 1 minute. Bitcoin's Nakamoto consensus and long unreliable blocktime mean that a timestamp client must wait hours to a full day before they can be confident a timestamp will be upgraded to a full proof. 

Beyond that, Bitcoin's facility for native smart contracts is limited, while Zilliqa is a smart contract platform. The potential benefit for having a real-world oracle that exposes trustworthy proofs of existance on-chain is hard to fully imagine, but it certainly makes a lot of sense for the Zilliqa network to host this service, reliably and free of up-front cost in order to provide a more robust option to innovators looking to distrupt established processes in legal practices and financial applications worldwide. In some countries it is already included in the law that Blockchain-backed timestamps can be considered notorized if they can be audited.

This service's design borrows some from the OpenTimestamps project, but due to the differences between Zilliqa and Bitcoin it must be adapted heavily to achieve most benefit. The .ots file format may one day be supported, but for now we will rely on JSON, as one of the primary goals of this project is proofs between machines and servers. 


## System
This system is a JSON-RPC 2.0 Server implemented in FastAPI, which keeps a persistent merkle tree in sync with a file-backed log and periodic on-chain updates. The on-chain updates serve to anchor the merkle tree's state to blocknumbers of the Zilliqa blockchain and provide notorization of files as proof of existence, backed by the entire hashpower of the Zilliqa mainnet. 
Docker-Swarm and ZODB are relied on heavily to manage the system and provide persistence. The implementation is intended to be cloud-portable in Docker containers, but only AWS will be tested in production. 
 
### RPC Service
We use JSON-RPC 2.0 for several reasons. Mainly, because of the nature of merkle proofs we will always provide create-or-update functionality from the same endpoing, JSON-RPC defines itself around method calls to POST endpoint(s), so the remaining functionality of REST is not needed. Additionally, this is more typical for IoT and service meshes, since RPC is message-oriented knowing the system is sufficient. Finally, Zilliqa's interactions are all defined as a JSON-RPC 2.0 service so familiarity and compatibility will benefit any developers looking to fork the project as the basis for their own dapp. 

### Smart Contracts

(* Mutable variable storing the latest merkle root *)
uint256 Merkle Root


### Incomplete and Complete Proof Files

### Client-side digest generation, privacy features.

## Development

To learn the basics of our development approach, this [guide](https://testdriven.io/blog/fastapi-crud/) may be helpful.

Once you Run `.src/build.sh`,  go to 
[http://localhost:8002/docs](http://localhost:8002/docs) to easily interact with the system.

run your pytests in the container with `./src/test.sh`
