#!/usr/bin/env python3
"""
Women's football scouting AI — WSL 2023/24
Mitchelle Ngare, Dartmouth '27

What it does
------------
1. Loads the WSL 2023/24 player table (296 players, StatsBomb open data,
   already built in wsl_202324_player_table.csv).
2. Ranks attackers by xG per 90 (900+ minutes only, so small samples
   don't win).
3. Joins market values and computes value-per-xG:
       value_per_xg = market_value_eur / xg_per90
   Lower = cheaper attacking output.
4. Finds similar, cheaper players for a given player.

IMPORTANT — values are a proxy, not 2023/24 prices
---------------------------------------------------
The market values below are CURRENT Nov 2026 Soccerdonna values,
checked 2026-11-14. They are NOT 2023/24 prices. Label them that way
in any demo / report. The one season-start fact we do have:
Elisabeth Terland was NOT in the July 2023 Soccerdonna top 10,
so she was worth EUR 275,000 or less at season start — then scored
13 goals in 2023/24, moved to Manchester United, and is now EUR 700,000.
That is a timing story, not a current bargain.

Run it
-------
    python3 scouting.py
    python3 scouting.py --player "Elisabeth Terland"
    python3 scouting.py --min-minutes 900 --top 10 --out value_per_xg.csv

No extra packages needed — only the Python standard library.
"""

import argparse
import csv
import math
import sys
from pathlib import Path

# --- Files -----------------------------------------------------------------
HERE = Path(__file__).resolve().parent
PLAYER_CSV = HERE / "wsl_202324_player_table.csv"

# --- Market values: CURRENT Nov 2026 Soccerdonna, proxy only ---------------
# player name (as in the CSV) -> (market value EUR, age now, team now)
# xG/90 comes from the 2023/24 table, so value-per-xG mixes a 2023/24
# performance number with a Nov 2026 price. Say so every time.
MARKET_VALUES = {
    "Viviane Asseyi": (50_000, 32, "West Ham United LFC"),
    "Martha Thomas": (50_000, 30, "Newcastle United"),
    "Bethany England": (75_000, 32, "Crystal Palace"),
    "Francesca Kirby": (85_000, 33, "Brighton & Hove Albion WFC"),
    "Sophie Roman Haug": (210_000, 27, "Liverpool WFC"),
    "Martina Piemonte": (340_000, 29, "AS Roma"),
    "Sjoeke Nüsken": (750_000, 25, "Chelsea FCW"),
    "Elisabeth Terland": (700_000, 25, "Manchester United W"),
}

# Attacking positions in the StatsBomb table. Keep this list explicit —
# "attacker" is a modelling choice, not a column in the data.
ATTACK_POSITIONS = (
    "Forward", "Wing", "Attacking Midfield", "Striker",
)

MIN_MINUTES_DEFAULT = 900


def is_attacker(position: str) -> bool:
    return any(p in position for p in ATTACK_POSITIONS)


def load_players(path: Path = PLAYER_CSV) -> list[dict]:
    """Load the player table, converting numeric columns to float/int."""
    if not path.exists():
        sys.exit(f"Could not find {path}. Run this script from the same "
                 f"folder as wsl_202324_player_table.csv")
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    players = []
    for r in rows:
        try:
            players.append({
                "player": r["player"],
                "team": r["team"],
                "position": r["position"],
                "minutes": float(r["minutes"]),
                "matches": int(r["matches"]),
                "goals": int(r["goals"]),
                "xg": float(r["xg"]),
                "xg_per90": float(r["xg_per90"]),
                "shots_per90": float(r["shots_per90"]),
                "assists": int(r["assists"]),
                "shot_assists": int(r["shot_assists"]),
                "passes": int(r["passes"]),
                "pass_pct": float(r["pass_pct"]),
                "carries_per90": float(r["carries_per90"]),
                "dribbles_completed": int(r["dribbles_completed"]),
            })
        except (KeyError, ValueError) as e:
            print(f"Skipping row {r.get('player')}: {e}", file=sys.stderr)
    return players


def attackers(players: list[dict], min_minutes: int = MIN_MINUTES_DEFAULT) -> list[dict]:
    """Attackers with enough minutes to trust their per-90 numbers."""
    return [p for p in players
            if p["minutes"] >= min_minutes and is_attacker(p["position"])]


def value_per_xg_table(players: list[dict], min_minutes: int = MIN_MINUTES_DEFAULT) -> list[dict]:
    """
    The Week 2 result, reproduced in code.

    For the 8 priced attackers: value_per_xg = value / xG-per-90.
    Returns cheapest first. Players without a price are left out —
    do NOT invent a value for them.
    """
    out = []
    for p in attackers(players, min_minutes):
        if p["player"] not in MARKET_VALUES or p["xg_per90"] <= 0:
            continue
        value, age_now, team_now = MARKET_VALUES[p["player"]]
        out.append({
            **p,
            "market_value_eur": value,
            "age_now": age_now,
            "value_per_xg": value / p["xg_per90"],
            "value_per_goal": value / p["goals"] if p["goals"] else None,
        })
    return sorted(out, key=lambda r: r["value_per_xg"])


def find_similar(target_name: str, players: list[dict],
                 min_minutes: int = MIN_MINUTES_DEFAULT, n: int = 5) -> list[dict]:
    """
    Find similar, cheaper players for `target_name`.

    Similarity = Euclidean distance on standardised per-90 features
    (xG, shots, carries, shot assists). Standardising matters: without
    it, the feature with the biggest numbers (carries) would dominate.
    Only returns players cheaper than the target, where we know a price.
    """
    pool = attackers(players, min_minutes)
    target = next((p for p in pool if p["player"] == target_name), None)
    if target is None:
        close = [p["player"] for p in pool if target_name.lower() in p["player"].lower()]
        hint = f" Did you mean: {', '.join(close)}?" if close else ""
        raise ValueError(f"No attacker called '{target_name}' with "
                         f"{min_minutes}+ minutes.{hint}")

    features = ["xg_per90", "shots_per90", "carries_per90"]
    # shot assists per 90, derived (not a column in the CSV)
    for p in pool:
        p["shot_assists_per90"] = p["shot_assists"] / p["minutes"] * 90
    features.append("shot_assists_per90")

    means = {f: sum(p[f] for p in pool) / len(pool) for f in features}
    sds = {f: (sum((p[f] - means[f]) ** 2 for p in pool) / len(pool)) ** 0.5 or 1
           for f in features}

    def distance(a, b):
        return math.sqrt(sum(((a[f] - means[f]) / sds[f]
                              - (b[f] - means[f]) / sds[f]) ** 2 for f in features))

    target_value = MARKET_VALUES.get(target_name, (math.inf, None, None))[0]
    scored = []
    for p in pool:
        if p["player"] == target_name:
            continue
        value = MARKET_VALUES.get(p["player"], (math.inf, None, None))[0]
        if value >= target_value:      # only cheaper alternatives
            continue
        scored.append({**p, "distance": distance(p, target),
                       "market_value_eur": value})
    return sorted(scored, key=lambda r: r["distance"])[:n]


def print_value_table(rows: list[dict]) -> None:
    print("\nValue per 1.0 xG/90 — cheapest attacking output first")
    print("Market values are CURRENT Nov 2026 Soccerdonna (proxy), NOT 2023/24 prices.")
    print(f"{'Player':<22} {'xG/90':>6} {'Goals':>5} {'Value':>10} {'EUR per xG/90':>14}")
    for r in rows:
        print(f"{r['player']:<22} {r['xg_per90']:>6.2f} {r['goals']:>5} "
              f"€{r['market_value_eur']:>9,} €{r['value_per_xg']:>13,.0f}")
    print("\nRead it as: Asseyi / Thomas cost ~€120k per unit of xG/90;")
    print("Terland / Nüsken cost ~€1.5–1.7m — about 12–14x more.")
    print("The four cheapest were all 27–30 in 2023/24: proven output at")
    print("a low price, with a short remaining peak — not young talent.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-minutes", type=int, default=MIN_MINUTES_DEFAULT,
                    help="Minimum minutes to include a player (default 900)")
    ap.add_argument("--top", type=int, default=10,
                    help="How many top xG/90 attackers to show (default 10)")
    ap.add_argument("--player", type=str, default=None,
                    help='Find similar cheaper players, e.g. --player "Elisabeth Terland"')
    ap.add_argument("--out", type=str, default=None,
                    help="Write the value-per-xG table to this CSV file")
    args = ap.parse_args()

    players = load_players()
    print(f"Loaded {len(players)} players from {PLAYER_CSV.name}")

    # 1. Top attackers by xG/90
    top = sorted(attackers(players, args.min_minutes),
                 key=lambda p: p["xg_per90"], reverse=True)[:args.top]
    print(f"\nTop {args.top} attackers by xG/90 ({args.min_minutes}+ minutes):")
    for p in top:
        print(f"  {p['player']:<24} {p['team']:<28} {p['xg_per90']:.2f} "
              f"({p['goals']} goals, {p['minutes']:.0f} min)")

    # 2. Value per xG — the Week 2 table
    vtable = value_per_xg_table(players, args.min_minutes)
    print_value_table(vtable)

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=[
                "player", "team", "position", "minutes", "goals",
                "xg_per90", "market_value_eur", "value_per_xg", "value_per_goal"])
            w.writeheader()
            w.writerows([{k: r[k] for k in w.fieldnames} for r in vtable])
        print(f"\nWrote value-per-xG table to {args.out}")

    # 3. Similar cheaper players, if asked
    if args.player:
        try:
            similar = find_similar(args.player, players, args.min_minutes)
        except ValueError as e:
            sys.exit(str(e))
        print(f"\nSimilar, cheaper players to {args.player}:")
        for p in similar:
            print(f"  {p['player']:<24} {p['team']:<28} xG/90 {p['xg_per90']:.2f} "
                  f"€{p['market_value_eur']:,}  (distance {p['distance']:.2f})")


if __name__ == "__main__":
    main()
