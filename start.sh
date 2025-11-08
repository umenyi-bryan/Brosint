#!/usr/bin/env bash
set -e
source venv/bin/activate
python check_deps.py
python webapp/app.py
