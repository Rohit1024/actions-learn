import { appendFileSync } from 'node:fs';

export function greet(name: string): string {
  if (!name.trim() || /[\r\n]/u.test(name)) throw new Error('name must be a nonempty single line');
  return `Hello, ${name.trim()}!`;
}

if (require.main === module) {
  try {
    const greeting = greet(process.env.INPUT_NAME ?? 'World');
    if (!process.env.GITHUB_OUTPUT) throw new Error('GITHUB_OUTPUT is required');
    appendFileSync(process.env.GITHUB_OUTPUT, `greeting=${greeting}\n`);
    console.log(greeting);
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
