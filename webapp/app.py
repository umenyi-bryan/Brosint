# webapp/app.py
import os, json
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

from core.searcher import search
from core.email_lookup import lookup as email_lookup
from core.phone_lookup import lookup as phone_lookup
from core.social_lookup import lookup as social_lookup
from core.whois_lookup import lookup as whois_lookup
from core.filemeta import extract as filemeta_extract
from core.hypothesis_engine import analyze as hypothesis_analyze
from utils.formatter import format_for_web

APP_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_FILE = os.path.join(os.path.dirname(APP_DIR), "report.json")

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    report = {}
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE) as f:
                report = json.load(f)
        except Exception:
            report = {}
    return render_template("index.html", report=report)

@app.route("/api/search", methods=["POST"])
def api_search():
    body = request.get_json() or {}
    q = body.get("query")
    if not q:
        return jsonify({"error":"missing query"}), 400
    hits = search(q, limit=15)
    return jsonify({"query": q, "results": hits})

@app.route("/api/upload", methods=["POST"])
def api_upload():
    # Accept file uploads (images). Save to webapp/uploads and return server path.
    if "file" not in request.files:
        return jsonify({"error":"no file"}), 400
    f = request.files["file"]
    updir = os.path.join(APP_DIR, "uploads")
    os.makedirs(updir, exist_ok=True)
    savepath = os.path.join(updir, f.filename)
    f.save(savepath)
    return jsonify({"path": savepath, "filename": f.filename})

@app.route("/api/scan", methods=["POST"])
def api_scan():
    body = request.get_json() or {}
    email = body.get("email")
    phone = body.get("phone")
    username = body.get("username")
    domain = body.get("domain")
    file_path = body.get("file")  # path previously returned by /api/upload

    results = {}
    if email:
        results["email"] = email_lookup(email)
        # whois domain automatically
        if "@" in email:
            dom = email.split("@",1)[1]
            results["whois"] = whois_lookup(dom)
    if phone:
        results["phone"] = phone_lookup(phone)
    if username:
        results["social"] = social_lookup(username)
    if domain:
        results["whois"] = whois_lookup(domain)
    if file_path:
        results["filemeta"] = filemeta_extract(file_path)

    results["hypothesis"] = hypothesis_analyze(results)

    structured = format_for_web(results)
    try:
        with open(REPORT_FILE, "w") as f:
            json.dump(structured, f, indent=2)
    except Exception:
        pass

    return jsonify(structured)

def start_web():
    print("\n🚀 BROsint — Neon dashboard at http://127.0.0.1:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=True)
