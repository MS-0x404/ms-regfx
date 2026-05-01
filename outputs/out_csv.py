import csv
import datetime

def csv_report(result):
    with open("report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Chiave", "Nome", "Dato"])
        for v in result["valori"]:
            writer.writerow([result["chiave"], v["nome"], v["dato"]])
        
