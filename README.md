# MATLAB Lab — Öğrenim Sitesi

3 MATLAB slayt PDF'inden derlenen **özet notlar**, **100 zorlayıcı soruluk soru bankası**
ve kodunu yazdığın, hata yaptığında **hatayı ve nasıl düzeltileceğini anlatan** geri bildirim
sistemi. Tamamen yerel çalışır; internet bağlantısı gerekmez.

---

## Hızlı başlangıç

```bash
cd ~/matlab-site
./start.sh
```

Tarayıcı `http://127.0.0.1:8787/` adresinde açılır. Durdurmak için `Ctrl+C`.

Farklı port için: `PORT=8788 ./start.sh`

---

## Ne var içinde?

| Bölüm | İçerik |
|---|---|
| **Özet Notlar** | 3 PDF'in tamamı 15 konuya özetlendi. Her konuda "Özet Noktalar", açıklamalar, MATLAB kod örnekleri ve çıktıları, "tuzak" uyarıları. |
| **Soru Bankası** | 100 soru, 15 konuya dağılmış, 5 zorluk seviyesinde. Her soruda kod yazılır, **çalıştırılır**, sonuç otomatik denetlenir. |
| **Hızlı Referans** | 50 fonksiyonun tek sayfalık sözlüğü — aranabilir. |

### Sorular nasıl çalışıyor?

1. Soruyu aç → editör hazır kodla gelir.
2. Kodunu yaz → `Çalıştır`'a bas (veya `Ctrl+Enter`).
3. Kod **gerçekten çalıştırılır** (GNU Octave) ve sonuç **otomatik denetlenir**.
4. Yanlışsa:
   - **Ne bekleniyordu, ne buldun?** → değer karşılaştırması (`Beklenen: [19 22; 43 50]` / `Bulunan: 5`)
   - **Hata çıkarsa** → hatanın Türkçe açıklaması + "nasıl düzeltilir" önerisi
     (dizi sınırı, boyut uyuşmazlığı, süslü parantez, tanımsız fonksiyon, sıfıra bölme, sözdizimi…)
   - **İpucu** ve **Çözüm** butonları (istediğinde)
5. İlerleme tarayıcıda saklanır — kodu yarıda bırakıp kaldığın yerden devam edersin.

Sorular `sonuc` değişkenine bakarak denetlenir; soru metninde hangi değişkeni
ataman gerektiği yazılıdır.

---

## Gereksinimler

| Bileşen | Durum | Not |
|---|---|---|
| Python 3 | Şart | Yalnızca standart kütüphane — `pip install` gerekmez |
| GNU Octave | Şart (kod çalıştırma için) | `sudo pacman -S octave` |
| Tarayıcı | Şart | Chrome / Firefox / Chromium |

**Node.js kullanılmıyor.** Bu makinedeki Node kurulumu kırık (`libcrypto.so.4` eksik),
bu yüzden backend saf Python 3 stdlib ile yazıldı — sıfır bağımlılık, sıfır derleme.

> MATLAB'in kendisi lisanslı değil. GNU Octave, MATLAB sözdiziminin büyük kısmını
> çalıştırır ve hata mesajları da benzerdir; bu yüzden motor olarak Octave kullanıldı.
> Ödevlerde MATLAB kullanıyorsan aynı kodlar orada da çalışacaktır.

---

## Klasör yapısı

```
matlab-site/
├── start.sh                 # başlatma betiği (tarayıcıyı da açar)
├── server.py                # HTTP sunucusu (saf stdlib)
├── matlab-lab.desktop       # masaüstü kısayolu (.desktop)
├── mlab/
│   ├── questions.py         # 100 soru + doğrulama blokları + çözümler
│   ├── notes.py             # özet notlar + hızlı referans sözlüğü
│   └── runner.py            # Octave çalıştırma motoru + Türkçe hata tanısı
├── web/
│   ├── index.html
│   ├── style.css
│   ├── app.js               # yönlendirme, soru akışı, ilerleme
│   └── editor.js            # sözdizimi renklendirmeli kod editörü
├── assets/matlab-lab.svg    # uygulama ikonu
└── tests/
    ├── test_all.py          # 100 sorunun referans çözümünü doğrular
    ├── test_negative.py     # yanlış cevapların reddedildiğini doğrular
    └── tools/               # geliştirici araçları (headless Chrome ile UI testi)
```

---

## Testler

```bash
cd ~/matlab-site
python3 tests/test_all.py         # 100/100 referans çözüm geçmeli
python3 tests/test_negative.py    # 100/100 yanlış cevap reddedilmeli
```

İlk test 100 sorunun her birini çözümüyle çalıştırıp doğrulama bloğunun
"doğru" dediğini kontrol eder. İkinci test her soruya bilerek yanlış bir cevap
verir ve reddedildiğini doğrular.

---

## Kaynaklar

* `~/Desktop/MATLAB'e Giriş Matrisler ve Temel Kavramlar.pdf` (50 sayfa)
* `~/Desktop/slayt2.pdf` — MATLAB'de Diziler (55 sayfa)
* `~/Desktop/slayt3.pdf` — MATLAB'de Operatörler (22 sayfa)

---

## İpuçları

* **Kısayollar:** `Ctrl+Enter` çalıştırır · `Tab` girintiler · `Shift+Tab` geri girinti
* **Temayı değiştir:** sağ üstteki ◐ düğmesi (koyu ↔ açık)
* **Soruya bağlantı:** `http://127.0.0.1:8787/#/sorular/42` doğrudan 42. soruyu açar
* **Filtreler:** soldaki arama kutusu soru metninde, çözümde ve konu başlığında arar
