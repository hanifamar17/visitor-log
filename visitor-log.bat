@echo off

REM Wait for main.py (adjust the timeout if necessary)
timeout /t 3

REM Open the browser to http://127.0.0.1:5555
start "" "http://127.0.0.1:5555"

