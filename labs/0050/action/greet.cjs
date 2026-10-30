'use strict';

function greet(name) {
  if (typeof name !== 'string' || /[\r\n]/u.test(name) || !name.trim()) {
    throw new Error('name must be a nonempty, single-line string');
  }
  return `Hello, ${name.trim()}!`;
}

module.exports = { greet };
