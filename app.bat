@echo off

REM Navigate to the visitor-log directory
cd /d "E:\App-Development\visitor-log"

REM Run the main.py script using Python
start "" "python" "E:\App-Development\visitor-log\app.py"

REM Wait for main.py (adjust the timeout if necessary)
timeout /t 2

REM Open the browser to http://127.0.0.1:5555
start "" "http://127.0.0.1:5555"

