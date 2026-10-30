'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { lifecycle } = require('./lifecycle.cjs');
const { setup, cleanup } = require('./resource.cjs');

test('successful main and post cross separate process/state boundaries', () => {
  const result = lifecycle();
  assert.equal(result.main.status, 0);
  assert.equal(result.post.status, 0);
  assert.equal(result.output, 'resource=ready\n');
  assert.equal(result.resourceRemaining, false);
  assert.equal(result.repeat.stdout, 'cleanup already complete');
  assert.equal(result.combinedStatus, 0);
});
for (const scenario of ['main-failure', 'partial-setup']) {
  test(`${scenario} still cleans persisted state without erasing original failure`, () => {
    const result = lifecycle(scenario);
    assert.equal(result.main.status, 1);
    assert.equal(result.post.status, 0);
    assert.equal(result.resourceRemaining, false);
    assert.equal(result.output, '');
    assert.equal(result.combinedStatus, 1);
  });
}
test('missing state is a safe no-op', () => {
  const result = lifecycle('missing-state');
  assert.equal(result.post.status, 0);
  assert.equal(result.post.stdout, 'cleanup skipped: no resource state');
});
test('deliberate failure to forward state leaves the resource for harness teardown', () => {
  const result = lifecycle('lost-state');
  assert.equal(result.post.status, 0);
  assert.equal(result.resourceRemaining, true);
});
test('cleanup failure is visible even after successful primary work', () => {
  const result = lifecycle('cleanup-failure');
  assert.equal(result.main.status, 0);
  assert.equal(result.post.status, 1);
  assert.equal(result.combinedStatus, 1);
  assert.equal(result.resourceRemaining, true);
});
test('state-write failure rolls back newly allocated directory', () => {
  const root = fs.mkdtempSync(path.join(__dirname, '.rollback-'));
  try {
    assert.throws(() => setup({ RUNNER_TEMP: root, GITHUB_STATE: path.join(root, 'absent/state') }), /ENOENT/u);
    assert.deepEqual(fs.readdirSync(root), []);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
test('cleanup refuses an unowned directory, an outside path, and a symlink', () => {
  const root = fs.mkdtempSync(path.join(__dirname, '.ownership-'));
  try {
    const unowned = path.join(root, 'actions-learn-unowned');
    fs.mkdirSync(unowned);
    fs.writeFileSync(path.join(unowned, '.owner'), 'someone else');
    assert.throws(() => cleanup({ RUNNER_TEMP: root, STATE_resource: unowned }), /ownership marker/u);
    assert.throws(() => cleanup({ RUNNER_TEMP: root, STATE_resource: path.dirname(root) }), /outside/u);
    // Directory junctions avoid Windows symlink privilege requirements.
    const link = path.join(root, 'actions-learn-link');
    fs.symlinkSync(unowned, link, 'junction');
    assert.throws(() => cleanup({ RUNNER_TEMP: root, STATE_resource: link }), /ownership marker/u);
    assert.ok(fs.existsSync(unowned));
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
