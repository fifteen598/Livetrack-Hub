@echo off

REM Run live_flask.py first
start /B python live_flask.py

REM Wait for 5 seconds to ensure Flask server is up
ping 127.0.0.1 -n 6 > nul

REM Run the GUI
python guiapp.py

pause
