/** Team naming policy; contains no runner, filesystem, or release API calls. */
export function releaseKey(component: string, channel: string): string {
  if (!/^[a-z][a-z0-9-]{0,31}$/u.test(component) || /[\r\n]/u.test(component)) {
    throw new Error('component must match [a-z][a-z0-9-]{0,31}');
  }
  if (channel !== 'preview' && channel !== 'stable') {
    throw new Error('channel must be preview or stable');
  }
  return `${component}-${channel}`;
}
