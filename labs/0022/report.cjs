'use strict';
const INITIAL_URL = 'https://api.github.com/repos/acme/widget/issues?per_page=2';

async function issueReport({ request, sleep, now, budgetMs = 1500, maxPages = 3 }) {
  const deadline = now() + budgetMs;
  const visited = new Set();
  const issues = [];
  let url = INITIAL_URL;
  while (url) {
    if (visited.has(url)) throw new Error('pagination cycle');
    if (visited.size >= maxPages) throw new Error('page budget exceeded');
    // These are fixed fixtures. A real adapter must configure the API base URL for GHES.
    const parsed = new URL(url);
    if (parsed.origin !== 'https://api.github.com' || parsed.pathname !== '/repos/acme/widget/issues') {
      throw new Error('unexpected pagination destination');
    }
    visited.add(url);
    let response;
    for (let attempt = 1; attempt <= 2; attempt += 1) {
      if (now() >= deadline) throw new Error('request deadline exceeded');
      response = await request({ method: 'GET', url });
      if (now() >= deadline) throw new Error('request deadline exceeded');
      const headers = response.headers ?? {};
      if (response.status === 429 || (response.status === 403 &&
        (headers['x-ratelimit-remaining'] === '0' || headers['retry-after']))) {
        throw new Error('rate limited; no retry inside this lab budget');
      }
      if (response.status === 200) break;
      if (response.status !== 503 || attempt === 2) throw new Error(`API status ${response.status}`);
      if (now() + 250 >= deadline) throw new Error('retry would exceed deadline');
      await sleep(250); // Only a GET retry; fake time in this lab, no actual waiting.
    }
    if (!Array.isArray(response.data) || response.data.some(row =>
      !row || !Number.isSafeInteger(row.id) || typeof row.title !== 'string')) {
      throw new Error('invalid API response shape');
    }
    issues.push(...response.data.filter(row => !Object.hasOwn(row, 'pull_request')));
    if (response.nextUrl !== undefined && typeof response.nextUrl !== 'string') {
      throw new Error('invalid next URL');
    }
    url = response.nextUrl;
  }
  return { count: issues.length, titles: issues.map(issue => issue.title) };
}

module.exports = { issueReport, INITIAL_URL };
