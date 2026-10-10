# Veritabanı tabloları. Her sınıf bir tablo, her alan bir sütun.
# Tablo adları CLAUDE.md'deki gibi Türkçe, alan adları İngilizce.
from datetime import datetime
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, create_engine

DEFAULT_DB_PATH = "data/turk_cin.db"


class Eser(SQLModel, table=True):
    __tablename__ = "eserler"

    id: Optional[int] = Field(default=None, primary_key=True)
    title_zh: str = Field(unique=True)  # 舊唐書
    title_tr: Optional[str] = None  # Eski Tang Tarihi
    wikisource_title: str  # Vikikaynak'taki sayfa adı


class Bolum(SQLModel, table=True):
    __tablename__ = "bolumler"
    # Aynı eserin aynı cildi iki kez kaydedilmesin
    __table_args__ = (UniqueConstraint("work_id", "volume"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    work_id: int = Field(foreign_key="eserler.id")
    volume: str  # 194上
    heading_zh: Optional[str] = None  # 列傳第一百四十四上 突厥上
    source_url: str
    text_zh: str  # Vikikaynak'tan indirilen ham metin
    downloaded_at: datetime


class Pasaj(SQLModel, table=True):
    __tablename__ = "pasajlar"

    id: Optional[int] = Field(default=None, primary_key=True)
    section_id: int = Field(foreign_key="bolumler.id")
    position: int  # bölüm içindeki sıra no
    text_zh: str
    text_with_placeholders: Optional[str] = None  # isimler {NAME_1} ile değiştirilmiş hali
    note: Optional[str] = None  # uzman notu


class Ceviri(SQLModel, table=True):
    __tablename__ = "ceviriler"

    id: Optional[int] = Field(default=None, primary_key=True)
    passage_id: int = Field(foreign_key="pasajlar.id")
    text_tr: str
    path: str  # "A", "B", "C" ya da "manual"
    model: Optional[str] = None  # elle yapılmışsa boş
    produced_by: Optional[str] = None
    produced_at: datetime
    verified: bool = False
    note: Optional[str] = None  # uzman notu


class Isim(SQLModel, table=True):
    __tablename__ = "isimler"

    id: Optional[int] = Field(default=None, primary_key=True)
    original: str  # 始畢
    pinyin: Optional[str] = None
    turkish: Optional[str] = None
    middle_chinese: Optional[str] = None
    source: Optional[str] = None  # bu okunuş nereden geldi
    uncertain: bool = True


class PasajIsmi(SQLModel, table=True):
    __tablename__ = "pasaj_isimleri"

    passage_id: int = Field(foreign_key="pasajlar.id", primary_key=True)
    name_id: int = Field(foreign_key="isimler.id", primary_key=True)
    placeholder: str  # NAME_1


class Terim(SQLModel, table=True):
    __tablename__ = "terimler"

    id: Optional[int] = Field(default=None, primary_key=True)
    original: str = Field(unique=True)  # 可汗
    turkish: Optional[str] = None  # kağan
    category: str  # "title", "tribe" ya da "culture"


class PasajTerimi(SQLModel, table=True):
    __tablename__ = "pasaj_terimleri"

    passage_id: int = Field(foreign_key="pasajlar.id", primary_key=True)
    term_id: int = Field(foreign_key="terimler.id", primary_key=True)
    placeholder: Optional[str] = None  # TITLE_1


class BoySayimi(SQLModel, table=True):
    __tablename__ = "boy_sayimlari"
    __table_args__ = (UniqueConstraint("section_id", "tribe"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    section_id: int = Field(foreign_key="bolumler.id")
    tribe: str  # 突厥
    count: int


def get_engine(db_url: str = f"sqlite:///{DEFAULT_DB_PATH}"):
    """Veritabanı bağlantısını oluşturur."""
    return create_engine(db_url)


def create_tables(engine) -> None:
    """Yukarıdaki bütün tabloları kurar. Zaten varsa dokunmaz."""
    SQLModel.metadata.create_all(engine)
