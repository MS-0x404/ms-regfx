import json


def json_report(result):
    with open("report.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
