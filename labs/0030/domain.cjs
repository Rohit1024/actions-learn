function packageText(candidate) {
  if (!/^preview-[0-9]{1,4}$/u.test(candidate)) throw new Error('candidate must match preview-N (1 through 4 digits)');
  return `candidate=${candidate}\n`;
}
module.exports = { packageText };
