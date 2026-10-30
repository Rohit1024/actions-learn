'use strict';

const { buildSync } = require('esbuild');
const { readFileSync, writeFileSync, mkdirSync } = require('node:fs');
const { resolve, dirname } = require('node:path');

const mode = process.argv[2];
if (!['--write', '--check'].includes(mode)) {
  throw new Error('usage: node labs/0058/build.cjs --write|--check [lab-root]');
}
const root = resolve(process.argv[3] ?? __dirname);
const bytes = Buffer.from(buildSync({
  absWorkingDir: root,
  entryPoints: ['action/src/index.ts'],
  bundle: true, platform: 'node', target: 'node24', format: 'cjs',
  tsconfigRaw: {}, write: false,
}).outputFiles[0].contents);
const destination = resolve(root, 'action/dist/index.cjs');
if (mode === '--write') {
  mkdirSync(dirname(destination), { recursive: true });
  writeFileSync(destination, bytes);
  console.log('Wrote action/dist/index.cjs');
} else if (!readFileSync(destination).equals(bytes)) {
  console.error('FAIL: stale distribution; rebuild with --write and review the diff');
  process.exitCode = 1;
} else {
  console.log('PASS: distribution matches source');
}
