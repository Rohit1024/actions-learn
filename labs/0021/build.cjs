'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { bundle } = require('./bundle.cjs');
fs.mkdirSync(path.join(__dirname, 'dist'), { recursive: true });
fs.writeFileSync(path.join(__dirname, 'dist/index.cjs'), bundle());
console.log('Built labs/0021/dist/index.cjs.');
