import os
import re
import csv
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Button, Text
from PIL import Image, ImageTk


class KleinanzeigenScraper:
    """Scrapes all ads from a dealer page and stores them locally."""

    def __init__(self, base_url, output_dir="Inserate"):
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def sanitize(self, text: str) -> str:
        text = text.strip().replace(' ', '_')
        text = re.sub(r'[\\/:*?"<>|]', '', text)
        return text

    def motor_group(self, title: str) -> str:
        match = re.search(r"(\d\.\d)", title)
        if match:
            return f"Motor_{match.group(1)}"
        return "Other"

    def scrape(self):
        ads = []
        page = 1
        while True:
            url = f"{self.base_url}?page={page}"
            resp = requests.get(url)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.text, "html.parser")
            listing_links = [a["href"] for a in soup.select('a[href*="/s-anzeige/"]')]
            if not listing_links:
                break
            for link in listing_links:
                ad_url = urljoin(self.base_url, link)
                data = self.scrape_ad(ad_url)
                if data:
                    ads.append(data)
            page += 1
        self.export_csv(ads)

    def scrape_ad(self, url):
        resp = requests.get(url)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        title_el = soup.select_one("h1")
        title = title_el.get_text(strip=True) if title_el else "N/A"
        price_el = soup.select_one(".ad-price")
        price = price_el.get_text(strip=True) if price_el else "N/A"
        desc_el = soup.select_one("#viewad-description-text")
        description = desc_el.get_text(strip=True) if desc_el else "N/A"
        image_urls = [img["src"] for img in soup.select('img[src*="kA_"]')]
        folder = self.prepare_folders(title)
        self.save_text(folder, "titel.txt", title)
        self.save_text(folder, "preis.txt", price)
        self.save_text(folder, "beschreibung.txt", description)
        self.download_images(folder / "bilder", image_urls)
        return {
            "title": title,
            "price": price,
            "description": description,
            "folder": str(folder),
            "images": len(image_urls),
        }

    def prepare_folders(self, title: str) -> Path:
        group = self.motor_group(title)
        group_dir = self.output_dir / group
        ad_dir = group_dir / self.sanitize(title)
        (ad_dir / "bilder").mkdir(parents=True, exist_ok=True)
        return ad_dir

    def save_text(self, folder: Path, name: str, text: str):
        with open(folder / name, "w", encoding="utf-8") as fh:
            fh.write(text)

    def download_images(self, folder: Path, urls):
        folder.mkdir(parents=True, exist_ok=True)
        for i, url in enumerate(urls, 1):
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    ext = os.path.splitext(url)[1].split("?")[0]
                    with open(folder / f"img{i}{ext}", "wb") as fh:
                        fh.write(r.content)
            except requests.RequestException:
                continue

    def export_csv(self, ads):
        csv_file = self.output_dir / "export.csv"
        fieldnames = ["title", "price", "folder", "images"]
        with open(csv_file, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for ad in ads:
                writer.writerow({k: ad.get(k, "") for k in fieldnames})


def load_ads(base_path="Inserate"):
    ads = []
    base = Path(base_path)
    for group in base.iterdir():
        if group.is_dir():
            for ad in group.iterdir():
                if (ad / "titel.txt").exists():
                    with open(ad / "titel.txt", "r", encoding="utf-8") as fh:
                        title = fh.read()
                    with open(ad / "preis.txt", "r", encoding="utf-8") as fh:
                        price = fh.read()
                    with open(ad / "beschreibung.txt", "r", encoding="utf-8") as fh:
                        desc = fh.read()
                    images = list((ad / "bilder").glob("*"))
                    ads.append({"title": title, "price": price, "desc": desc, "images": images})
    return ads


class AdViewer:
    def __init__(self, ads):
        self.ads = ads
        self.index = 0
        self.root = Tk()
        self.root.title("Inserate Viewer")
        self.title_label = Label(self.root, text="")
        self.title_label.pack()
        self.price_label = Label(self.root, text="")
        self.price_label.pack()
        self.text_box = Text(self.root, height=10, width=60)
        self.text_box.pack()
        self.image_label = Label(self.root)
        self.image_label.pack()
        self.next_btn = Button(self.root, text="Weiter", command=self.next_ad)
        self.next_btn.pack()
        self.show_ad()
        self.root.mainloop()

    def show_ad(self):
        ad = self.ads[self.index]
        self.title_label.config(text=ad["title"])
        self.price_label.config(text=ad["price"])
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", ad["desc"])
        img_path = ad["images"][0] if ad["images"] else None
        if img_path:
            img = Image.open(img_path)
            img.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
        else:
            self.image_label.config(image="")

    def next_ad(self):
        self.index = (self.index + 1) % len(self.ads)
        self.show_ad()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "scrape":
        scraper = KleinanzeigenScraper(
            "https://www.kleinanzeigen.de/pro/euromotors2007---motorenhandel"
        )
        scraper.scrape()
    else:
        ads = load_ads()
        if not ads:
            print("Keine Inserate gefunden. Führe zuerst den Scraper aus.")
        else:
            AdViewer(ads)
