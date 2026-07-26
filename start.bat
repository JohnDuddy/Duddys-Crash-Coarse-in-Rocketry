@echo off
cd /d C:\dev\NASA
powershell -NoProfile -Command "try { Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:5080/health' -TimeoutSec 1 | Out-Null; Start-Process 'http://127.0.0.1:5080/'; exit 0 } catch { exit 1 }"
if %errorlevel% equ 0 exit /b
start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:5080/'"
"C:\Users\drdud\AppData\Local\Programs\Python\Python313\python.exe" -B app.py
