const fs = require('node:fs');
const path = require('node:path');
const { packageText } = require('./domain.cjs');
try {
  const kind = process.env.KIND;
  const candidate = process.env.CANDIDATE;
  if (!['build', 'test'].includes(kind)) throw new Error('kind must be build or test');
  packageText(candidate);
  if (process.env.FAIL_KIND === kind) throw new Error(`deliberate ${kind} failure before evidence`);
  if (!process.env.EVIDENCE_DIR || !process.env.GITHUB_OUTPUT) throw new Error('EVIDENCE_DIR and GITHUB_OUTPUT must be set');
  fs.mkdirSync(process.env.EVIDENCE_DIR, { recursive: true });
  fs.writeFileSync(path.join(process.env.EVIDENCE_DIR, `${kind}.json`), JSON.stringify({ schema: 1, candidate, kind, passed: true }) + '\n');
  fs.appendFileSync(process.env.GITHUB_OUTPUT, `artifact=evidence-${kind}\n`);
  console.log(`evidence ready: ${kind}`);
} catch (error) { console.error(error.message); process.exitCode = 1; }
