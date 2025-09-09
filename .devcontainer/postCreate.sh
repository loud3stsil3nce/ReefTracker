#!/usr/bin/env bash
set -euo pipefail
sudo apt-get update -y
sudo apt-get install -y libpq-dev build-essential
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
# If you don't have requirements.txt yet, these cover your settings and apps:
pip install django dj-database-url "psycopg[binary]" crispy-bootstrap5 django-crispy-forms