'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { greet } = require('./greet.cjs');

test('trims a recipient without changing Unicode or literal shell-like text', () => {
  assert.equal(greet('  Ada  '), 'Hello, Ada!');
  assert.equal(greet('रोहित'), 'Hello, रोहित!');
  assert.equal(greet('$(exit 99)'), 'Hello, $(exit 99)!');
});

test('rejects nonstrings, empty names, and output-record injection', () => {
  for (const name of [undefined, 42, '', '   ', 'Ada\nother=injected', 'Ada\rother=injected']) {
    assert.throws(() => greet(name), /nonempty, single-line/u);
  }
});
