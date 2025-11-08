from flask import Flask, render_template, jsonify, send_from_directory
import os, json
app = Flask(__name__, static_folder='static', template_folder='templates')
REPORT_JSON = os.path.join(os.path.dirname(__file__), '..', 'report.json')
@app.route('/')
def index():
    data = {}
    if os.path.exists(REPORT_JSON):
        with open(REPORT_JSON,'r') as f:
            data = json.load(f)
    return render_template('index.html', data=data)
@app.route('/api/report')
def api_report():
    if os.path.exists(REPORT_JSON):
        with open(REPORT_JSON,'r') as f:
            return jsonify(json.load(f))
    return jsonify({"error":"no report"}), 404
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
