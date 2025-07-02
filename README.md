# Revix Inserate Builder

Dieses Projekt lädt alle Inserate eines Kleinanzeigen-Händlers herunter und speichert sie lokal.
Mit der integrierten Tkinter-Oberfläche lassen sich die Anzeigen bequem durchblättern und auswerten.
Die Daten bleiben komplett auf dem eigenen Rechner.

## Voraussetzungen
- Python 3
- Pakete: `requests`, `beautifulsoup4`, `pillow`
- Optional für PDF-Export: `reportlab`

Alle Abhängigkeiten können über die beiliegende `requirements.txt` installiert werden:
```bash
pip install -r requirements.txt
```

## Nutzung
### 1. Inserate herunterladen
```bash
python main.py scrape --output Inserate
```
Die Daten werden strukturiert im gewählten Ordner abgelegt. Zusätzlich entsteht eine `daten.csv` mit den wichtigsten Angaben.

### 2. Inserate ansehen
```bash
python main.py view --output Inserate
```
Ein kleines Fenster zeigt Titel, Preis, Beschreibung und das erste Bild an. Über "Weiter" und "Zurück" kann man blättern; eine Suchbox filtert die Anzeigen.

Das Skript nutzt einen Browser-ähnlichen User-Agent und pausiert kurz zwischen den Anfragen, um die Quelle nicht zu überlasten.
