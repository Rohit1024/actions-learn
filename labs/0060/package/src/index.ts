import { appendFileSync } from 'node:fs';
import { releaseKey } from './domain.js';

try {
  const key = releaseKey(
    process.env.INPUT_COMPONENT ?? 'docs',
    process.env.INPUT_CHANNEL ?? 'preview',
  );
  const output = process.env.GITHUB_OUTPUT;
  if (!output) throw new Error('GITHUB_OUTPUT must be set');
  appendFileSync(output, `release-key=${key}\n`, 'utf8');
  console.log(`Computed release key: ${key}`);
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
