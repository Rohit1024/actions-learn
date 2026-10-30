'use strict';
// A real module-resolution boundary. The test materializes this synthetic
// dependency in a temporary project; it does not run npm or a setup action.
const fs = require('node:fs');
const path = require('node:path');
try {
  const fixture = require(path.join(process.cwd(), 'node_modules/fixture-dependency/index.cjs'));
  const output = path.resolve(process.argv[2]);
  fs.writeFileSync(output, JSON.stringify({ schema: 1, message: fixture() }) + '\n');
  console.log('BUILT: result.json');
} catch (error) {
  console.error(`BUILD FAILED: ${error.code || error.message}`);
  process.exitCode = 1;
}
