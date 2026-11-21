// news-image-20261121 entry (Node 22, standard library only).
//
// The image is built in this session and shipped as entry.png beside this
// file: a one-day front page for Saturday, 21 November 2026, drawn
// programmatically (PIL) with real text and flat drawn icons.
// This program's only job is to hand that image to the grader, unchanged.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);

if (!existsSync(src)) {
  throw new Error('entry.png is missing from the repository');
}

const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);

// Sanity check: the copy must be whole — same byte count as the source.
if (statSync(dest).size !== statSync(src).size) {
  throw new Error('entry.png copy is incomplete');
}
