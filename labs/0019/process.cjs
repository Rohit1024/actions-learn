'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

// Reused by later Module 5 labs. This supplies files; it does not parse runner commands.
function run(entry, values = {}, options = {}) {
  const dir = fs.mkdtempSync(path.join(__dirname, '.process-'));
  const output = path.join(dir, 'output.txt');
  fs.writeFileSync(output, options.prior ?? '', 'utf8');
  const env = { ...process.env };
  for (const key of Object.keys(env)) {
    if (/^(INPUT_|STATE_|GITHUB_|LAB_)/u.test(key)) delete env[key];
  }
  Object.assign(env, { GITHUB_OUTPUT: output }, values);
  for (const [key, value] of Object.entries(env)) if (value === undefined) delete env[key];
  try {
    const child = spawnSync(process.execPath, [entry], {
      env, cwd: options.cwd ?? dir, encoding: 'utf8', timeout: 10000,
    });
    if (child.error) throw child.error;
    return { status: child.status, stdout: child.stdout, stderr: child.stderr,
      output: fs.readFileSync(output, 'utf8') };
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

module.exports = { run };
