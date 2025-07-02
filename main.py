import argparse
from pathlib import Path

from scraper import KleinanzeigenScraper
from export import export_csv, export_pdf
from utils import load_ads
from viewer import AdViewer


DEALER_URL = "https://www.kleinanzeigen.de/pro/euromotors2007---motorenhandel"


def run_scrape(output: str):
    scraper = KleinanzeigenScraper(DEALER_URL, output_dir=output)
    ads = scraper.scrape()
    if ads:
        export_csv(Path(output) / "daten.csv", ads)
        for ad in ads:
            export_pdf(Path(ad["folder"]) / "info.pdf", ad)


def run_view(output: str):
    ads = load_ads(output)
    if not ads:
        print("Keine Inserate gefunden. Bitte zuerst den Scraper ausführen.")
    else:
        AdViewer(ads)


def main():
    parser = argparse.ArgumentParser(description="Revix Inserate Builder")
    parser.add_argument("command", choices=["scrape", "view"], help="Aktion")
    parser.add_argument("--output", default="Inserate", help="Speicherort")
    args = parser.parse_args()

    if args.command == "scrape":
        run_scrape(args.output)
    elif args.command == "view":
        run_view(args.output)


if __name__ == "__main__":
    main()
