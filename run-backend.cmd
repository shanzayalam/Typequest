@echo off
setlocal
cd /d "C:\Users\HP\OneDrive\Documents\New project\backend"
call ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
