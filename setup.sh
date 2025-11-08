#!/usr/bin/env bash
set -e
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Setup complete. Run demo:"
echo "source venv/bin/activate && python brosint.py --demo --email demo@example.com --user janedoe --file tests/sample.jpg --web"
