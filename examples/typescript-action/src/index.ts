import { appendFileSync } from 'node:fs';

export function greet(name: string): string {
  if (/[\r\n]/u.test(name) || !name.trim()) {
    throw new Error('name must be a nonempty, single-line string');
  }
  return `Hello, ${name.trim()}!`;
}

try {
  const greeting = greet(process.env.INPUT_NAME ?? 'World');
  const outputPath = process.env.GITHUB_OUTPUT;
  if (!outputPath) {
    throw new Error('GITHUB_OUTPUT must be set');
  }
  appendFileSync(outputPath, `greeting=${greeting}\n`, 'utf8');
  console.log(greeting);
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
