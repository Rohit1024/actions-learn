'use strict';
const scenarios = require('./fixtures/scenarios.json');

// A normalized transport seam, not an HTTP implementation or a full Octokit mock.
// nextUrl represents the rel="next" URL already extracted by the real client.
function fakeClient(scenario) {
  if (!Object.hasOwn(scenarios, scenario)) throw new Error('unknown fixture scenario');
  const responses = structuredClone(scenarios[scenario]);
  const calls = [];
  const waits = [];
  let elapsed = 0;
  return {
    calls, waits,
    now: () => elapsed,
    sleep: async ms => { waits.push(ms); elapsed += ms; },
    request: async ({ method, url }) => {
      calls.push({ method, url });
      const response = responses.shift();
      if (method !== 'GET' || !response || response.url !== url) {
        throw new Error('unexpected fixture request');
      }
      return response;
    },
  };
}

module.exports = { fakeClient };
