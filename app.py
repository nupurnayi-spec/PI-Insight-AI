from flask import Flask,render_template,jsonify,request,redirect,url_for,session,flash,Response
from config import Config
from services.database import init_db,get_tags
from services.analytics import get_dashboard_metrics,get_asset_health,get_tag_series,get_events,run_anomaly_scan
import csv,io
app=Flask(__name__); app.config.from_object(Config); init_db()
@app.route("/")
def dashboard():
    if "user" not in session:return redirect(url_for("login"))
    return render_template("dashboard.html",metrics=get_dashboard_metrics())
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form.get("username")=="admin" and request.form.get("password")=="admin123":session["user"]="admin";return redirect(url_for("dashboard"))
        flash("Invalid demo credentials.")
    return render_template("login.html")
@app.route("/logout")
def logout():session.clear();return redirect(url_for("login"))
def auth():return "user" in session
@app.route("/assets")
def assets():return redirect(url_for("login")) if not auth() else render_template("assets.html",assets=get_asset_health())
@app.route("/trends")
def trends():return redirect(url_for("login")) if not auth() else render_template("trends.html")
@app.route("/events")
def events():return redirect(url_for("login")) if not auth() else render_template("events.html",events=get_events())
@app.route("/ai-anomalies")
def ai_anomalies():return redirect(url_for("login")) if not auth() else render_template("ai_anomalies.html",results=run_anomaly_scan())
@app.route("/api/overview")
def api_overview():return jsonify(get_dashboard_metrics())
@app.route("/api/tags")
def api_tags():return jsonify(get_tags())
@app.route("/api/series/<path:tag_name>")
def api_series(tag_name):return jsonify(get_tag_series(tag_name))
@app.route("/api/anomalies")
def api_anomalies():return jsonify(run_anomaly_scan())
@app.route("/reports/assets.csv")
def asset_report():
    out=io.StringIO();rows=get_asset_health();w=csv.DictWriter(out,fieldnames=["asset","type","health","risk","status"]);w.writeheader();w.writerows(rows)
    return Response(out.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment;filename=pi_asset_health.csv"})
if __name__=="__main__":app.run(debug=True)
