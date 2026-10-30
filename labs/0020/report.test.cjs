'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { timingReport } = require('./report.cjs');

test('valid and exact-budget reports use the public result contract', () => {
  assert.deepEqual(timingReport([2, 3], 5), { count: 2, totalSeconds: 5, withinBudget: true });
});
test('empty and zero boundary', () => {
  assert.deepEqual(timingReport([], 0), { count: 0, totalSeconds: 0, withinBudget: true });
  assert.equal(timingReport([0.5], 0).withinBudget, false);
});
test('rejects malformed durations and budget', () => {
  for (const values of [null, '[]', [-1], [NaN], [Infinity], ['3']]) {
    assert.throws(() => timingReport(values, 5), /durations/u);
  }
  for (const budget of [-1, NaN, Infinity, '5']) assert.throws(() => timingReport([], budget), /budget/u);
  assert.throws(() => timingReport([Number.MAX_VALUE, Number.MAX_VALUE], 10), /overflow/u);
});
test('no mutation and repeatable with identical explicit arguments', () => {
  const values = Object.freeze([2, 3]);
  assert.deepEqual(timingReport(values, 5), timingReport(values, 5));
  assert.deepEqual(values, [2, 3]);
});
