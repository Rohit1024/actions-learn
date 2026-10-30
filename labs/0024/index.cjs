'use strict';
const fs = require('node:fs');
const { workspaceFile, lineCount } = require('./lines.cjs');

try {
  const workspace = process.env.GITHUB_WORKSPACE;
  const candidate = workspaceFile(workspace, process.env.INPUT_FILE ?? '');
  // Recheck containment after resolving filesystem links.
  const root = fs.realpathSync(workspace);
  const actual = fs.realpathSync(candidate);
  workspaceFile(root, require('node:path').relative(root, actual));
  const count = lineCount(fs.readFileSync(actual, 'utf8'));
  if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT must be set');
  fs.appendFileSync(process.env.GITHUB_OUTPUT, `count=${count}\n`, 'utf8');
  console.log(`lines=${count}`);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
