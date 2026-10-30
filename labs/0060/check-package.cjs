'use strict';

const assert = require('node:assert/strict');
const { mkdtempSync, readFileSync, writeFileSync, rmSync, existsSync } = require('node:fs');
const { join, resolve, isAbsolute } = require('node:path');
const { tmpdir } = require('node:os');
const { spawnSync } = require('node:child_process');

const root = resolve(process.argv[2] ?? join(__dirname, 'package'));
const scratch = mkdtempSync(join(tmpdir(), 'consumer snapshot '));
try {
  const metadataPath = join(root, 'action.yml');
  assert.ok(existsSync(metadataPath), 'missing root action.yml');
  // This inspector deliberately supports this lab metadata, not arbitrary YAML.
  const metadata = readFileSync(metadataPath, 'utf8');
  assert.match(metadata, /using: node24/);
  const main = /^  main: ([a-zA-Z0-9_./-]+)$/m.exec(metadata)?.[1];
  assert.ok(main && !isAbsolute(main) && !main.split('/').includes('..'), 'invalid runs.main');
  const entrypoint = join(root, main);
  assert.ok(existsSync(entrypoint), `missing runtime file: ${main}`);
  const output = join(scratch, 'consumer output.txt');
  writeFileSync(output, '');
  const env = { ...process.env, INPUT_COMPONENT: 'docs', INPUT_CHANNEL: 'stable', GITHUB_OUTPUT: output };
  const result = spawnSync(process.execPath, [entrypoint], { cwd: scratch, env, encoding: 'utf8', timeout: 10000 });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(readFileSync(output, 'utf8'), 'release-key=docs-stable\n');
  console.log('PASS: root metadata selects a runnable distribution from a different working directory');
  console.log('PASS: isolated consumer received release-key=docs-stable');
} catch (error) {
  console.error(`FAIL: ${error.message}`);
  process.exitCode = 1;
} finally {
  rmSync(scratch, { recursive: true, force: true });
}
