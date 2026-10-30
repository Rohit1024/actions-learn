const fs = require('node:fs');
const path = require('node:path');
function check({ label, strict, maxItems, token }, rows) {
  if (typeof label !== 'string' || !label.trim() || /[\r\n]/u.test(label) || label.length > 80) throw new Error('label must be a nonblank single line of at most 80 UTF-16 code units');
  if (typeof strict !== 'boolean') throw new Error('strict must be boolean');
  if (!Number.isInteger(maxItems) || maxItems < 1 || maxItems > 3) throw new Error('max-items must be an integer from 1 through 3');
  if (token !== 'fixture-only-not-a-credential') throw new Error('fixture token missing or invalid');
  if (!Array.isArray(rows) || rows.length > maxItems || rows.some(row => typeof row.passed !== 'boolean')) throw new Error('fixture rows exceed bound or have invalid passed fields');
  if (strict && rows.some(row => !row.passed)) throw new Error('strict checks failed');
  return `checked:${rows.length}:${strict ? 'strict' : 'tolerant'}`;
}
if (require.main === module) {
  try {
    if (!['true', 'false'].includes(process.env.STRICT)) throw new Error('STRICT must be true or false text');
    const result = check({ label: process.env.LABEL, strict: process.env.STRICT === 'true', maxItems: Number(process.env.MAX_ITEMS), token: process.env.FIXTURE_TOKEN }, JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures/checks.json'), 'utf8')));
    if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `summary=${result}\n`);
    console.log(result);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
module.exports = { check };
