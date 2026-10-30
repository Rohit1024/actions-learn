const { test } = require('node:test');
const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { check } = require('./worker.cjs');
const base = { label: 'preview', strict: true, maxItems: 2, token: 'fixture-only-not-a-credential' };
test('typed domain accepts booleans and bounded rows', () => {
  assert.equal(check(base, [{ passed: true }, { passed: true }]), 'checked:2:strict');
  assert.equal(check({ ...base, strict: false }, [{ passed: false }]), 'checked:1:tolerant');
});
test('types and domain bounds are separate requirements', () => {
  for (const change of [{ label: '' }, { label: 'bad\nlabel' }, { strict: 'false' }, { maxItems: 1.5 }, { maxItems: 0 }, { maxItems: 4 }, { token: '' }]) {
    assert.throws(() => check({ ...base, ...change }, [{ passed: true }]));
  }
  assert.throws(() => check(base, [{ passed: false }]), /strict checks failed/u);
  assert.throws(() => check({ ...base, maxItems: 1 }, [{ passed: true }, { passed: true }]), /exceed bound/u);
});
test('actual adapter returns output without exposing fixture token', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'module5 typed '));
  try {
    const output = path.join(directory, 'output file');
    fs.writeFileSync(output, 'prior=kept\n');
    const env = { ...process.env, LABEL: 'preview', STRICT: 'true', MAX_ITEMS: '2', FIXTURE_TOKEN: base.token, GITHUB_OUTPUT: output };
    const good = spawnSync(process.execPath, [path.join(__dirname, 'worker.cjs')], { env, encoding: 'utf8', timeout: 5000 });
    assert.equal(good.status, 0, good.stderr);
    assert.equal(good.stdout, 'checked:2:strict\n');
    assert.equal(fs.readFileSync(output, 'utf8'), 'prior=kept\nsummary=checked:2:strict\n');
    assert.ok(!good.stdout.includes(base.token));
    for (const change of [{ STRICT: 'yes' }, { FIXTURE_TOKEN: '' }, { MAX_ITEMS: 'two' }]) {
      fs.writeFileSync(output, 'prior=kept\n');
      const bad = spawnSync(process.execPath, [path.join(__dirname, 'worker.cjs')], { env: { ...env, ...change }, encoding: 'utf8', timeout: 5000 });
      assert.equal(bad.status, 1);
      assert.equal(fs.readFileSync(output, 'utf8'), 'prior=kept\n');
      assert.ok(!bad.stderr.includes(base.token));
    }
  } finally { fs.rmSync(directory, { recursive: true, force: true }); }
});
