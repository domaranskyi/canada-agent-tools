import json,os,time,base64,urllib.request as u
T=os.environ["APIFY_TOKEN"]
def api(m,p,b=None):
    r=u.Request("https://api.apify.com/v2"+p,method=m,data=json.dumps(b).encode() if b is not None else None,headers={"Authorization":"Bearer "+T,"Content-Type":"application/json"})
    try: return json.load(u.urlopen(r))
    except Exception as e: print("ERR",m,p,getattr(e,'read',lambda:b'')()[:800].decode()); return None
files=["Dockerfile","requirements.txt","README.md","LICENSES.md",".dockerignore","src/__init__.py","src/__main__.py","src/main.py"]+[".actor/"+f for f in os.listdir(".actor")]
sf=[{"name":f,"format":"TEXT","content":open(f).read()} for f in files]
sf.append({"name":"data/index.json.gz","format":"BASE64","content":base64.b64encode(open("data/index.json.gz","rb").read()).decode()})
ver={"versionNumber":"0.1","sourceType":"SOURCE_FILES","buildTag":"latest","sourceFiles":sf}
if os.path.exists(".actor_id"): A=open(".actor_id").read(); api("PUT",f"/acts/{A}/versions/0.1",ver)
else:
    a=api("POST","/acts",{"name":"ukraine-sanctions-screener-nsdc","title":"Ukraine Sanctions Screener (NSDC)","isPublic":False,
      "categories":["BUSINESS","AI"],"seoTitle":"Ukraine Sanctions Screener – NSDC State Sanctions Register",
      "defaultRunOptions":{"build":"latest","timeoutSecs":300,"memoryMbytes":512},"versions":[ver]})["data"]
    A=a["id"]; open(".actor_id","w").write(A)
b=api("POST",f"/acts/{A}/builds?version=0.1&waitForFinish=60")["data"]
while b["status"] in("READY","RUNNING"): time.sleep(5); b=api("GET",f"/actor-builds/{b['id']}")["data"]
print(A,b["id"],b["status"])
