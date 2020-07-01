/* Test Cases:
1. Anchor messages rejected until Authority is set
2. Only _owner can set Authority
3. Authority can send merkle roots
4. Non-anchor (even _owner) cannot send anchor events
*/

/* setup testing environment */

const fs = require('fs')
const { Zilliqa } = require('@zilliqa-js/zilliqa');
const {
    toBech32Address
} = require('@zilliqa-js/crypto');
deploy = require('../deploy')
const zilliqa = new Zilliqa('https://dev-api.zilliqa.com');

function exportToJsonFile(jsonData, name) {
  let dataStr = JSON.stringify(jsonData);
  fs.writeFileSync(name, dataStr, (err) => {
      if (err) throw err;
      console.log('Data written to file');
  });
  console.log("wrote json to FormData.json")
}

async function test(contractAddr) {
  /**
   * initialising contract class. Contract class is a convenient way for you to use
   * repeatedly call contracts and make queries from.
   *
   * There's two types of "data" in scilla. Mutable fields (available through getState)
   * and immutable fields (cannot be changed once deployed, available through getInit)
   */
  const contract = zilliqa.contracts.at(contractAddr);
  const allState = await contract.getState();
  console.log(`Getting the entire contract state`);
  exportToJsonFile(allState,"state_init.json")

  const initState = await contract.getInit();
  console.log(`Getting the contract init (immutable variables)`);
  console.log(initState);

  console.log(`\n\nGetting the Anchor from the contract`);
  const state2 = await contract.getSubState('authority');
  console.log(state2);

  console.log(`\n\nGetting a particular entry in a map`);
  const state3 = await contract.getSubState('latestMerkleRoot');
  console.log(state3);

  /**
   * Don't want to initialise a class as you are just making an adhoc query? Try this.
   */

  console.log(
    `\n\nYou can also get state / substate directly without using the Contract class.`,
  );
  const state4 = await zilliqa.blockchain.getSmartContractSubState(
    '0x69277b2ecf69cc6356f57cc057ab5ca7f8910abd',
    'authority'
  );
  console.log(state4.result);
}

async function main(){
    //main assumes that you want to deploy a new contract
    // Standard anchor.scilla deployed on devnet
    // const contractAddr = toBech32Address("69277b2ecf69cc6356f57cc057ab5ca7f8910abd");
    newAddr=toBech32Address("dd5aa7b3b029caf0cb070ee230bded6265ff0304")
    test(newAddr);
}
main();

