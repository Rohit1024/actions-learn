'use strict';

const assert = require('node:assert/strict');
const { mkdtempSync, cpSync, rmSync, mkdirSync, renameSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');
const { spawnSync } = require('node:child_process');

const scratch = mkdtempSync(join(tmpdir(), 'broken release '));
try {
  for (const kind of ['source-only', 'nested-metadata']) {
    const candidate = join(scratch, kind);
    cpSync(join(__dirname, 'package'), candidate, { recursive: true });
    if (kind === 'source-only') rmSync(join(candidate, 'dist'), { recursive: true });
    else {
      mkdirSync(join(candidate, 'nested'));
      renameSync(join(candidate, 'action.yml'), join(candidate, 'nested/action.yml'));
    }
    const result = spawnSync(process.execPath, [join(__dirname, 'check-package.cjs'), candidate], { encoding: 'utf8' });
    assert.equal(result.status, 1);
    assert.match(result.stderr, kind === 'source-only' ? /missing runtime file/ : /missing root action.yml/);
    console.log(`${kind}: ${result.stderr.trim()}`);
  }
  console.log('PASS: both incomplete release snapshots were rejected; original candidate preserved');
} finally {
  rmSync(scratch, { recursive: true, force: true });
}
