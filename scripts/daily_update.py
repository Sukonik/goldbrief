#!/usr/bin/env python3
"""Public-information-only, no AI-written summaries. Failure retains last good feed."""
import datetime as dt
import email.utils
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
EASTERN=ZoneInfo("America/New_York")
now=dt.datetime.now(dt.timezone.utc)
et=now.astimezone(EASTERN)
target=ROOT/"data/daily.json"
existing=json.loads(target.read_text())
manual=os.environ.get("GOLDBRIEF_MANUAL","false").lower()=="true"
if not manual and not (et.hour in (8,9) and et.minute>=0):
    print("Skipped non-8:30am ET cron invocation:",et.isoformat());raise SystemExit(0)
if not manual and existing.get("local_date")==et.date().isoformat():
    print("Today's edition already exists.");raise SystemExit(0)
terms=["AI companies when:2d","artificial intelligence models when:2d"]
stories=[]
seen=set()
for term in terms:
    url="https://news.google.com/rss/search?"+urllib.parse.urlencode({"q":term,"hl":"en-US","gl":"US","ceid":"US:en"})
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"GoldBriefEditorialRSS/1.0 (public news headlines)"})
        with urllib.request.urlopen(req,timeout=18) as rsp: data=rsp.read(1500000)
        feed=ET.fromstring(data)
        for item in feed.findall("./channel/item")[:20]:
            title=" ".join((item.findtext("title") or "").split()).strip()
            link=(item.findtext("link") or "").strip()
            source_node=item.find("source")
            source=(source_node.text or "").strip() if source_node is not None else "Google News RSS"
            date=(item.findtext("pubDate") or "").strip()
            if not title or not link.startswith("https://"):continue
            try:
                parsed=email.utils.parsedate_to_datetime(date).astimezone(dt.timezone.utc)
                if abs((now-parsed).total_seconds())>3*86400:continue
                iso=parsed.date().isoformat()
            except (TypeError,ValueError,OverflowError):iso=""
            ident=title.casefold()
            if ident in seen:continue
            seen.add(ident)
            stories.append({"title":title[:210],"url":link,"source":source[:90],"date":iso,"classification":"automated_external_unreviewed"})
    except Exception as ex:print("Feed unavailable:",term,type(ex).__name__,str(ex)[:180])
if not stories:
    print("No valid source headlines; preserving previous snapshot.")
    raise SystemExit(0)
stories.sort(key=lambda s:s["date"],reverse=True)
output={"generated_at":now.isoformat(timespec="seconds"),"local_date":et.date().isoformat(),"mode":"automatic-source-headlines-only","source_type":"Google News RSS aggregation","verification":"unreviewed; titles and links provided by outside publishers","stories":stories[:16],"note":"Links/headlines supplied by external RSS; no GoldBrief factual endorsement, generated summaries or fabricated metrics."}
target.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n")
print("Daily external headlines collected:",len(output["stories"]),output["local_date"])
