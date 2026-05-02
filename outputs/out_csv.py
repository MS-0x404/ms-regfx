import csv
import datetime

def csv_report(result):
    with open("report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Chiave", "Nome", "Dato"])
        def ricorsive(nodo):
            for v in nodo["valori"]:
                writer.writerow([nodo["chiave"], v["nome"], v["dato"]])
            for n in nodo.get("sottochiavi", []):
                ricorsive(n)
        ricorsive(result)
        
        
