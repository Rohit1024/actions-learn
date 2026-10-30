'use strict';
const path = require('node:path');

function workspaceFile(workspace, input, pathApi = path) {
  if (typeof workspace !== 'string' || !pathApi.isAbsolute(workspace)) throw new Error('workspace must be absolute');
  if (typeof input !== 'string' || !input.trim() || /[\r\n]/u.test(input) || pathApi.isAbsolute(input)) {
    throw new Error('file must be a nonempty relative single-line path');
  }
  const candidate = pathApi.resolve(workspace, input);
  const relative = pathApi.relative(workspace, candidate);
  if (relative === '..' || relative.startsWith(`..${pathApi.sep}`) || pathApi.isAbsolute(relative)) {
    throw new Error('file must stay inside workspace');
  }
  return candidate;
}

function lineCount(text) {
  if (typeof text !== 'string') throw new Error('text must be a string');
  if (!text) return 0;
  const normalized = text.replace(/\r\n?/gu, '\n');
  const content = normalized.endsWith('\n') ? normalized.slice(0, -1) : normalized;
  return content.split('\n').length;
}

module.exports = { workspaceFile, lineCount };
