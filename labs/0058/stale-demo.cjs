'use strict';

const assert = require('node:assert/strict');
const { mkdtempSync, cpSync, readFileSync, writeFileSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');
const { spawnSync } = require('node:child_process');

const copy = mkdtempSync(join(tmpdir(), 'stale action '));
try {
  cpSync(join(__dirname, 'action'), join(copy, 'action'), { recursive: true });
  const build = mode => spawnSync(process.execPath, [join(__dirname, 'build.cjs'), mode, copy], { encoding: 'utf8' });
  assert.equal(build('--check').status, 0);
  const source = join(copy, 'action/src/domain.ts');
  writeFileSync(source, readFileSync(source, 'utf8').replace(
    'return `${component}-${channel}`;', 'return `v2-${component}-${channel}`;'));
  const stale = build('--check');
  assert.equal(stale.status, 1);
  console.log(stale.stderr.trim());
  const output = join(copy, 'output.txt');
  const invoke = () => {
    writeFileSync(output, '');
    const env = { ...process.env, INPUT_COMPONENT: 'docs', INPUT_CHANNEL: 'preview', GITHUB_OUTPUT: output };
    const run = spawnSync(process.execPath, [join(copy, 'action/dist/index.cjs')], { env, encoding: 'utf8' });
    assert.equal(run.status, 0, run.stderr);
    return readFileSync(output, 'utf8').trim();
  };
  assert.equal(invoke(), 'release-key=docs-preview');
  console.log('Before rebuild: release-key=docs-preview');
  assert.equal(build('--write').status, 0);
  assert.equal(build('--check').status, 0);
  assert.equal(invoke(), 'release-key=v2-docs-preview');
  console.log('After rebuild: release-key=v2-docs-preview');
  console.log('PASS: stale failure and repair observed in a temporary copy');
} finally {
  rmSync(copy, { recursive: true, force: true });
}
