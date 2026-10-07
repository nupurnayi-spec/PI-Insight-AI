# PI-Insight AI

Portfolio-ready industrial time-series intelligence platform inspired by AVEVA PI System concepts.

## Purpose
Demonstrate PI-style Tags, AF Elements/Attributes, trends, Event Frames-style events, KPI/AHI-style asset health and AI anomaly detection using synthetic data.

**Public-GitHub safe:** no company/client PI Server, credentials, tag names or confidential data.

## Run on Windows
```powershell
cd PI_Insight_AI
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000
Demo login: `admin` / `admin123`

## PI concept mapping
PI Tag -> database tag
PI AF Database -> asset hierarchy
AF Element -> industrial asset
AF Attribute -> measurement definition
PI Analysis -> analytics service
Event Frame -> event records
PI Vision -> trend/dashboard UI
AHI -> simplified asset-health score

This is a learning/portfolio simulation, not an official AVEVA PI implementation.
