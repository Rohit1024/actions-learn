'use strict';

const { buildSync } = require('esbuild');
const { readFileSync } = require('node:fs');

const result = buildSync({
  entryPoints: ['examples/typescript-action/src/index.ts'],
  bundle: true,
  platform: 'node',
  target: 'node24',
  format: 'cjs',
  write: false,
});

const committed = readFileSync('examples/typescript-action/dist/index.cjs');
if (!committed.equals(Buffer.from(result.outputFiles[0].contents))) {
  console.error('TypeScript bundle is stale. Run task actions:build and commit dist/index.cjs.');
  process.exitCode = 1;
} else {
  console.log('Committed TypeScript bundle matches source.');
}
