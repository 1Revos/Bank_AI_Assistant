@echo off
chcp 65001 > nul
cd /d "%~dp0"

"venv\Scripts\python.exe" app.py

echo.
echo Приложение успешно закрыто.
pause
