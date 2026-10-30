const fs = require('node:fs');
const path = require('node:path');
const { packageText } = require('./domain.cjs');
try {
  const text = packageText(process.env.CANDIDATE ?? '');
  if (!process.env.WORK_DIR) throw new Error('WORK_DIR must be set');
  fs.mkdirSync(process.env.WORK_DIR, { recursive: true });
  fs.writeFileSync(path.join(process.env.WORK_DIR, 'bundle.txt'), text);
  console.log('built synthetic bundle.txt');
} catch (error) { console.error(error.message); process.exitCode = 1; }
