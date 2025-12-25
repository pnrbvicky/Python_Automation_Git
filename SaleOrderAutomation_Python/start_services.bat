@echo off
echo ===============================
echo Starting Dummy DMS Service
echo ===============================

start cmd /k python dummy_dms\run_dms.py

timeout /t 3

echo ===============================
echo Starting Dummy Merlin API
echo ===============================

start cmd /k python dummy_merlin_portal\dummy_merlin_api.py

echo ===============================
echo Services are running
echo ===============================

pause
