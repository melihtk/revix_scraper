# Revix Inserate Builder

Dieses Werkzeug ruft alle Inserate eines Kleinanzeigen-Händlers ab und speichert die Inhalte lokal. Anschließend können die gespeicherten Inserate in einer kleinen Tkinter-GUI durchgeblättert werden.

## Voraussetzungen
- Python 3
- Pakete: `requests`, `beautifulsoup4`, `pillow`

## Nutzung

1. **Scraping ausführen**
   ```bash
   python revix_scraper.py scrape
   ```
   Die Inserate werden im Ordner `Inserate/` abgelegt. Zusätzlich wird eine `export.csv` erzeugt.

2. **GUI starten**
   ```bash
   python revix_scraper.py
   ```
   Es öffnet sich ein Fenster, in dem jeweils Titel, Preis, Beschreibung und das erste Bild angezeigt werden. Mit dem Button "Weiter" wird das nächste Inserat geladen.
