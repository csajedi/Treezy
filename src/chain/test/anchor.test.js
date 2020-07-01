const test = require('tape')
const fs = require('fs')
const { Zilliqa } = require('@zilliqa-js/zilliqa');
const { toBech32Address } = require('@zilliqa-js/crypto');
const zilliqa = new Zilliqa('https://dev-api.zilliqa.com');
const state_0 = require('./state_0.json');
anchor = require('../anchor_root')
/**
 * Run with:
 * node anchor.test.js|npx tap-dot
 * 
 *  Here we test that:
 * 1 - An authority can send arbitrary anchor events and 
 * 2 - non-authorities (including owner) cannot send anchor events. 
*/
contractAddr=toBech32Address("dd5aa7b3b029caf0cb070ee230bded6265ff0304")
const contract = zilliqa.contracts.at(contractAddr);

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
test('testing the fresh contract will reject anchors', function (t) {
    //send an anchor event as Alice wallet

});
test('testing the present authority can update anchor', function (t) {
    //send an anchor event as Alice wallet

    t.deepEqual()
});