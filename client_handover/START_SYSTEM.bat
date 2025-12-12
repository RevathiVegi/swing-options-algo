@echo off
cd /d %~dp0
echo Starting Swing Options simulation...
docker compose up -d
echo Done. To view logs: docker compose logs -f swing-sim
pause
