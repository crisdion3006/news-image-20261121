# News image — 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/crisdion3006/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/crisdion3006/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page summarising the world's news of
Saturday 21 November 2026 in a single 1024×1024 image, built for the
[make.fun](https://make.fun/bounty/news-image-20261121) news-image bounty.

## What's on the page

- **Lead story — Ukraine war:** Russia's "double-tap" strike on Kryvyi
  Rih kills a 7-year-old boy and a 20-year-old paramedic; 42 injured,
  23 apartment blocks and a hospital damaged.
- **Climate — COP31:** talks spill into overtime in Antalya; the closing
  plenary is suspended while the draft drops fossil fuels and sets a
  $120bn finance target.
- **Justice — The Hague:** the ICJ rules 9–6 that Myanmar committed
  genocide against the Rohingya — the court's first-ever state genocide
  finding.
- **Weather — India:** Cyclone Akvan weakens over Odisha after landfall
  near Gopalpur; 300,000 people evacuated.
- **Tech — cybersecurity:** JPMorgan, Visa and Mastercard hit in a
  third-party vendor breach claimed by ransomware group n0n; no payment
  data taken, the banks say.
- **Also today:** Russia's overnight barrage (3 ballistic missiles,
  148 drones), Ethiopia named host of COP32 in 2027, and 39 trains
  cancelled as Akvan lashes India's east coast.

## How it works

`build_image.py` draws the whole page with Pillow — masthead, dateline,
a night-skyline illustration for the lead story, four illustrated cards,
and the footer strip — and writes `entry.png`. Every element is placed
from fixed coordinates with a fixed random seed, so re-running the
script produces the same image every time.

`main.ts` (Node 22) copies `entry.png` to `/output/entry.png`
byte for byte, which keeps the two judged runs identical.

## Run it

```sh
python3 build_image.py   # regenerates entry.png
node main.ts             # writes /output/entry.png
```

## Licence

MIT — see [LICENSE](LICENSE).
