const { test } = require('node:test');
const assert = require('node:assert/strict');
const { packageText } = require('./domain.cjs');
test('synthetic package format is deterministic', () => {
  assert.equal(packageText('preview-1'), 'candidate=preview-1\n');
});
test('invalid candidate fails before packaging', () => {
  for (const value of ['', 'main', 'preview-1\nready=true', 'preview-10000']) assert.throws(() => packageText(value));
});
