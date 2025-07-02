from pathlib import Path
import csv
from typing import List, Dict

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
    from reportlab.lib.styles import getSampleStyleSheet
except Exception:  # pragma: no cover - optional dependency
    SimpleDocTemplate = None


def export_csv(csv_path: Path, ads: List[Dict]) -> None:
    fieldnames = ["title", "price", "folder", "images", "group"]
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for ad in ads:
            writer.writerow({k: ad.get(k, "") for k in fieldnames})


def export_pdf(pdf_path: Path, ad: Dict) -> None:
    if SimpleDocTemplate is None:
        return
    doc = SimpleDocTemplate(str(pdf_path))
    styles = getSampleStyleSheet()
    elems = [
        Paragraph(ad["title"], styles["Heading1"]),
        Paragraph(ad.get("price", ""), styles["Normal"]),
        Paragraph(ad.get("description", ""), styles["Normal"]),
    ]
    for img in ad.get("images", []):
        elems.append(Image(str(img), width=300, height=200))
    doc.build(elems)
