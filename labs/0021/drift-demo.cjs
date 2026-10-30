'use strict';
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const { run } = require('../0019/process.cjs');
const dir = fs.mkdtempSync(path.join(__dirname, '.drift-'));
function command(script, args = []) {
  const child = spawnSync(process.execPath, [script, ...args], { encoding: 'utf8' });
  if (child.error) throw child.error;
  return child;
}
try {
  for (const item of ['src', 'dist', 'bundle.cjs', 'build.cjs', 'check-dist.cjs', 'tsconfig.json']) {
    fs.cpSync(path.join(__dirname, item), path.join(dir, item), { recursive: true });
  }
  const source = path.join(dir, 'src/index.ts');
  const before = fs.readFileSync(source, 'utf8');
  assert.ok(before.includes('Hello,'), 'expected greeting mutation target');
  fs.writeFileSync(source, before.replace('Hello,', 'Welcome,'));
  const compiler = path.resolve(__dirname, '../../node_modules/typescript/bin/tsc');
  const compiled = command(compiler, ['--project', path.join(dir, 'tsconfig.json')]);
  assert.equal(compiled.status, 0, compiled.stdout + compiled.stderr);
  console.log('typecheck exit=0');
  const destination = path.join(dir, 'dist/index.cjs');
  const originalDist = fs.readFileSync(destination);
  assert.equal(command(path.join(dir, 'check-dist.cjs')).status, 1);
  assert.ok(fs.readFileSync(destination).equals(originalDist), 'check must not repair dist');
  console.log('drift check exit=1; dist unchanged');
  assert.equal(run(destination, { INPUT_NAME: 'Ada' }).output, 'greeting=Hello, Ada!\n');
  console.log('consumer before build: Hello, Ada!');
  assert.equal(command(path.join(dir, 'build.cjs')).status, 0);
  assert.equal(command(path.join(dir, 'check-dist.cjs')).status, 0);
  assert.equal(run(destination, { INPUT_NAME: 'Ada' }).output, 'greeting=Welcome, Ada!\n');
  console.log('intentional build + drift check exit=0');
  console.log('consumer after build: Welcome, Ada!');
} finally {
  fs.rmSync(dir, { recursive: true, force: true });
}
