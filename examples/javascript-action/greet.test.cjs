'use strict';

const assert = require('node:assert/strict');
const { test } = require('node:test');
const { greet } = require('./greet.cjs');

test('greets a trimmed name', () => {
  assert.equal(greet('  Ada  '), 'Hello, Ada!');
});

test('preserves Unicode and shell-like text as data', () => {
  assert.equal(greet('रोहित'), 'Hello, रोहित!');
  assert.equal(greet('$(exit 99)'), 'Hello, $(exit 99)!');
});

test('rejects empty, multiline, and non-string inputs', () => {
  for (const name of ['', '  ', 'Ada\noutput=injected', 'Ada\rname', null, 42]) {
    assert.throws(() => greet(name), /nonempty, single-line/);
  }
});
