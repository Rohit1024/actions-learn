'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { mkdtempSync, writeFileSync, readFileSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');
const { spawnSync } = require('node:child_process');
const cases = require('./cases.json');
const adapter = process.env.LAB_ADAPTER === 'broken' ? 'broken.cjs' : 'index.cjs';

function run(name, { existing = '', outputAvailable = true, unwritable = false } = {}) {
  const directory = mkdtempSync(join(tmpdir(), 'module2 output with spaces '));
  const output = join(directory, 'output with spaces.txt');
  const env = { ...process.env };
  delete env.INPUT_NAME;
  delete env.GITHUB_OUTPUT;
  if (name !== null) env.INPUT_NAME = name;
  writeFileSync(output, existing, 'utf8');
  if (outputAvailable) env.GITHUB_OUTPUT = unwritable ? directory : output;
  try {
    const result = spawnSync(process.execPath, [join(__dirname, adapter)], {
      cwd: directory, env, encoding: 'utf8', timeout: 10_000,
    });
    assert.ifError(result.error);
    return { ...result, output: readFileSync(output, 'utf8') };
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

for (const fixture of cases) {
  test(fixture.label, () => {
    const result = run(fixture.name);
    if (fixture.error) {
      assert.notEqual(result.status, 0, 'invalid input must fail the process');
      assert.ok(result.stderr.includes(fixture.error), result.stderr);
      assert.equal(result.stdout, '');
      assert.equal(result.output, '', 'failure must not publish a success output');
    } else {
      assert.equal(result.status, 0, result.stderr);
      assert.equal(result.stderr, '');
      assert.equal(result.stdout, `${fixture.greeting}\n`);
      assert.equal(result.output, `greeting=${fixture.greeting}\n`);
    }
  });
}

test('appends without erasing an earlier record', () => {
  const result = run('Ada', { existing: 'existing=value\n' });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.output, 'existing=value\ngreeting=Hello, Ada!\n');
});

test('validation failure leaves prior records unchanged', () => {
  const result = run('Ada\nother=injected', { existing: 'existing=value\n' });
  assert.notEqual(result.status, 0);
  assert.equal(result.stdout, '');
  assert.equal(result.output, 'existing=value\n');
});

test('missing runner output path is an explicit process failure', () => {
  const result = run('Ada', { outputAvailable: false });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /GITHUB_OUTPUT/u);
  assert.equal(result.stdout, '');
  assert.equal(result.output, '');
});

test('output write failure cannot be reported as success', () => {
  const result = run('Ada', { unwritable: true });
  assert.notEqual(result.status, 0);
  assert.notEqual(result.stderr, '');
  assert.equal(result.stdout, '');
  assert.equal(result.output, '');
});
