#!/usr/bin/env python3
"""Collect public RSS headlines into data/daily.json. No AI-written summaries.

Every story is labelled automated_external_unreviewed. A failed or invalid run keeps the last good feed.
"""
import datetime as dt, email.utils, json, os, re, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT = Path(__file__).resolve().parents[1]
EASTERN = ZoneInfo("America/New_York")
TARGET = ROOT / "data/daily.json"
QUERIES = [("usa", "AI companies when:2d", "US", "en-US", "US:en"),
           ("usa", "artificial intelligence models when:2d", "US", "en-US", "US:en"),
           ("international", "artificial intelligence when:2d", "GB", "en-GB", "GB:en"),
           ("international", "AI Europe OR China OR India OR Japan when:2d", "IN", "en-IN", "IN:en")]
STOP = set("the a an of to in on for and with as at by is are be from how why what new ai says after over into its it's".split())

def tokens(title):
    return {w for w in re.findall(r"[a-z0-9]+", title.casefold().rsplit(" - ", 1)[0]) if w not in STOP and len(w) > 2}

def fetch(region, q, gl, hl, ceid, now):
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q, "hl": hl, "gl": gl, "ceid": ceid})
    req = urllib.request.Request(url, headers={"User-Agent": "GoldBriefEditorialRSS/1.1 (public news headlines)"})
    with urllib.request.urlopen(req, timeout=18) as rsp:
        feed = ET.fromstring(rsp.read(1500000))
    for item in feed.findall("./channel/item")[:25]:
        title = " ".join((item.findtext("title") or "").split())
        link = (item.findtext("link") or "").strip()
        node = item.find("source"); source = (node.text or "").strip() if node is not None else "Google News RSS"
        try:
            published = email.utils.parsedate_to_datetime(item.findtext("pubDate") or "").astimezone(dt.timezone.utc)
        except (TypeError, ValueError, OverflowError):
            continue  # undated items cannot be shown with a timestamp
        if not title or not link.startswith("https://") or abs((now - published).total_seconds()) > 3 * 86400:
            continue
        yield {"title": title[:210], "url": link, "source": source[:90], "region": region,
               "published_at": published.isoformat(timespec="minutes"), "date": published.date().isoformat(),
               "classification": "automated_external_unreviewed"}

def cluster(stories):
    """Merge near-duplicate headlines (token overlap); keep the first, record the other outlets."""
    kept = []
    for s in sorted(stories, key=lambda s: s["published_at"], reverse=True):
        t = tokens(s["title"])
        for k in kept:
            u = k["_t"]
            if t and u and len(t & u) / len(t | u) >= 0.6:
                if s["source"] != k["source"] and s["source"] not in k["also_reported_by"]:
                    k["also_reported_by"].append(s["source"])
                if s["region"] != k["region"]: k["region"] = "both"
                break
        else:
            kept.append({**s, "_t": t, "also_reported_by": []})
    for k in kept: del k["_t"]
    return kept

def validate(doc):
    errs = []
    if not doc["stories"]: errs.append("no stories")
    for i, s in enumerate(doc["stories"]):
        if not s["url"].startswith("https://"): errs.append(f"story {i}: non-https url")
        if s["classification"] != "automated_external_unreviewed": errs.append(f"story {i}: wrong label")
        if not s["title"] or not s["source"]: errs.append(f"story {i}: missing title/source")
        try: dt.datetime.fromisoformat(s["published_at"])
        except ValueError: errs.append(f"story {i}: bad timestamp")
    return errs

def main():
    now = dt.datetime.now(dt.timezone.utc); et = now.astimezone(EASTERN)
    existing = json.loads(TARGET.read_text())
    manual = os.environ.get("GOLDBRIEF_MANUAL", "false").lower() == "true"
    if not manual and not et.hour in (8, 9):
        print("Skipped: not the 8:30 AM ET window:", et.isoformat()); return 0
    if not manual and existing.get("local_date") == et.date().isoformat():
        print("Today's edition already exists."); return 0
    raw, failed = [], []
    for q in QUERIES:
        try: raw += list(fetch(*q[:1], *q[1:], now))
        except Exception as ex: failed.append(f"{q[1]}: {type(ex).__name__}"); print("Feed unavailable:", q[1], type(ex).__name__, str(ex)[:160])
    stories = cluster(raw)[:24]
    doc = {"generated_at": now.isoformat(timespec="seconds"), "local_date": et.date().isoformat(),
           "target_time": "8:30 AM America/New_York; GitHub scheduled runs may start later",
           "actual_run_et": et.isoformat(timespec="minutes"),
           "mode": "automatic-source-headlines-only", "source_type": "Google News RSS aggregation",
           "verification": "unreviewed; titles and links provided by outside publishers",
           "feeds_failed": failed, "stories": stories,
           "note": "Headlines and links are supplied by outside publishers via RSS. GoldBrief has not fact-checked them and does not endorse them. No generated summaries or metrics."}
    errs = validate(doc)
    if errs:
        print("Validation failed, keeping previous snapshot:", "; ".join(errs[:5])); return 0
    TARGET.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    print("Collected", len(stories), "clustered headlines for", doc["local_date"]); return 0

if __name__ == "__main__":
    sys.exit(main())
