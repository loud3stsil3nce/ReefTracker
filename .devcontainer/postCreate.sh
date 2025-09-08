#!/usr/bin/env bash
set -eu

# System libs for psycopg / Pillow, etc.
sudo apt-get update -y
sudo apt-get install -y build-essential libpq-dev libjpeg-dev zlib1g-dev

# Python venv + deps
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip

# If your repo has requirements.txt, this will install them:
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# Handy: install common libs if missing
pip install --upgrade "psycopg[binary]" django-environ

# Create a dev .env if missing
if [ ! -f .env ]; then
  cp .env.example .env || true
fi

echo "✅ postCreate finished"
