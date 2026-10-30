"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/index.ts
var index_exports = {};
__export(index_exports, {
  greet: () => greet
});
module.exports = __toCommonJS(index_exports);
var import_node_fs = require("node:fs");
function greet(name) {
  if (!name.trim() || /[\r\n]/u.test(name)) throw new Error("name must be a nonempty single line");
  return `Hello, ${name.trim()}!`;
}
if (require.main === module) {
  try {
    const greeting = greet(process.env.INPUT_NAME ?? "World");
    if (!process.env.GITHUB_OUTPUT) throw new Error("GITHUB_OUTPUT is required");
    (0, import_node_fs.appendFileSync)(process.env.GITHUB_OUTPUT, `greeting=${greeting}
`);
    console.log(greeting);
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  greet
});
