@echo off
title NS Rail Live Pulse - Dashboard & Hourly Ingestion
echo =====================================================================
echo  🚆 Starting NS Rail Live Pulse (Live Stream + Hourly Scheduler)
echo  Open your browser at: http://127.0.0.1:8000
echo =====================================================================
python run.py --dashboard --interval 3600
pause
