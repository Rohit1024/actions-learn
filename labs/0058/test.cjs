'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { buildSync } = require('esbuild');
const { spawnSync } = require('node:child_process');
const { mkdtempSync, writeFileSync, readFileSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');

const scratch = mkdtempSync(join(tmpdir(), 'release key tests '));
const purePath = join(scratch, 'domain.cjs');
writeFileSync(purePath, buildSync({
  entryPoints: [join(__dirname, 'action/src/domain.ts')], bundle: true,
  platform: 'node', target: 'node24', format: 'cjs', tsconfigRaw: {}, write: false,
}).outputFiles[0].contents);
const { releaseKey } = require(purePath);
test.after(() => rmSync(scratch, { recursive: true, force: true }));

test('pure policy returns a stable consumer key', () => {
  assert.equal(releaseKey('docs', 'preview'), 'docs-preview');
  assert.equal(releaseKey('web-2', 'stable'), 'web-2-stable');
});
test('pure policy rejects malformed components and channels', () => {
  for (const input of ['', ' Docs', 'Docs', '../docs', 'a'.repeat(33), 'docs\nother=x', 'docs\n', 'docs\r', '$(exit 99)']) {
    assert.throws(() => releaseKey(input, 'preview'), /component/);
  }
  for (const channel of ['', 'nightly', 'stable\r']) {
    assert.throws(() => releaseKey('docs', channel), /channel/);
  }
});

function run(inputs = {}, { output = true, unwritable = false } = {}) {
  const path = join(scratch, 'runner output.txt');
  writeFileSync(path, 'existing=value\n');
  const env = { ...process.env };
  for (const key of ['INPUT_COMPONENT', 'INPUT_CHANNEL', 'GITHUB_OUTPUT']) delete env[key];
  Object.assign(env, inputs);
  if (output) env.GITHUB_OUTPUT = unwritable ? scratch : path;
  const result = spawnSync(process.execPath, [join(__dirname, 'action/dist/index.cjs')], {
    env, encoding: 'utf8', timeout: 10000,
  });
  return { ...result, records: readFileSync(path, 'utf8') };
}
test('real distribution accepts direct-process defaults and appends output', () => {
  const result = run();
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.records, 'existing=value\nrelease-key=docs-preview\n');
  assert.match(result.stdout, /Computed release key: docs-preview/);
});
test('real distribution transports explicit inputs', () => {
  const result = run({ INPUT_COMPONENT: 'web-2', INPUT_CHANNEL: 'stable' });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.records, 'existing=value\nrelease-key=web-2-stable\n');
});
test('invalid data cannot publish success or injected records', () => {
  for (const inputs of [{ INPUT_COMPONENT: '' }, { INPUT_COMPONENT: 'docs\nother=x' },
    { INPUT_COMPONENT: 'docs\n' }, { INPUT_COMPONENT: 'docs\r' },
    { INPUT_CHANNEL: 'nightly' }, { INPUT_COMPONENT: '$(exit 99)' }]) {
    const result = run(inputs);
    assert.equal(result.status, 1);
    assert.equal(result.records, 'existing=value\n');
    assert.equal(result.stdout, '');
    assert.match(result.stderr, /component|channel/);
  }
});
test('missing output path is an execution failure', () => {
  const result = run({}, { output: false });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /GITHUB_OUTPUT/);
  assert.equal(result.records, 'existing=value\n');
});
test('unwritable output destination fails without a success log', () => {
  const result = run({}, { unwritable: true });
  assert.equal(result.status, 1);
  assert.equal(result.stdout, '');
  assert.equal(result.records, 'existing=value\n');
});
