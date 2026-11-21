# 21 November 2026 — The World in One Image

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/crisdion3006/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/crisdion3006/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-day front page summing up the world news of **Saturday, 21 November 2026**, built for the [make.fun](https://make.fun/bounty/news-image-20261121) bounty `news-image-20261121`.

## The day's stories

- **Ukraine war** — Russian "double-tap" strike on Kryvyi Rih kills a 7-year-old boy and a 20-year-old paramedic; 42 injured, 23 apartment blocks and a hospital damaged, as Russia launches 148 drones overnight.
- **Climate** — COP31 spills into overtime in Antalya: closing plenary suspended Friday night; the draft drops fossil fuels and a $120bn finance target.
- **Justice** — World court finds Myanmar committed genocide against the Rohingya: the ICJ's first-ever state genocide finding, 9–6, about 10,000 killed in 2017; reparations ordered.
- **Weather** — Cyclone Akvan weakens over Odisha after landfall near Gopalpur at 70–80 kmph; 300,000 people evacuated as heavy rain and flooding continue.
- **Tech** — JPMorgan, Visa and Mastercard confirm third-party vendor breaches: ransomware group n0n claims customer data; no payment data taken.
- **Also today** — Russia attacks Ukraine with 3 ballistic missiles and 148 drones overnight; Ethiopia named host of COP32 in 2027; 39 trains cancelled as Akvan lashes India's east coast.

## How the image is made

`entry.png` (1024×1024, PNG) is drawn programmatically with Python PIL: every word is real rendered text, and each story's picture is a flat icon drawn from shapes — no AI-generated text, so nothing is garbled. The build script is `build_image.py`. `main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
