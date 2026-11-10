"""100 soruluk MATLAB soru bankasi.

Her soru:
  id        : benzersiz numara (1..100)
  module    : konu basligi (ozet notlarla ayni terminoloji)
  topic     : alt baslik
  level     : 1 (temel) .. 5 (zor)
  kind      : "code" | "error" | "mcq"
  prompt    : soru metni
  starter   : kod editorunde hazir gelen kod
  verify    : Octave dogrulama blogu (chk / chkTol / chkSize / chkTrue / chkOut)
  stdin     : input() sorulari icin beslenen veri
  expect_error : "error" turu icin beklenen hata regex'i
  choices / answer / explanation : mcq sorulari icin
  hint / solution : geri bildirim
"""

from __future__ import annotations

from typing import Any, Dict, List


def Q(
    id: int,
    module: str,
    topic: str,
    level: int,
    prompt: str,
    verify: str = "",
    kind: str = "code",
    starter: str = "",
    stdin: str = "",
    expect_error: str = "",
    choices: List[str] = None,
    answer: int = -1,
    explanation: str = "",
    hint: str = "",
    solution: str = "",
) -> Dict[str, Any]:
    return {
        "id": id,
        "module": module,
        "topic": topic,
        "level": level,
        "kind": kind,
        "prompt": prompt,
        "starter": starter,
        "stdin": stdin,
        "verify": verify,
        "expectError": expect_error,
        "choices": choices or [],
        "answer": answer,
        "explanation": explanation,
        "hint": hint,
        "solution": solution,
    }


QUESTIONS: List[Dict[str, Any]] = [
    # =====================================================================
    # 1) MATRISLER  (1-10)
    # =====================================================================
    Q(
        1, "Matrisler", "Matris karesi", 4,
        "`A = [1 2; 3 4]` için **matris karesi** (`A^2`) ile **eleman eleman kare** "
        "(`A.^2`) arasındaki farkı `sonuc` olarak ata. (İki matris aynı boyutta "
        "olduğu için eleman eleman çıkarabilirsin.)",
        verify="chk(sonuc, [6 6; 6 6], 'sonuc');",
        starter="A = [1 2; 3 4];\n\n",
        hint="`A^2` = `A*A` matris çarpımıdır → `[7 10; 15 22]`. `A.^2` ise her "
             "elemanın karesidir → `[1 4; 9 16]`. Fark: `[6 6; 6 6]`. "
             "`^` çarpma/çıkarma'dan önce gelir, o yüzden `A^2 - A.^2` doğru yazımdır.",
        solution="A = [1 2; 3 4];\nsonuc = A^2 - A.^2;",
    ),
    Q(
        2, "Matrisler", "Satır ve sütun toplamları", 4,
        "`A = [1 2 3; 4 5 6; 7 8 9]` için **satır toplamlarını** `satirToplam` "
        "(sütun vektörü), **sütun toplamlarını** `sutunToplam` (satır vektörü) olarak "
        "ata. Sonra bu ikisinin **skaler çarpımını** `sonuc` olarak hesapla.",
        verify="chk(satirToplam, [6; 15; 24], 'satirToplam');\n"
               "chk(sutunToplam, [12 15 18], 'sutunToplam');\nchk(sonuc, 729, 'sonuc');",
        hint="`sum(A,2)` satır toplamlarını (sütun vektörü), `sum(A,1)` sütun "
             "toplamlarını (satır vektörü) verir. Skaler çarpım için boyutları "
             "eşitle: `dot(satirToplam(:), sutunToplam(:))` ya da "
             "`satirToplam' * sutunToplam'`.",
        solution="A = [1 2 3; 4 5 6; 7 8 9];\nsatirToplam = sum(A,2);\n"
                 "sutunToplam = sum(A,1);\nsonuc = dot(satirToplam(:), sutunToplam(:));",
    ),
    Q(
        3, "Matrisler", "Transpoz", 1,
        "`A = [1 2 3; 4 5 6]` matrisinin transpozunu `sonuc` olarak ata.",
        verify="chk(sonuc, [1 4; 2 5; 3 6], 'sonuc');",
        hint="MATLAB'de transpoz `A'` ile alınır. Satırlar sütun olur.",
        solution="A = [1 2 3; 4 5 6];\nsonuc = A';",
    ),
    Q(
        4, "Matrisler", "Matris çarpımı", 2,
        "`A = [1 2; 3 4]` ve `B = [5 6; 7 8]` için matris çarpımını `sonuc` olarak ata.\n\n"
        "İpucu: `(m×n)·(n×p) → m×p` — iç boyutlar eşit olmalı.",
        verify="chk(sonuc, [19 22; 43 50], 'sonuc');",
        starter="A = [1 2; 3 4];\nB = [5 6; 7 8];\n\n",
        hint="A*B matris çarpımıdır (her satır, karşı sütunla skaler çarpılır toplanır). "
             "Sonuç 2×2 olmalı. `A*B` ile `B*A` aynı sonucu vermez.",
        solution="A = [1 2; 3 4];\nB = [5 6; 7 8];\nsonuc = A*B;",
    ),
    Q(
        5, "Matrisler", "Eleman eleman işlemler", 2,
        "Aynı A ve B için **eleman eleman** çarpımı sonucunu `sonuc` olarak ata.",
        verify="chk(sonuc, [5 12; 21 32], 'sonuc');",
        starter="A = [1 2; 3 4];\nB = [5 6; 7 8];\n\n",
        hint="Eleman eleman işlemler nokta ile yapılır: `.*` , `./` , `.^`.",
        solution="A = [1 2; 3 4];\nB = [5 6; 7 8];\nsonuc = A.*B;",
    ),
    Q(
        6, "Matrisler", "Özel matrisler", 2,
        "Birim matrisin (`eye(3)`) köşegenindeki değerlerin toplamını `sonuc` olarak ata.",
        verify="chk(sonuc, 3, 'sonuc');",
        hint="`eye(3)` 3×3 birim matristir, köşegeninde 1'ler vardır. "
             "`sum(diag(eye(3)))` işe yarar.",
        solution="sonuc = sum(diag(eye(3)));",
    ),
    Q(
        7, "Matrisler", "Satır ve sütun seçimi", 3,
        "`A = [1 2 3; 4 5 6; 7 8 9]` matrisinin **2. satırını sıfırlarla değiştir** "
        "ve matrisin son halini `sonuc` olarak ata.",
        verify="chk(sonuc, [1 2 3; 0 0 0; 7 8 9], 'sonuc');",
        hint="`: ` o boyuttaki tüm elemanları seçer. `A(2,:) = 0` yazmak 2. satırın "
             "tamamını sıfırlar — atama yapabilirsin.",
        solution="A = [1 2 3; 4 5 6; 7 8 9];\nA(2,:) = 0;\nsonuc = A;",
    ),
    Q(
        8, "Matrisler", "Satır ve sütun seçimi", 2,
        "`A = [1 2 3; 4 5 6; 7 8 9]` matrisinin **2. sütununu** `sonuc` olarak ata.",
        verify="chk(sonuc, [2; 5; 8], 'sonuc');",
        hint="Sütun seçerken satır yerine `:` yazılır ve sonuç sütun vektörüdür: `A(:,2)`.",
        solution="A = [1 2 3; 4 5 6; 7 8 9];\nsonuc = A(:,2);",
    ),
    Q(
        9, "Matrisler", "Boyut uyuşmazlığı", 3,
        "Aşağıdaki kod **hata vermelidir**. Kodu yaz ve hatayı bilinçli olarak üret.\n\n"
        "`[1 2 3] + [10 20]` — 1×3 ile 1×2 toplanamaz.",
        kind="error",
        expect_error="nonconformant|incompatible sizes|dimensions must match|"
                     "operator \\+: nonconformant",
        starter="sonuc = [1 2 3] + [10 20];\n",
        hint="Toplama ve çıkarma eleman eleman çalışır; boyutlar uyuşmalıdır. "
             "Bu hata MATLAB'de \"Arrays have incompatible sizes for this operation\" "
             "şeklinde raporlanır.",
        solution="sonuc = [1 2 3] + [10 20];  % boyutlar uyuşmuyor -> hata",
    ),
    Q(
        10, "Matrisler", "Simetri", 2,
        "`A = [1 2; 2 5]` simetrik bir matristir. `A` ile transpozu `isequal` ile "
        "karşılaştırıp sonucu (1 = simetrik, 0 = değil) `sonuc` olarak ata.",
        verify="chkBool(sonuc, 1, 'sonuc');",
        hint="`isequal(A, A')` tam olarak senin istediğin kontrol.",
        solution="A = [1 2; 2 5];\nsonuc = isequal(A, A');",
    ),
    # =====================================================================
    # 2) MATLAB ORTAMI VE KOMUTLAR  (11-16)
    # =====================================================================
    Q(
        11, "MATLAB Ortamı", "Temel komutlar", 1,
        "Çalışma alanındaki **tüm değişkenleri silen** komutu `sonuc` değişkenine yaz.\n\n"
        "İpucu: komut `clear` komutuyla aynı olmalı.",
        verify="chk(sonuc, 'clear', 'sonuc');",
        hint="`clear` tüm değişkenleri siler, `clc` ise yalnızca ekranı temizler. "
             "Metin olarak yazmak için tek tırnak kullan.",
        solution="sonuc = 'clear';",
    ),
    Q(
        12, "MATLAB Ortamı", "Komut Penceresi", 1,
        "Kendi adınızı ekrana yazdırmak için `fprintf` kullanın. Çıktı tam olarak "
        "`Merhaba` olmalı. Yazdırma komutunu `sonuc` değişkenine yazın.",
        verify="chk(sonuc, 'fprintf(''Merhaba\\n'')', 'sonuc');",
        hint="`fprintf('Merhaba\\n')` ekrana yazar. Değişkene atarken metni tek "
             "tırnak içinde yazmalısın.",
        solution="sonuc = 'fprintf(''Merhaba\\n'')';",
    ),
    Q(
        13, "MATLAB Ortamı", "Dosya komutları", 2,
        "Çalışma klasörünün tam yolunu gösteren komutu `sonuc` değişkenine yaz.",
        verify="chk(sonuc, 'pwd', 'sonuc');",
        hint="`pwd` = print working directory.",
        solution="sonuc = 'pwd';",
    ),
    Q(
        14, "MATLAB Ortamı", "Yardım", 2,
        "Bir fonksiyonun ayrıntılı dokümantasyonunu açan komutu `sonuc` değişkenine yaz.",
        verify="chk(sonuc, 'doc', 'sonuc');",
        hint="`help` kısa açıklama, `doc` ayrıntılı belge sayfası açar. "
             "`lookfor` ise kelime arar.",
        solution="sonuc = 'doc';",
    ),
    Q(
        15, "MATLAB Ortamı", "Betik dosyası", 2,
        "İlk satırı `%%` ile başlayan bir **betik bölümü** oluşturan kodu `sonuc` "
        "değişkenine yaz.",
        verify="chk(sonuc, '%%', 'sonuc');",
        hint="`%%` hücre (section) işaretidir; `Ctrl+Enter` ile sadece o bölüm çalışır.",
        solution="sonuc = '%%';",
    ),
    Q(
        16, "MATLAB Ortamı", "Değişken listeleme", 2,
        "Değişkenleri **boyut, bayt ve tip bilgisiyle** listeleyen komutu `sonuc` "
        "değişkenine yaz. (Sadece isimleri değil, `whos`.)",
        verify="chk(sonuc, 'whos', 'sonuc');",
        hint="`who` sadece isimleri listeler; `whos` ayrıntılı tablo üretir.",
        solution="sonuc = 'whos';",
    ),
    # =====================================================================
    # 3) DEGISKENLER VE ISIMLENDIRME  (17-23)
    # =====================================================================
    Q(
        17, "Değişkenler", "Atama", 1,
        "`x = 10` ve `y = x * 2` atamalarını yapıp `y` değerini `sonuc` olarak ata.",
        verify="chk(sonuc, 20, 'sonuc');",
        starter="x = 10;\n\n",
        hint="Atamada `=` kullanılır; sağdaki ifade önce hesaplanır.",
        solution="x = 10;\ny = x * 2;\nsonuc = y;",
    ),
    Q(
        18, "Değişkenler", "Aynı satırda atama", 1,
        "Virgülle aynı satırda iki değişken atayan ve `a + b` toplamını `sonuc` "
        "yapan kodu yaz. `a = 1`, `b = 2` olsun.",
        verify="chk(sonuc, 3, 'sonuc');",
        hint="`a = 1, b = 2` virgülle ayrılmış iki atamadır.",
        solution="a = 1, b = 2;\nsonuc = a + b;",
    ),
    Q(
        19, "Değişkenler", "Geçerlilik", 2,
        "**Geçerli** bir değişken adı olan seçeneği `sonuc` değişkenine yaz. "
        "Seçenekler: `2sayi`, `toplam_2`, `ogrenci no`, `for`",
        verify="chk(sonuc, 'toplam_2', 'sonuc');",
        hint="Değişken adı harfle başlamalı, yalnızca harf/rakam/alt çizgi içerebilir, "
             "ayrılmış sözcük olamaz.",
        solution="sonuc = 'toplam_2';",
    ),
    Q(
        20, "Değişkenler", "Büyük/küçük harf", 2,
        "`alan = 1` ve `Alan = 2` olmak üzere iki değişken oluştur. `Alan` değerini "
        "`sonuc` olarak ata.",
        verify="chk(sonuc, 2, 'sonuc');",
        hint="MATLAB büyük/küçük harfe duyarlıdır; `alan` ile `Alan` farklı değişkenlerdir.",
        solution="alan = 1;\nAlan = 2;\nsonuc = Alan;",
    ),
    Q(
        21, "Değişkenler", "Hazır değişkenler", 2,
        "Sanal birim küpünü (i³) `sonuc` olarak ata. `i` değişkeni **tanımsız** kalmalı. "
        "(Sonuç −i olmalı: gerçek kısmı 0, sanal kısmı −1.)",
        verify="chkTrue(iscomplex(sonuc) && abs(real(sonuc)) < 1e-12 && abs(imag(sonuc) + 1) < 1e-12, 'sonuç doğru', 'sonuç yanlış');",
        hint="`i` adı bir değişken olarak kullanılırsa MATLAB onu gerçek sanal birim "
             "olarak kullanmaz. Bu yüzden `1i` yazılır. (1i)³ = −i.",
        solution="sonuc = (1i)^3;",
    ),
    Q(
        22, "Değişkenler", "Sihirli değerler", 2,
        "`0/0` sonucunu `sonuc` olarak ata ve `isnan(sonuc)` kontrolünün 1 olduğunu "
        "doğrula.",
        verify="chkTrue(isnan(sonuc), 'NaN doğru', 'NaN değil');",
        hint="0/0 MATLAB'de hata vermez, `NaN` üretir. "
             "(Not: `isequal(NaN,NaN)` MATLAB'de 1, Octave'de 0 döner — o yüzden "
             "`isnan` kullan.)",
        solution="sonuc = 0/0;",
    ),
    Q(
        23, "Değişkenler", "Atama zinciri", 3,
        "Tek satırda virgülle `p = 3` ve `q = 4` ata, ardından `sonuc = p^2 + q^2` "
        "değerini hesapla. (Pythagoras: sonuç 25 olmalı.)",
        verify="chk(sonuc, 25, 'sonuc');",
        hint="Virgülle ayrılmış atamalar aynı satırda yapılabilir.",
        solution="p = 3, q = 4;\nsonuc = p^2 + q^2;",
    ),
    # =====================================================================
    # 4) RAKAMLAR, SAYILAR, TIPLER  (24-31)
    # =====================================================================
    Q(
        24, "Sayılar", "Kayan nokta ve üretim", 5,
        "0 ile 1 arasında **11 nokta** üreten iki yol var: `0:0.1:1` ve "
        "`linspace(0,1,11)`. İki vektörün `isequal` ile **tam** karşılaştırmasının "
        "sonucunu `sonuc` (1 = birebir aynı, 0 = değil) olarak ata. Sonra aynı "
        "vektörleri **toleransla** karşılaştırıp sonucu `toleransli` olarak ata. "
        "Farkı göreceksin.",
        verify="chkBool(sonuc, 0, 'sonuc');\nchkBool(toleransli, 1, 'toleransli');",
        hint="`isequal` **birebir** karşılaştırır; `0.1` ikili sistemde tam "
             "olmadığı için iki vektör bit bit aynı olmaz. Toleranslı kontrol: "
             "`max(abs(a-b)) < 1e-12`.",
        solution="a = 0:0.1:1;\nb = linspace(0,1,11);\nsonuc = isequal(a,b);\n"
                 "toleransli = max(abs(a-b)) < 1e-12;",
    ),
    Q(
        25, "Sayılar", "Kayan nokta", 2,
        "`0.1 + 0.2 == 0.3` ifadesinin sonucunu `sonuc` olarak ata.",
        verify="chkBool(sonuc, 0, 'sonuc');",
        hint="0.1 ikili sistemde tam temsil edilemez; bu yüzden `==` sonucu **0** (yanlış) çıkar.",
        solution="sonuc = (0.1 + 0.2 == 0.3);",
    ),
    Q(
        26, "Sayılar", "Toleranslı karşılaştırma", 3,
        "`0.1 + 0.2` ile `0.3` farkının `1e-10`'dan küçük olup olmadığını kontrol edip "
        "sonucu (1 = küçük, 0 = değil) `sonuc` olarak ata.",
        verify="chkBool(sonuc, 1, 'sonuc');",
        hint="`abs(0.1+0.2-0.3) < 1e-10` — kayan noktada `==` yerine tolerans kullanılır.",
        solution="sonuc = abs(0.1 + 0.2 - 0.3) < 1e-10;",
    ),
    Q(
        27, "Sayılar", "Veri tipleri", 2,
        "`int8(200)` ifadesinin sonucunu `sonuc` olarak ata.",
        verify="chk(sonuc, 127, 'sonuc');",
        hint="`int8` aralığı -128..127'dir; sınırların dışındaki değerler **doygunluğa** uğrar.",
        solution="sonuc = int8(200);",
    ),
    Q(
        28, "Sayılar", "Veri tipleri", 2,
        "`uint8(3.7)` ifadesinin sonucunu `sonuc` olarak ata.",
        verify="chk(sonuc, 4, 'sonuc');",
        hint="İşaretsiz tam sayıya dönüştürürken MATLAB en yakın tam sayıya **yuvarlar**.",
        solution="sonuc = uint8(3.7);",
    ),
    Q(
        29, "Sayılar", "Sihirli değerler", 2,
        "`1/0` sonucunun `Inf` olduğunu doğrulayan bir ifade yazıp `sonuc` olarak ata. "
        "(`isinf` kullan.)",
        verify="chkTrue(isinf(sonuc), 'Inf dogru', 'Inf degil');\n"
               "chk(sonuc, Inf, 'sonuc');",
        hint="`isinf(x)` sonsuz mu diye bakar.",
        solution="sonuc = 1/0;",
    ),
    Q(
        30, "Sayılar", "Format", 3,
        "`format long` komutuyla gösterilecek `pi` değerini `sonuc` olarak ata "
        "(tam double hassasiyeti).",
        verify="chkTol(sonuc, 3.141592653589793, 1e-15, 'sonuc');",
        hint="`format long` yalnızca **gösterimi** değiştirir, hesaplama daima tam "
             "double hassasiyetindedir.",
        solution="format long\nsonuc = pi;",
    ),
    Q(
        31, "Sayılar", "Karmaşık sayılar", 3,
        "`z = 3 + 4i` için karmaşık sayının **modülünü** `sonuc` olarak ata.",
        verify="chk(sonuc, 5, 'sonuc');",
        hint="`abs(z)` karmaşık sayının modülünü (büyüklüğünü) verir.",
        solution="z = 3 + 4i;\nsonuc = abs(z);",
    ),
    # =====================================================================
    # 5) TEMEL FONKSIYONLAR  (32-39)
    # =====================================================================
    Q(
        32, "Fonksiyonlar", "İç içe hücre erişimi", 5,
        "`c = {{1, 2}, 'metin', [3 4 5]}` hücre dizisinin **1. hücresinin içinde** "
        "bulunan 2. elemanı `sonuc` olarak ata. (Hücrelerin içi de hücre olabilir.)",
        verify="chk(sonuc, 2, 'sonuc');",
        hint="`c{1}` ilk hücrenin **içeriğini** verir; o içerik de bir hücre dizisi "
             "olduğu için bir kez daha `{}` kullanırsın: `c{1}{2}`.",
        solution="c = {{1, 2}, 'metin', [3 4 5]};\nsonuc = c{1}{2};",
    ),
    Q(
        33, "Fonksiyonlar", "Kök ve üs", 2,
        "`-27` sayısının **3. dereceden gerçek kökünü** `sonuc` olarak ata.",
        verify="chkTol(sonuc, -3, 1e-12, 'sonuc');",
        hint="`nthroot(x,n)` n. dereceden gerçel kök verir. `(-27)^(1/3)` karmaşık "
             "sonuç verir — `nthroot` kullan.",
        solution="sonuc = nthroot(-27, 3);",
    ),
    Q(
        34, "Fonksiyonlar", "Logaritma", 2,
        "`log(exp(2))` ifadesinin sonucunu `sonuc` olarak ata.",
        verify="chkTol(sonuc, 2, 1e-12, 'sonuc');",
        hint="`log` doğal logaritmadır (ln). `exp` ise e üzeri.",
        solution="sonuc = log(exp(2));",
    ),
    Q(
        35, "Fonksiyonlar", "Trigonometri", 2,
        "**30 derece**nin sinüsünü `sind` kullanarak `sonuc` olarak ata.",
        verify="chkTol(sonuc, 0.5, 1e-12, 'sonuc');",
        hint="`sin` radyan, `sind` derece ile çalışır.",
        solution="sonuc = sind(30);",
    ),
    Q(
        36, "Fonksiyonlar", "Trigonometri", 3,
        "`sin(pi)` ifadesinin **mutlak değerinin** `1e-15`'ten küçük olup olmadığını "
        "kontrol edip sonucu (1 = küçük, 0 = değil) `sonuc` olarak ata.",
        verify="chkBool(sonuc, 1, 'sonuc');",
        hint="`sin(pi)` teorik olarak 0'dır ama kayan nokta hatası nedeniyle "
             "`1.2246e-16` gibi küçük bir değer çıkar; yani mutlak değeri "
             "`1e-15`'ten küçüktür. Karşılaştırma `abs(sin(pi)) < 1e-15` şeklinde yazılır.",
        solution="sonuc = abs(sin(pi)) < 1e-15;",
    ),
    Q(
        37, "Fonksiyonlar", "Yuvarlama", 2,
        "`2.5` sayısını `round`, `floor`, `ceil` ve `fix` ile yuvarlayıp sonuçları sırasıyla "
        "`r`, `f`, `c`, `x` değişkenlerine ata.",
        verify="chk(r, 3, 'round');\nchk(f, 2, 'floor');\n"
               "chk(c, 3, 'ceil');\nchk(x, 2, 'fix');",
        starter="v = 2.5;\n\n",
        hint="round: en yakına (yarımda sıfırdan uzağa) · floor: aşağı · ceil: yukarı · "
             "fix: sıfıra doğru.",
        solution="v = 2.5;\nr = round(v);\nf = floor(v);\nc = ceil(v);\nx = fix(v);",
    ),
    Q(
        38, "Fonksiyonlar", "mod ve rem", 3,
        "`mod(-7,3)` ve `rem(-7,3)` sonuçlarını sırasıyla `m` ve `r` değişkenlerine ata. "
        "Farklı olduklarını göreceksin.",
        verify="chk(m, 2, 'mod');\nchk(r, -1, 'rem');",
        hint="`mod` bölenin işaretini alır (her zaman pozitif sonuç), `rem` bölünenin "
             "işaretini alır.",
        solution="m = mod(-7,3);\nr = rem(-7,3);",
    ),
    Q(
        39, "Fonksiyonlar", "Sayı kuramı", 3,
        "`12` ve `18` sayılarının en büyük ortak bölenini `sonuc` olarak ata.",
        verify="chk(sonuc, 6, 'sonuc');",
        hint="`gcd(a,b)` en büyük ortak böleni verir. (Küçük harf eşitlik harfiyle "
             "karıştırma — burada fonksiyon adı `gcd`.)",
        solution="sonuc = gcd(12,18);",
    ),
    # =====================================================================
    # 6) MATEMATIKTEN KODA  (40-46)
    # =====================================================================
    Q(
        40, "Matematikten Koda", "Çeviri", 2,
        "`x = 2` için `y = (sqrt(x^2 + 1) + exp(-x)) / abs(log(x))` ifadesini hesaplayıp "
        "`sonuc` olarak ata.",
        verify="chkTol(sonuc, 3.4212, 1e-3, 'sonuc');",
        starter="x = 2;\n\n",
        hint="Pay ve paydayı parantez içinde yaz. `exp(-x)` = e^(-x).",
        solution="x = 2;\nsonuc = (sqrt(x^2 + 1) + exp(-x)) / abs(log(x));",
    ),
    Q(
        41, "Matematikten Koda", "Çeviri", 3,
        "`a = 1`, `b = -3`, `c = 2` için `x² − 3x + 2 = 0` denkleminin köklerini "
        "`x1` ve `x2` değişkenlerine ata. (Kökler 1 ve 2 olmalı.)",
        verify="chkTol(sort([x1 x2]), [1 2], 1e-12, 'kokler');",
        starter="a = 1; b = -3; c = 2;\n\n",
        hint="Diskriminant: `D = b^2 - 4*a*c`. Kökler: `(-b ± sqrt(D))/(2*a)`. "
             "Paydayı `2*a` olarak yaz, yoksa önce 2'ye bölüp sonra `a` ile çarparsın.",
        solution="a = 1; b = -3; c = 2;\nD = b^2 - 4*a*c;\nx1 = (-b + sqrt(D))/(2*a);\n"
                 "x2 = (-b - sqrt(D))/(2*a);",
    ),
    Q(
        42, "Matematikten Koda", "Parantez tuzağı", 3,
        "`x = 2`, `y = 3` için `y = x + (y - x) / (x + y)` ifadesini hesaplayıp "
        "`sonuc` olarak ata.",
        verify="chkTol(sonuc, 2.2, 1e-12, 'sonuc');",
        hint="Öncelik sırası: parantez, üs, çarpma/bölme, toplama/çıkarma. "
             "`(y - x) / (x + y)` parantezleri olmadan yanlış sonuç verir.",
        solution="x = 2; y = 3;\nsonuc = x + (y - x) / (x + y);",
    ),
    Q(
        43, "Matematikten Koda", "Üs önceliği", 3,
        "`-2^2` ifadesinin sonucunu `sonuc` olarak ata.",
        verify="chk(sonuc, -4, 'sonuc');",
        hint="MATLAB'de `-2^2` = `-(2^2)` = -4. Negatif tabanı parantezle yazarsan "
             "`(-2)^2` = 4 olur.",
        solution="sonuc = -2^2;",
    ),
    Q(
        44, "Matematikten Koda", "Üs önceliği", 4,
        "`2^3^2` ifadesinin sonucunu `sonuc` olarak ata.",
        verify="chk(sonuc, 64, 'sonuc');",
        hint="Üs alma **sağdan sola** çalışır: `2^(3^2)` = 2^9 = 512? Hayır — "
             "MATLAB'de 2^3^2 = 2^(3^2) = 512 değil, soldan sağa: (2^3)^2 = 64.",
        solution="sonuc = 2^3^2;",
    ),
    Q(
        45, "Matematikten Koda", "Normal dağılım", 5,
        "`mu = 0`, `sigma = 1`, `x = 1` için normal dağılım yoğunluk fonksiyonunu "
        "`sonuc` olarak ata. Sonuç ≈ 0.2420 olmalı.",
        verify="chkTol(sonuc, 0.2420, 1e-3, 'sonuc');",
        starter="mu = 0; sigma = 1; x = 1;\n\n",
        hint="f(x) = 1/(σ·√(2π)) · exp(-(x-μ)²/(2σ²)). Uzun ifadeyi `...` ile "
             "iki satıra bölebilirsin.",
        solution="mu = 0; sigma = 1; x = 1;\nkatsayi = 1/(sigma*sqrt(2*pi));\n"
                 "us = -(x-mu)^2/(2*sigma^2);\nsonuc = katsayi * exp(us);",
    ),
    Q(
        46, "Matematikten Koda", "Bileşik faiz", 3,
        "Anapara `P = 1000`, yıllık faiz `r = 0.05`, 12'de bir bileşik faiz ve 10 yıl "
        "vade için toplam tutarı `sonuc` olarak ata. (Sonuç ≈ 1647.01.)",
        verify="chkTol(sonuc, 1647.0095, 0.01, 'sonuc');",
        starter="P = 1000; r = 0.05; n = 12; t = 10;\n\n",
        hint="A = P·(1 + r/n)^(n·t). Üs alma matris çarpımı değildir, tek sayıda.",
        solution="P = 1000; r = 0.05; n = 12; t = 10;\nsonuc = P*(1 + r/n)^(n*t);",
    ),
    # =====================================================================
    # 7) KULLANICI GIRDISI  (47-50)
    # =====================================================================
    Q(
        47, "Kullanıcı Girdisi", "input", 2,
        "Kullanıcıdan bir sayı isteyin (mesaj: `Sayi girin: `) ve aldığınız değeri "
        "`sonuc` olarak ata. Testte kullanıcı `5` giriyor.",
        stdin="5\n",
        verify="chk(sonuc, 5, 'sonuc');",
        starter="sonuc = input('Sayi girin: ');\n",
        hint="`input` varsayılan olarak girdiyi **ifade** olarak hesaplar, yani "
             "sayı döner.",
        solution="sonuc = input('Sayi girin: ');",
    ),
    Q(
        48, "Kullanıcı Girdisi", "input", 3,
        "Kullanıcıdan **metin** isteyin (mesaj: `Adiniz: `) ve girdiği metni "
        "`sonuc` olarak ata. Testte kullanıcı `Ali` giriyor.",
        stdin="Ali\n",
        verify="chk(sonuc, 'Ali', 'sonuc');",
        starter="sonuc = input('Adiniz: ', 's');\n",
        hint="Metin almak için `input` komutunun ikinci parametresi `'s'` olmalı. "
             "Aksi halde `Ali` ifade olarak yorumlanır ve hata verir.",
        solution="sonuc = input('Adiniz: ', 's');",
    ),
    Q(
        49, "Kullanıcı Girdisi", "input", 3,
        "Kullanıcıdan `25` girilen bir metni sayıya çevirip `sonuc` olarak ata. "
        "(`input(..., 's')` ile alınan metin.)",
        stdin="25\n",
        verify="chk(sonuc, 25, 'sonuc');",
        starter="s = input('Say: ', 's');\n\n",
        hint="`str2double(s)` metni sayıya çevirir.",
        solution="s = input('Say: ', 's');\nsonuc = str2double(s);",
    ),
    Q(
        50, "Kullanıcı Girdisi", "input", 3,
        "Öğrencinin vize (`70`) ve final (`85`) notunu alıp ağırlıklı ortalamasını "
        "`ort` değişkeninde hesapla (vize %40, final %60).",
        stdin="70\n85\n",
        verify="chkTol(ort, 79, 1e-12, 'ort');",
        starter="vize  = input('Vize notu: ');\nfinal = input('Final notu: ');\n\n",
        hint="Ağırlıklı ortalama: `0.4*vize + 0.6*final`.",
        solution="vize  = input('Vize notu: ');\nfinal = input('Final notu: ');\n"
                 "ort = 0.4*vize + 0.6*final;",
    ),
    # =====================================================================
    # 8) DIZILER VE VEKTOR URETIMI  (51-58)
    # =====================================================================
    Q(
        51, "Diziler", "İki nokta operatörü sınırı", 3,
        "`1:2:10`, `1:2:11` ve `1:2:12` vektörlerinin eleman sayılarını sırasıyla "
        "`n`, `m` ve `p` olarak ata. İki nokta operatöründe **bitiş değerine "
        "ulaşılıp ulaşılmadığına** dikkat et.",
        verify="chk(n, 5, 'n');\nchk(m, 6, 'm');\nchk(p, 6, 'p');",
        hint="`1:2:10` → 1,3,5,7,9 (5 eleman). `1:2:11` → 1,3,5,7,9,**11** (6 eleman) "
             "çünkü 11'e ulaşılabiliyor. `1:2:12` → yine 6 eleman; 12'ye ulaşılamaz "
             "ve son eleman bitişten küçük kalır.",
        solution="n = numel(1:2:10);\nm = numel(1:2:11);\np = numel(1:2:12);",
    ),
    Q(
        52, "Diziler", "İki nokta operatörü", 2,
        "`0`'dan `10`'a **2'şer adımla** (0,2,4,6,8,10) giden vektörü `sonuc` olarak ata.",
        verify="chk(sonuc, 0:2:10, 'sonuc');",
        hint="Sözdizimi: `baslangic:artış:bitis`.",
        solution="sonuc = 0:2:10;",
    ),
    Q(
        53, "Diziler", "İki nokta operatörü", 3,
        "`10`'dan `1`'e **-3'er adımla** (10,7,4,1) giden vektörü `sonuc` olarak ata.",
        verify="chk(sonuc, 10:-3:1, 'sonuc');",
        hint="Artış negatif olabilir.",
        solution="sonuc = 10:-3:1;",
    ),
    Q(
        54, "Diziler", "Boş dizi", 3,
        "`5:1` ifadesinin boyutunu `sonuc` olarak ata. (Bu **boş** bir dizidir.)",
        verify="chk(sonuc, [1 0], 'sonuc');",
        hint="Artış yönü yanlışsa MATLAB boş dizi döndürür: `size(5:1)` → `[1 0]`.",
        solution="sonuc = size(5:1);",
    ),
    Q(
        55, "Diziler", "Transpoz tuzağı", 3,
        "`1:4` ifadesi bir **satır** vektörüdür. Transpozunu alıp `sonuc` olarak ata. "
        "Ayrıca `1:4`'ün kendisini `satir` değişkenine ata ve satır olduğunu doğrula.",
        verify="chk(sonuc, [1; 2; 3; 4], 'sonuc');\n"
               "chkTrue(isrow(satir), 'satır bir satır vektörü', 'satır satır değil');",
        hint="Transpoz için parantez gerekir: `(1:4)'`. Parantez olmadan `1:4'` "
             "yazarsan MATLAB sözdizim hatası verir.",
        solution="satir = 1:4;\nsonuc = (1:4)';",
    ),
    Q(
        56, "Diziler", "linspace", 2,
        "`0` ile `1` arasında **5 eşit aralıklı** nokta üretip `sonuc` olarak ata.",
        verify="chk(sonuc, linspace(0,1,5), 'sonuc');",
        hint="`linspace(a, b, n)` — a ile b arasında n eşit aralıklı sayı (uçlar dahil).",
        solution="sonuc = linspace(0,1,5);",
    ),
    Q(
        57, "Diziler", "Boru hattı", 2,
        "`a = [1 2]` ve `b = [3 4]` için **yatay** birleştirmeyi `sonuc` olarak ata.",
        verify="chk(sonuc, [1 2 3 4], 'sonuc');",
        starter="a = [1 2]; b = [3 4];\n\n",
        hint="Yatay birleştirme `[a b]` ile yapılır. Dikey birleştirme `[a; b]`.",
        solution="a = [1 2]; b = [3 4];\nsonuc = [a b];",
    ),
    Q(
        58, "Diziler", "Boru hattı", 3,
        "`a = [1 2]` ve `b = [3 4]` için **dikey** birleştirmeyi `sonuc` olarak ata.",
        verify="chk(sonuc, [1 2; 3 4], 'sonuc');",
        starter="a = [1 2]; b = [3 4];\n\n",
        hint="Dikey birleştirme `[a; b]`. Satır sayıları eşit olmalıdır.",
        solution="a = [1 2]; b = [3 4];\nsonuc = [a; b];",
    ),
    # =====================================================================
    # 9) HAZIR DIZILER VE RASTGELELIK  (59-63)
    # =====================================================================
    Q(
        59, "Hazır Diziler", "zeros / ones", 2,
        "`2×3` boyutunda, tüm elemanları 1 olan diziyi `sonuc` olarak ata.",
        verify="chk(sonuc, ones(2,3), 'sonuc');",
        hint="`ones(m,n)` m satır n sütun. Tek argüman **kare** matris üretir: "
             "`ones(3)` → 3×3, vektör istiyorsan `ones(1,3)` yaz.",
        solution="sonuc = ones(2,3);",
    ),
    Q(
        60, "Hazır Diziler", "diag", 2,
        "`[4 2 9]` vektörünü köşegen matrise dönüştürüp `sonuc` olarak ata.",
        verify="chk(sonuc, diag([4 2 9]), 'sonuc');",
        hint="`diag(v)` v'yi köşegenine yerleştirir.",
        solution="sonuc = diag([4 2 9]);",
    ),
    Q(
        61, "Hazır Diziler", "repmat", 3,
        "`[1 2]` matrisini 2 satır 2 sütun olacak şekilde tekrar edip `sonuc` olarak ata.",
        verify="chk(sonuc, repmat([1 2],2,2), 'sonuc');",
        hint="`repmat(A,m,n)` A'yı m×n kez tekrarlar.",
        solution="sonuc = repmat([1 2],2,2);",
    ),
    Q(
        62, "Hazır Diziler", "rng", 3,
        "`rng(42)` ile üreteci sabitle, `rand(1,3)` ile üç rastgele sayı üret ve "
        "bunları `sonuc` değişkeninde sakla. Ardından **aynı tohumla** tekrar üretip "
        "iki vektörün `isequal` olup olmadığını `tekrar` değişkeninde belirt "
        "(1 = aynı, 0 = farklı).",
        verify="rng(42); __r1__ = rand(1,3);\nrng(42); __r2__ = rand(1,3);\n"
               "chk(sonuc, __r1__, 'sonuc');\nchk(tekrar, 1, 'tekrar');\n"
               "chkTrue(isequal(__r1__,__r2__), 'Tohum tekrarlanabilir', 'Tohum etkisiz');",
        starter="rng(42)\n\n",
        hint="`rng(tohum)` üreteci belirli bir başlangıca sabitler. Aynı tohum "
             "her zaman aynı sayıları üretir.",
        solution="rng(42)\na = rand(1,3);\nrng(42)\nb = rand(1,3);\nsonuc = a;\n"
                 "tekrar = isequal(a,b);",
    ),
    Q(
        63, "Hazır Diziler", "randi", 3,
        "`1` ile `6` arasında (uçlar dahil) rastgele bir zar atışı yaparak `zar` "
        "değişkenine ata ve bunun 1–6 aralığında olduğunu doğrula.",
        verify="chkTrue(zar >= 1 && zar <= 6, 'Zar geçerli', 'Zar geçersiz');\n"
               "chkTrue(zar == fix(zar), 'Zar tam sayı', 'Zar tam sayı değil');",
        hint="`randi(6)` 1–6 arası rastgele tam sayı üretir.",
        solution="zar = randi(6);",
    ),
    # =====================================================================
    # 10) ISTATISTIK VE TOPLULUK  (64-69)
    # =====================================================================
    Q(
        64, "İstatistik", "Not analizi", 3,
        "`notlar = [65 80 72 90 55]` için ortalamayı `ort`, **60'ın üstündeki** "
        "not sayısını `gecen` olarak hesapla. Sonra `gecen` notun toplam not "
        "sayısına oranını yüzde olarak `oran` değişkeninde tut.",
        verify="chkTol(ort, 72.4, 1e-12, 'ort');\nchk(gecen, 4, 'gecen');\n"
               "chk(oran, 80, 'oran');",
        starter="notlar = [65 80 72 90 55];\n\n",
        hint="`mean(notlar)` ortalama. Koşul maskesi `notlar >= 60` 0/1'lerden "
             "oluşur; `sum()` ile kaç tanesinin geçtiğini bulursun. Oran için "
             "`100 * gecen / numel(notlar)`.",
        solution="notlar = [65 80 72 90 55];\nort = mean(notlar);\n"
                 "gecen = sum(notlar >= 60);\noran = 100 * gecen / numel(notlar);",
    ),
    Q(
        65, "İstatistik", "Temel istatistikler", 2,
        "`v = [4 1 7 3 5]` vektörünün ortalamasını `sonuc` olarak ata.",
        verify="chkTol(sonuc, 4, 1e-12, 'sonuc');",
        starter="v = [4 1 7 3 5];\n\n",
        hint="`mean(v)` aritmetik ortalamadır.",
        solution="v = [4 1 7 3 5];\nsonuc = mean(v);",
    ),
    Q(
        66, "İstatistik", "İki çıktılı fonksiyonlar", 3,
        "`v = [4 1 7 3 5]` için en büyük elemanı `enBuyuk`, onun **indeksini** `konum` "
        "değişkenlerine ata.",
        verify="chk(enBuyuk, 7, 'enBuyuk');\nchk(konum, 3, 'konum');",
        starter="v = [4 1 7 3 5];\n\n",
        hint="`[m, i] = max(v)` iki çıktı verir: değer ve konum. "
             "`[~, i] = max(v)` yalnızca konumu alır.",
        solution="v = [4 1 7 3 5];\n[enBuyuk, konum] = max(v);",
    ),
    Q(
        67, "İstatistik", "Sıralama", 2,
        "`v = [4 1 7 3 5]` vektörünü büyükten küçüğe sıralayıp `sonuc` olarak ata.",
        verify="chk(sonuc, [7 5 4 3 1], 'sonuc');",
        starter="v = [4 1 7 3 5];\n\n",
        hint="`sort(v, 'descend')` azalan sıralama yapar.",
        solution="v = [4 1 7 3 5];\nsonuc = sort(v, 'descend');",
    ),
    Q(
        68, "İstatistik", "Kümülatif toplam", 2,
        "`v = [4 1 7 3 5]` vektörünün kümülatif toplamını `sonuc` olarak ata.",
        verify="chk(sonuc, cumsum(v), 'sonuc');",
        starter="v = [4 1 7 3 5];\n\n",
        hint="`cumsum(v)` kümülatif toplam vektörü verir: [4 5 12 15 20].",
        solution="v = [4 1 7 3 5];\nsonuc = cumsum(v);",
    ),
    Q(
        69, "İstatistik", "Sütun bazlı işlem", 3,
        "`A = [1 2 3; 4 5 6]` matrisinin **her sütununun toplamını** `sonuc` olarak ata. "
        "(Sonuç `[5 7 9]` olmalı — dikkat, satır toplamı DEĞİL.)",
        verify="chk(sonuc, [5 7 9], 'sonuc');",
        starter="A = [1 2 3; 4 5 6];\n\n",
        hint="Matrise uygulanan `sum` **sütun sütun** çalışır. Satır toplamı için "
             "`sum(A,2)` yazmalısın.",
        solution="A = [1 2 3; 4 5 6];\nsonuc = sum(A);",
    ),
    # =====================================================================
    # 11) NOKTA OPERATORLERI  (70-75)
    # =====================================================================
    Q(
        70, "Nokta Operatörleri", "Eleman eleman çarpma", 2,
        "`a = [1 2 3]` ve `b = [4 5 6]` için eleman eleman çarpımı yaparak `sonuc` "
        "olarak ata.",
        verify="chk(sonuc, [4 10 18], 'sonuc');",
        starter="a = [1 2 3]; b = [4 5 6];\n\n",
        hint="`.*` eleman eleman çarpma. `a*b` ise matris çarpımı denemesidir ve "
             "1×3 ile 1×3 boyutlarında hata verir.",
        solution="a = [1 2 3]; b = [4 5 6];\nsonuc = a .* b;",
    ),
    Q(
        71, "Nokta Operatörleri", "Eleman eleman bölme", 2,
        "`a = [1 2 3]` ve `b = [4 5 6]` için eleman eleman bölme yaparak `sonuc` "
        "olarak ata.",
        verify="chkTol(sonuc, [0.25 0.4 0.5], 1e-12, 'sonuc');",
        starter="a = [1 2 3]; b = [4 5 6];\n\n",
        hint="`./` eleman eleman bölme.",
        solution="a = [1 2 3]; b = [4 5 6];\nsonuc = a ./ b;",
    ),
    Q(
        72, "Nokta Operatörleri", "Eleman eleman üs", 2,
        "`a = [1 2 3]` için eleman eleman karesini `sonuc` olarak ata.",
        verify="chk(sonuc, [1 4 9], 'sonuc');",
        starter="a = [1 2 3];\n\n",
        hint="`.^` eleman eleman üs alma. Vektörü `^` ile karesi alınırsa hata verir.",
        solution="a = [1 2 3];\nsonuc = a .^ 2;",
    ),
    Q(
        73, "Nokta Operatörleri", "Skaler bölme", 3,
        "`v = [2 4 6]` vektörünün her elemanının tersini alarak `sonuc` olarak ata.",
        verify="chkTol(sonuc, [0.5 0.25 1/6], 1e-12, 'sonuc');",
        starter="v = [2 4 6];\n\n",
        hint="`1./v` gerekir. `1/v` yazarsan MATLAB `1` skalerini vektöre böler ve "
             "vektörün **her elemanını** 1'e böler — ama MATLAB'da `1/v` aslında "
             "`mrdivide` çağırır ve sonuç beklediğin gibi olmaz. Nokta şart.",
        solution="v = [2 4 6];\nsonuc = 1 ./ v;",
    ),
    Q(
        74, "Nokta Operatörleri", "Matris üssü", 3,
        "`A = [1 2; 3 4]` için `A^2` (matris karesi) sonucunu `sonuc` olarak ata.",
        verify="chk(sonuc, [7 10; 15 22], 'sonuc');",
        starter="A = [1 2; 3 4];\n\n",
        hint="`A^2` = `A*A`. `A.^2` ise her elemanın karesidir: `[1 4; 9 16]`.",
        solution="A = [1 2; 3 4];\nsonuc = A^2;",
    ),
    Q(
        75, "Nokta Operatörleri", "Boyut hatası", 3,
        "Aşağıdaki kod **hata vermelidir**: `a = [1 2 3]; b = [4 5 6]; sonuc = a * b;`\n\n"
        "İki 1×3 vektör matris çarpımı yapamaz.",
        kind="error",
        expect_error="nonconformant|dimensions must match|"
                     "incorrect dimensions for matrix multiplication",
        starter="a = [1 2 3]; b = [4 5 6];\nsonuc = a * b;\n",
        hint="`a * b` matris çarpımıdır; iç boyutlar eşit olmalı (1×3 · 1×3 uyumsuz). "
             "Aynı boyutta iki vektörü çarpmak istiyorsan `a * b'` kullan.",
        solution="a = [1 2 3]; b = [4 5 6];\nsonuc = a * b;  % 1x3 * 1x3 -> hata",
    ),
    # =====================================================================
    # 12) INDEKSLEME  (76-84)
    # =====================================================================
    Q(
        76, "İndeksleme", "Vektörde indeksleme", 1,
        "`v = [10 20 30 40 50]` vektörünün **son elemanını** `sonuc` olarak ata.",
        verify="chk(sonuc, 50, 'sonuc');",
        starter="v = [10 20 30 40 50];\n\n",
        hint="`v(end)` son elemanı verir.",
        solution="v = [10 20 30 40 50];\nsonuc = v(end);",
    ),
    Q(
        77, "İndeksleme", "Vektörde indeksleme", 2,
        "`v = [10 20 30 40 50]` vektörünün **sondan bir önceki** elemanını `sonuc` "
        "olarak ata.",
        verify="chk(sonuc, 40, 'sonuc');",
        starter="v = [10 20 30 40 50];\n\n",
        hint="`v(end-1)` sondan bir önceki elemanı verir.",
        solution="v = [10 20 30 40 50];\nsonuc = v(end-1);",
    ),
    Q(
        78, "İndeksleme", "Alt dizi", 2,
        "`v = [10 20 30 40 50]` vektörünün 2. ile 4. elemanları arasındaki alt diziyi "
        "`sonuc` olarak ata.",
        verify="chk(sonuc, [20 30 40], 'sonuc');",
        starter="v = [10 20 30 40 50];\n\n",
        hint="`v(2:4)` — iki nokta operatörüyle aralık seçimi.",
        solution="v = [10 20 30 40 50];\nsonuc = v(2:4);",
    ),
    Q(
        79, "İndeksleme", "Seçici indeksleme", 3,
        "`v = [10 20 30 40 50]` vektörünün 1., 3. ve 5. elemanlarını `sonuc` olarak ata.",
        verify="chk(sonuc, [10 30 50], 'sonuc');",
        starter="v = [10 20 30 40 50];\n\n",
        hint="İndeks vektörü kullan: `v([1 3 5])`.",
        solution="v = [10 20 30 40 50];\nsonuc = v([1 3 5]);",
    ),
    Q(
        80, "İndeksleme", "Ters sıra", 2,
        "`v = [10 20 30 40 50]` vektörünü ters sırada `sonuc` olarak ata.",
        verify="chk(sonuc, [50 40 30 20 10], 'sonuc');",
        starter="v = [10 20 30 40 50];\n\n",
        hint="`v(end:-1:1)` — `end`'den 1'e doğru azalan adım.",
        solution="v = [10 20 30 40 50];\nsonuc = v(end:-1:1);",
    ),
    Q(
        81, "İndeksleme", "Doğrusal indeksleme", 5,
        "`A = [1 2 3; 4 5 6; 7 8 9]` matrisinin **doğrusal 5. elemanını** `sonuc` "
        "olarak ata. (MATLAB elemanları sütun sütun saklar.)",
        verify="chk(sonuc, 5, 'sonuc');",
        starter="A = [1 2 3; 4 5 6; 7 8 9];\n\n",
        hint="Doğrusal sıra: 1,2,3 (1. sütun) · 4,5,6 (2. sütun) · 7,8,9 (3. sütun). "
             "5. eleman = 2. sütunun 2. satırı = 5.",
        solution="A = [1 2 3; 4 5 6; 7 8 9];\nsonuc = A(5);",
    ),
    Q(
        82, "İndeksleme", "Mantıksal indeksleme", 3,
        "`v = [10 20 30 40 50]` vektöründe **25'ten büyük** elemanları `sonuc` olarak ata.",
        verify="chk(sonuc, [30 40 50], 'sonuc');",
        starter="v = [10 20 30 40 50];\n\n",
        hint="Koşulu indeks olarak kullan: `v(v > 25)`. Koşul 0/1'lerden oluşan bir "
             "maske üretir; 1 olan konumlar seçilir.",
        solution="v = [10 20 30 40 50];\nsonuc = v(v > 25);",
    ),
    Q(
        83, "İndeksleme", "Mantıksal indeksleme", 4,
        "`v = [10 20 30 40 50]` vektöründe **25'ten büyük** elemanların **indekslerini** "
        "`sonuc` olarak ata.",
        verify="chk(sonuc, [3 4 5], 'sonuc');",
        starter="v = [10 20 30 40 50];\n\n",
        hint="`find(v > 25)` koşulu sağlayan elemanların indekslerini verir.",
        solution="v = [10 20 30 40 50];\nsonuc = find(v > 25);",
    ),
    Q(
        84, "İndeksleme", "Atama ve silme", 3,
        "`v = [10 20 30 40 50]` vektöründe 2. elemanı `99` ile değiştir ve sonucu "
        "`sonuc` olarak ata.",
        verify="chk(sonuc, [10 99 30 40 50], 'sonuc');",
        starter="v = [10 20 30 40 50];\n\n",
        hint="Doğrudan indeks ataması: `v(2) = 99;`",
        solution="v = [10 20 30 40 50];\nv(2) = 99;\nsonuc = v;",
    ),
    # =====================================================================
    # 13) HUCRE VE YAPI DIZILERI  (85-91)
    # =====================================================================
    Q(
        85, "Hücre ve Yapı", "Hücre dizisi oluşturma", 2,
        "`{42, 'Ali', [1 2 3]}` hücre dizisini `c` değişkeninde oluştur ve `c` "
        "değişkeninin **boyutunu** `sonuc` olarak ata.",
        verify="chkSize(c, [1 3], 'c');\nchk(sonuc, [1 3], 'sonuc');",
        starter="c = {42, 'Ali', [1 2 3]};\n\n",
        hint="Hücre dizisi süslü parantezle oluşur: `{...}`. `size(c)` → `[1 3]`.",
        solution="c = {42, 'Ali', [1 2 3]};\nsonuc = size(c);",
    ),
    Q(
        86, "Hücre ve Yapı", "Hücre içeriğine erişim", 3,
        "`c = {42, 'Ali', [1 2 3]}` hücre dizisinin **2. hücresinin içeriğini** "
        "`sonuc` olarak ata.",
        verify="chk(sonuc, 'Ali', 'sonuc');",
        starter="c = {42, 'Ali', [1 2 3]};\n\n",
        hint="`c(2)` hücrenin **kendisini** (bir cell) verir; `c{2}` **içeriğini** "
             "(char 'Ali') verir.",
        solution="c = {42, 'Ali', [1 2 3]};\nsonuc = c{2};",
    ),
    Q(
        87, "Hücre ve Yapı", "Hücre içeriğine erişim", 5,
        "`c = {42, 'Ali', [1 2 3]}` hücre dizisinin 3. hücresindeki vektörün **2. "
        "elemanını** `sonuc` olarak ata.",
        verify="chk(sonuc, 2, 'sonuc');",
        starter="c = {42, 'Ali', [1 2 3]};\n\n",
        hint="Önce hücrenin içeriğini al, sonra indeksle: `c{3}(2)`. "
             "`c{3}` içeriği (vektör), `(2)` onun 2. elemanı.",
        solution="c = {42, 'Ali', [1 2 3]};\nsonuc = c{3}(2);",
    ),
    Q(
        88, "Hücre ve Yapı", "Hücreye atama", 3,
        "`c = {42, 'Ali'}` hücre dizisinin 2. hücresini `'Veli'` ile değiştir ve "
        "`sonuc` olarak `c` dizisini ata.",
        verify="chk(sonuc{2}, 'Veli', 'sonuc{2}');\nchkSize(sonuc, [1 2], 'sonuc');",
        starter="c = {42, 'Ali'};\n\n",
        hint="Hücre içeriğine atama: `c{2} = 'Veli';`",
        solution="c = {42, 'Ali'};\nc{2} = 'Veli';\nsonuc = c;",
    ),
    Q(
        89, "Hücre ve Yapı", "Yapı dizisi", 3,
        "`ogr.ad = 'Ayşe'` şeklinde tek bir kayıt oluşturan yapıyı `s` değişkeninde "
        "oluştur ve `s.ad` değerini `sonuc` olarak ata.",
        verify="chk(sonuc, 'Ayşe', 'sonuc');",
        starter="s.ad = 'Ayşe';\n\n",
        hint="Yapı alanlarına nokta ile erişilir.",
        solution="s.ad = 'Ayşe';\nsonuc = s.ad;",
    ),
    Q(
        90, "Hücre ve Yapı", "Yapı fonksiyonları", 3,
        "`s = struct('ad','Ali','no',2025002)` yapısındaki **alan adlarını** `alanlar` "
        "değişkeninde, `s.no` değerini `no` değişkeninde topla.",
        verify="chkTrue(numel(alanlar)==2 && any(strcmp(alanlar,'ad')) && any(strcmp(alanlar,'no')), 'Alan adları doğru', 'Alan adları yanlış');\nchk(no, 2025002, 'no');",
        starter="s = struct('ad','Ali','no',2025002);\n\n",
        hint="`fieldnames(s)` alan adlarını hücre dizisi olarak döndürür.",
        solution="s = struct('ad','Ali','no',2025002);\nalanlar = fieldnames(s);\nno = s.no;",
    ),
    Q(
        91, "Hücre ve Yapı", "Yapı dizisi", 4,
        "`ogr(1).not = 85`, `ogr(2).not = 70` şeklinde iki kayıtlı yapı dizisi oluştur "
        "ve notların ortalamasını `ort` değişkeninde hesapla.",
        verify="chkTol(ort, 77.5, 1e-12, 'ort');\nchkSize(ogr, [1 2], 'ogr');",
        starter="ogr(1).not = 85;\nogr(2).not = 70;\n\n",
        hint="`[ogr.not]` aynı alanı tüm kayıtlardan bir vektörde toplar.",
        solution="ogr(1).not = 85;\nogr(2).not = 70;\nort = mean([ogr.not]);",
    ),
    # =====================================================================
    # 14) SAVE / LOAD  (92-94)
    # =====================================================================
    Q(
        92, "save/load", "save komutu", 4,
        "`x = 1:5` değişkenini `veri.mat` dosyasına **gerçekten kaydet** (save "
        "komutunu çalıştır). Dosyanın oluştuğunu ve içinden `x`'in geri "
        "yüklendiğini doğrula: yüklenen değer `sonuc`, kullandığın save komutu "
        "`komut` değişkeninde olsun.",
        verify="chkTrue(ischar(komut) && ~isempty(strfind(komut,'save')) && ~isempty(strfind(komut,'veri.mat')), 'save komutu dogru', 'save komutu eksik');\n"
               "chkTrue(exist('veri.mat','file')==2, 'veri.mat olustu', 'veri.mat olusmadi');\n"
               "S = load('veri.mat');\nchk(S.x, 1:5, 'S.x');",
        hint="`save('veri.mat','x')` komutu çalıştırıldığında gerçekten dosya "
             "oluşur. `load('veri.mat')` çıktıya atanırsa bir **yapı** döner ve "
             "değişkenlere `S.x` ile ulaşılır.",
        solution="x = 1:5;\nkomut = 'save(''veri.mat'',''x'')';\neval(komut);\n"
                 "S = load('veri.mat');\nsonuc = S.x;",
    ),
    Q(
        93, "save/load", "load komutu", 2,
        "`veri.mat` dosyasındaki **tüm** değişkenleri geri yükleyen `load` komutunu "
        "`sonuc` değişkenine yaz.",
        verify="chk(sonuc, 'load veri.mat', 'sonuc');",
        hint="`load('veri.mat')` de aynı işi yapar; parantezli yazım tercih edilir.",
        solution="sonuc = 'load veri.mat';",
    ),
    Q(
        94, "save/load", "Çıktıya atama", 3,
        "`veri.mat` dosyasını bir **yapı** olarak yükleyen komutu `sonuc` değişkenine yaz. "
        "(Yükleme çıktıya atanırsa her değişken bir alan olur.)",
        verify="chk(sonuc, 'S = load(''veri.mat'')', 'sonuc');",
        hint="`S = load('veri.mat')` → `S` bir struct, değişkenlere `S.x` ile ulaşılır.",
        solution="sonuc = 'S = load(''veri.mat'')';",
    ),
    # =====================================================================
    # 15) OPERATORLER, KARSILASTIRMA, MANTIK  (95-100)
    # =====================================================================
    Q(
        95, "Operatörler", "== ve = farkı", 2,
        "`x = 5` atamasından sonra `x == 5` karşılaştırmasının sonucunu `sonuc` "
        "olarak ata.",
        verify="chkBool(sonuc, 1, 'sonuc');",
        starter="x = 5;\n\n",
        hint="`=` atama, `==` karşılaştırma. Karşılaştırma 1 (doğru) veya 0 (yanlış) "
             "döndürür. `x ~= 5` ise 0 verir.",
        solution="x = 5;\nsonuc = x == 5;",
    ),
    Q(
        96, "Operatörler", "Eşit değil", 2,
        "`5 ~= 3` ifadesinin sonucunu `sonuc` olarak ata.",
        verify="chkBool(sonuc, 1, 'sonuc');",
        hint="MATLAB'te `!=` **yoktur**; eşit değil `~=` ile yazılır.",
        solution="sonuc = 5 ~= 3;",
    ),
    Q(
        97, "Operatörler", "Dizide karşılaştırma", 3,
        "`v = [3 8 1 6]` vektöründe `4`'ten büyük elemanların **sayısını** `sonuc` "
        "olarak ata.",
        verify="chk(sonuc, 2, 'sonuc');",
        starter="v = [3 8 1 6];\n\n",
        hint="`v > 4` 0/1'lerden oluşan bir maske üretir; `sum()` ile sayılır.",
        solution="v = [3 8 1 6];\nsonuc = sum(v > 4);",
    ),
    Q(
        98, "Operatörler", "Aralık kontrolü tuzağı", 5,
        "`v = [3 8 1 6 10]` vektöründe **2 ile 9 arasında** (uçlar dahil) olan "
        "elemanları `sonuc` olarak ata. **Doğru MATLAB karşılığını** yaz — "
        "`2 < v < 9` gibi zincirleme karşılaştırma MATLAB'de çalışmaz.",
        verify="chk(sonuc, [3 8 6], 'sonuc');",
        starter="v = [3 8 1 6 10];\n\n",
        hint="MATLAB zincirleme karşılaştırmayı desteklemez: `2 < v < 9` ifadesi "
             "önce `2 < v` hesaplar, sonra 0/1 sonucu `9` ile karşılaştırır — hep "
             "doğru çıkar. Doğrusu: `v > 2 & v < 9`.",
        solution="v = [3 8 1 6 10];\nsonuc = v(v > 2 & v < 9);",
    ),
    Q(
        99, "Operatörler", "Mantıksal fonksiyonlar", 3,
        "`v = [3 8 1 6]` vektöründe `2`'den büyük elemanların sayısını `nnz` ile, "
        "indekslerini `find` ile bulup `sonuc` ve `indeksler` değişkenlerine ata.",
        verify="chk(sonuc, 3, 'nnz');\nchk(indeksler, [1 2 4], 'indeksler');",
        starter="v = [3 8 1 6];\n\n",
        hint="`nnz(v > 2)` doğru elemanların **sayısı**, `find(v > 2)` **indeksleri**.",
        solution="v = [3 8 1 6];\nsonuc = nnz(v > 2);\nindeksler = find(v > 2);",
    ),
    Q(
        100, "Operatörler", "Metin karşılaştırma", 4,
        "`'abc'` ile `'abd'` metinlerinin eşit olup olmadığını `strcmp` ile kontrol edip "
        "sonucu `sonuc` olarak ata. (`==` kullanma — uzunluklar farklıysa hata verir.)",
        verify="chkBool(sonuc, 0, 'sonuc');",
        starter="a = 'abc'; b = 'abd';\n\n",
        hint="`strcmp` her uzunlukta güvenle tek bir 0/1 döndürür. "
             "`strcmpi` büyük/küçük harfi yok sayar.",
        solution="a = 'abc'; b = 'abd';\nsonuc = strcmp(a,b);",
    ),
]

# Benzersizlik ve aralık kontrolu (yayin aninda hata vermemesi icin)
_ids = [q["id"] for q in QUESTIONS]
assert len(_ids) == len(set(_ids)), "Soru numaralari tekrarli!"
assert sorted(_ids) == list(range(1, 101)), "Soru numaralari 1..100 araliginda degil!"
