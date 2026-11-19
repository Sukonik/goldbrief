#!/usr/bin/env python3
"""Copy delayed prices for the Markets page tickers from Payout Lab into data/quotes.json.

Payout Lab (https://github.com/Sukonik/payout-lab) publishes data.json three times a day; each ticker's
record carries its own refresh time. Prices are DELAYED snapshots (unofficial Yahoo Finance / Tiingo
data), never a live feed. On any failure the previous file is kept.
"""
import datetime as dt, json, sys, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://sukonik.github.io/payout-lab/data.json"
markets = json.loads((ROOT / "data/markets.json").read_text(encoding="utf-8"))["markets"]
wanted = sorted({m["quote_ticker"] for m in markets if m.get("quote_ticker")})
try:
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "GoldBriefQuotes/1.0 (public data snapshot)"})
    with urllib.request.urlopen(req, timeout=30) as rsp:
        data = json.loads(rsp.read(8_000_000))
    tickers = data["tickers"]
except Exception as ex:
    print("Payout Lab unavailable, keeping previous quotes:", type(ex).__name__, str(ex)[:160]); sys.exit(0)
quotes, missing = {}, []
for t in wanted:
    r = tickers.get(t)
    if isinstance(r, dict) and isinstance(r.get("p"), (int, float)) and r["p"] > 0 and r.get("u"):
        quotes[t] = {"price": r["p"], "updated": r["u"], "source": r.get("src", "unknown")}
    else:
        missing.append(t)
if not quotes:
    print("No usable quotes; keeping previous file."); sys.exit(0)
out = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "source": "Payout Lab", "source_url": SOURCE,
       "payout_lab_updated": data.get("updated"), "currency": "USD",
       "note": "Delayed snapshot of unofficial Yahoo Finance / Tiingo data via Payout Lab. Not a live feed; each ticker has its own refresh time.",
       "quotes": quotes, "missing": missing}
(ROOT / "data/quotes.json").write_text(json.dumps(out, indent=2) + "\n")
print("Quotes:", ", ".join(f"{k} {v['price']} ({v['updated'][:16]})" for k, v in quotes.items()), "| missing:", missing or "none")
