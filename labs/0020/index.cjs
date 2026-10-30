'use strict';
const { appendFileSync } = require('node:fs');
const { timingReport } = require('./report.cjs');

try {
  const rawBudget = process.env.INPUT_BUDGET ?? '10';
  if (!rawBudget.trim()) throw new Error('budget must not be blank');
  const report = timingReport(JSON.parse(process.env.INPUT_DURATIONS ?? '[]'), Number(rawBudget));
  if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
  appendFileSync(process.env.GITHUB_OUTPUT, `report=${JSON.stringify(report)}\n`, 'utf8');
  console.log(JSON.stringify(report));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
