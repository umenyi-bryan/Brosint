import json, os
from jinja2 import Environment, FileSystemLoader

def save(data, out="report.json"):
    with open(out, "w") as f:
        json.dump(data, f, indent=2)
    # HTML version
    env = Environment(loader=FileSystemLoader("ui"))
    tpl = env.get_template("report.html")
    with open(out.replace(".json",".html"), "w") as h:
        h.write(tpl.render(result=data))
