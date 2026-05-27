@echo off
set "PROJECT_DIR=%~dp0"

echo Starting Brain DnD Bot...

start "Brain DnD" /D "%PROJECT_DIR%" cmd /k ollama run ministral-3:14b-cloud
start "Bot DnD" /D "%PROJECT_DIR%" cmd /k "venv\Scripts\activate && python main.py"

echo INFO ready!
exit /b