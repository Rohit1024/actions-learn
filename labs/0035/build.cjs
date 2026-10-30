'use strict';
const { buildSync } = require('esbuild');
const fs = require('node:fs');
const path = require('node:path');
const args = process.argv.slice(2);
const rootIndex = args.indexOf('--root');
const root = rootIndex < 0 ? __dirname : path.resolve(args[rootIndex + 1]);
const target = path.join(root, 'dist/index.cjs');
const result = buildSync({
  absWorkingDir: root, entryPoints: ['src/index.ts'], outfile: 'dist/index.cjs',
  bundle: true, platform: 'node', target: 'node24', format: 'cjs',
  write: false, logLevel: 'silent',
}).outputFiles[0].contents;
if (args.includes('--check')) {
  if (!fs.existsSync(target) || !Buffer.from(result).equals(fs.readFileSync(target))) {
    console.error('FAIL: distribution differs from current source and builder');
    process.exitCode = 1;
  } else console.log('PASS: distribution matches current source and builder');
} else {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, result);
  console.log('Built local candidate dist/index.cjs');
}
