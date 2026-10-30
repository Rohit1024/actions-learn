'use strict';
const { buildSync } = require('esbuild');

// One option set for generation and comparison; no timestamps or machine-specific paths.
function bundle() {
  return Buffer.from(buildSync({
    absWorkingDir: __dirname,
    entryPoints: ['src/index.ts'],
    outfile: 'dist/index.cjs',
    bundle: true,
    platform: 'node',
    target: 'node24',
    format: 'cjs',
    write: false,
    logLevel: 'silent',
  }).outputFiles[0].contents);
}

module.exports = { bundle };
