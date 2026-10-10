# İlerleme

Şu anki aşama: **1 - 24 hanedan tarihinde boy adlarını tara**

Aşama 0 tamamlandı (2026-10-10): demo JSON şablonu olduğu gibi kabul edildi.

## Yapılanlar

- 2026-10-09: Proje iskeleti kuruldu (git, sanal ortam, klasörler, pytest).
- 2026-10-10: 舊唐書 194 başlığı teyit edildi: 卷194上 = 列傳第一百四十四上 突厥上.
  Bölüm iki parça: 194上 (突厥上) ve 194下 (突厥下).
- 2026-10-10: Demo pasajı seçildi: 卷194上'ün ilk cümleleri (始畢可汗咄吉者…).
  Elle hazırlanmış örnek çıktı: `demo/pasaj_194a_001.json`.

- 2026-10-10: SQLModel ile 9 tablo kuruldu (`pipeline/models.py`, veritabanı `data/turk_cin.db`).
- 2026-10-10: `pipeline/download.py`: tek cildi Vikikaynak API'sinden indirip kaydediyor.
  舊唐書 194上 indirildi (13.358 karakter, kalite %25).
- 2026-10-10: Depo GitHub'a gönderildi: github.com/DevTrAl/turk-cin-kaynaklari (herkese açık).

## Aşama 4 için notlar

- Terimlerin yazım varyantları var: 舊唐書 194上'de 特勤 yerine 特勒, bir yerde 設 yerine 殺
  geçiyor. Terim listesine varyantlar da eklenmeli (uzmana sorulacak).
- Vikikaynak metinlerinin kalite işareti var (194上: %25, düzeltilmemiş). `bolumler.text_quality`.

## Sıradaki

- Boy listesi dosyası (`pipeline/boylar.txt`, geniş liste) ve sayım fonksiyonu.
- Sonra: 舊唐書'nin 200 cildini indir ve say.
