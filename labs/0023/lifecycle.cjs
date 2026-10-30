'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

// Deliberately narrow runner simulation: one action, one single-line state key.
// It does not implement pre/post scheduling, expression evaluation or cancellation.
function lifecycle(scenario = 'success') {
  if (!['success', 'main-failure', 'partial-setup', 'missing-state', 'lost-state', 'cleanup-failure'].includes(scenario)) {
    throw new Error('unknown lifecycle scenario');
  }
  const root = fs.mkdtempSync(path.join(__dirname, '.lifecycle-'));
  const state = path.join(root, 'state.txt');
  const output = path.join(root, 'output.txt');
  fs.writeFileSync(state, '');
  fs.writeFileSync(output, '');
  const env = { ...process.env };
  for (const key of Object.keys(env)) if (/^(INPUT_|STATE_|GITHUB_|LAB_)/u.test(key)) delete env[key];
  Object.assign(env, { RUNNER_TEMP: root, GITHUB_STATE: state, GITHUB_OUTPUT: output,
    LAB_FAIL_MAIN: scenario === 'main-failure' ? '1' : '0',
    LAB_FAIL_SETUP: scenario === 'partial-setup' ? '1' : '0',
    LAB_FAIL_CLEANUP: scenario === 'cleanup-failure' ? '1' : '0' });
  function execute(file, childEnv) {
    const result = spawnSync(process.execPath, [path.join(__dirname, file)], {
      env: childEnv, encoding: 'utf8', timeout: 10000,
    });
    if (result.error) throw result.error;
    return { status: result.status, stdout: result.stdout.trim(), stderr: result.stderr.trim() };
  }
  try {
    const main = scenario === 'missing-state' ? null : execute('index.cjs', env);
    const saved = fs.readFileSync(state, 'utf8');
    if (saved && (!saved.startsWith('resource=') || saved.trimEnd().includes('\n'))) {
      throw new Error('unexpected lab state format');
    }
    const resource = saved ? saved.slice('resource='.length).trimEnd() : undefined;
    const postEnv = { ...env };
    if (resource && scenario !== 'lost-state') postEnv.STATE_resource = resource;
    const post = execute('cleanup.cjs', postEnv);
    const repeat = post.status === 0 ? execute('cleanup.cjs', postEnv) : null;
    return {
      main, post, repeat,
      output: fs.readFileSync(output, 'utf8'),
      resourceRemaining: Boolean(resource && fs.existsSync(resource)),
      combinedStatus: (main?.status ?? 0) !== 0 || post.status !== 0 ? 1 : 0,
    };
  } finally {
    // Harness teardown prevents the deliberately lost-state exercise leaving litter.
    fs.rmSync(root, { recursive: true, force: true });
  }
}

module.exports = { lifecycle };
if (require.main === module) console.log(JSON.stringify(lifecycle(process.argv[2]), null, 2));
