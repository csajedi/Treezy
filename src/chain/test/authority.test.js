const test = require('tape')
// Scenario 0: No Authority set
// Should NOT - allow any merkle roots to be set until the Authority is set
// Should NOT - allow a non-owner to set the Authority
// Should - Allow the _owner to set the Authority