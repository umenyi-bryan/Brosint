#!/usr/bin/env python3
import argparse, json, os, sys, subprocess
from dotenv import load_dotenv
from utils.banner import animated_banner
from utils.colors import info, ok, warn, err
load_dotenv()

from core import email_lookup, phone_lookup, social_lookup, whois_lookup, meta_extract, ip_lookup, hypothesis_engine

def build_structured(query, results):
    obj = {"query": query, "results": results}
    obj["hypothesis"] = hypothesis_engine.generate_hypothesis(obj)
    return obj

def parse_args():
    p = argparse.ArgumentParser(prog="BROsint", description="BROsint — online-capable OSINT")
    p.add_argument("--email")
    p.add_argument("--phone")
    p.add_argument("--user")
    p.add_argument("--file")
    p.add_argument("--demo", action="store_true", help="Run offline demo (no external API calls)")
    p.add_argument("--online", action="store_true", help="Force online mode (equivalent to not using --demo)")
    p.add_argument("--web", action="store_true", help="Start web UI after run")
    p.add_argument("--json", help="output JSON filename (defaults to report.json)")
    return p.parse_args()

def main():
    args = parse_args()
    animated_banner()
    # online unless user explicitly requested --demo
    online = False if args.demo else True
    if not online:
        info("Running in demo (offline) mode")
    else:
        warn("Online mode: BROsint will perform external public lookups (respect privacy & laws)")

    query = {"email": args.email, "phone": args.phone, "user": args.user, "file": args.file}
    results = {"email_intel": None, "phone_intel": None, "social_intel": None, "whois": None, "meta": None, "ip_intel": None}

    if args.email:
        info(f"Collecting email intel for {args.email}")
        results["email_intel"] = email_lookup.lookup(args.email, online=online)
        if "@" in args.email:
            domain = args.email.split("@",1)[1]
            info(f"Collecting whois for {domain}")
            results["whois"] = whois_lookup.lookup(domain, online=online)

    if args.phone:
        info(f"Collecting phone intel for {args.phone}")
        results["phone_intel"] = phone_lookup.lookup(args.phone, online=online)

    if args.user:
        info(f"Collecting social intel for {args.user}")
        results["social_intel"] = social_lookup.lookup(args.user, online=online)

    if args.file:
        info(f"Extracting metadata from {args.file}")
        results["meta"] = meta_extract.extract(args.file, online=online)

    # try to find an IP candidate inside enrichment (simple)
    ip_candidate = None
    ei = results.get("email_intel") or {}
    if isinstance(ei, dict):
        for k in ("ip","origin_ip","remote_ip"):
            if ei.get(k):
                ip_candidate = ei.get(k); break

    if ip_candidate:
        info(f"Collecting IP intel for {ip_candidate}")
        results["ip_intel"] = ip_lookup.lookup(ip_candidate, online=online)

    structured = build_structured(query, results)
    out = args.json or "report.json"
    with open(out,"w") as fh:
        json.dump(structured, fh, indent=2)
    ok(f"Wrote structured report to {out}")

    if args.web:
        host = "127.0.0.1"; port = 5000
        print(f"\\n🚀 Serving BROsint dashboard on http://{host}:{port}\\n")
        print("[CTRL+C to stop server]\\n")
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__),'webapp','app.py')])

if __name__ == "__main__":
    main()
