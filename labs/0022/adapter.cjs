'use strict';
const { appendFileSync } = require('node:fs');
const { fakeClient } = require('./fake-client.cjs');
const { issueReport } = require('./report.cjs');

async function runAction(swallowErrors = false) {
  try {
    const client = fakeClient(process.env.INPUT_SCENARIO ?? 'pages');
    let report;
    if (swallowErrors) {
      // Deliberate defect used only by broken.cjs.
      report = await issueReport(client).catch(() => ({ count: 0, titles: [] }));
    } else {
      report = await issueReport(client);
    }
    if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
    appendFileSync(process.env.GITHUB_OUTPUT, `report=${JSON.stringify(report)}\n`, 'utf8');
    console.log(`count=${report.count}; requests=${client.calls.length}; waits=${JSON.stringify(client.waits)}`);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

module.exports = { runAction };
