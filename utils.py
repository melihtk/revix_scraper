from pathlib import Path
import re
from urllib.parse import urljoin
import requests


def sanitize(text: str) -> str:
    """Sanitize strings for use as folder names."""
    cleaned = text.strip().replace(" ", "_")
    cleaned = re.sub(r'[\\/:*?"<>|]', '', cleaned)
    return cleaned


def motor_group(title: str) -> str:
    """Very naive extraction of the engine size from a title."""
    match = re.search(r"(\d\.\d)", title)
    if match:
        return f"Motor_{match.group(1)}"
    return "Other"


def ensure_folder(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_text(folder: Path, name: str, text: str) -> None:
    with open(folder / name, "w", encoding="utf-8") as fh:
        fh.write(text)


def download_images(session: requests.Session, base_url: str, folder: Path, urls) -> int:
    ensure_folder(folder)
    count = 0
    for i, url in enumerate(urls, 1):
        try:
            r = session.get(urljoin(base_url, url))
            if r.status_code == 200:
                ext = Path(url).suffix.split("?")[0] or ".jpg"
                with open(folder / f"img{i}{ext}", "wb") as fh:
                    fh.write(r.content)
                count += 1
        except requests.RequestException:
            continue
    return count


def ad_exists(base: Path, group: str, title: str) -> bool:
    return (base / group / sanitize(title)).exists()


def load_ads(base_path: str = "Inserate"):
    ads = []
    base = Path(base_path)
    if not base.exists():
        return ads
    for group in base.iterdir():
        if not group.is_dir():
            continue
        for ad in group.iterdir():
            if (ad / "titel.txt").exists():
                with open(ad / "titel.txt", "r", encoding="utf-8") as fh:
                    title = fh.read()
                with open(ad / "preis.txt", "r", encoding="utf-8") as fh:
                    price = fh.read()
                with open(ad / "beschreibung.txt", "r", encoding="utf-8") as fh:
                    desc = fh.read()
                images = list((ad / "bilder").glob("*"))
                ads.append({
                    "title": title,
                    "price": price,
                    "description": desc,
                    "images": images,
                    "path": ad
                })
    return ads
