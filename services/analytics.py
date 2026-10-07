import pandas as pd,numpy as np
from sklearn.ensemble import IsolationForest
from .database import connection,get_assets,get_tag,get_readings,get_events_db
def get_tag_series(name):
 t=get_tag(name);return get_readings(t["id"]) if t else []
def latest(name):
 s=get_tag_series(name);return s[-1]["value"] if s else 0
def calculate_health(asset):
 limits={"GEN-01":[("GEN-01.Temperature",90),("GEN-01.Vibration",6)],"TRF-01":[("TRF-01.Temperature",95),("TRF-01.Load",100)],"PMP-01":[("PMP-01.Vibration",6),("PMP-01.Flow",200)],"MTR-01":[("MTR-01.Temperature",100),("MTR-01.Current",150)],"BUS-01":[("BUS-01.Voltage",240)],"CVT-01":[("CVT-01.Temperature",100)]}
 vals=[min(100,max(0,latest(t)/lim*100)) for t,lim in limits.get(asset,[])];stress=np.mean(vals) if vals else 20;return round(max(0,100-stress*.35),1)
def get_asset_health():
 out=[]
 for a in get_assets():
  h=calculate_health(a["name"]);risk="Low" if h>=80 else ("Medium" if h>=65 else "High");status="Healthy" if h>=80 else ("Watch" if h>=65 else "Attention");out.append({"asset":a["name"],"type":a["asset_type"],"health":h,"risk":risk,"status":status})
 return out
def run_anomaly_scan():
 out=[];c=connection();names=[r["name"] for r in c.execute("SELECT name FROM tags")];c.close()
 for name in names:
  s=get_tag_series(name)
  if len(s)<30:continue
  d=pd.DataFrame(s);d["mean"]=d.value.rolling(12).mean();d["std"]=d.value.rolling(12).std().fillna(0);d["delta"]=d.value.diff().fillna(0);X=d[["value","mean","std","delta"]].fillna(0);labels=IsolationForest(contamination=.03,random_state=42).fit_predict(X)
  for _,r in d[labels==-1].tail(4).iterrows():out.append({"tag":name,"timestamp":r.timestamp,"value":round(float(r.value),2),"signal":"Anomaly","reason":"Multivariate time-series deviation"})
 return out[-20:]
def get_events():return get_events_db()
def get_dashboard_metrics():
 a=get_asset_health();e=get_events();n=run_anomaly_scan();return {"asset_count":len(a),"average_health":round(float(np.mean([x["health"] for x in a])),1),"high_risk_assets":sum(x["risk"]=="High" for x in a),"open_events":sum(x["status"]!="Closed" for x in e),"ai_anomalies":len(n),"assets":a}
