const fs = require('node:fs');
try {
  if (process.argv.length !== 3) throw new Error('expected exactly one file argument');
  if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
  const file = process.argv[2];
  const text = fs.readFileSync(file, 'utf8').replace(/\r\n?/gu, '\n');
  const count = text === '' ? 0 : text.replace(/\n$/u, '').split('\n').length;
  fs.appendFileSync(process.env.GITHUB_OUTPUT, `lines=${count}\n`);
  console.log(JSON.stringify({ argument: file, lines: count }));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
