from fastapi import FastAPI, HTTPException
from typing import Dict
from datetime import datetime
import pandas as pd

mhd_db = {}

def mhd_eintragen():
    product_name = input(" Produktname: ").strip()
    mhd_str = input(" MHD (TT.MM.JJJJ): ").strip()
    batch_str = input(" Batchanzahl: ").strip()
    einheit = input(" Einheit z.B. (Stück, Liter, kg) : ").strip()

    if not product_name:
        print(" Produktname darf nicht leer sein")
        return

    if not mhd_str:
        print(" Mhd ist ein Pflichtfeld. Bitte gib ein Datum ein.")
        return

    if not einheit:
        print(" Bitte gib eine Einheit ein( Stück, kg, Liter).")

    try:
        batch = int(batch_str)
        if batch <=0:
            print("Die Batch-Anzahl muss eine positive Zahl sein")
            return
    except ValueError:
        print("Ungültige Batchanzahl")
        return

    if product_name in mhd_db:
        print(f" Produkt '{product_name}' existiert bereits.")
        return

    try:
        mhd_datum = datetime.strptime(mhd_str, "%d.%m.%Y")
    except ValueError:
        print("Ungültige Datumformat!! Bitte TT.MM.JJ.verwenden.")
        return

    if mhd_datum.date() < datetime.now().date():
        print("Das Datum liegt in der Vergangenheit zurück")
        return



    print("\n Vorschau der Eingabe")
    print(f"  - Produktname: {product_name}:")
    print(f"  • MHD:   {mhd_datum.strftime('%d.%m.%Y')}")
    print(f"  • Batch: {daten['einheit']}")

    bestätigen = input("\nMöchtest du diese Daten speichern? (j/n): ")
    if bestätigen != "j":
        print(" Eingabe verworfen.")
        return

    if product_name in mhd_db:
        print(f" Produkt '{product_name}' existiert bereits.")
        update = input(" Möchtest du es trotzdem aktualisieren? (j/n): ").lower().strip()
        if update != "j":
            print(" Aktualisierung abgebrochen")
            return

    mhd_db[product_name] = {"mhd":mhd_datum, "batch": batch, "einheit": einheit}
    print(f" MHD für '{product_name}' gespeichert oder aktualisiert: {mhd_datum.strftime('%d.%m.%Y')} (Batch: {batch} {einheit}) ")


while True:
    mhd_eintragen()
    weiter = input("\nNoch ein Produkt eintragen oder ändern? (j/n): ").lower()
    if weiter != "j":
        break


print("\n Alle eingetragenen Produkte")
for name, daten in mhd_db.items():
    print(f"  - Produktname: {name}:")
    print(f"  • MHD:   {daten['mhd'].strftime('%d.%m.%Y')}")
    print(f"  • Batch: {daten['batch']} {daten['einheit']}")