FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "simulator.py", "-c", "swing_options/config/production.yaml"]

# Ensure logs/out folder exist and add a non-root user
RUN mkdir -p /app/logs /app/out \
 && groupadd -r appuser || true \
 && useradd -r -g appuser -d /home/appuser -s /sbin/nologin appuser || true \
 && chown -R appuser:appuser /app

USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD [ -f "/app/logs/sim.log" ] || exit 1


