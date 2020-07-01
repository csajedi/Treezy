//Note: that this will not work until you use update_authority.js to set the authority to alice's address
// contract address: 69277b2ecf69cc6356f57cc057ab5ca7f8910abd
const process = require('process');
const {BN, Long, bytes, units} = require('@zilliqa-js/util');
const {Zilliqa} = require('@zilliqa-js/zilliqa');
const {
    toBech32Address,
    getAddressFromPrivateKey,
} = require('@zilliqa-js/crypto');


async function main() {
    console.log(process.argv)
    var root = process.argv[2]
    console.log("anchoring root:")
    console.log(`${root}`)
    const zilliqa = new Zilliqa('https://dev-api.zilliqa.com');
    const CHAIN_ID = 333;
    const MSG_VERSION = 1;
    const VERSION = bytes.pack(CHAIN_ID, MSG_VERSION);
    privkey = 'b8260f6da177a67b9368b27b2ae813b134852202037610934fee866b0ff401a5';
    zilliqa.wallet.addByPrivateKey(
        privkey
    );
    const address = getAddressFromPrivateKey(privkey);
    console.log("Your account address is:");
    console.log(`${address}`);
    const myGasPrice = units.toQa('1000', units.Units.Li); // Gas Price that will be used by all transactions


    const ftAddr = toBech32Address("69277b2ecf69cc6356f57cc057ab5ca7f8910abd");
    try {
        const contract = zilliqa.contracts.at(ftAddr);
        const callTx = await contract.call(
            'updateRoot',
            [
                {
                    vname: 'new_root',
                    type: 'String',
                    value: root, //alice's key
                },
            ],
            {
                // amount, gasPrice and gasLimit must be explicitly provided
                version: VERSION,
                amount: new BN(0),
                gasPrice: myGasPrice,
                gasLimit: Long.fromNumber(10000),
            }
        );
        console.log(JSON.stringify(callTx.receipt, null, 4));

    } catch (err) {
        console.log(err);
    }
}

main();