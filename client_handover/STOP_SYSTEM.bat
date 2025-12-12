@echo off
cd /d %~dp0
echo Stopping Swing Options simulation...
docker compose down
echo Stopped.
pause
