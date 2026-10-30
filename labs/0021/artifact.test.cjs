'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const { run } = require('../0019/process.cjs');
const entry = path.join(__dirname, 'dist/index.cjs');

test('execute distributed CJS from another working directory', () => {
  const result = run(entry, { INPUT_NAME: 'Ada' });
  assert.equal(result.status, 0);
  assert.equal(result.output, 'greeting=Hello, Ada!\n');
  assert.equal(result.stderr, '');
});
test('artifact default and Unicode contract', () => {
  assert.equal(run(entry).output, 'greeting=Hello, World!\n');
  assert.equal(run(entry, { INPUT_NAME: '  रोहित  ' }).output, 'greeting=Hello, रोहित!\n');
});
test('artifact rejects invalid input without output', () => {
  const result = run(entry, { INPUT_NAME: 'Ada\nother=injected' });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /single-line/u);
  assert.equal(result.output, '');
});
test('artifact requires the runner output path', () => {
  const result = run(entry, { INPUT_NAME: 'Ada', GITHUB_OUTPUT: undefined });
  assert.equal(result.status, 1);
  assert.equal(result.output, '');
});
