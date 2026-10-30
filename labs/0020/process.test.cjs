'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const { run } = require('../0019/process.cjs');
const entry = path.join(__dirname, 'index.cjs');

test('adapter parses strings and writes the exact public JSON output', () => {
  const result = run(entry, { INPUT_DURATIONS: '[2,3]', INPUT_BUDGET: '5' });
  assert.equal(result.status, 0);
  assert.equal(result.stderr, '');
  assert.equal(result.output, 'report={"count":2,"totalSeconds":5,"withinBudget":true}\n');
});
test('direct-process defaults match documented metadata defaults', () => {
  const result = run(entry);
  assert.equal(result.status, 0);
  assert.equal(result.output, 'report={"count":0,"totalSeconds":0,"withinBudget":true}\n');
});
test('malformed JSON, numeric strings inside JSON, and blank budget fail without output', () => {
  for (const env of [{ INPUT_DURATIONS: '[' }, { INPUT_DURATIONS: '["3"]' },
    { INPUT_BUDGET: ' ' }, { INPUT_BUDGET: 'NaN' }]) {
    const result = run(entry, env);
    assert.equal(result.status, 1);
    assert.notEqual(result.stderr, '');
    assert.equal(result.output, '');
  }
});
test('exceeded budget is a valid report for the caller to gate', () => {
  const result = run(entry, { INPUT_DURATIONS: '[6]', INPUT_BUDGET: '5' });
  assert.equal(result.status, 0);
  assert.match(result.output, /"withinBudget":false/u);
});
