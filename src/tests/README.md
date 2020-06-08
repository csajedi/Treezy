# Testing Strategy

There are two kinds of tests we concern ourselves with at present:

* Unit Tests
* Stability Tests

The Unit tests are found in the typical pytest locations and can all be run collectively via src/test.sh.

The Stability Tests are tests of the performance of the service at the limits of its implementation. In our case, this is mainly done by stress testing the server. See src/stability_test.sh for how this is done. Briefly, we attempt to spam the server with various requests and use the logger to catch errors.