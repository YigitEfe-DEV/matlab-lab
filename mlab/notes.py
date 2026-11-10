"""Ozet notlar — 3 PDF slaytlarinin derlenmis ozeti.

Kaynaklar:
  [P1] "MATLAB'e Giris - Matrisler ve Temel Kavramlar" (50 sayfa)
  [P2] "MATLAB'de Diziler - Vektörler, matrisler ve dizi turleri" (55 sayfa)
  [P3] "MATLAB'de Operatorler - Aritmetik, karsilastirma, mantiksal operatorler" (22 sayfa)
"""

from __future__ import annotations

from typing import Any, Dict, List

NOTES: List[Dict[str, Any]] = [
    # =====================================================================
    {
        "id": "matrisler",
        "title": "Matrisler",
        "source": "[P1] Matris nedir? · Temel işlemler",
        "icon": "grid",
        "summary": "MATLAB'de her değişken bir matristir. Boyut yazarken önce satır, sonra "
                   "sütun sayısı gelir; elemanlara A(i,j) ile erişilir.",
        "keypoints": [
            "Boyut: m×n → önce satır (m), sonra sütun (n).",
            "Eleman erişimi: A(i, j) → i. satır, j. sütun.",
            "Skaler 1×1, satır vektörü 1×n, sütun vektörü m×1, kare matris n×n.",
            "Dört temel işlem: A+B, A−B, k·A, A·B, A'.",
            "A·B için iç boyutlar eşit olmalı; (m×n)·(n×p) → m×p.",
            "Matris çarpımı değişmez: genellikle A·B ≠ B·A.",
        ],
        "sections": [
            {
                "title": "Boyuta göre adlar",
                "points": [
                    "**Skaler** 1×1 — tek bir sayı: `[7]`",
                    "**Satır vektörü** 1×n — `[1 2 3]`",
                    "**Sütun vektörü** m×1 — `[1; 2; 3]`",
                    "**Kare matris** n×n — `[12 34; 56 78]`",
                ],
                "code": {
                    "matlab": "A = [1 2 3; 4 5 6];\nsize(A)      % 2 3\nA(2,3)      % 6",
                    "cikti": "ans =\n     2     3\nans =\n     6",
                },
            },
            {
                "title": "Özel matrisler",
                "points": [
                    "**Sıfır matrisi** — `zeros(3)`",
                    "**Birim matris** — `eye(3)`; A·I = A",
                    "**Köşegen matris** — `diag([4 2 9])`",
                    "**Simetrik matris** — A' = A; kontrol: `isequal(A, A')`",
                ],
                "code": {
                    "matlab": "zeros(3)\neye(3)\ndiag([4 2 9])\nisequal([1 2; 2 5]', [1 2; 2 5])",
                    "cikti": "ans =\n     0     0     0\n     0     0     0\n     0     0     0\n"
                             "ans =\n     1     0     0\n     0     1     0\n     0     0     1\n"
                             "ans =\n     4     0     0\n     0     2     0\n     0     0     9\n"
                             "ans =\n     1",
                },
            },
            {
                "title": "Matris çarpımı — satır × sütun",
                "points": [
                    "Her satır, karşı sütunla **skaler çarpılıp toplanır**.",
                    "1. satır · 1. sütun: 1·5 + 2·7 = 19",
                    "A·B ≠ B·A (çarpma değişmez değildir).",
                ],
                "code": {
                    "matlab": "A = [1 2; 3 4];\nB = [5 6; 7 8];\nA*B\nB*A",
                    "cikti": "ans =\n    19    22\n    43    50\nans =\n    23    34\n    31    46",
                },
                "notes": [
                    "**Dikkat:** A·B ile B·A sonuçları farklıdır. Bu yüzden "
                    "matris çarpımında sıra önemlidir.",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "ortam",
        "title": "MATLAB Ortamı ve Komutlar",
        "source": "[P1] Çalışma ortamı · Temel komutlar · Dosya komutları",
        "icon": "terminal",
        "summary": "MATLAB'in panel düzeni (Komut Penceresi, Editor, Workspace, Current "
                   "Folder) ve sık kullanılan ortak komutlar.",
        "keypoints": [
            "Komut Penceresi: komutu yaz, Enter'a bas, sonucu gör.",
            "Editor: `.m` betik dosyaları; F5 çalıştırır, `%%` bölüm oluşturur.",
            "Workspace: bellekteki değişkenler (ad, değer, boyut).",
            "`clc` ekranı temizler, `clear` değişkenleri siler, `close all` grafikleri kapatır.",
            "`who` isimleri, `whos` ayrıntılı tabloyu listeler.",
            "`pwd` / `cd` / `ls` / `dir` / `mkdir` / `what` / `edit` dosya komutları.",
        ],
        "sections": [
            {
                "title": "Ortam komutları",
                "points": [
                    "`clc` — Komut Penceresini temizler (değişkenler silinmez)",
                    "`clear` — Workspace'teki tüm değişkenleri siler",
                    "`clear x y` — yalnızca x ve y değişkenlerini siler",
                    "`close all` — açık tüm figure pencerelerini kapatır",
                    "`exit` — MATLAB'i kapatır (`quit` ile aynı)",
                ],
                "code": {
                    "matlab": "clc\nclear x y\nwho\nwhos\nexit",
                    "cikti": "",
                },
            },
            {
                "title": "Dosya komutları",
                "points": [
                    "`pwd` — geçerli klasörün yolu",
                    "`cd klasor` / `cd ..` — klasör değiştir",
                    "`ls` veya `dir` — içeriği listele",
                    "`mkdir ad` — yeni klasör oluştur",
                    "`what` — klasördeki MATLAB dosyalarını listele",
                    "`edit ad` — dosyayı Editor'de aç (yoksa oluştur)",
                ],
                "code": {
                    "matlab": "pwd\nls\nmkdir calisma\ncd calisma\ncd ..",
                    "cikti": "",
                },
            },
            {
                "title": "Yardım",
                "points": [
                    "`help sqrt` — kısa açıklama",
                    "`doc sqrt` — ayrıntılı belge sayfası",
                    "`lookfor square` — açıklamada kelime arar",
                    "`which sqrt` — fonksiyonun konumu",
                ],
                "notes": [
                    "Fonksiyon adını biliyorsan `help`/`doc`; bilmiyorsan `lookfor`.",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "degiskenler",
        "title": "Değişkenler ve İsimlendirme",
        "source": "[P1] Değişken kavramı · Özel değişkenler",
        "icon": "variable",
        "summary": "Değişken bellekteki bir kutudur; `=` eşitlik değil atamadır. "
                   "Karşılaştırma için `==` kullanılır.",
        "keypoints": [
            "`=` atamadır; sağdaki ifade hesaplanır, soldaki isme yazılır.",
            "Karşılaştırma `==`, eşit değil `~=` (MATLAB'te `!=` yoktur).",
            "Ad kuralları: harfle başlar, harf/rakam/alt çizgi, Türkçe karakter yok.",
            "Büyük/küçük harfe duyarlı: `alan` ≠ `Alan`.",
            "En fazla 63 karakter (`namelengthmax`).",
            "Hazır fonksiyon adını değişken adı olarak kullanma.",
        ],
        "sections": [
            {
                "title": "Geçerli / geçersiz isimler",
                "points": [
                    "**Geçerli:** `x1`, `alan_toplam`, `maxDeger`, `ogrenciSayisi`",
                    "**Geçersiz:** `1x` (rakamla başlar), `alan toplam` (boşluk), "
                    "`öğrenci` (Türkçe karakter), `for` (ayrılmış sözcük), `a-b` (çıkarma)",
                ],
                "notes": [
                    "**Kötü fikir:** `sum = 10` yazarsan `sum()` fonksiyonu artık çalışmaz. "
                    "Düzeltmek için `clear sum`.",
                ],
            },
            {
                "title": "Özel (hazır) değişkenler",
                "points": [
                    "`ans` — son sonucun tutulduğu değişken",
                    "`pi` — π sabiti",
                    "`i`, `j` — sanal birim (güvenli yazım: `1i`)",
                    "`Inf` — sonsuz (ör. `1/0`)",
                    "`NaN` — tanımsız (ör. `0/0`)",
                ],
                "code": {
                    "matlab": "ans\npi\n1/0\n0/0",
                    "cikti": "ans =\n    3.1416\nans =\n   Inf\nans =\n   NaN",
                },
            },
        ],
    },
    # =====================================================================
    {
        "id": "sayilar",
        "title": "Rakamlar, Sayılar ve Veri Tipleri",
        "source": "[P1] Rakamlar ve sayılar",
        "icon": "hash",
        "summary": "Her sayı varsayılan olarak `double` (64 bit kayan nokta) saklanır. "
                   "Ondalıklı sayılarda `==` güvenilmezdir.",
        "keypoints": [
            "Tipler: double, single, int8…int64, uint8…uint64, logical, char.",
            "`double` 8 bayt, 15–16 anlamlı basamak.",
            "`int8(200)` → 127 (doygunluk); `uint8(3.7)` → 4 (yuvarlama).",
            "`format` yalnızca **gösterimi** değiştirir, hesaplar tam double hassasiyetindedir.",
            "0.1 ikili sistemde tam değildir → `0.1+0.2 == 0.3` **0** verir.",
            "Ondalıklı karşılaştırmada tolerans kullan: `abs(a-b) < 1e-10`.",
            "Karmaşık sayı: `3+4i`, `abs`, `real`, `imag`, `conj`.",
        ],
        "sections": [
            {
                "title": "Format komutları",
                "points": [
                    "`format short` → 3.1416",
                    "`format long` → 3.141592653589793",
                    "`format shortE` / `longE` → bilimsel gösterim",
                    "`format rat` → 355/113",
                    "`format bank` → 3.14",
                    "`format compact` / `loose` → boş satır sayısı",
                ],
                "code": {
                    "matlab": "format long\npi\nformat short\npi",
                    "cikti": "ans =\n   3.141592653589793\nans =\n    3.1416",
                },
            },
            {
                "title": "Kayan nokta tuzağı",
                "points": [
                    "`0.1 + 0.2 == 0.3` → **0** (yanlış!)",
                    "`abs(0.1+0.2-0.3) < 1e-10` → **1** (doğru)",
                ],
                "notes": [
                    "0.1, ikili sistemde sonsuz basamaklıdır; 1/3'ün ondalık sistemde "
                    "0.333… olması gibi. Kural: ondalıklı sayıları `==` ile değil, "
                    "toleransla karşılaştır.",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "fonksiyonlar",
        "title": "Temel Fonksiyonlar",
        "source": "[P1] Fonksiyonlar",
        "icon": "function",
        "summary": "Kök, logaritma, trigonometri, yuvarlama ve sayı kuramı "
                   "fonksiyonlarının hızlı referansı.",
        "keypoints": [
            "`sqrt` karekök, `nthroot(x,n)` n. derece gerçek kök.",
            "`exp` e üzeri, `log` ln, `log10` 10 tabanı, `log2` 2 tabanı.",
            "`sin/cos/tan` **radyan**; `sind/cosd/tand` **derece**.",
            "`deg2rad` derece→radyan, `rad2deg` radyan→derece.",
            "Yuvarlama: `round` (en yakın), `floor` (aşağı), `ceil` (yukarı), `fix` (sıfıra).",
            "`mod` bölenin, `rem` bölünenin işaretini alır.",
            "Sayı kuramı: `sign`, `gcd`, `lcm`, `isprime`, `primes`, `nchoosek`.",
        ],
        "sections": [
            {
                "title": "Hızlı tablo",
                "points": [
                    "| Fonksiyon | Anlamı | Örnek |",
                    "|---|---|---|",
                    "| `sqrt(16)` | karekök | 4 |",
                    "| `nthroot(-27,3)` | 3. derece gerçel kök | -3 |",
                    "| `abs(-7)` | mutlak değer | 7 |",
                    "| `exp(1)` | e | 2.7183 |",
                    "| `log(exp(2))` | ln | 2 |",
                    "| `log10(1000)` | 10 tabanı | 3 |",
                    "| `factorial(5)` | faktöriyel | 120 |",
                    "| `gcd(12,18)` | EBOB | 6 |",
                    "| `lcm(4,6)` | EKOK | 12 |",
                    "| `nchoosek(5,2)` | C(5,2) | 10 |",
                ],
            },
            {
                "title": "Yuvarlama tablosu",
                "points": [
                    "| x | round | floor | ceil | fix |",
                    "|---|---|---|---|---|",
                    "| 2.7 | 3 | 2 | 3 | 2 |",
                    "| 2.5 | 3 | 2 | 3 | 2 |",
                    "| -2.5 | -3 | -3 | -2 | -2 |",
                ],
                "notes": [
                    "round: en yakına (yarımda sıfırdan uzağa) · floor: aşağı · "
                    "ceil: yukarı · fix: sıfıra doğru.",
                    "`mod(-7,3)` = **2**, `rem(-7,3)` = **-1** — negatif sayılarda farklıdır.",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "matematikten-koda",
        "title": "Matematikten Kodaya Çevirme",
        "source": "[P1] Hafta 1 · Matematikten koda",
        "icon": "sigma",
        "summary": "Matematiksel ifadeyi MATLAB'e çevirirken iki tuzak vardır: "
                   "çarpma işareti asla gizli değildir, kesirler parantezle yazılır.",
        "keypoints": [
            "x² → `x^2`   |x| → `abs(x)`   √x → `sqrt(x)`",
            "2x → `2*x`   (çarpma işareti zorunlu)",
            "e^x → `exp(x)`   ln x → `log(x)`",
            "a/(b+c) → `a/(b+c)` (pay ve payda parantezde)",
            "Öncelik: parantez → üs → çarpma/bölme → toplama/çıkarma.",
            "Aynı öncelikte soldan sağa: `2^3^2` = (2^3)^2 = 64.",
            "`-2^2` = -(2^2) = -4.",
        ],
        "sections": [
            {
                "title": "Örnek 1 — parantez tuzağı",
                "points": [
                    "y = (√(x²+1) + e^(−x)) / |ln x|, x = 2 → 3.4212",
                ],
                "code": {
                    "matlab": "x = 2;\ny = (sqrt(x^2 + 1) + exp(-x)) / abs(log(x))",
                    "cikti": "y =\n    3.4212",
                },
                "notes": [
                    "**Sık yapılan hata:** `sqrt(x^2+1) + exp(x)/abs(log(x))` → 2.4313 "
                    "(yanlış). Parantez atlanınca bölme sadece son terime uygulanır.",
                ],
            },
            {
                "title": "Örnek 2 — ikinci derece denklem",
                "points": [
                    "x² − 3x + 2 = 0 için D = b² − 4ac, kökler = (−b ± √D)/(2a)",
                ],
                "code": {
                    "matlab": "a = 1; b = -3; c = 2;\nD = b^2 - 4*a*c\nx1 = (-b + sqrt(D))/(2*a)\nx2 = (-b - sqrt(D))/(2*a)",
                    "cikti": "D =\n     1\nx1 =\n     2\nx2 =\n     1",
                },
                "notes": [
                    "**Sık yapılan hata:** `(-b + sqrt(D))/2*a` — işlemler soldan sağa "
                    "yapılır: önce 2'ye böler, sonra `a` ile çarpar. Doğrusu "
                    "`(-b + sqrt(D))/(2*a)`.",
                ],
            },
            {
                "title": "Örnek 3 — uzun ifadeyi bölmek",
                "points": [
                    "Normal dağılım yoğunluk fonksiyonu: f(x) = 1/(σ√(2π)) · e^(−(x−μ)²/(2σ²))",
                    "Uzun ifadeyi `...` ile alt satıra böl ve parçalara ayır.",
                ],
                "code": {
                    "matlab": "mu = 0; sigma = 1; x = 1;\nkatsayi = 1/(sigma*sqrt(2*pi));\nus = -(x-mu)^2/(2*sigma^2);\nf = katsayi * exp(us)",
                    "cikti": "f =\n    0.2420",
                },
            },
        ],
    },
    # =====================================================================
    {
        "id": "input",
        "title": "Kullanıcı Girdisi (input)",
        "source": "[P1] Hafta 1 · Kullanıcı girdisi",
        "icon": "keyboard",
        "summary": "`input` girilen metni MATLAB ifadesi olarak hesaplar. Metin almak "
                   "için ikinci parametre `'s'` olmalıdır.",
        "keypoints": [
            "`input('mesaj')` — girdiyi **hesaplar** (sayı/vektör/matris döner).",
            "`input('mesaj','s')` — girdiyi **metin** (char) olarak döndürür.",
            "Boş Enter → boş matris `[]`.",
            "`str2double` metni sayıya, `num2str` sayıyı metne çevirir.",
        ],
        "sections": [
            {
                "title": "Sözdizimi",
                "points": [
                    "| Çağrı | Dönen tip |",
                    "|---|---|---|",
                    "| `input(m)` | sayı veya matris |",
                    "| `input(m,'s')` | metin (char) |",
                    "| `str2double(s)` | sayı |",
                    "| `num2str(x)` | metin |",
                ],
                "code": {
                    "matlab": "x = input('Bir sayi girin: ')\nv = input('Vektor girin: ')\nad = input('Adiniz: ', 's')\nn = str2double(input('Say: ', 's'))",
                    "cikti": "Bir sayi girin: 5\nx =\n     5\nVektor girin: [1 2 3]\nv =\n     1     2     3\n"
                             "Adiniz: Ayse\nad =\n    'Ayse'\nSay: 25\nn =\n    25",
                },
                "notes": [
                    "**Tuzak:** `input('Adiniz: ')` yazarsan `Ayşe` bir **isim** "
                    "olduğu için MATLAB hata verir. Metin için mutlaka `'s' kullan.",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "diziler",
        "title": "Diziler ve Vektör Üretimi",
        "source": "[P2] Dizi kavramı · Vektörler · Birleştirme",
        "icon": "list",
        "summary": "MATLAB'de her değişken bir dizidir; skaler bile 1×1'dir. Vektörler "
                   "`:` ve `linspace` ile üretilir.",
        "keypoints": [
            "`[1 2 3]` satır vektörü · `[1; 2; 3]` sütun vektörü · `[1 2; 3 4]` matris.",
            "Satır/sütun ayırıcı: boşluk (veya `,`) yatay, `;` dikey.",
            "`a:h:b` → **adım** verilir; `linspace(a,b,n)` → **eleman sayısı** verilir.",
            "Bitiş değeri aşılmaz; ulaşılamıyorsa son eleman eşiği geçmeyen büyük değerdir.",
            "Artış yönü yanlışsa sonuç **boş dizidir** (`5:1` → 1×0).",
            "Transpozda parantez gerekir: `(1:4)'`.",
            "`[a b]` yatay, `[a; b]` dikey birleştirme (veya `horzcat`/`vertcat`).",
        ],
        "sections": [
            {
                "title": "İki nokta operatörü",
                "points": [
                    "`1:5` → 1 2 3 4 5",
                    "`0:2:10` → 0 2 4 6 8 10",
                    "`10:-3:1` → 10 7 4 1",
                    "`0:0.25:1` → 0 0.25 0.50 0.75 1",
                    "`5:1` → **boş** (1×0)",
                ],
            },
            {
                "title": "':' mi, linspace mi?",
                "points": [
                    "| | `a:h:b` | `linspace(a,b,n)` |",
                    "|---|---|---|",
                    "| Ne verilir? | artış (h) | eleman sayısı (n) |",
                    "| Bitiş dahil mi? | ancak tam denk gelirse | her zaman |",
                    "| Tipik kullanım | sayaç, indeks: `1:n` | grafik ekseni |",
                    "| Örnek | `0:0.1:1` → 11 eleman | `linspace(0,1,11)` → aynı |",
                ],
                "notes": [
                    "**Kural:** Adımı biliyorsan `:` , nokta sayısını biliyorsan `linspace`.",
                ],
            },
            {
                "title": "Birleştirme",
                "points": [
                    "`a = [1 2]; b = [3 4];`",
                    "`[a b]` → `[1 2 3 4]` (yatay; satır sayıları eşit olmalı)",
                    "`[a; b]` → `[1 2; 3 4]` (dikey; sütun sayıları eşit olmalı)",
                    "`[a 0 a]` → `[1 2 0 1 2]`",
                ],
                "notes": [
                    "`[1 2; 3]` → hata: *Dimensions of arrays being concatenated are "
                    "not consistent.*",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "hazir-diziler",
        "title": "Hazır Diziler ve Rastgelelik",
        "source": "[P2] Hazır diziler · rand · randi · randn · randperm · rng",
        "icon": "dice",
        "summary": "Sık kullanılan dizi üreticileri. Tek argüman **kare** matris üretir — "
                   "vektör istiyorsan iki boyut yaz.",
        "keypoints": [
            "`zeros(m,n)`, `ones(m,n)`, `eye(n)`, `diag(v)`, `repmat(A,m,n)`.",
            "Tek argüman kare matris verir: `zeros(3)` → 3×3, `zeros(1,3)` → 1×3.",
            "`rand` → (0,1) aralığı; `randi(imax)` → 1…imax (uçlar dahil).",
            "`randn` normal dağılım (μ=0, σ=1); `randperm` rastgele permütasyon.",
            "`rng(tohum)` üreteci sabitler → deneyler tekrarlanabilir olur.",
            "`[a,b]` aralığına ölçekleme: `a + (b-a)*rand(1,n)`.",
        ],
        "sections": [
            {
                "title": "Üreticiler",
                "points": [
                    "| Fonksiyon | Anlamı |",
                    "|---|---|",
                    "| `rand(1,5)` | 5 adet (0,1) rastgele sayı |",
                    "| `randi(6,1,10)` | 10 zar atışı (1–6) |",
                    "| `randi([5 15],3,3)` | 3×3, 5–15 arası tam sayı |",
                    "| `randn(1,5)` | normal dağılımlı 5 sayı |",
                    "| `randperm(5)` | 1–5'in rastgele sırası |",
                ],
                "code": {
                    "matlab": "rng(42);\na = rand(1,3)\nrng(42);\nb = rand(1,3)\nisequal(a,b)",
                    "cikti": "a =\n    0.7941    0.5210    0.4148\nb =\n    0.7941    0.5210    0.4148\n"
                             "ans =\n     1",
                },
            },
        ],
    },
    # =====================================================================
    {
        "id": "istatistik",
        "title": "İstatistik ve Topluluk Fonksiyonları",
        "source": "[P2] Vektörlerde · Matrislerde · Boyut seçimi",
        "icon": "chart",
        "summary": "Matrise uygulanan `sum`, `mean`, `max` gibi fonksiyonlar **sütun "
                   "sütun** çalışır. Yönü `sum(A,1)` / `sum(A,2)` ile belirlersin.",
        "keypoints": [
            "Vektörde: `sum`, `max`, `min`, `mean`, `prod`, `sort`, `median`, `cumsum`.",
            "Matriste varsayılan **sütun** toplamı: `sum(A)` → sütun başına bir değer.",
            "`sum(A,1)` sütun boyunca · `sum(A,2)` satır boyunca · `sum(A,'all')` tümü.",
            "`[m,i] = max(v)` → değer ve **indeks**; `[~,i] = max(v)` yalnızca indeks.",
            "Diğerleri: `std`, `var`, `mode`, `cumprod`, `diff`, `dot`.",
            "`var(x) = std(x)^2`.",
        ],
        "sections": [
            {
                "title": "Boyut seçimi",
                "points": [
                    "`A = [1 2 3; 4 5 6];` için:",
                    "`sum(A)` → `5 7 9` (sütun toplamları)",
                    "`sum(A,2)` → `[6; 15]` (satır toplamları)",
                    "`sum(A,'all')` → `21`",
                    "`max(A,[],2)` → `[3; 6]` (satır en büyükleri)",
                    "`max(A,[],'all')` → `6`",
                ],
                "code": {
                    "matlab": "A = [1 2 3; 4 5 6];\nsum(A)\nsum(A,2)\nmean(A,2)\nmax(A,[],'all')",
                    "cikti": "ans =\n     5     7     9\nans =\n     6\n    15\nans =\n     2\n     5\nans =\n     6",
                },
                "notes": [
                    "`max(A)` **sütun** en büyüklerini verir. Tüm matrisin en büyüğü "
                    "için `max(A(:))` ya da `max(A,[],'all')` gerekir.",
                ],
            },
            {
                "title": "İki çıktılı fonksiyonlar",
                "points": [
                    "`[m, i] = max(v)` → m: değer, i: vektördeki konumu",
                    "`[~, idx] = sort(v,'descend')` → sadece indeksler",
                    "`~` istenmeyen çıktıyı atlar; o çıktı için değişken oluşturulmaz.",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "nokta-operatorleri",
        "title": "Nokta Operatörleri ve Skaler İşlemler",
        "source": "[P3] Aritmetik operatörler · Nokta ne zaman gerekir?",
        "icon": "dot",
        "summary": "`*` matris çarpımı, `.*` eleman eleman çarpımdır. Vektörlerde "
                   "eleman işlemi istiyorsan nokta şart.",
        "keypoints": [
            "`*` matris çarpımı · `.*` eleman eleman çarpım.",
            "`/` sağa bölme · `./` eleman eleman bölme.",
            "`\\` sola bölme · `.\\` eleman eleman sola bölme.",
            "`^` matris üssü (kare matrislerde) · `.^` eleman eleman üs.",
            "`+` ve `−` her zaman eleman elemandır.",
            "Skalerle çarpma/bölmede nokta gerekmez: `2*v`, `v/2`.",
            "Skaler **bölünen** veya **üs** ise nokta gerekir: `1./v`, `v.^2`.",
        ],
        "sections": [
            {
                "title": "Nokta ne zaman gerekir?",
                "points": [
                    "| İşlem | skaler ∘ skaler | skaler ∘ dizi | dizi ∘ dizi |",
                    "|---|---|---|---|",
                    "| `+ −` | gerekmez | gerekmez | gerekmez |",
                    "| `*` | gerekmez | gerekmez | **gerekmez** (`.*` kullan) |",
                    "| `/` | gerekmez | dizi/skaler: gerekmez | **gerekmez** (`./` kullan) |",
                    "| `^` | gerekmez | **gerekmez** (`.^` kullan) | **gerekmez** (`.^` kullan) |",
                ],
                "notes": [
                    "**Tuzak:** `a = [1 2 3]; a*b` → *Incorrect dimensions for matrix "
                    "multiplication.* Aynı boyutta iki vektörü çarpmak istiyorsan `a * b'`.",
                ],
            },
            {
                "title": "Fonksiyon karşılıkları",
                "points": [
                    "| Operatör | Fonksiyon |",
                    "|---|---|",
                    "| `a+b` | `plus(a,b)` |",
                    "| `a−b` | `minus(a,b)` |",
                    "| `a.*b` | `times(a,b)` |",
                    "| `A*B` | `mtimes(A,B)` |",
                    "| `a./b` | `rdivide(a,b)` |",
                    "| `a.^b` | `power(a,b)` |",
                    "| `A^n` | `mpower(A,n)` |",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "indeksleme",
        "title": "İndeksleme",
        "source": "[P2] Vektörde indeksleme · Matriste indeksleme · Mantıksal indeksleme",
        "icon": "target",
        "summary": "`end`, `:` ve mantıksal maskelerle dizilerin herhangi bir parçasına "
                   "erişebilir, değiştirebilir veya silebilirsin.",
        "keypoints": [
            "`v(end)` son eleman · `v(end-1)` sondan bir önceki.",
            "`v(2:4)` alt dizi · `v([1 3 5])` seçici indeksleme.",
            "`v(end:-1:1)` ters sıra.",
            "`A(2,:)` satır · `A(:,1)` sütun · `A(1:2,2:3)` blok.",
            "Doğrusal indeks **sütun sütun** sayılır: A(4) → 2. sütunun 1. satırı.",
            "`v(v > 25)` mantıksal indeksleme; `find(v>25)` indeksleri verir.",
            "`v(2) = []` eleman siler; `A(:,1) = []` sütunu siler.",
                    "Dizi dışına atama (`v(7)=70`) diziyi büyütür, boşluklar 0 olur.",
        ],
        "sections": [
            {
                "title": "Doğrusal indeksleme",
                "points": [
                    "`A = [1 2 3; 4 5 6; 7 8 9]` → doğrusal sıra:",
                    "1,2,3 (1. sütun) · 4,5,6 (2. sütun) · 7,8,9 (3. sütun)",
                    "`A(4)` → **20** değil, 2. sütunun 1. satırı → **4**",
                    "`A(:)` → tek sütun vektörü",
                ],
                "notes": [
                    "MATLAB elemanları bellekte **sütun sütun** saklar. Bu yüzden "
                    "`A(4)`, beklediğin 4. eleman (4) değil 2. sütunun 1. satırıdır.",
                ],
            },
            {
                "title": "Mantıksal indeksleme",
                "points": [
                    "`v = [10 20 30 40 50]`",
                    "`v > 25` → `0 0 1 1 1` (maske)",
                    "`v(v > 25)` → `30 40 50`",
                    "`find(v > 25)` → `3 4 5`",
                    "`v(v > 25) = 0` → `10 20 0 0 0`",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "hucre-yapi",
        "title": "Hücre ve Yapı Dizileri",
        "source": "[P2] Dizi türleri · Hücre dizileri · Yapı dizileri",
        "icon": "layers",
        "summary": "Dört dizi türü: sayısal, karakter (char), hücre (cell) ve yapı "
                   "(struct). Hücrede `()` kutu verir, `{}` içeriği verir.",
        "keypoints": [
            "**char** — `'metin'`, 1×n; her karakter bir elemandır.",
            "**cell** — `{1, 'a', [2 3]}`; her hücre farklı tipte olabilir.",
            "**struct** — `s.ad = 'Ali'`; alanlara nokta ile erişilir.",
            "`c(2)` → hücrenin kendisi (1×1 cell); `c{2}` → içeriği.",
            "`c{3}(2)` → önce 3. hücrenin içeriği, sonra onun 2. elemanı.",
            "`s.(alan)` → dinamik alan erişimi.",
            "`[ogr.not]` → tüm kayıtların aynı alanını vektörde toplar.",
            "**Sayısal diziye `{ }` ile erişim hata verir.**",
        ],
        "sections": [
            {
                "title": "Dört parantez, dört görev",
                "points": [
                    "| İşaret | Görev |",
                    "|---|---|",
                    "| `[ ]` | dizi oluşturma, birleştirme, çoklu çıktı |",
                    "| `( )` | indeksleme, fonksiyon çağrısı, işlem önceliği |",
                    "| `{ }` | hücre oluşturma, hücre içeriği |",
                    "| `.` | yapı alanı, eleman işlemi (`.*`), ondalık ayırıcı |",
                ],
            },
            {
                "title": "Hücre dizisi örneği",
                "points": [
                    "`c = {42, 'Ali', [1 2 3]};`",
                    "`c(2)` → `{'Ali'}` (class: cell)",
                    "`c{2}` → `'Ali'` (class: char)",
                    "`c{3}(2)` → `2`",
                    "`class(c(2))` → `'cell'`, `class(c{2})` → `'char'`",
                ],
                "code": {
                    "matlab": "c = {42, 'Ali', [1 2 3]};\nclass(c(2))\nclass(c{2})\nc{3}(2)",
                    "cikti": "ans =\n    'cell'\nans =\n    'char'\nans =\n     2",
                },
                "notes": [
                    "**Tuzak:** `A = [1 2 3]; A{1}` → *Brace indexing is not supported "
                    "for variables of this type.* Sayısal dizide daima `( )`.",
                ],
            },
            {
                "title": "Yapı dizileri",
                "points": [
                    "`ogr(1).ad = 'Ayşe'; ogr(1).not = 85;`",
                    "`ogr(2).ad = 'Ali';   ogr(2).not = 70;`",
                    "`size(ogr)` → `1 2`",
                    "`[ogr.not]` → `85 70`",
                    "`fieldnames(s)`, `isfield(s,'no')`, `rmfield(s,'no')`",
                ],
            },
        ],
    },
    # =====================================================================
    {
        "id": "save-load",
        "title": "Kaydetme ve Yükleme",
        "source": "[P2] MAT dosyaları · save · load",
        "icon": "save",
        "summary": "Workspace geçicidir — MATLAB kapanınca veya `clear` yazılınca "
                   "değişkenler silinir. `.mat` dosyaları ikili olarak saklar.",
        "keypoints": [
            "`save('veri.mat')` — tüm değişkenler",
            "`save veri.mat x y` — yalnızca x ve y",
            "`save('veri.mat','A','-append')` — var olan dosyaya ekle",
            "`save sonuc.txt A -ascii` — metin olarak sakla",
            "`load('veri.mat')` — geri yükle",
            "`S = load('veri.mat')` → struct döner, `S.A` ile erişilir.",
            "Tüm türler (sayısal, char, cell, struct) olduğu gibi geri gelir.",
        ],
        "sections": [
            {
                "title": "Kaydet, temizle, geri yükle",
                "points": [
                    "`notlar = [65 80 72 90 55];`",
                    "`save('sinif.mat','notlar')`",
                    "`clear` — hepsi silinir",
                    "`load('sinif.mat')` — geri gelir",
                ],
                "code": {
                    "matlab": "notlar = [65 80 72 90 55];\nisimler = {'Ali','Ayse'};\nsave('sinif.mat','notlar','isimler')\nclear\nload('sinif.mat')\nmean(notlar)",
                    "cikti": "ans =\n   72.4000",
                },
            },
        ],
    },
    # =====================================================================
    {
        "id": "operatorler",
        "title": "Operatörler, Karşılaştırma ve Mantık",
        "source": "[P3] Operatör kavramı · Karşılaştırma · Mantıksal operatörler",
        "icon": "toggle",
        "summary": "Karşılaştırma her zaman mantıksal (1/0) sonuç verir. `&&`/`||` "
                   "kısa devre yapar ve yalnızca skalerlerde çalışır.",
        "keypoints": [
            "Aritmetik: `+ − * / \\ ^ .* ./ .^`",
            "Karşılaştırma: `== ~= < <= > >=` → daima 1 veya 0.",
            "Mantıksal: `& | ~ && ||`.",
            "MATLAB'te `!=` **yoktur** — `~=` kullan.",
            "0 dışındaki tüm değerler (negatifler dahil) doğrudur.",
            "`&`, `|`, `~` eleman eleman çalışır; `&&`, `||` yalnızca skaler.",
            "`any` en az biri, `all` hepsi, `find` indeksler, `nnz` sayı.",
            "**Zincirleme karşılaştırma (`2 < v < 9`) MATLAB'de çalışmaz.**",
        ],
        "sections": [
            {
                "title": "Doğruluk tablosu",
                "points": [
                    "| a | b | a&b | a\\|b | xor(a,b) | ~a |",
                    "|---|---|---|---|---|---|",
                    "| 0 | 0 | 0 | 0 | 0 | 1 |",
                    "| 0 | 1 | 0 | 1 | 1 | 1 |",
                    "| 1 | 0 | 0 | 1 | 1 | 0 |",
                    "| 1 | 1 | 1 | 1 | 0 | 0 |",
                ],
            },
            {
                "title": "Aralık kontrolü tuzağı",
                "points": [
                    "`v = [3 8 1 6 10];`",
                    "`v > 2 & v < 9` → `1 1 0 1 0` → seçilen: `3 8 6`",
                    "`2 < v < 9` → **HER ZAMAN 1** (yanlış!)",
                    "**Neden?** Önce `2 < v` hesaplanır (0/1), sonra bu 0/1 sonucu `9` "
                    "ile karşılaştırılır — 9'dan küçük olduğu için hep doğru.",
                ],
                "code": {
                    "matlab": "v = [3 8 1 6 10];\nv > 2 & v < 9\n2 < v < 9",
                    "cikti": "ans =\n     1     1     0     1     0\nans =\n     1     1     1     1     1",
                },
            },
            {
                "title": "Kısa devre operatörleri",
                "points": [
                    "`&&` — ilki 0 ise durur (VE)",
                    "`||` — ilki 1 ise durur (VEYA)",
                    "Sadece **skaler** mantıksal değerlerle çalışır.",
                ],
                "code": {
                    "matlab": "x = 0;\n(x ~= 0) && (10/x > 1)\n(x == 0) || (10/x > 1)",
                    "cikti": "ans =\n     0\nans =\n     1",
                },
                "notes": [
                    "`[1 1] && 1` → hata: *Operands to the logical AND (&&) and OR (||) "
                    "operators must be convertible to logical scalar values.*",
                ],
            },
            {
                "title": "Metin karşılaştırma",
                "points": [
                    "`'abc' == 'abd'` → `1 0 0` (harf harf karşılaştırır)",
                    "`'abc' == 'ab'` → hata (boyut uyuşmazlığı)",
                    "`strcmp('abc','ab')` → `0` (her uzunlukta güvenli)",
                    "`strcmpi('ABC','abc')` → `1` (büyük/küçük harf yok sayılır)",
                ],
            },
        ],
    },
]

GLOSSARY: List[Dict[str, Any]] = [
    {"fn": "size(A)", "desc": "Boyut: satır ve sütun sayısı", "ex": "size([1 2;3 4]) → 2 2"},
    {"fn": "length(A)", "desc": "En büyük boyut", "ex": "length([1 2 3]) → 3"},
    {"fn": "numel(A)", "desc": "Toplam eleman sayısı", "ex": "numel([1 2;3 4]) → 4"},
    {"fn": "ndims(A)", "desc": "Boyut sayısı", "ex": "ndims(A) → 2"},
    {"fn": "class(A)", "desc": "Veri tipi", "ex": "class(7) → 'double'"},
    {"fn": "isempty(A)", "desc": "Dizi boş mu?", "ex": "isempty([]) → 1"},
    {"fn": "isnumeric / ischar", "desc": "Tip kontrolü", "ex": "isnumeric('a') → 0"},
    {"fn": "isequal(a,b)", "desc": "Tamamen aynı mı?", "ex": "isequal([1 2],[1 2]) → 1"},
    {"fn": "sum / mean", "desc": "Toplam / ortalama (matriste sütun sütun)", "ex": "sum(A,2) → satır toplamı"},
    {"fn": "max / min", "desc": "En büyük / en küçük", "ex": "[m,i] = max(v)"},
    {"fn": "sort(v,'descend')", "desc": "Azalan sıralama", "ex": "sort([3 1 2],'descend') → 3 2 1"},
    {"fn": "cumsum / cumprod", "desc": "Kümülatif toplam / çarpım", "ex": "cumsum([1 2 3]) → 1 3 6"},
    {"fn": "median / mode", "desc": "Ortanca / en sık değer", "ex": "median([1 2 3 4]) → 2.5"},
    {"fn": "std / var", "desc": "Standart sapma / varyans", "ex": "var(x) = std(x)^2"},
    {"fn": "diff(x)", "desc": "Ardışık farklar", "ex": "diff([1 4 9]) → 3 5"},
    {"fn": "dot(a,b)", "desc": "Skaler çarpım", "ex": "dot([1 2 3],[4 5 6]) → 32"},
    {"fn": "zeros / ones", "desc": "0 / 1 dolu dizi", "ex": "zeros(1,3) → 1×3"},
    {"fn": "eye(n)", "desc": "Birim matris", "ex": "eye(3)"},
    {"fn": "diag(v)", "desc": "Köşegen matris", "ex": "diag([4 2 9])"},
    {"fn": "repmat(A,m,n)", "desc": "Tekrarlı dizi", "ex": "repmat([1 2],2,2)"},
    {"fn": "linspace(a,b,n)", "desc": "n eşit aralıklı nokta", "ex": "linspace(0,1,5)"},
    {"fn": "a:h:b", "desc": "Artış h ile vektör", "ex": "0:2:10"},
    {"fn": "rand / randi", "desc": "Rastgele ondalık / tam sayı", "ex": "randi(6,1,10)"},
    {"fn": "rng(seed)", "desc": "Üreteci sabitle", "ex": "rng(42)"},
    {"fn": "find(koşul)", "desc": "Doğru elemanların indeksleri", "ex": "find(v>2)"},
    {"fn": "nnz(koşul)", "desc": "Doğru eleman sayısı", "ex": "nnz(v>2)"},
    {"fn": "any / all", "desc": "En az biri / hepsi", "ex": "all(v>0)"},
    {"fn": "strcmp / strcmpi", "desc": "Metin karşılaştırma", "ex": "strcmp('a','a') → 1"},
    {"fn": "upper / lower", "desc": "Büyük / küçük harf", "ex": "upper('ali') → 'ALI'"},
    {"fn": "str2double / num2str", "desc": "Metin ↔ sayı", "ex": "str2double('2.5')"},
    {"fn": "strrep / strfind / strsplit", "desc": "Değiştir / bul / böl", "ex": "strfind('ana','a') → 1 3"},
    {"fn": "fieldnames / isfield", "desc": "Yapı alanları", "ex": "fieldnames(s)"},
    {"fn": "abs / sqrt / nthroot", "desc": "Mutlak / karekök / n. kök", "ex": "nthroot(-27,3) → -3"},
    {"fn": "exp / log / log10", "desc": "e^x / ln x / log10 x", "ex": "log(exp(2)) → 2"},
    {"fn": "sin / sind", "desc": "Radyan / derece sinüs", "ex": "sind(30) → 0.5"},
    {"fn": "round / floor / ceil / fix", "desc": "Yuvarlama çeşitleri", "ex": "round(2.5) → 3"},
    {"fn": "mod / rem", "desc": "Kalan (farklı işaret kuralı)", "ex": "mod(-7,3) → 2"},
    {"fn": "gcd / lcm", "desc": "EBOB / EKOK", "ex": "gcd(12,18) → 6"},
    {"fn": "isprime / primes / nchoosek", "desc": "Asal sayı araçları", "ex": "nchoosek(5,2) → 10"},
    {"fn": "disp / fprintf", "desc": "Ekrana yazdır", "ex": "fprintf('%.2f\\n', pi)"},
    {"fn": "input", "desc": "Kullanıcıdan değer al", "ex": "input('Ad: ','s')"},
    {"fn": "save / load", "desc": "Değişken kaydet / yükle", "ex": "load('veri.mat')"},
    {"fn": "clc / clear / close all", "desc": "Ekran / değişken / grafik temizle", "ex": "clear x y"},
    {"fn": "pwd / cd / ls / mkdir", "desc": "Klasör komutları", "ex": "pwd"},
    {"fn": "help / doc / lookfor / which", "desc": "Yardım komutları", "ex": "doc sqrt"},
    {"fn": "who / whos", "desc": "Değişken listesi", "ex": "whos"},
    {"fn": "fprintf / num2str / strtrim", "desc": "Biçimlendirme", "ex": "num2str(pi)"},
    {"fn": "A' / transpose(A)", "desc": "Transpoz", "ex": "[1 2]' → 1;2"},
    {"fn": "horzcat / vertcat", "desc": "Yatay / dikey birleştirme", "ex": "horzcat(a,b)"},
    {"fn": "reshape / repmat", "desc": "Yeniden boyutlandır / tekrarla", "ex": "repmat(A,2,2)"},
]
