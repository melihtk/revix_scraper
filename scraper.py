from pathlib import Path
from typing import List, Dict
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utils import sanitize, motor_group, ensure_folder, save_text, download_images, ad_exists


class KleinanzeigenScraper:
    """Scrape all ads from a dealer page and store them locally."""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
        )
    }

    def __init__(self, base_url: str, output_dir: str = "Inserate") -> None:
        self.base_url = base_url.rstrip("/")
        self.output_dir = Path(output_dir)
        ensure_folder(self.output_dir)
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def scrape(self) -> List[Dict]:
        ads: List[Dict] = []
        page = 1
        while True:
            url = f"{self.base_url}?page={page}"
            resp = self.session.get(url)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.text, "html.parser")
            links = [a["href"] for a in soup.select('a[href*="/s-anzeige/"]')]
            if not links:
                break
            for link in links:
                ad_url = urljoin(self.base_url, link)
                data = self.scrape_ad(ad_url)
                if data:
                    ads.append(data)
                time.sleep(1)
            page += 1
        return ads

    def scrape_ad(self, url: str) -> Dict | None:
        resp = self.session.get(url)
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

        group = motor_group(title)
        if ad_exists(self.output_dir, group, title):
            # Skip already downloaded ads
            return None
        folder = self.output_dir / group / sanitize(title)
        ensure_folder(folder / "bilder")

        save_text(folder, "titel.txt", title)
        save_text(folder, "preis.txt", price)
        save_text(folder, "beschreibung.txt", description)
        image_count = download_images(self.session, self.base_url, folder / "bilder", image_urls)
        return {
            "title": title,
            "price": price,
            "description": description,
            "folder": str(folder),
            "images": image_count,
            "group": group,
        }
