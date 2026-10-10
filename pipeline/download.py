# Vikikaynak'tan tek bir cildi indirip veritabanına yazar.
#
# Kullanım (proje klasöründen):
#   .venv/Scripts/python -m pipeline.download 舊唐書 194上
import os
import re
import sys
from datetime import datetime, timezone

import requests
from sqlmodel import Session, select

from pipeline.models import DEFAULT_DB_PATH, Bolum, Eser, create_tables, get_engine

API_URL = "https://zh.wikisource.org/w/api.php"
# Wikimedia, istek atan programın kendini tanıtmasını istiyor
USER_AGENT = "turk-cin-kaynaklari/0.1 (research project)"


def page_title(work: str, volume: str) -> str:
    """("舊唐書", "194上") -> "舊唐書/卷194上" """
    return f"{work}/卷{volume}"


def parse_header(wikitext: str) -> tuple[str | None, str | None]:
    """Wiki işaretlemesinin başındaki bilgi kutusundan başlığı ve kalite işaretini çıkarır."""
    heading = None
    match = re.search(r"section\s*=\s*(.*?)\s*\|", wikitext)
    if match:
        # "'''卷一百九十四上'''<br>列傳第一百四十四上　突厥上" -> son parça
        heading = match.group(1).split("<br>")[-1].strip("' ")

    quality = None
    match = re.search(r"textquality\|(\d+%)", wikitext)
    if match:
        quality = match.group(1)

    return heading, quality


def fetch_section(work: str, volume: str) -> dict:
    """Tek cildin düz metnini, başlığını ve kalite işaretini Vikikaynak API'sinden getirir."""
    title = page_title(work, volume)
    params = {
        "action": "query",
        "titles": title,
        "prop": "extracts|revisions",  # tek istekte hem düz metin hem wiki işaretlemesi
        "explaintext": 1,
        "rvprop": "content",
        "rvslots": "main",
        "format": "json",
        "formatversion": 2,
    }
    response = requests.get(API_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()  # HTTP hatası varsa burada durur
    page = response.json()["query"]["pages"][0]

    if page.get("missing"):
        raise ValueError(f"Vikikaynak'ta böyle bir sayfa yok: {title}")

    wikitext = page["revisions"][0]["slots"]["main"]["content"]
    heading, quality = parse_header(wikitext)
    return {
        "text": page["extract"],
        "heading": heading,
        "text_quality": quality,
        "url": f"https://zh.wikisource.org/wiki/{title}",
    }


def save_section(session: Session, work: str, volume: str, fetched: dict) -> Bolum:
    """İndirilen cildi kaydeder. Eser ya da cilt zaten varsa yenisini eklemez."""
    eser = session.exec(select(Eser).where(Eser.title_zh == work)).first()
    if eser is None:
        eser = Eser(title_zh=work, wikisource_title=work)
        session.add(eser)
        session.commit()

    bolum = session.exec(
        select(Bolum).where(Bolum.work_id == eser.id, Bolum.volume == volume)
    ).first()
    if bolum is not None:
        return bolum

    bolum = Bolum(
        work_id=eser.id,
        volume=volume,
        heading_zh=fetched["heading"],
        source_url=fetched["url"],
        text_zh=fetched["text"],
        text_quality=fetched["text_quality"],
        downloaded_at=datetime.now(timezone.utc),
    )
    session.add(bolum)
    session.commit()
    return bolum


if __name__ == "__main__":
    # Windows terminalinde Çince karakterler bozuk görünmesin
    sys.stdout.reconfigure(encoding="utf-8")
    work, volume = sys.argv[1], sys.argv[2]

    os.makedirs(os.path.dirname(DEFAULT_DB_PATH), exist_ok=True)
    engine = get_engine()
    create_tables(engine)

    fetched = fetch_section(work, volume)
    with Session(engine) as session:
        bolum = save_section(session, work, volume, fetched)
        print(f"Kaydedildi: {work} {bolum.volume} | {bolum.heading_zh} | "
              f"{len(bolum.text_zh)} karakter | kalite: {bolum.text_quality}")
