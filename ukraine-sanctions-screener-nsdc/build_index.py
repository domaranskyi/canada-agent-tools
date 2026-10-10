"""Build lean index from NSDC 'actions' CSV exports. Usage: python build_index.py <dir> <DD.MM.YYYY>"""
import csv,json,gzip,re,sys,collections
csv.field_size_limit(10**9)
D,SNAP=sys.argv[1],sys.argv[2]; snap_iso="-".join(reversed(SNAP.split(".")))
ACT={"Застосування санкцій":"applied","Зміна санкцій":"amended","Скасування санкцій":"lifted"}
def ids(*fields):
    out=[]
    for f in fields:
        for seg in (f or "").split(";"):
            seg=seg.strip()
            if ":" not in seg: continue
            lab,val=seg.split(":",1); m=re.match(r"(.*?)\s*\[(.*)\]\s*$",val)
            v,c=(m.group(1),m.group(2)) if m else (val,None)
            if v.strip(): out.append({"type":lab.strip(),"value":v.strip(),"country":c})
    return out
idx=[];counts={}
for typ in ["individual","legal","vessel"]:
    rows=list(csv.DictReader(open(f"{D}/{SNAP} {typ} actions.csv",encoding="utf-8-sig")))
    g=collections.defaultdict(list)
    for r in rows: g[r["sid"]].append(r)
    for sid,rs in g.items():
        rs.sort(key=lambda r:(r["decree_date"],r["id"])); last=rs[-1]
        withdata=[r for r in rs if r["action_type"]!="Скасування санкцій"] or rs; cur=withdata[-1]
        end=cur["sanctions_end_date"]
        st="lifted" if last["action_type"]=="Скасування санкцій" else ("expired" if end and end<snap_iso else "active")
        names=[]
        for r in rs:
            for n in [r["name"],r["translit_name"]]+r["aliases"].split(";"):
                n=n.strip()
                if n and n not in names: names.append(n)
        idv=[];seen=set()
        for r in rs:
            for i in ids(r.get("reg_id"),r.get("tax_id"),r.get("identity_docs")):
                if i["value"] not in seen: seen.add(i["value"]); idv.append(i)
        idx.append({"sid":sid,"type":typ,"name":cur["name"],"translit":cur["translit_name"],"names":names,"ids":idv,
          "birthdate":cur.get("birthdate") or None,"country":cur.get("country") or cur.get("citizenship") or None,
          "status":st,"sanctions_term":cur["sanctions_term"] or None,"sanctions_end_date":end or None,
          "decree":cur["decree"],"date":cur["decree_date"],"first_decree":rs[0]["decree"],"first_date":rs[0]["decree_date"],
          "last_action":ACT.get(last["action_type"],last["action_type"]),"last_action_decree":last["decree"],"last_action_date":last["decree_date"],
          "actions":[{"action":ACT.get(r["action_type"]),"decree":r["decree"],"date":r["decree_date"]} for r in rs]})
    counts[typ]={"action_rows":len(rows),"subjects":len(g)}
meta={"snapshot":SNAP,"snapshot_iso":snap_iso,"counts":counts,"status":dict(collections.Counter(e["status"] for e in idx))}
json.dump({"meta":meta,"entries":idx},gzip.open("data/index.json.gz","wt",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
print(json.dumps(meta,ensure_ascii=False))
