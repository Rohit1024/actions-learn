// Extended copy of examples/typescript-action/src/index.ts; the shared example is unchanged.
import { appendFileSync } from 'node:fs';

export function greet(name: string): string {
  if (typeof name !== 'string' || /[\r\n]/u.test(name) || !name.trim()) {
    throw new Error('name must be a nonempty, single-line string');
  }
  return `Hello, ${name.trim()}!`;
}

try {
  const greeting = greet(process.env.INPUT_NAME ?? 'World');
  const output = process.env.GITHUB_OUTPUT;
  if (!output) throw new Error('GITHUB_OUTPUT must be set');
  appendFileSync(output, `greeting=${greeting}\n`, 'utf8');
  console.log(greeting);
} catch (error: unknown) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
