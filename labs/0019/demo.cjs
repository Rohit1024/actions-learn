'use strict';
const path = require('node:path');
const { run } = require('./process.cjs');
const broken = process.argv.includes('--broken');
const missing = process.argv.includes('--missing');
console.log(JSON.stringify(run(path.join(__dirname, broken ? 'broken.cjs' : 'index.cjs'),
  missing ? {} : { INPUT_NAME: 'Ada' }), null, 2));
