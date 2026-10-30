// action/src/index.ts
var import_node_fs = require("node:fs");

// action/src/domain.ts
function releaseKey(component, channel) {
  if (!/^[a-z][a-z0-9-]{0,31}$/u.test(component) || /[\r\n]/u.test(component)) {
    throw new Error("component must match [a-z][a-z0-9-]{0,31}");
  }
  if (channel !== "preview" && channel !== "stable") {
    throw new Error("channel must be preview or stable");
  }
  return `${component}-${channel}`;
}

// action/src/index.ts
try {
  const key = releaseKey(
    process.env.INPUT_COMPONENT ?? "docs",
    process.env.INPUT_CHANNEL ?? "preview"
  );
  const output = process.env.GITHUB_OUTPUT;
  if (!output) throw new Error("GITHUB_OUTPUT must be set");
  (0, import_node_fs.appendFileSync)(output, `release-key=${key}
`, "utf8");
  console.log(`Computed release key: ${key}`);
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
