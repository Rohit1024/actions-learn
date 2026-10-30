'use strict';

const { appendFileSync } = require('node:fs');
const { greet } = require('./greet.cjs');

try {
  const greeting = greet(process.env.INPUT_NAME ?? '');
  if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
  appendFileSync(process.env.GITHUB_OUTPUT, `greeting=${greeting}\n`, 'utf8');
  console.log(greeting);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
