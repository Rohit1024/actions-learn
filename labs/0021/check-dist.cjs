'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { bundle } = require('./bundle.cjs');
const destination = path.join(__dirname, 'dist/index.cjs');
if (!fs.existsSync(destination) || !fs.readFileSync(destination).equals(bundle())) {
  console.error('STALE: run node labs/0021/build.cjs; review source and dist together.');
  process.exitCode = 1;
} else {
  console.log('PASS: labs/0021/dist/index.cjs matches source.');
}
