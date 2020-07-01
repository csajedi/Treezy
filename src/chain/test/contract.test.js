const test = require('tape')
const fs = require('fs')

const {BN, Long, bytes, units} = require('@zilliqa-js/util');
const { Zilliqa } = require('@zilliqa-js/zilliqa');
const { toBech32Address } = require('@zilliqa-js/crypto');
const zilliqa = new Zilliqa('https://dev-api.zilliqa.com'); //alice is signer
const zilliqa2 = new Zilliqa('https://dev-api.zilliqa.com'); //owner is signer
const state_0 = require('./state_0.json');
/**
 * Run with:
 * node contract.test.js|npx tap-dot
 * 
 * Assumes:
 * The contract address is for a freshly deployed anchor.scilla, run node ../deploy.js to get a new one
 * 
 *  Here we test that:
 * 0 - Test runner can read fresh contract (please redeploy after running tests)
 * 1 - does NOT allow any merkle roots to be set until the Authority is set
 * 2 - does not allow a non-owner to set the Authority
 * 3 - The _owner can set a new anchor
 * 4 - An authority can send arbitrary anchor events. 
*/

const CHAIN_ID = 333;
const MSG_VERSION = 1;
const VERSION = bytes.pack(CHAIN_ID, MSG_VERSION);
const myGasPrice = units.toQa('1000', units.Units.Li); // Gas Price that will be used by all transactions

privkey = 'b8260f6da177a67b9368b27b2ae813b134852202037610934fee866b0ff401a5';
owner_pkey = "07e0b1d1870a0ba1b60311323cb9c198d6f6193b2219381c189afab3f5ac41a9" //see deploy.js 
zilliqa.wallet.addByPrivateKey(
    privkey
);
zilliqa2.wallet.addByPrivateKey(
    owner_pkey
);
contractAddr=toBech32Address("74bb87daf6cddf92e8642d66a71f38836f55caab")
const contract = zilliqa.contracts.at(contractAddr);
const contract2 = zilliqa2.contracts.at(contractAddr);

/***
 * Determine if the contract provided is still in the fresh state
 */
test('testing if the contract is still fresh', async function(t){
    const allState = await contract.getState();
    t.deepEqual(allState,state_0)
    t.end()

})

/**
 * Determine if the fresh contract without a set authority will reject the anchor
 * Expects: rejected contract call, state remains the same.
 */
test('testing the fresh contract will reject anchors', async function (t) {
    //send an anchor event as Alice wallet
    const callTx = await contract.call(
        'updateRoot',
        [
            {
                vname: 'new_root',
                type: 'String',
                value: 'SHOULD_BE_REJECTED',
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
    t.equal(callTx.receipt.success, false)
    
    //Contract should remain unchanged
    const allState = await contract.getState();
    t.deepEqual(allState,state_0)
    t.end()

});

test('testing non-owners cannot update authority', async function (t) {
    //make up any old wallet
    zilliqa.wallet.create()
    //send an authority update as non-owner
    const callTx = await contract.call(
        'updateAuthorityKey',
        [
            {
                vname: 'new_authority',
                type: 'ByStr20',
                value: '0xC3f26e2F23DEA88a103411Ec1cF174a3FC4D8838', 
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
    t.equal(callTx.receipt.success, false)
    
    //Contract should remain unchanged
    const allState = await contract.getState();
    t.deepEqual(allState,state_0)
    t.end()
});

test('testing the owner can update the contract authority', async function (t) {
    const contract = zilliqa2.contracts.at(contractAddr);
    //send an authority update as owner
    const callTx = await contract.call(
        'updateAuthorityKey',
        [
            {
                vname: 'new_authority',
                type: 'ByStr20',
                value: '0xC3f26e2F23DEA88a103411Ec1cF174a3FC4D8838', //this is alice's key
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
    t.equal(callTx.receipt.success, true)
    
    //Contract should have changed
    const allState = await contract.getState();
    t.notDeepEqual(allState,state_0)
    
    //substate for authority should be set
    const subState = await contract.getSubState("authority")
    t.equals(subState.authority.arguments[0],'0xc3f26e2f23dea88a103411ec1cf174a3fc4d8838')
    t.end()
});


test('testing the authority can update the contract root', async function (t) {
    //send an authority update as owner
    const callTx = await contract.call(
                'updateRoot',
                [
                    {
                        vname: 'new_root',
                        type: 'String',
                        value: 'SHOULD_BE_ACCEPTED',
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
            t.equal(callTx.receipt.success, true)
    
    
    //substate for root should be set
    const subState = await contract.getSubState("latestMerkleRoot")
    t.equals(subState.latestMerkleRoot.arguments[0],'SHOULD_BE_ACCEPTED')
    t.end()
});
