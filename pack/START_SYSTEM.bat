@echo off
echo Starting Swing Options system...
docker compose -p swing-options up -d
if %ERRORLEVEL%==0 (
  echo System started.
) else (
  echo Failed to start system. Please check Docker Desktop is running.
)
pause
