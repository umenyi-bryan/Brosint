import argparse, json
from utils.banner import show_banner
from collectors import email, phone, username
from correlator.core import correlate
from utils import report
from flask import Flask, send_file
import threading

__author__ = "Chinedu"
__version__ = "1.0.0"
__license__ = "MIT"
__description__ = "BROsint - Advanced OSINT Tool for identity hypothesis generation"
app = Flask(__name__)

@app.route("/")
def home():
    return send_file("report.html")


def run_web():
    app.run(host="0.0.0.0", port=8080)

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="BROsint - Advanced OSINT Identity Correlator (demo)")
    parser.add_argument("--email", help="Email address")
    parser.add_argument("--phone", help="Phone number")
    parser.add_argument("--username", help="Username")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--web", action="store_true", help="Launch web UI")
    args = parser.parse_args()

    evidence = []
    if args.demo:
        evidence += email.collect("demo@example.com")
        evidence += phone.collect("+2348012345678")
        evidence += username.collect("janedoe")
    else:
        if args.email: evidence += email.collect(args.email)
        if args.phone: evidence += phone.collect(args.phone)
        if args.username: evidence += username.collect(args.username)

    data = correlate(evidence)
    report.save(data)
    print("\n[+] Report saved as report.json and report.html\n")

    if args.web:
        print("Starting web server at http://localhost:8080 ...")
        threading.Thread(target=run_web, daemon=True).start()
        import time; time.sleep(10000)

if __name__ == "__main__":
    main()
