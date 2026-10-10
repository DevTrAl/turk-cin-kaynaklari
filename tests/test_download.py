# İndirme modülünün internete çıkmayan kısımlarını dener.
from sqlmodel import Session, select

from pipeline.download import page_title, parse_header, save_section
from pipeline.models import Bolum, Eser, create_tables, get_engine

# Vikikaynak'tan gelen gerçek bilgi kutusunun kısaltılmış hali
SAMPLE_WIKITEXT = (
    "{{header2| title = [[../]]| section = '''卷一百九十四上'''<br>列傳第一百四十四上　突厥上"
    "| previous = [[../卷193|列女]]| next = [[../卷194下|突厥下]]| theme = 歷史"
    "| type = 史書| notes ={{textquality|25%}}}}\n○突厥之始…"
)

FAKE_FETCHED = {
    "text": "○突厥之始，啟民之前…",
    "heading": "列傳第一百四十四上　突厥上",
    "text_quality": "25%",
    "url": "https://zh.wikisource.org/wiki/舊唐書/卷194上",
}


def test_page_title():
    assert page_title("舊唐書", "194上") == "舊唐書/卷194上"


def test_parse_header():
    heading, quality = parse_header(SAMPLE_WIKITEXT)
    assert heading == "列傳第一百四十四上　突厥上"
    assert quality == "25%"


def test_parse_header_without_infobox():
    assert parse_header("sadece metin") == (None, None)


def test_save_section_twice_creates_one_row():
    engine = get_engine("sqlite://")
    create_tables(engine)
    with Session(engine) as session:
        save_section(session, "舊唐書", "194上", FAKE_FETCHED)
        save_section(session, "舊唐書", "194上", FAKE_FETCHED)

        assert len(session.exec(select(Eser)).all()) == 1
        bolumler = session.exec(select(Bolum)).all()
        assert len(bolumler) == 1
        assert bolumler[0].text_quality == "25%"
