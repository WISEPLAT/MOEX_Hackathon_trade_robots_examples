export const incrementPatchVersion = (version: string): string => {
  const versionArray = version.split('.');

  if (versionArray.length !== 3) {
    throw new Error('Invalid version format. Must be in the form of "x.y.z"');
  }

  const major = parseInt(versionArray[0], 10);
  const minor = parseInt(versionArray[1], 10);
  const patch = parseInt(versionArray[2], 10) + 1;

  if (isNaN(major) || isNaN(minor) || isNaN(patch)) {
    throw new Error('Invalid version format. Must be in the form of "x.y.z"');
  }

  return `${major}.${minor}.${patch}`;
}