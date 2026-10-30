'use strict';

const { mkdtempSync, writeFileSync, readFileSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');
const { spawnSync } = require('node:child_process');

const broken = process.argv.includes('--broken');
const directory = mkdtempSync(join(tmpdir(), 'metadata contract '));
try {
  const output = join(directory, 'runner output.txt');
  const invalidAdapter = join(directory, 'missing-validation.cjs');
  writeFileSync(invalidAdapter,
    "require('node:fs').appendFileSync(process.env.GITHUB_OUTPUT, `greeting=Hello, ${process.env.INPUT_NAME}!\\n`);\n");
  const cases = [
    ['runner-supplied default', 'World', 0, 'greeting=Hello, World!\n'],
    ['explicit recipient', 'Ada', 0, 'greeting=Hello, Ada!\n'],
    ['explicit empty process input', '', 1, ''],
    ['whitespace process input', '   ', 1, ''],
    ['output-record injection', 'Ada\nother=injected', 1, ''],
  ];
  for (const [label, name, status, expected] of cases) {
    writeFileSync(output, 'existing=value\n');
    const result = spawnSync(process.execPath,
      [broken ? invalidAdapter : join(__dirname, 'action/index.cjs')], {
        env: { ...process.env, INPUT_NAME: name, GITHUB_OUTPUT: output },
        encoding: 'utf8', timeout: 10000,
      });
    const actual = readFileSync(output, 'utf8');
    if (result.status !== status || actual !== `existing=value\n${expected}`) {
      console.error(`FAIL: ${label}; exit=${result.status}; output=${JSON.stringify(actual)}`);
      process.exitCode = 1;
      break;
    }
    console.log(`PASS: ${label}; exit=${result.status}`);
  }
} finally {
  rmSync(directory, { recursive: true, force: true });
}
