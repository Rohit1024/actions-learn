'use strict';

// Deliberate defect: a logged exception does not set failure status.
const { appendFileSync } = require('node:fs');
const { greet } = require('./greet.cjs');

try {
  const greeting = greet(process.env.INPUT_NAME ?? 'World');
  if (!process.env.GITHUB_OUTPUT) {
    throw new Error('GITHUB_OUTPUT must be set');
  }
  appendFileSync(process.env.GITHUB_OUTPUT, `greeting=${greeting}\n`, 'utf8');
  console.log(greeting);
} catch (error) {
  console.error(error.message);
}
