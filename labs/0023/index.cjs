'use strict';
const fs = require('node:fs');
const { setup } = require('./resource.cjs');

try {
  const resource = setup(process.env);
  if (!fs.existsSync(resource)) throw new Error('resource missing');
  if (process.env.LAB_FAIL_MAIN === '1') throw new Error('primary work failed deliberately');
  if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
  fs.appendFileSync(process.env.GITHUB_OUTPUT, 'resource=ready\n', 'utf8');
  console.log('primary work succeeded');
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
