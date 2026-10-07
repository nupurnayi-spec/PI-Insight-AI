import os
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY","pi-insight-demo-secret")
    DATABASE=os.path.join(BASE_DIR,"data","pi_insight.db")
