'use strict';

// Deliberate defect: action.yml cannot enforce this process's input validation.
const { appendFileSync } = require('node:fs');
const greeting = `Hello, ${(process.env.INPUT_NAME ?? '').trim()}!`;
appendFileSync(process.env.GITHUB_OUTPUT, `greeting=${greeting}\n`, 'utf8');
console.log(greeting);
