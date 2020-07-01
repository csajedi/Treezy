# Chain Strategy

Our SideTree only needs to submit a new anchor periodically in order to back the evolution of the tree with the entire hashpower of the Zilliqa blockchain. This subdirectory contains node scripts that are called within the anchor.py wrapper in order to anchor the tree's root across the language boundary.

## test keystore

for convenience of demonstration, a keystore (alice.json) was created to be the authority in testing. The pkey: b8260f6da177a67b9368b27b2ae813b134852202037610934fee866b0ff401a5, and pass: 'alice123'