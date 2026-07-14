#!/usr/bin/env bash
set -euo pipefail

# Helper to run ingestion using docker-compose. Place your `waf.pdf` in `./data/waf.pdf`.

cd "$(dirname "$0")/.."

echo "Starting Postgres and running ingestion..."
docker compose -f docker/docker-compose.yml up --build --abort-on-container-exit ingest

echo "Ingestion finished." 
