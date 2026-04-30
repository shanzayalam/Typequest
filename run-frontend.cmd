@echo off
setlocal
set "PATH=C:\Users\HP\OneDrive\Documents\New project\tools\node-v24.14.1-win-x64;%PATH%"
cd /d "C:\Users\HP\OneDrive\Documents\New project\frontend"
call "C:\Users\HP\OneDrive\Documents\New project\tools\node-v24.14.1-win-x64\npm.cmd" run dev -- --host 127.0.0.1 --port 5173
