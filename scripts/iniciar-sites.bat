@echo off
cd /d "%~dp0"
python servidor-sites.py --host 127.0.0.1 --port 8766
pause
