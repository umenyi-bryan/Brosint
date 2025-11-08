#!/usr/bin/env python3
"""
BROsint dependency checker.
Run: python check_deps.py
It will read requirements.txt and pip-install missing packages into the active venv.
"""
import subprocess, sys, os

REQ_FILE = os.path.join(os.path.dirname(__file__), "requirements.txt")
if not os.path.exists(REQ_FILE):
    print("requirements.txt not found. Please create one.")
    sys.exit(1)

print("Checking Python dependencies...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQ_FILE])
    print("All dependencies installed/updated.")
except subprocess.CalledProcessError as e:
    print("pip failed:", e)
    sys.exit(2)
