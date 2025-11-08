import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, send_file
from colorama import Fore, Style, init
import json, subprocess, time, io, zipfile

# safe imports from core modules (these should be free-mode implementations)
from core import email_lookup, social_lookup, whois_lookup, ip_lookup, meta_extract, hypothesis_engine

init(autoreset=True)
ascii = f"""{Fore.CYAN}
██████╗ ██████╗  ██████╗ ███████╗██╗███╗   ██╗████████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
██████╔╝██████╔╝██║   ██║███████╗██║██╔██╗ ██║   ██║
██╔═══╝ ██╔══██╗██║   ██║╚════██║██║██║╚██╗██║   ██║
██║     ██║  ██║╚██████╔╝███████║██║██║ ╚████║   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝
{Style.RESET_ALL}
BROsint - Bright Responsible OSINT
Author: Chinedu | Version: 1.0.0
"""
print(ascii)
print(Fore.GREEN + "🚀 BROsint Dashboard running at http://127.0.0.1:5000\n")

app = Flask(__name__, template_folder="templates", static_folder="static")

# default report path (app will also keep last_report.json)
REPORT_OUT = os.path.join(os.path.dirname(__file__), "..", "report.json")
LAST_REPORT = os.path.join(app.static_folder, "last_report.json")

def build_structured_output(query, results):
    obj = {"query": query, "results": results}
    obj["hypothesis"] = hypothesis_engine.generate_hypothesis(obj)
    obj["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return obj

@app.route("/")
def home():
    # index will fetch last_report.json via JS
    return render_template("dashboard.html")

@app.route("/api/lookup", methods=["POST"])
def api_lookup():
    data = request.get_json() or request.form
    qtype = data.get("type")
    q = data.get("query")
    online = data.get("online", True)
    if not q or not qtype:
        return jsonify({"error":"missing query or type"}), 400

    results = {}
    try:
        if qtype == "email":
            results["email_intel"] = email_lookup.lookup(q, online=online)
            # domain whois
            if "@" in q:
                domain = q.split("@",1)[1]
                results["whois"] = whois_lookup.lookup(domain, online=online)
        elif qtype == "username":
            results["social_intel"] = social_lookup.lookup(q, online=online)
        elif qtype == "domain":
            results["whois"] = whois_lookup.lookup(q, online=online)
        elif qtype == "ip":
            results["ip_intel"] = ip_lookup.lookup(q, online=online)
        elif qtype == "file":
            results["meta"] = meta_extract.extract(q, online=online)
        else:
            return jsonify({"error":"invalid lookup type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    structured = build_structured_output({"type": qtype, "query": q}, results)

    # write report files
    with open(REPORT_OUT, "w") as f:
        json.dump(structured, f, indent=2)
    with open(LAST_REPORT, "w") as f:
        json.dump(structured, f, indent=2)

    return jsonify(structured)

@app.route("/api/report")
def api_report():
    if os.path.exists(LAST_REPORT):
        with open(LAST_REPORT, "r") as f:
            return jsonify(json.load(f))
    if os.path.exists(REPORT_OUT):
        with open(REPORT_OUT, "r") as f:
            return jsonify(json.load(f))
    return jsonify({"error":"no report"}), 404

@app.route("/api/export", methods=["GET"])
def api_export():
    # Create an in-memory ZIP containing the latest report and static assets (for release)
    if not os.path.exists(REPORT_OUT):
        return jsonify({"error":"no report to export"}), 404
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(REPORT_OUT, arcname=os.path.basename(REPORT_OUT))
        # include web assets for quick sharing
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        for root, _, files in os.walk(static_dir):
            for fn in files:
                path = os.path.join(root, fn)
                arc = os.path.relpath(path, os.path.dirname(__file__))
                z.write(path, arcname=arc)
    mem.seek(0)
    return send_file(mem, download_name="BROsint_report.zip", as_attachment=True)

if __name__ == "__main__":
    # start
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
