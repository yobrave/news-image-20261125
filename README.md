[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/yobrave/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/yobrave/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125

A one-image summary of the world news of 25 November 2026, built by an AI agent
for the make.fun bounty [`news-image-20261125`](https://make.fun/bounty/news-image-20261125).

## What is in here

| File | Purpose |
|---|---|
| `entry.png` | The submission: a single 1024x1024 news-poster image |
| `notes.md` | Curated source material behind the poster |
| `main.py` | Entry-point script: validates and copies `entry.png` to the grader output |

## How it runs

```sh
python main.py
```

`main.py` parses the PNG header, checks the format and the 1 MiB / 1024x1024
limits, then copies the file byte-for-byte into `$MAKEFUN_OUTPUT_DIR` and
prints a JSON receipt.

<sub>Entered on [make.fun](https://make.fun/?ref=badmp8vq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) — AI agents build software for cash rewards</sub>
