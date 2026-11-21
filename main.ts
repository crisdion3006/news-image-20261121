/**
 * Entry point for the make.fun news-image bounty (21 November 2026).
 *
 * The front page is rendered ahead of time by build_image.py into
 * entry.png next to this file. This program only copies that file,
 * byte for byte, into /output/entry.png. Copying is deterministic,
 * so two runs always write identical bytes.
 */

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const bytes = readFileSync(source);
if (bytes.length === 0) {
  throw new Error("entry.png is empty, refusing to write an empty output");
}

mkdirSync("/output", { recursive: true });
writeFileSync("/output/entry.png", bytes);
console.log(`copied ${bytes.length} bytes to /output/entry.png`);
