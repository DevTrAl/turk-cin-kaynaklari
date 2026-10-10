# Tabloların kurulup kayıt alabildiğini, bellekteki geçici bir veritabanında dener.
from datetime import datetime, timezone

from sqlalchemy import inspect
from sqlmodel import Session, select

from pipeline.models import Bolum, Eser, create_tables, get_engine


def make_engine():
    # "sqlite://" = dosya yok, sadece bellekte; test bitince kaybolur
    engine = get_engine("sqlite://")
    create_tables(engine)
    return engine


def test_all_tables_created():
    engine = make_engine()
    tables = set(inspect(engine).get_table_names())
    assert tables == {
        "eserler", "bolumler", "pasajlar", "ceviriler", "isimler",
        "pasaj_isimleri", "terimler", "pasaj_terimleri", "boy_sayimlari",
    }


def test_save_and_read_section():
    engine = make_engine()
    with Session(engine) as session:
        work = Eser(title_zh="舊唐書", title_tr="Eski Tang Tarihi", wikisource_title="舊唐書")
        session.add(work)
        session.commit()

        section = Bolum(
            work_id=work.id,
            volume="194上",
            heading_zh="列傳第一百四十四上 突厥上",
            source_url="https://zh.wikisource.org/wiki/舊唐書/卷194上",
            text_zh="突厥之始…",
            downloaded_at=datetime(2026, 10, 10, tzinfo=timezone.utc),
        )
        session.add(section)
        session.commit()

        found = session.exec(select(Bolum).where(Bolum.volume == "194上")).one()
        assert found.heading_zh == "列傳第一百四十四上 突厥上"
        assert found.work_id == work.id
