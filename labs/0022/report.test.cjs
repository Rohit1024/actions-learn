'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const { fakeClient } = require('./fake-client.cjs');
const { issueReport, INITIAL_URL } = require('./report.cjs');
const { run } = require('../0019/process.cjs');

test('all pages are followed and pull requests excluded from issue report', async () => {
  const client = fakeClient('pages');
  assert.deepEqual(await issueReport(client), { count: 2, titles: ['Fix runner', 'Document\noutputs'] });
  assert.equal(client.calls.length, 2);
  assert.deepEqual(client.calls[0], { method: 'GET', url: INITIAL_URL });
  assert.match(client.calls[1].url, /page=2$/u);
});
test('empty 200 is valid and differs from denied access', async () => {
  assert.deepEqual(await issueReport(fakeClient('empty')), { count: 0, titles: [] });
  const client = fakeClient('denied');
  await assert.rejects(issueReport(client), /API status 403/u);
  assert.equal(client.calls.length, 1);
  assert.deepEqual(client.waits, []);
});
test('rate limits fail without violating upstream waiting instructions', async () => {
  for (const scenario of ['rate', 'primary-rate']) {
    const client = fakeClient(scenario);
    await assert.rejects(issueReport(client), /rate limited/u);
    assert.equal(client.calls.length, 1);
    assert.deepEqual(client.waits, []);
  }
});
test('503 GET retries once using injected time and request contract', async () => {
  const client = fakeClient('transient');
  assert.deepEqual(await issueReport(client), { count: 1, titles: ['Recovered'] });
  assert.equal(client.calls.length, 2);
  assert.deepEqual(client.calls[0], client.calls[1]);
  assert.deepEqual(client.waits, [250]);
});
test('unavailable service, malformed shape and cycles reject', async () => {
  for (const [scenario, message] of [['unavailable', /503/u], ['malformed', /shape/u], ['cycle', /cycle/u]]) {
    await assert.rejects(issueReport(fakeClient(scenario)), message);
  }
});
test('page and retry time budgets are enforced', async () => {
  await assert.rejects(issueReport({ ...fakeClient('pages'), maxPages: 1 }), /page budget/u);
  const client = fakeClient('transient');
  await assert.rejects(issueReport({ ...client, budgetMs: 100 }), /deadline/u);
  assert.deepEqual(client.waits, []);
});
test('process serializes multiline titles safely in one JSON output record', () => {
  const result = run(path.join(__dirname, 'index.cjs'));
  assert.equal(result.status, 0);
  assert.equal(result.stdout, 'count=2; requests=2; waits=[]\n');
  assert.equal(result.output, 'report={"count":2,"titles":["Fix runner","Document\\noutputs"]}\n');
  assert.equal(result.output.split('\n').length, 2);
});
test('all failed processes, including page-two failure, publish no report', () => {
  for (const scenario of ['denied', 'rate', 'primary-rate', 'unavailable', 'partial', 'malformed', 'cycle', 'unknown']) {
    const result = run(path.join(__dirname, 'index.cjs'), { INPUT_SCENARIO: scenario });
    assert.equal(result.status, 1, scenario);
    assert.notEqual(result.stderr, '', scenario);
    assert.equal(result.stdout, '', scenario);
    assert.equal(result.output, '', scenario);
  }
});
test('broken denial handler fabricates success that the real process rejects', () => {
  const result = run(path.join(__dirname, 'broken.cjs'), { INPUT_SCENARIO: 'denied' });
  assert.equal(result.status, 0);
  assert.equal(result.output, 'report={"count":0,"titles":[]}\n');
});
test('success appends and missing output path fails without publishing a report', () => {
  const result = run(path.join(__dirname, 'index.cjs'), { INPUT_SCENARIO: 'empty' }, { prior: 'prior=kept\n' });
  assert.equal(result.status, 0);
  assert.equal(result.output, 'prior=kept\nreport={"count":0,"titles":[]}\n');
  const missing = run(path.join(__dirname, 'index.cjs'), { GITHUB_OUTPUT: undefined });
  assert.equal(missing.status, 1);
  assert.match(missing.stderr, /GITHUB_OUTPUT must be set/u);
  assert.equal(missing.output, '');
});
