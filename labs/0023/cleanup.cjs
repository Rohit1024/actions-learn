'use strict';
try {
  console.log(require('./resource.cjs').cleanup(process.env));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
