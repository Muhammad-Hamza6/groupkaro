#!/usr/bin/env bash
set -euo pipefail

# --- Wait for Postgres ------------------------------------------------------
if [ -n "${DATABASE_URL:-}" ]; then
  echo "Waiting for Postgres..."
  python - << 'PY'
import os, sys, time
import psycopg

url = os.environ["DATABASE_URL"]
for attempt in range(60):
    try:
        psycopg.connect(url, connect_timeout=2).close()
        print("Postgres is up.")
        sys.exit(0)
    except Exception as exc:
        print(f"  attempt {attempt + 1}/60 — {exc.__class__.__name__}")
        time.sleep(1)
print("Postgres never became ready.", file=sys.stderr)
sys.exit(1)
PY
fi

# --- Apply migrations -------------------------------------------------------
echo "Applying migrations..."
python manage.py migrate --noinput

# --- Hand off to CMD --------------------------------------------------------
exec "$@"
