'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { workspaceFile, lineCount } = require('./lines.cjs');
const { run } = require('../0019/process.cjs');
const entry = path.join(__dirname, 'index.cjs');
const values = { GITHUB_WORKSPACE: __dirname, INPUT_FILE: 'fixtures/report with spaces-रोहित.txt' };

test('LF, CRLF, lone CR, empty, blank lines and no final newline have defined semantics', () => {
  for (const text of ['a\nb\n', 'a\r\nb\r\n', 'a\rb\r', 'a\nb']) assert.equal(lineCount(text), 2);
  assert.equal(lineCount(''), 0);
  assert.equal(lineCount('\n'), 1);
  assert.equal(lineCount('a\n\n'), 2);
});
test('POSIX path model preserves spaces and rejects escape', () => {
  assert.equal(workspaceFile('/work/repo', 'reports/a b.txt', path.posix), '/work/repo/reports/a b.txt');
  assert.throws(() => workspaceFile('/work/repo', '../other.txt', path.posix), /inside/u);
});
test('Windows path model handles drive paths and rejects other drives and traversal', () => {
  assert.equal(workspaceFile('C:\\work\\repo', 'reports\\a b.txt', path.win32), 'C:\\work\\repo\\reports\\a b.txt');
  assert.throws(() => workspaceFile('C:\\work\\repo', '..\\other.txt', path.win32), /inside/u);
  assert.throws(() => workspaceFile('C:\\work\\repo', 'D:\\other.txt', path.win32), /relative/u);
  assert.throws(() => workspaceFile('C:\\work\\repo', 'D:other.txt', path.win32), /inside/u);
});
test('real host process works with spaces and Unicode from an unrelated cwd', () => {
  const result = run(entry, values);
  assert.deepEqual(result, { status: 0, stdout: 'lines=2\n', stderr: '', output: 'count=2\n' });
});
test('missing file and escaped path fail without a success output', () => {
  for (const file of ['missing.txt', '../outside.txt', '']) {
    const result = run(entry, { ...values, INPUT_FILE: file });
    assert.equal(result.status, 1);
    assert.equal(result.output, '');
  }
});
test('real CRLF fixture is counted identically', () => {
  const dir = fs.mkdtempSync(path.join(__dirname, '.crlf-'));
  try {
    fs.writeFileSync(path.join(dir, 'report.txt'), 'a\r\nb\r\n', 'utf8');
    const result = run(entry, { GITHUB_WORKSPACE: dir, INPUT_FILE: 'report.txt' });
    assert.equal(result.status, 0);
    assert.equal(result.output, 'count=2\n');
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
test('a filesystem link cannot redirect the input outside the workspace', () => {
  const dir = fs.mkdtempSync(path.join(__dirname, '.link-'));
  try {
    const workspace = path.join(dir, 'workspace');
    const outside = path.join(dir, 'outside');
    fs.mkdirSync(workspace);
    fs.mkdirSync(outside);
    fs.writeFileSync(path.join(outside, 'report.txt'), 'private\n', 'utf8');
    fs.symlinkSync(outside, path.join(workspace, 'linked'), 'junction');
    const result = run(entry, { GITHUB_WORKSPACE: workspace, INPUT_FILE: 'linked/report.txt' });
    assert.equal(result.status, 1);
    assert.match(result.stderr, /inside workspace/u);
    assert.equal(result.output, '');
    assert.equal(fs.readFileSync(path.join(outside, 'report.txt'), 'utf8'), 'private\n');
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
test('hidden wc dependency fails when executable is unavailable; Node repair still works', () => {
  const env = { ...values, PATH: path.join(__dirname, 'fixtures') };
  const broken = run(path.join(__dirname, 'broken.cjs'), env);
  assert.equal(broken.status, 1);
  assert.match(broken.stderr, /ENOENT/u);
  assert.equal(run(entry, env).output, 'count=2\n');
});
