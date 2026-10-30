'use strict';
const fs = require('node:fs');
const path = require('node:path');
const MARKER = 'actions-learn-0023\n';

function setup(env) {
  if (!env.RUNNER_TEMP || !env.GITHUB_STATE) throw new Error('RUNNER_TEMP and GITHUB_STATE must be set');
  const root = fs.realpathSync(env.RUNNER_TEMP);
  const directory = fs.mkdtempSync(path.join(root, 'actions-learn-'));
  try {
    fs.writeFileSync(path.join(directory, '.owner'), MARKER, 'utf8');
    if (/[\r\n]/u.test(directory)) throw new Error('resource path must be single-line');
    fs.appendFileSync(env.GITHUB_STATE, `resource=${directory}\n`, 'utf8');
  } catch (error) {
    // Roll back before returning ownership when state cannot be persisted.
    fs.rmSync(directory, { recursive: true, force: true });
    throw error;
  }
  if (env.LAB_FAIL_SETUP === '1') throw new Error('setup failed after state persisted');
  fs.writeFileSync(path.join(directory, 'payload.txt'), 'disposable\n', 'utf8');
  return directory;
}

function cleanup(env) {
  const directory = env.STATE_resource;
  if (!directory) return 'cleanup skipped: no resource state';
  if (!env.RUNNER_TEMP) throw new Error('RUNNER_TEMP must be set');
  const root = fs.realpathSync(env.RUNNER_TEMP);
  const candidate = path.resolve(directory);
  if (path.dirname(candidate) !== root || !path.basename(candidate).startsWith('actions-learn-')) {
    throw new Error('refusing cleanup outside owned temp directory');
  }
  if (!fs.existsSync(candidate)) return 'cleanup already complete';
  const stat = fs.lstatSync(candidate);
  if (stat.isSymbolicLink() || !stat.isDirectory() ||
      fs.readFileSync(path.join(candidate, '.owner'), 'utf8') !== MARKER) {
    throw new Error('refusing cleanup without ownership marker');
  }
  if (env.LAB_FAIL_CLEANUP === '1') throw new Error('cleanup failed deliberately');
  fs.rmSync(candidate, { recursive: true });
  return 'cleanup removed owned resource';
}

module.exports = { setup, cleanup };
