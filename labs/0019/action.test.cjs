'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const { run } = require('./process.cjs');
const entry = path.join(__dirname, 'index.cjs');

test('real process trims input and appends without overwriting prior output', () => {
  const result = run(entry, { INPUT_NAME: '  Ada  ' }, { prior: 'prior=kept\n' });
  assert.deepEqual(result, { status: 0, stdout: 'Hello, Ada!\n', stderr: '',
    output: 'prior=kept\ngreeting=Hello, Ada!\n' });
});
for (const [label, name] of [['missing', undefined], ['blank', '  '],
  ['multiline', 'Ada\nother=injected'], ['carriage return', 'Ada\rname']]) {
  test(`${label} input fails before output`, () => {
    const result = run(entry, { INPUT_NAME: name });
    assert.equal(result.status, 1);
    assert.match(result.stderr, /nonempty, single-line/u);
    assert.equal(result.stdout, '');
    assert.equal(result.output, '');
  });
}
test('Unicode and shell-like text remain literal data', () => {
  const result = run(entry, { INPUT_NAME: 'रोहित $(exit 99)' });
  assert.equal(result.status, 0);
  assert.equal(result.output, 'greeting=Hello, रोहित $(exit 99)!\n');
});
test('missing runner output path fails truthfully', () => {
  const result = run(entry, { INPUT_NAME: 'Ada', GITHUB_OUTPUT: undefined });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /GITHUB_OUTPUT must be set/u);
  assert.equal(result.output, '');
});
test('deliberate broken adapter exposes missing validation', () => {
  const result = run(path.join(__dirname, 'broken.cjs'));
  assert.equal(result.status, 0);
  assert.equal(result.output, 'greeting=Hello, !\n');
});
