const fs = require('node:fs');
const path = require('node:path');
const { packageText } = require('./domain.cjs');
function requireEvidence({ candidate, buildResult, testResult, directory }) {
  packageText(candidate);
  for (const [kind, result] of [['build', buildResult], ['test', testResult]]) {
    if (result !== 'success') throw new Error(`${kind} result must be success (got ${result || 'missing'})`);
    const folder = path.join(directory, kind);
    const names = fs.readdirSync(folder);
    if (names.length !== 1 || names[0] !== `${kind}.json`) throw new Error(`${kind} evidence must contain exactly ${kind}.json`);
    const bytes = fs.readFileSync(path.join(folder, names[0]), 'utf8');
    if (bytes.length > 1024) throw new Error(`${kind} evidence exceeds bound`);
    const record = JSON.parse(bytes);
    if (Object.keys(record).sort().join(',') !== 'candidate,kind,passed,schema' || record.schema !== 1 || record.kind !== kind || record.candidate !== candidate || record.passed !== true) throw new Error(`${kind} evidence does not match required candidate/schema/pass`);
  }
  return true;
}
if (require.main === module) {
  try {
    requireEvidence({ candidate: process.env.CANDIDATE, buildResult: process.env.BUILD_RESULT, testResult: process.env.TEST_RESULT, directory: process.env.EVIDENCE_DIR });
    if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
    fs.appendFileSync(process.env.GITHUB_OUTPUT, 'ready=true\n');
    console.log('READY: build + test evidence match preview candidate');
  } catch (error) { console.error(`BLOCKED: ${error.message}`); process.exitCode = 1; }
}
module.exports = { requireEvidence };
