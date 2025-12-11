# Deliverables & Handover

This branch `release/client-ready` contains the production-ready code and Docker assets.

Files included:
- simulator.py, run_sim.py
- swing_options/ (package)
- requirements.txt, Dockerfile, docker-compose.yaml
- .env.example (.env must be created by client with credentials)
- README.md (deployment & run instructions)
- tests/

**Secrets:** Do NOT commit .env or actual API keys. Use .env (gitignored), Docker secrets, or Vault in production.

**How to run with Docker (example):**
1. Copy `.env.example` to `.env` and fill credentials.
2. docker build -t swing-options .
3. docker run --restart unless-stopped -d --name swing-options-container --env-file .env swing-options

