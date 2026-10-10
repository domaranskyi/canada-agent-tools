"""Ukraine Sanctions Screener (NSDC). PPE event 'screened-name' charged per screened name/ID query."""
import gzip, json, re, unicodedata, os
from rapidfuzz import process, fuzz
from apify import Actor

SRC = "https://drs.nsdc.gov.ua"
D = json.load(gzip.open(os.path.join(os.path.dirname(__file__), "..", "data", "index.json.gz"), "rt", encoding="utf-8"))
META, E = D["meta"], D["entries"]
ATTR = (f"Source: State Sanctions Register (Державний реєстр санкцій), National Security and Defense Council of Ukraine (RNBO/NSDC), "
        f"{SRC}. Offline snapshot dated {META['snapshot']}; may not reflect later decrees. Verify on the official register.")
TR = dict(zip("абвгґдеєжзиіїйклмнопрстуфхцчшщьюяыэёъ", ["a","b","v","h","g","d","e","ie","zh","z","y","i","i","i","k","l","m","n","o","p","r","s","t","u","f","kh","ts","ch","sh","shch","","iu","ia","y","e","e",""]))
LEGAL = {"тов","ооо","пао","пат","ат","ао","зао","оао","ip","llc","ltd","jsc","pjsc","ojsc","cjsc","inc","limited","company","co",
         "товариство","обмеженою","відповідальністю","акціонерне","публічне","приватне","закрите","відкрите","общество","ограниченной","ответственностью","акционерное","публичное"}
def norm(s):
    s = unicodedata.normalize("NFKC", s or "").lower().replace("’", "").replace("'", "").replace("ʼ", "")
    s = "".join(TR.get(c, c) for c in s)
    s = re.sub(r"[^\w]+", " ", s)
    return " ".join(t for t in s.split() if t not in LEGAL)
def nid(s): return re.sub(r"[^0-9a-z]", "", (s or "").lower())
CH, OWN = [], []
for i, e in enumerate(E):
    for n in {norm(x) for x in e["names"]}:
        if n: CH.append(n); OWN.append(i)
IDX = {}
for i, e in enumerate(E):
    for d in e["ids"]:
        k = nid(d["value"])
        if len(k) >= 4: IDX.setdefault(k, set()).add(i)
def scorer(a, b, **k): return max(fuzz.token_sort_ratio(a, b), fuzz.token_set_ratio(a, b) * (0.95 if min(len(a), len(b)) > 3 else 0))
def rec(e, score, via):
    return {"name": e["name"], "translit_name": e["translit"], "type": e["type"], "score": round(score, 3), "matched_on": via,
            "status": e["status"], "ids": e["ids"], "aliases": e["names"], "birthdate": e["birthdate"], "country": e["country"],
            "decree": e["decree"], "date": e["date"], "first_decree": e["first_decree"], "first_date": e["first_date"],
            "last_action": e["last_action"], "last_action_decree": e["last_action_decree"], "last_action_date": e["last_action_date"],
            "sanctions_term": e["sanctions_term"], "sanctions_end_date": e["sanctions_end_date"], "register_id": e["sid"], "sourceUrl": SRC}

async def main():
    async with Actor:
        inp = await Actor.get_input() or {}
        names = [n for n in (inp.get("names") or []) if str(n).strip()]
        idq = [n for n in (inp.get("ids") or []) if str(n).strip()]
        th = float(inp.get("fuzzyThreshold") or 0.85); th = th / 100 if th > 1 else th
        types = set(inp.get("entityTypes") or ["individual", "legal", "vessel"])
        active_only = bool(inp.get("activeOnly", False)); mx = int(inp.get("maxMatchesPerName", 10))
        if not names and not idq: raise ValueError("Provide at least one entry in 'names' or 'ids'.")
        Actor.log.info(f"Index snapshot {META['snapshot']}: {len(E)} subjects. Screening {len(names)} names, {len(idq)} IDs.")
        ok = lambda e: e["type"] in types and (not active_only or e["status"] == "active")
        queries = [("name", n) for n in names] + [("id", n) for n in idq]
        for kind, q in queries:
            best = {}
            if kind == "name":
                nq = norm(q)
                if nq:
                    for _, s, j in process.extract(nq, CH, scorer=scorer, score_cutoff=th * 100, limit=200):
                        i = OWN[j]
                        if ok(E[i]) and s / 100 > best.get(i, (0,))[0]: best[i] = (s / 100, "name")
            else:
                for i in IDX.get(nid(q), ()):
                    if ok(E[i]): best[i] = (1.0, "id")
            ms = sorted((rec(E[i], s, v) for i, (s, v) in best.items()), key=lambda r: (-r["score"], r["status"] != "active"))[:mx]
            await Actor.push_data({"query": q, "query_type": kind, "matched": bool(ms), "match_count": len(ms),
                "active_match": any(m["status"] == "active" for m in ms), "top_score": ms[0]["score"] if ms else None,
                "matches": ms, "fuzzyThreshold": th, "snapshot_date": META["snapshot"], "sourceUrl": SRC, "attribution": ATTR})
            await Actor.charge("screened-name")
