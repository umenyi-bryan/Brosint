#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from webapp.app import start_web

def main():
    start_web()

if __name__ == "__main__":
    main()
