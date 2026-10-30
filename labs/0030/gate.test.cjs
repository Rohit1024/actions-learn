const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { requireEvidence } = require('./gate.cjs');
function fixture(run) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'module5 gate '));
  const context = { candidate: 'preview-1', buildResult: 'success', testResult: 'success', directory };
  for (const kind of ['build', 'test']) {
    fs.mkdirSync(path.join(directory, kind));
    fs.writeFileSync(path.join(directory, kind, `${kind}.json`), JSON.stringify({ schema: 1, candidate: 'preview-1', kind, passed: true }));
  }
  try { run(context); } finally { fs.rmSync(directory, { recursive: true, force: true }); }
}
test('all required evidence joins', () => fixture(context => assert.equal(requireEvidence(context), true)));
test('failed skipped cancelled or missing result blocks', () => fixture(context => {
  for (const result of ['failure', 'skipped', 'cancelled', '']) assert.throws(() => requireEvidence({ ...context, testResult: result }), /result must be success/u);
}));
test('missing evidence file blocks despite successful result', () => fixture(context => {
  fs.unlinkSync(path.join(context.directory, 'test/test.json'));
  assert.throws(() => requireEvidence(context), /exactly test.json/u);
}));
test('stale candidate blocks', () => fixture(context => assert.throws(() => requireEvidence({ ...context, candidate: 'preview-2' }), /does not match/u)));
test('false or wrong-kind evidence blocks', () => fixture(context => {
  for (const change of [{ passed: false }, { passed: 'true' }, { kind: 'build' }, { schema: 2 }]) {
    fs.writeFileSync(path.join(context.directory, 'test/test.json'), JSON.stringify({ schema: 1, candidate: 'preview-1', kind: 'test', passed: true, ...change }));
    assert.throws(() => requireEvidence(context), /does not match/u);
  }
}));
test('extra evidence file blocks', () => fixture(context => {
  fs.writeFileSync(path.join(context.directory, 'test/duplicate.json'), '{}');
  assert.throws(() => requireEvidence(context), /exactly test.json/u);
}));
test('malformed JSON blocks', () => fixture(context => {
  fs.writeFileSync(path.join(context.directory, 'test/test.json'), '{bad');
  assert.throws(() => requireEvidence(context), SyntaxError);
}));
