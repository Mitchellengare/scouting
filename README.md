# Women's football scouting — dashboard and README

This file has both pieces you asked for: a one-page dashboard first, then a README you can copy straight into GitHub as `README.md`.

---

# Part 1 — One-page dashboard

## WSL 2023/24 scouting at a glance

- **Dataset:** 296 players, 132 matches, Women's Super League 2023/24 (StatsBomb open data)
- **Trusted sample:** 151 players with 900+ minutes
- **Question:** Who produces the most attacking output, what does that output cost, and who plays the same way for less?

## Top 10 attackers by xG per 90 (900+ minutes)

| Player | Team (2023/24) | xG/90 | Goals | Minutes |
|---|---|---:|---:|---:|
| Khadija Monifa Shaw | Manchester City WFC | 0.76 | 21 | 1,462 |
| Alessia Russo | Arsenal WFC | 0.65 | 12 | 1,824 |
| Sjoeke Nüsken | Chelsea FCW | 0.52 | 7 | 1,203 |
| Lauren James | Chelsea FCW | 0.46 | 13 | 1,151 |
| Guro Reiten | Chelsea FCW | 0.44 | 7 | 1,120 |
| Francesca Kirby | Chelsea FCW | 0.44 | 3 | 993 |
| Bethany England | Tottenham Hotspur Women | 0.43 | 5 | 1,066 |
| Viviane Asseyi | West Ham United LFC | 0.42 | 6 | 2,058 |
| Elisabeth Terland | Brighton & Hove Albion WFC | 0.42 | 13 | 1,891 |
| Bethany Mead | Arsenal WFC | 0.41 | 8 | 1,500 |

Shaw is the clear outlier at 0.76 xG per 90. Russo is second, and no one else is above 0.52.

## Value per xG — cheapest attacking output first

Value per 1.0 xG/90 = market value ÷ xG per 90. Lower means cheaper attacking output.

| Player | xG/90 | Goals | Market value | € per 1.0 xG/90 |
|---|---:|---:|---:|---:|
| Viviane Asseyi | 0.42 | 6 | €50,000 | €119,048 |
| Martha Thomas | 0.41 | 7 | €50,000 | €121,951 |
| Bethany England | 0.43 | 5 | €75,000 | €174,419 |
| Francesca Kirby | 0.44 | 3 | €85,000 | €193,182 |
| Sophie Roman Haug | 0.35 | 7 | €210,000 | €600,000 |
| Martina Piemonte | 0.40 | 3 | €340,000 | €850,000 |
| Sjoeke Nüsken | 0.52 | 7 | €750,000 | €1,442,308 |
| Elisabeth Terland | 0.42 | 13 | €700,000 | €1,666,667 |

> **Important:** Market values are current November 2026 Soccerdonna values, used as a proxy. They are **not** 2023/24 prices. Do not present them as season prices.

**How to read it:** Asseyi and Thomas cost about €120,000 per unit of xG/90. Terland and Nüsken cost about €1.5–1.7 million — roughly 12–14× more for a similar unit of output.

The four cheapest players were all 27–30 in 2023/24. That is proven output at a low price with a short remaining peak, not young undervalued talent.

## Similar, cheaper players to Elisabeth Terland

Terland in 2023/24: 0.42 xG/90, 13 goals, Brighton & Hove Albion WFC. Current value: €700,000.

| Similar player | Team (2023/24) | xG/90 | Value | Distance |
|---|---|---:|---:|---:|
| Sophie Roman Haug | Liverpool WFC | 0.35 | €210,000 | 0.95 |
| Martha Thomas | Tottenham Hotspur Women | 0.41 | €50,000 | 0.96 |
| Martina Piemonte | Everton LFC | 0.40 | €340,000 | 1.04 |
| Viviane Asseyi | West Ham United LFC | 0.42 | €50,000 | 1.05 |
| Bethany England | Tottenham Hotspur Women | 0.43 | €75,000 | 1.33 |

Lower distance means a more similar playing profile, based on xG, shots, carries, and shot assists per 90.

**Demo line:** Players like Terland, for a fraction of the price — Thomas and Asseyi match her xG/90 at €50,000 instead of €700,000.

## The Terland timing story

Terland was not in the July 2023 Soccerdonna top 10, so her value at the start of 2023/24 was €275,000 or less. She then scored 13 goals in 2023/24, moved to Manchester United, and her value rose to €700,000. The market caught up — she is a timing story, not a current bargain.

---

# Part 2 — README for GitHub

Copy everything below the line into a file called `README.md` in your repository.

---

# Women's Football Scouting AI — WSL 2023/24

Find undervalued women's football attackers using public performance data: rank players by expected goals (xG) per 90, compare that output to market value, and find similar players who cost less.

Built by Mitchelle Ngare, Dartmouth '27, Computer Science.

## What it does

The script `scouting.py` does three things:

1. **Ranks attackers by xG per 90** — loads the WSL 2023/24 player table (296 players) and lists the top attackers, counting only players with 900+ minutes so a small sample does not win.

2. **Works out value per xG** — for the 8 attackers with a checked market value, it calculates `market value ÷ xG per 90`. Lower is cheaper attacking output.

3. **Finds similar, cheaper players** — given a player, it finds attackers with a similar per-90 profile (xG, shots, carries, and shot assists) who cost less.

## Key findings

- Khadija Monifa Shaw leads the league at 0.76 xG per 90 (21 goals), ahead of Alessia Russo at 0.65.
- Viviane Asseyi (€119,048 per 1.0 xG/90) and Martha Thomas (€121,951) are the cheapest attacking output among the priced players.
- Elisabeth Terland is the most expensive per unit at €1,666,667, after her value rose from €275,000 or less at the start of 2023/24 to €700,000 following 13 goals and a move to Manchester United.
- The cheapest four were all 27–30 in 2023/24: proven output at a low price, with a short remaining peak.

## How to run it

No extra packages are needed — only Python 3 and the standard library.

Put `scouting.py` and `wsl_202324_player_table.csv` in the same folder, then run:

```bash
python3 scouting.py
python3 scouting.py --player "Elisabeth Terland"
python3 scouting.py --min-minutes 900 --top 10 --out value_per_xg.csv
```

If the CSV is in a different folder, point to it:

```bash
python3 scouting.py --csv /path/to/wsl_202324_player_table.csv
```

### Options

- `--player "Name"` — find similar, cheaper players for that player
- `--min-minutes 900` — minimum minutes to include a player (default: 900)
- `--top 10` — how many top attackers to show (default: 10)
- `--out value_per_xg.csv` — write the value-per-xG table to a CSV file
- `--csv PATH` — path to the player table, if it is not next to the script

## Files

- `scouting.py` — the analysis script
- `wsl_202324_player_table.csv` — player table for WSL 2023/24: 296 players from 132 matches, with minutes, goals, xG, shots, passes, carries, and per-90 rates
- `wsl_202324_summary.json` — summary of the dataset and top performers

## Method

- **Attacker** means a position containing Forward, Wing, Attacking Midfield, or Striker. This is a modelling choice, stated in the code.
- **xG per 90** is expected goals per 90 minutes played.
- **Value per xG** is `market value (EUR) ÷ xG per 90`.
- **Similarity** is Euclidean distance on standardised per-90 features: xG, shots, carries, and shot assists. Standardising stops the feature with the largest numbers from dominating. Lower distance means more similar. Only players cheaper than the target, with a known price, are returned.

## Data and the value caveat

Performance data is from StatsBomb open data for the FA Women's Super League 2023/24.

Market values are **current November 2026 Soccerdonna values, checked 14 November 2026, used as a proxy only**. They are not 2023/24 prices, and value per xG therefore mixes a 2023/24 performance number with a November 2026 price. Label it that way in any report or demo.

Only 8 attackers have a checked market value in the script. Players without a price are left out of the value table — no value is invented for them.

The one season-start fact available is for Terland: she was not in the July 2023 top 10, so she was worth €275,000 or less at season start.

## Limitations

- With only 8 priced players, this does not produce a full-table undervalued flag.
- Current values reflect what the market thinks now, not what a player cost during 2023/24, so a player who has already moved and re-priced, like Terland, will look expensive even if she was cheap at the time.
- xG per 90 measures chance quality, not finishing, availability, or fit for a particular team.

## Next steps

- Add season-start (July 2023) values so value per xG uses prices from the same period as the performance data.
- Price more attackers to test whether the cheap-output pattern holds beyond the first 8.
- Add an undervalued flag for the full table once enough players are priced.
