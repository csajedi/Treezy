# Rewrite anchor_root.js to see if pyzil is viable - NOT VIABLE
from pprint import pprint

from pyzil.crypto import zilkey
from pyzil.zilliqa import chain
from pyzil.zilliqa.units import Zil, Qa
from pyzil.contract import Contract
from pyzil.account import Account, BatchTransfer
chain.set_active_chain(chain.TestNet) 

account=Account(private_key="b8260f6da177a67b9368b27b2ae813b134852202037610934fee866b0ff401a5")
contract_addr = "69277b2ecf69cc6356f57cc057ab5ca7f8910abd"
contract = Contract.load_from_address(contract_addr)

contract.account = account


resp = contract.call(method="updateRoot", params=[Contract.value_dict("new_root", "String", "zzzzcd612d792941b9e4e341ab01ef4cac6cee40ed0c0ef902a7c5dc380d5865")])
pprint(resp)
pprint(contract.last_receipt)
