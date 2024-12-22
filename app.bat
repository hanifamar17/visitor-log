@echo off

REM Navigate to the buku_kunjung directory
cd /d "E:\App-Development\buku_kunjung"

REM Run the main.py script using Python
start "" "python" "E:\App-Development\buku_kunjung\app.py"

REM Wait for main.py (adjust the timeout if necessary)
timeout /t 3

REM Open the browser to http://127.0.0.1:5555
start "" "http://127.0.0.1:5555"

