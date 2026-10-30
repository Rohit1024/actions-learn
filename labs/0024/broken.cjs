'use strict';
// Deliberate hidden dependency on a Unix executable and its newline semantics.
const { execFileSync } = require('node:child_process');
const path = require('node:path');
try {
  const file = path.resolve(process.env.GITHUB_WORKSPACE, process.env.INPUT_FILE);
  console.log(execFileSync('wc', ['-l', file], { encoding: 'utf8' }).trim());
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
