#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daily data refresh for Home.Watch (standard library only).

Sources (all public):
  - CPSC recalls API (saferproducts.gov), with the CPSC recalls RSS as a fallback
  - OpenFEMA disaster declarations
  - Google News RSS search headlines
  - MET Norway locationforecast (CC BY 4.0) for the freeze & heat board
  - YouTube oEmbed to verify curated videos

A failing source never breaks the run: the previous file is kept.
"""
import datetime
import email.utils
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from content.cities import CITIES  # noqa: E402

DATA = os.path.join(ROOT, "data")
UA = "HomeWatchSite/1.0 (+https://home.watch; daily data refresh)"
NOW = datetime.datetime.now(datetime.timezone.utc)
STAMP = NOW.strftime("%Y-%m-%dT%H:%MZ")


def log(*a):
    print("[update]", *a, flush=True)


def get(url, accept="application/json", timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def read_json(name, default):
    try:
        with open(os.path.join(DATA, name), encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def write_json(name, obj):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    log("wrote", name)


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


# ------------------------------------------------------------------ recalls
HOME_WORDS = re.compile(
    r"heater|furnace|boiler|smoke|carbon monoxide|\bCO\b|alarm|detector|dehumidifier|humidifier|air condition|"
    r"extension cord|power strip|surge|outlet|charger|batter|generator|lamp|light|dryer|washer|dishwasher|"
    r"refrigerator|freezer|ice maker|oven|range|stove|cooktop|microwave|toaster|fryer|kettle|coffee|fan\b|"
    r"thermostat|lock|garage|door|window|blind|ladder|extinguisher|sprinkler|faucet|hose|valve|pipe|toilet|"
    r"fireplace|grill|propane|gas|camera|doorbell|sensor|router|appliance|dresser|chest|furniture|pool|spa|"
    r"hot tub|water|electric|wiring|breaker|cabinet|bed|mattress|vacuum|blanket|cord",
    re.I)


def recalls():
    start = (NOW - datetime.timedelta(days=150)).strftime("%Y-%m-%d")
    items = []
    try:
        _, body = get("https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallDateStart=" + start)
        for r in json.loads(body):
            title = clean(r.get("Title"))
            prods = " ".join(clean(p.get("Name")) for p in (r.get("Products") or []))
            text = " ".join([title, prods, clean(r.get("Description"))])
            if not HOME_WORDS.search(text):
                continue
            hz = (r.get("Hazards") or [{}])[0].get("Name") or ""
            img = (r.get("Images") or [{}])[0].get("URL") or ""
            items.append({"title": title, "url": r.get("URL") or "https://www.cpsc.gov/Recalls",
                          "date": (r.get("RecallDate") or "")[:10], "hazard": clean(hz)[:140], "image": img})
        items.sort(key=lambda x: x["date"], reverse=True)
        log("recalls via API:", len(items))
    except Exception as e:  # fall back to RSS
        log("recall API failed:", e)
        try:
            _, body = get("https://www.cpsc.gov/Newsroom/CPSC-RSS-Feed/Recalls-RSS", "application/rss+xml")
            for it in ET.fromstring(body).iter("item"):
                title = clean(it.findtext("title"))
                desc = clean(it.findtext("description"))
                if not HOME_WORDS.search(title + " " + desc):
                    continue
                try:
                    d = email.utils.parsedate_to_datetime(it.findtext("pubDate")).date().isoformat()
                except Exception:
                    d = ""
                items.append({"title": title, "url": it.findtext("link") or "https://www.cpsc.gov/Recalls", "date": d, "hazard": "", "image": ""})
            log("recalls via RSS:", len(items))
        except Exception as e2:
            log("recall RSS failed:", e2)
    if items:
        write_json("recalls.json", {"updated": STAMP, "source": "U.S. Consumer Product Safety Commission", "items": items[:40]})


# ------------------------------------------------------------------ FEMA
FEMA_TYPES = {"DR": "Major disaster", "EM": "Emergency", "FM": "Fire management"}


def fema():
    url = ("https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?"
           + urllib.parse.urlencode({"$orderby": "declarationDate desc", "$top": "500",
                                     "$select": "disasterNumber,state,declarationType,declarationDate,incidentType,declarationTitle,designatedArea"}))
    try:
        _, body = get(url)
        rows = json.loads(body).get("DisasterDeclarationsSummaries", [])
        seen, items = {}, []
        for r in rows:
            n = r.get("disasterNumber")
            if n in seen:
                seen[n]["areas"] += 1
                continue
            item = {"number": n, "state": r.get("state", ""), "date": (r.get("declarationDate") or "")[:10],
                    "type": FEMA_TYPES.get(r.get("declarationType"), r.get("declarationType", "")),
                    "incident": r.get("incidentType", ""), "title": (r.get("declarationTitle") or "").title(), "areas": 1}
            seen[n] = item
            items.append(item)
        log("fema:", len(items))
        if items:
            write_json("fema.json", {"updated": STAMP, "source": "FEMA OpenFEMA", "items": items[:40]})
    except Exception as e:
        log("fema failed:", e)


# ------------------------------------------------------------------ news
NEWS_QUERIES = [
    '"home watch" service',
    '"vacant home" OR "vacant homes" insurance',
    'snowbirds home "while away"',
    'frozen pipes burst homes',
    'hurricane season homeowners prepare',
    'home break-ins vacation tips',
    'water leak detection home',
]


RELEVANT = re.compile(r"home|house|homeowner|propert|pipe|freez|frozen|hurricane|storm|leak|water damage|insur|vacant|snowbird|"
                      r"burglar|break-in|break in|squatter|flood|mold|winteri|security system|smoke alarm|carbon monoxide", re.I)
NOISE = re.compile(r"NYSE:|NASDAQ:|\bstock\b|shares|earnings|dividend|movie|film|netflix|streaming|season \d|episode|trailer|celebrity|\bNFL\b|\bNBA\b", re.I)


def news():
    items, seen = [], set()
    for q in NEWS_QUERIES:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q + " when:30d", "hl": "en-US", "gl": "US", "ceid": "US:en"})
        try:
            _, body = get(url, "application/rss+xml")
            for it in ET.fromstring(body).iter("item"):
                title = clean(it.findtext("title"))
                src = clean(it.findtext("source"))
                if src and title.endswith(" - " + src):
                    title = title[: -(len(src) + 3)]
                key = re.sub(r"[^a-z0-9]", "", title.lower())[:80]
                if not title or key in seen or not RELEVANT.search(title) or NOISE.search(title):
                    continue
                seen.add(key)
                try:
                    dt = email.utils.parsedate_to_datetime(it.findtext("pubDate"))
                except Exception:
                    dt = NOW
                items.append({"title": title, "url": it.findtext("link"), "source": src, "date": dt.date().isoformat(), "ts": dt.timestamp(), "topic": q})
            time.sleep(1)
        except Exception as e:
            log("news failed for", q, e)
    items.sort(key=lambda x: x["ts"], reverse=True)
    for x in items:
        x.pop("ts", None)
    log("news:", len(items))
    if items:
        write_json("news.json", {"updated": STAMP, "source": "Google News", "items": items[:40]})


# ------------------------------------------------------------------ freeze & heat board
def c2f(c):
    return round(c * 9 / 5 + 32)


def citywatch():
    prev = {c["name"]: c for c in read_json("citywatch.json", {}).get("cities", [])}
    out = []
    for name, region, country, lat, lon, role in CITIES:
        url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=%.4f&lon=%.4f" % (lat, lon)
        try:
            _, body = get(url)
            ts = json.loads(body)["properties"]["timeseries"]
            offset = datetime.timedelta(hours=round(lon / 15))  # approximate local day
            days = {}
            for t in ts:
                when = datetime.datetime.fromisoformat(t["time"].replace("Z", "+00:00")) + offset
                d = when.date().isoformat()
                temp = t["data"]["instant"]["details"].get("air_temperature")
                if temp is None:
                    continue
                day = days.setdefault(d, {"min": temp, "max": temp, "symbol": ""})
                day["min"] = min(day["min"], temp)
                day["max"] = max(day["max"], temp)
                nxt = t["data"].get("next_6_hours") or t["data"].get("next_1_hours") or {}
                sym = (nxt.get("summary") or {}).get("symbol_code", "")
                if sym and (11 <= when.hour <= 15 or not day["symbol"]):
                    day["symbol"] = sym
            keys = sorted(days)[:7]
            dl = [{"date": k, "min_c": round(days[k]["min"]), "max_c": round(days[k]["max"]),
                   "min_f": c2f(days[k]["min"]), "max_f": c2f(days[k]["max"]), "symbol": days[k]["symbol"].replace("_", " ")} for k in keys]
            mn, mx = min(days[k]["min"] for k in keys), max(days[k]["max"] for k in keys)
            out.append({"name": name, "region": region, "country": country, "role": role, "lat": lat, "lon": lon,
                        "min_c": round(mn), "max_c": round(mx), "min_f": c2f(mn), "max_f": c2f(mx),
                        "freeze_days": sum(1 for k in keys if days[k]["min"] <= 0),
                        "hard_freeze": mn <= -6.7,
                        "heat_days": sum(1 for k in keys if days[k]["max"] >= 37.8),
                        "days": dl})
        except Exception as e:
            log("met.no failed for", name, e)
            if name in prev:
                out.append(prev[name])
        time.sleep(0.3)
    log("citywatch:", len(out))
    if out:
        write_json("citywatch.json", {"updated": NOW.date().isoformat(), "source": "MET Norway (CC BY 4.0)", "cities": out})


# ------------------------------------------------------------------ videos
def videos():
    data = read_json("videos.json", {"items": []})
    kept = []
    for v in data.get("items", []):
        url = "https://www.youtube.com/oembed?" + urllib.parse.urlencode({"url": "https://www.youtube.com/watch?v=" + v["id"], "format": "json"})
        try:
            _, body = get(url)
            meta = json.loads(body)
            v["title"] = meta.get("title") or v.get("title", "")
            v["author"] = meta.get("author_name") or v.get("author", "")
            v["checked"] = NOW.date().isoformat()
            kept.append(v)
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 403, 404):
                log("dropping unavailable video", v["id"], e.code)
                continue
            kept.append(v)
        except Exception as e:
            log("video check error", v["id"], e)
            kept.append(v)
        time.sleep(0.2)
    data["items"] = kept
    data["updated"] = STAMP
    write_json("videos.json", data)


if __name__ == "__main__":
    for fn in (recalls, fema, news, citywatch, videos):
        try:
            fn()
        except Exception as exc:  # never fail the workflow
            log(fn.__name__, "crashed:", exc)
    log("done")
