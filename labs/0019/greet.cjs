'use strict';

// Copied from examples/javascript-action/greet.cjs; shared example is unchanged.
function greet(name) {
  if (typeof name !== 'string' || /[\r\n]/u.test(name) || !name.trim()) {
    throw new Error('name must be a nonempty, single-line string');
  }
  return `Hello, ${name.trim()}!`;
}

module.exports = { greet };
