import sqlite3,os,random,math
from datetime import datetime,timedelta
from config import Config
def connection():
 os.makedirs(os.path.dirname(Config.DATABASE),exist_ok=True);c=sqlite3.connect(Config.DATABASE);c.row_factory=sqlite3.Row;return c
def init_db():
 c=connection();c.executescript('''CREATE TABLE IF NOT EXISTS assets(id INTEGER PRIMARY KEY,name TEXT UNIQUE,asset_type TEXT,area TEXT);CREATE TABLE IF NOT EXISTS tags(id INTEGER PRIMARY KEY,name TEXT UNIQUE,asset_id INTEGER,attribute TEXT,unit TEXT,description TEXT);CREATE TABLE IF NOT EXISTS readings(id INTEGER PRIMARY KEY,tag_id INTEGER,timestamp TEXT,value REAL);CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,asset TEXT,event_type TEXT,severity TEXT,start_time TEXT,message TEXT,status TEXT);''')
 if c.execute("SELECT COUNT(*) FROM assets").fetchone()[0]==0:seed(c)
 c.commit();c.close()
def seed(c):
 assets=[("GEN-01","Generator","Generation"),("TRF-01","Transformer","Electrical"),("PMP-01","Cooling Pump","Cooling"),("MTR-01","Motor","Auxiliary"),("BUS-01","Busbar","Switchyard"),("CVT-01","CVT","Switchyard")]
 for x in assets:c.execute("INSERT INTO assets(name,asset_type,area) VALUES(?,?,?)",x)
 defs=[("GEN-01","Power","MW"),("GEN-01","Temperature","C"),("GEN-01","Vibration","mm/s"),("TRF-01","Temperature","C"),("TRF-01","Load","%"),("TRF-01","OilPressure","bar"),("PMP-01","Flow","m3/h"),("PMP-01","Vibration","mm/s"),("MTR-01","Current","A"),("MTR-01","Temperature","C"),("BUS-01","Voltage","kV"),("CVT-01","Temperature","C")]
 for asset,attr,unit in defs:
  aid=c.execute("SELECT id FROM assets WHERE name=?",(asset,)).fetchone()[0];c.execute("INSERT INTO tags(name,asset_id,attribute,unit,description) VALUES(?,?,?,?,?)",(f"{asset}.{attr}",aid,attr,unit,f"{attr} measurement"))
 now=datetime.now()
 for t in c.execute("SELECT id,name FROM tags").fetchall():
  for i in range(500):
   x=i/18;name=t["name"];v=50+5*math.sin(x)+random.gauss(0,1)
   if name.endswith("Power"):v=420+18*math.sin(x)+random.gauss(0,4)
   elif "Temperature" in name:v=65+8*math.sin(x/2)+random.gauss(0,1.5)
   elif "Vibration" in name:v=2.2+.5*math.sin(x)+random.gauss(0,.15)
   elif "Load" in name:v=68+10*math.sin(x)+random.gauss(0,2)
   elif "Voltage" in name:v=220+2*math.sin(x)+random.gauss(0,.4)
   elif "Current" in name:v=90+12*math.sin(x)+random.gauss(0,2)
   elif "Flow" in name:v=150+20*math.sin(x)+random.gauss(0,3)
   if 440<=i<=452 and ("Temperature" in name or "Vibration" in name):v*=1.35
   c.execute("INSERT INTO readings(tag_id,timestamp,value) VALUES(?,?,?)",(t["id"],(now-timedelta(minutes=(499-i)*10)).isoformat(timespec="minutes"),round(v,3)))
 for e in [("TRF-01","High Temperature","High","Transformer temperature exceeded expected band","Open"),("GEN-01","Vibration Spike","Medium","Synthetic vibration anomaly detected","Investigating"),("PMP-01","Low Flow","Medium","Cooling flow below expected band","Closed")]:c.execute("INSERT INTO events(asset,event_type,severity,start_time,message,status) VALUES(?,?,?,?,?,?)",(e[0],e[1],e[2],now.isoformat(timespec="minutes"),e[3],e[4]))
def get_assets():
 c=connection();r=[dict(x) for x in c.execute("SELECT * FROM assets ORDER BY name")];c.close();return r
def get_tags():
 c=connection();r=[dict(x) for x in c.execute("SELECT t.name,a.name asset,t.attribute,t.unit,t.description FROM tags t JOIN assets a ON a.id=t.asset_id ORDER BY a.name,t.attribute")];c.close();return r
def get_tag(name):
 c=connection();r=c.execute("SELECT * FROM tags WHERE name=?",(name,)).fetchone();c.close();return dict(r) if r else None
def get_readings(tid):
 c=connection();r=[dict(x) for x in c.execute("SELECT timestamp,value FROM readings WHERE tag_id=? ORDER BY timestamp",(tid,))];c.close();return r
def get_events_db():
 c=connection();r=[dict(x) for x in c.execute("SELECT * FROM events ORDER BY id DESC")];c.close();return r
