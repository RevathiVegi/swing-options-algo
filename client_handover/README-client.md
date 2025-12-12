# Swing Options — Handover Package (Client)

## What this contains
- start.sh / stop.sh (Linux/macOS)
- START_SYSTEM.bat / STOP_SYSTEM.bat (Windows)
- docker-compose.yml
- Short maintenance & troubleshooting guide

## Quick start (non-technical)
Prerequisites on the machine:
1. Docker Desktop installed (Windows/macOS) or Docker + docker-compose on Linux.
2. The zipped package extracted to a folder, or open the folder via:
   `\\wsl$\Ubuntu\home\drrev\swing-options-algo\client_handover` (if using WSL).

To start:
- On **Windows**: double-click `START_SYSTEM.bat`.
- On **Linux/macOS**: open terminal in this folder and run `./start.sh`.

To view logs:
- `docker compose logs -f swing-sim`
- Or open `client_handover/logs/sim.log` (this file is created by the service).

To stop:
- Use `STOP_SYSTEM.bat` on Windows or `./stop.sh` on Linux/macOS.

## Where files live on this folder
- `out/` — simulation output & generated reports (back up regularly).
- `logs/` — application logs (`sim.log`).
- `tools/` — read-only helper scripts originally shipped.

## Updating the service (for your support team)
1. Pull new image or rebuild from repo.
2. `docker compose down`
3. Replace image / `docker compose up -d`

## Contact / Support
- Developer: <Put developer name> — email: <email@example.com>
