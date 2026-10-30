'use strict';
// Demonstrate a real boundary mutant without modifying the maintained source.
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const dir = fs.mkdtempSync(path.join(__dirname, '.mutant-'));
try {
  const source = fs.readFileSync(path.join(__dirname, 'report.cjs'), 'utf8');
  if (!source.includes('totalSeconds <= budget')) throw new Error('mutation target no longer matches');
  fs.writeFileSync(path.join(dir, 'report.cjs'), source.replace('totalSeconds <= budget', 'totalSeconds < budget'));
  fs.copyFileSync(path.join(__dirname, 'report.test.cjs'), path.join(dir, 'report.test.cjs'));
  const child = spawnSync(process.execPath, ['--test', path.join(dir, 'report.test.cjs')], { encoding: 'utf8' });
  if (child.error) throw child.error;
  if (child.status !== 1 || !child.stdout.includes('valid and exact-budget')) {
    process.stdout.write(child.stdout);
    process.stderr.write(child.stderr);
    throw new Error('expected the exact-budget regression to reject the mutant');
  }
  console.log('PASS: exact-budget assertion rejected the <= to < mutant (test exit 1).');
} finally {
  fs.rmSync(dir, { recursive: true, force: true });
}
