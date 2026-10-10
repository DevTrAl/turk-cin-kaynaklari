# Çin Kaynaklarında Türkler

Çin hanedan tarihlerinde Türk boylarıyla ilgili pasajları bulan, Türkçeye çeviren
ve orijinal metin ile kaynak bilgisiyle yan yana sunan açık kaynaklı araç.

Hedef kitle Çince bilmeyen tarihçi ve öğrenci. Araç uzmanın yerine geçmez, onu
doğru cilde ve bölüme götürür. Atıf her zaman orijinal metne yapılır.

## Benimle nasıl çalışacaksın

Bu bölüm en önemlisi. Ben projenin sahibiyim ama şu an paslıyım:

- Geçmişim C#/.NET ve biraz Java. En son 2023'te düzenli kod yazdım.
- Python'da yeniyim. Git'i, sanal ortamları, API'leri az biliyorum.
- Bir yapay zeka ile bu şekilde kod yazmak benim için yeni.

Bu yüzden:

1. **Kod yazmadan önce ne yapacağını 3-5 cümleyle anlat** ve onayımı bekle.
   Büyük adımlarda önce plan çıkar.
2. **Küçük adımlarla ilerle.** Bir seferde tek dosya ya da tek özellik. Çalıştığını
   görmeden sonrakine geçme.
3. **Yazdığın her yeni şeyi kısaca açıkla.** Python'a özgü bir yapı kullanırsan
   C#'taki karşılığını söyle (ör. "list comprehension, LINQ'teki Select gibi").
4. **Benim çalıştırmam gereken komutları açıkça yaz** ve ne yaptığını tek satırda
   söyle. Kurulum adımlarını atlama.
5. **Her çalışan adımdan sonra commit öner**, mesajını da yaz.
6. **Her oturumun sonunda** ne yaptığımızı 3 maddede özetle ve sıradaki adımı öner.
7. **Anlamadığımı fark edersen dur ve sor.** Sadece "tamam" diyorsam arada bir
   yazdığın kodun ne yaptığını bana sordur.
8. **Yanlış bir şey istersem itiraz et.** Daha basit bir yol varsa söyle.
9. Benim yerime karar verme: kütüphane, mimari ya da kapsam değişikliği gibi
   seçimlerde seçenekleri ve önerini sun, kararı bana bırak.
10. Gereksiz soyutlama, erken optimizasyon ve istemediğim özellik ekleme.

Benimle Türkçe konuş. Kod, değişken adları ve commit mesajları İngilizce olsun,
yorum satırları Türkçe olabilir.

## Çeviri yolu

Ana hat B yolu, tamamı yerel ekran kartında (RTX 4070, 12 GB VRAM), sıfır maliyetle:

    Klasik Çince -> modern Çince (Xunzi) -> Türkçe (açık genel model)

- A yolu (klasik Çince -> Türkçe, doğrudan) ve C yolu (İngilizce üzerinden)
  bütçe gelince kontrol için eklenecek. Üç yol ayrışırsa pasaj "belirsiz" olur.
- Modeller Ollama ya da LM Studio üzerinden yerel API gibi çağrılır. Kod modele
  bağımlı yazılmaz, model adı ayardan değişir.
- Fine-tuning ilk sürümde yok.

## Değişmez kurallar

Bunlar projenin akademik olarak kabul görmesi için şart. Hiçbirini esnetme.

1. **İsimleri çeviriden koru.** Özel adlar ve unvanlar orijinal klasik metinden
   çıkarılır, çeviri adımlarına girmeden önce yer tutucuyla değiştirilir, sonra
   isim sözlüğünden Türkçe karşılığı yerine konur. Model isim çevirmez.
2. **Orijinali her zaman sakla ve göster.** Her pasajda klasik Çince metin, eser,
   cilt ve bölüm numarası bulunur. İsimlerin yanında orijinal karakterler durur:
   Kutlug (骨咄祿).
3. **Eski okunuşu ekle.** İsimlere Orta Çince okunuş açık akademik tablodan eklenir.
4. **Belirsizliği gizleme.** Alternatif okuma varsa ikisi de saklanır. Modelin emin
   olmadığı yerler işaretlenir.
5. **Terim takibi.** Unvanlar (可汗 kağan, 特勤 tigin, 設 şad, 葉護 yabgu), boy adları
   (突厥, 鐵勒, 回紇, 匈奴, 丁零, 高車) ve kültür terimleri etiketlenir.
6. **Taraf tutma.** Hangi boyun "Türk" sayılacağı tartışmalı. Geniş listeyle tara,
   kararı okuyana bırak.
7. **Her çeviride** hangi modelin hangi tarihte ürettiği kayıtlı olur.
8. **Telif.** Yayımlanmış Türkçe çeviriler ve telifli modern Çince baskılar depoya
   ya da siteye konmaz. Yalnızca yerelde ölçüm için kullanılır (.gitignore).
9. **Sır yok.** API anahtarı ve benzerleri yalnızca `.env` dosyasında, asla commit'te.

## Mimari

İki ayrı program:

- **Veri hattı (script):** indir -> böl -> bul -> isimleri çıkar -> sadeleştir ->
  çevir -> etiketle -> veritabanına yaz. Ben elle çalıştırırım.
- **Site:** FastAPI backend + React frontend. Yalnızca veritabanından okur,
  çeviri modeline hiç dokunmaz.

Araçlar: Python 3, `requests` (Vikikaynak API), OpenCC, SQLite + FTS5,
SQLModel ya da SQLAlchemy, FastAPI, React, pytest.

Tablolar: `eserler`, `bolumler`, `pasajlar`, `ceviriler`, `isimler`,
`pasaj_isimleri`, `terimler`. Çeviriler ayrı tabloda: aynı pasaj için birden
fazla modelin çevirisi ve ileride uzman düzeltmesi yan yana durur.

Metin kaynağı: Çince Vikikaynak (zh.wikisource.org).

## Aşamalar

Sırayla git, bir aşama bitmeden sonrakine başlama. Hangi aşamada olduğumuzu
`ILERLEME.md` dosyasında tut.

0. Tek pasajı elle hazırla, çıktı formatına karar ver (demo sayfası)
1. 24 hanedan tarihinde boy adlarını tara: "hangi eserde, hangi ciltte, kaç kez"
   (model gerektirmez)
2. Tek bölümü (舊唐書 194, Türkler) B yoluyla otomatik işle
3. 15-20 pasajı yayımlanmış Türkçe çeviriyle karşılaştır, hata türlerini kaydet
4. İsim sözlüğü, eski okunuş, terim etiketleri
5. FastAPI + React site
6. Diğer kaynaklara genişlet

İlk hedef yalnızca 舊唐書 194. Kaynak listesindeki bölüm numaraları teyit
edilmedi: bir bölümü indirmeden önce başlığını kontrol et, yanlışsa bana söyle.

## Kalite

- Pasaj bölme, isim koruma ve arama gibi çekirdek fonksiyonlar için test yaz.
- Yanlış çıkan her çeviriyi `hatalar.csv` dosyasına türüyle kaydetmemi hatırlat
  (isim, anlam kayması, uydurma, eksik cümle).
- Çince bilmiyorum. Bir çevirinin doğru olduğunu iddia etme, emin olmadığın
  yeri açıkça söyle.
