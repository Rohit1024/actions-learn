const fs = require('node:fs');
try {
  const label = process.argv[2] ?? '';
  if (process.argv.length !== 3 || !label.trim() || label.length > 160) {
    throw new Error('label must be nonblank and at most 160 UTF-16 code units');
  }
  if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
  fs.appendFileSync(process.env.GITHUB_OUTPUT, `label-json=${JSON.stringify(label)}\n`);
  console.log('label accepted');
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
