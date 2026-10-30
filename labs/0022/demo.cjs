'use strict';
const path = require('node:path');
const { run } = require('../0019/process.cjs');
const scenario = process.argv[2] ?? 'pages';
console.log(JSON.stringify(run(path.join(__dirname,
  process.argv.includes('--broken') ? 'broken.cjs' : 'index.cjs'), { INPUT_SCENARIO: scenario }), null, 2));
