"""MATLAB/Octave kodu calistirma motoru + hata tani (diagnosis).

Kod, gecici bir dizinde tek bir Octave oturumunda calistirilir:
  1. Kullanici kodu bir try/catch icinde kosulur -> hata olursa yakalanir.
  2. Hata olmadiysa sorunun `verify` blogu `__ok__` / `__msg__` degiskenlerini
     doldurur (beklenen deger ile karsilastirma + Turkce geri bildirim).
  3. Hata olduysa sorunun `expect_error` regex'i hatayla eslesiyorsa soru
     "dogru" sayilir (bu tip sorularin amaci hatayi bilincli uretmektir).
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

OCTAVE_BIN = shutil.which("octave-cli") or shutil.which("octave")
RUN_TIMEOUT = 20  # saniye
MAX_OUTPUT = 20000

# ---------------------------------------------------------------------------
# Turkce hata tani tablosu: (regex, baslik, aciklama, cozum)
# ---------------------------------------------------------------------------
DIAGNOSIS: List[tuple] = [
    (
        r"index\s*\(\s*[\d\w]+\s*\)\s*:\s*out of bound|index out of bound|"
        r"out of bound \d+|subscript index.*out of bound",
        "Dizi sınırının aşılması",
        "Dizide olmayan bir konuma erişmeye çalıştın. MATLAB dizilerde indeks "
        "1'den başlar ve son elemana `end` ile ulaşılır.",
        "`size(v)` ile boyutu kontrol et. Son eleman için `v(end)`, sondan biri "
        "için `v(end-1)` kullan. Geçersiz konumda MATLAB diziyi büyütmez; "
        "hata verir.",
    ),
    (
        r"nonconformant arguments|dimensions must match|incompatible sizes|"
        r"operator \+: nonconformant|operator \*: nonconformant|"
        r"operator /: nonconformant|nonconformant",
        "Boyut uyuşmazlığı",
        "İşlem yapılan iki dizinin boyutları birbiriyle uyumlu değil.",
        "`size(A)` ve `size(B)` çıktısını karşılaştır. Satır vektörüyle "
        "sütun vektörünü toplamak veya `[A B]` / `[A; B]` ile birleştirmek "
        "gerekir. Toplama ve çıkarma zaten eleman eleman çalışır.",
    ),
    (
        r"undefined (near|function|variable|function or variable)|"
        r"error: '[^']+' undefined",
        "Tanımsız fonksiyon veya değişken",
        "Çağırdığın isim MATLAB ortamında tanımlı değil. Ya isim yanlış yazıldı "
        "ya da dosya MATLAB yolundaki (path) bir klasörde değil.",
        "Fonksiyon adını kontrol et (yazım ve büyük/küçük harf duyarlıdır). "
        "`which isim` ile bulunabilir. Fonksiyon dosyan kendi klasöründe "
        "olmalıdır.",
    ),
    (
        r"value on right hand side of assignment is undefined|"
        r"value right hand side of assignment is undefined",
        "Değer henüz tanımlanmamış",
        "Bir değişkene ilk değer vermeden kullandın.",
        "Değişkeni önce oluştur: `x = 0;` sonra kullan. Ya da "
        "`exist('x','var')` ile kontrol et.",
    ),
    (
        r"brace indexing is not supported|invalid use of \{|"
        r"cannot be indexed with \{|indexed with \{",
        "Süslü parantez hatası",
        "`{ }` yalnızca hücre dizilerinde kullanılır. Sayısal bir diziye "
        "süslü parantezle erişemezsin.",
        "Sayısal dizide `( )` kullan: `A(2,3)`. `{ }` sadece hücre dizisi "
        "için: `c{2}`.",
    ),
    (
        r"invalid use of|invalid expression|parse error|invalid syntax|"
        r"syntax error",
        "Sözdizimi hatası",
        "Kod MATLAB/Octave tarafından ayrıştırılamadı.",
        "Parantezleri ve noktalı virgülleri kontrol et. Satır sonunu "
        "uzatacaksan `...` kullan. Küçük harf/büyük harf ve operatörleri "
        "(`.*`, `./`, `.^`) doğru yazdın mı?",
    ),
    (
        r"operator .*: nonconformant|operator .* undefined|"
        r"binary operator .* not implemented",
        "Geçersiz işlem kullanımı",
        "Operatörü bu türlerle kullanamazsın.",
        "`*` matris çarpımıdır ve iç boyutlar eşit olmalıdır; vektörlerde "
        "`.*`, `./`, `.^` kullan. Karşılaştırma için `==` (tek `=` değil) yaz.",
    ),
    (
        r"division by zero|divide by zero",
        "Sıfıra bölme",
        "Bir değeri sıfıra bölmeye çalıştın.",
        "Bölmeden önce paydanın sıfır olmadığını kontrol et. `0/0` → NaN, "
        "`1/0` → Inf üretir.",
    ),
    (
        r"maximum recursion depth exceeded|recursion",
        "Aşırı derin çağrı (recursion)",
        "Bir fonksiyon kendini sonsuz çağırıyor.",
        "Fonksiyonun sonlandırma koşulunu kontrol et; her çağrıda sonuca "
        "doğru ilerlediğinden emin ol.",
    ),
    (
        r"out of memory|cannot allocate",
        "Bellek yetersiz",
        "İşlem için gereken bellek ayrılamadı.",
        "Dizi boyutlarını kontrol et. `1:1e9` gibi devasa aralıklar "
        "oluşturmaktan kaçın.",
    ),
    (
        r"element number \d+ undefined in \(delete\)|index .* deleted",
        "Geçersiz silme",
        "Diziden silmek istediğin konum mevcut değil.",
        "Önce `length(v)` ile boyutu öğren, sonra `v(idx) = []` kullan.",
    ),
    (
        r"value cannot be assigned to|read-only|constant",
        "Atama hatası",
        "Bu değişkene veya alana atama yapılamaz.",
        "`end` gibi özel isimleri, `pi` gibi hazır sabitleri ya da bir "
        "fonksiyon adını değişken olarak kullanma.",
    ),
    (
        r"function name does not agree|function filename",
        "Fonksiyon dosya adı uyuşmazlığı",
        "Dosya adı, fonksiyon adıyla aynı olmalı.",
        "`ornek.m` dosyasında ilk fonksiyon `function cikti = ornek(...)` olmalı.",
    ),
    (
        r"conversion to .* from .* is not possible|cannot convert",
        "Tip dönüşüm hatası",
        "Bir değeri beklenen tipe çeviremedin.",
        "`str2double`, `double`, `char`, `num2str`, `cell` gibi dönüşüm "
        "fonksiyonlarını kullan.",
    ),
    (
        r"maximum number of elements|too many elements",
        "Dizi boyutu limiti",
        "Oluşturmak istediğin dizi izin verilen maksimumun üzerinde.",
        "Boyutu küçült veya `clear` ile belleği boşalt.",
    ),
    (
        r"stopped by user|interrupted",
        "İşlem durduruldu",
        "Kod çalıştırılırken durduruldu.",
        "Döngü veya sonsuz çevrim çok uzun sürüyor olabilir.",
    ),
]


@dataclass
class RunResult:
    ok: bool
    message: str = ""
    stdout: str = ""
    stderr: str = ""
    error: str = ""
    error_id: str = ""
    engine: str = "octave"
    timed_out: bool = False
    duration_ms: int = 0
    diagnosis: Optional[Dict[str, str]] = None
    expected_output: str = ""
    actual_output: str = ""
    diff: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "message": self.message,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "error": self.error,
            "errorId": self.error_id,
            "engine": self.engine,
            "timedOut": self.timed_out,
            "durationMs": self.duration_ms,
            "diagnosis": self.diagnosis,
            "expectedOutput": self.expected_output,
            "actualOutput": self.actual_output,
            "diff": self.diff,
        }


def diagnose(text: str) -> Optional[Dict[str, str]]:
    """Hata metnini Turkce aciklamaya cevirir."""
    if not text:
        return None
    low = text.lower()
    for pattern, title, desc, fix in DIAGNOSIS:
        if re.search(pattern, low):
            return {"title": title, "description": desc, "fix": fix}
    return None


# ---------------------------------------------------------------------------
# Octave yardimci fonksiyonlari (verify bloklari bunlari kullanir)
# ---------------------------------------------------------------------------
HELPERS = r"""
function [ok, s] = chk(actual, expected, label)
  % Tam esitlik kontrolu (dizi / sayi / char / mantiksal).
  if nargin < 3 || isempty(label), label = 'sonuc'; end
  if isequal(actual, expected)
    ok = true; s = '';
  else
    ok = false;
    s = sprintf('Beklenen %s: %s\nBulunan %s : %s', label, vstr(expected), label, vstr(actual));
  end
  chkstore(ok, s);
end

function [ok, s] = chkTol(actual, expected, tol, label)
  % Toleransli kayan nokta kontrolu.
  if nargin < 4 || isempty(label), label = 'sonuc'; end
  if isempty(actual) || isempty(expected) || ~isequal(size(actual), size(expected))
    ok = false;
    s = sprintf('Beklenen %s: %s\nBulunan %s : %s (boyutlar uyuşmuyor)', ...
      label, vstr(expected), label, vstr(actual));
    chkstore(ok, s);
    return;
  end
  d = abs(double(actual(:)) - double(expected(:)));
  if isempty(d) || max(d) <= tol
    ok = true; s = '';
  else
    ok = false;
    s = sprintf('Beklenen %s: %s\nBulunan %s : %s\nEn büyük fark (tolerans %g): %g', ...
      label, vstr(expected), label, vstr(actual), tol, max(d));
  end
  chkstore(ok, s);
end

function [ok, s] = chkTrue(cond, goodMsg, badMsg)
  % Mantiksal / boolean sonuc kontrolu.
  if cond
    ok = true; s = goodMsg;
  else
    ok = false; s = badMsg;
  end
  chkstore(ok, s);
end

function [ok, s] = chkSize(actual, expectedSize, label)
  % Boyut kontrolu (sadece size, deger degil).
  if nargin < 3 || isempty(label), label = 'boyut'; end
  if isequal(size(actual), expectedSize)
    ok = true; s = '';
  else
    ok = false;
    s = sprintf('Beklenen %s: %s\nBulunan %s : %s', ...
      label, mat2str(expectedSize), label, mat2str(size(actual)));
  end
  chkstore(ok, s);
end

function [ok, s] = chkBool(actual, expected, label)
  % Mantiksal (logical) sonuc kontrolu. Degerin 0/1 olmasi yetmez; tipinin de
  % 'logical' olmasi gerekir, aksi halde "sonuc = 0" tahmini soruyu gecer.
  if nargin < 3 || isempty(label), label = 'sonuc'; end
  if islogical(actual) && isscalar(actual) && (actual == expected)
    ok = true; s = '';
  else
    ok = false;
    if islogical(actual)
      tip = 'logical';
    else
      tip = class(actual);
    end
    s = sprintf('Beklenen %s: mantıksal %d (true/false)\nBulunan %s: %s (%s tipi)', ...
      label, expected, label, vstr(actual), tip);
  end
  chkstore(ok, s);
end

function [ok, s] = chkOut(cmd, expected, label)
  % Ekrana yazdirilan ciktiyi karsilastirir (evalc ile yakalanir).
  if nargin < 3 || isempty(label), label = 'cikti'; end
  got = evalc(cmd);
  if ischar(expected)
    e = expected;
  else
    e = vstr(expected);
  end
  e = strtrim(regexprep(e, '\s+', ' '));
  g = strtrim(regexprep(got, '\s+', ' '));
  if strcmp(e, g)
    ok = true; s = '';
  else
    ok = false;
    s = sprintf('Beklenen %s: %s\nBulunan %s : %s', label, e, label, g);
  end
  chkstore(ok, s);
end

function chkstore(ok, msg)
  % Sonucu global degiskene yazar. Birden fazla kontrol biriktirilir:
  % herhangi biri basarisiz olursa sonuc basarisizdir.
  global __MLAB_RESULT__
  if ok
    if isempty(__MLAB_RESULT__.msg) && ~isempty(msg)
      __MLAB_RESULT__.msg = msg;
    end
  else
    if isempty(__MLAB_RESULT__.msg)
      __MLAB_RESULT__.msg = msg;
    else
      __MLAB_RESULT__.msg = [__MLAB_RESULT__.msg sprintf('\n') msg];
    end
    __MLAB_RESULT__.nfail = __MLAB_RESULT__.nfail + 1;
  end
end

function s = vstr(x)
  try
    if ischar(x)
      s = ['''' x ''''];
    elseif islogical(x)
      if isscalar(x)
        if x, s = 'true (1)'; else, s = 'false (0)'; end
      else
        s = mat2str(double(x));
      end
    elseif isnumeric(x) && isscalar(x)
      s = strtrim(sprintf('%.10g', double(x)));
    elseif isnumeric(x)
      s = mat2str(x, 10);
    else
      s = ['<' class(x) '>'];
    end
  catch
    s = '<gosterilemedi>';
  end
end
"""


# ---------------------------------------------------------------------------
# Calistirma
# ---------------------------------------------------------------------------
def _build_driver(user_code: str, verify_code: str, expect_error: Optional[str]) -> str:
    """Kullanici kodunu + dogrulama blogunu tek bir Octave dosyasina donusturur."""
    indented_user = "\n".join(("  " + ln) if ln.strip() else ln for ln in user_code.splitlines())
    indented_verify = "\n".join(
        ("  " + ln) if ln.strip() else ln for ln in verify_code.splitlines()
    )
    error_branch = ""
    expect_error_present = "true" if expect_error else "false"
    if expect_error:
        error_branch = f"""
    if ~isempty(regexpi(__MLAB_RESULT__.err, {expect_error!r}, 'once'))
      __MLAB_RESULT__.ok = true;
      __MLAB_RESULT__.msg = 'Beklenen hatayı doğru şekilde ürettin.';
    else
      __MLAB_RESULT__.ok = false;
      __MLAB_RESULT__.msg = sprintf(['Beklenen hata türü oluşmadı.\\nAlınan hata: %s'], __MLAB_RESULT__.err);
    end"""
    else:
        error_branch = """
    __MLAB_RESULT__.ok = false;
    __MLAB_RESULT__.msg = sprintf(['Kodun bir hata ile durdu:\\n%s'], __MLAB_RESULT__.err);"""

    return f"""function __mlab_run__()
  global __MLAB_RESULT__
  __MLAB_RESULT__ = struct('ok', false, 'msg', '', 'err', '', 'errid', '', 'nfail', 0);

  try
%__USER_CODE_START__
{indented_user}
  catch __e__
    __MLAB_RESULT__.err = __e__.message;
    __MLAB_RESULT__.errid = __e__.identifier;
{error_branch}
    return;
  end

  try
{indented_verify}
    if {expect_error_present} && isempty(__MLAB_RESULT__.msg)
      __MLAB_RESULT__.ok = false;
      __MLAB_RESULT__.nfail = 1;
      __MLAB_RESULT__.msg = 'Beklenen hata oluşmadı. Kodun hatayı bilinçli üretmesi gerekiyor.';
    end
  catch __e2__
    __MLAB_RESULT__.err = __e2__.message;
    __MLAB_RESULT__.errid = __e2__.identifier;
    __MLAB_RESULT__.ok = false;
    __MLAB_RESULT__.nfail = 1;
    __MLAB_RESULT__.msg = sprintf(['Doğrulama sırasında hata: %s'], __e2__.message);
  end

  if __MLAB_RESULT__.nfail == 0
    __MLAB_RESULT__.ok = true;
  end
end
"""


def _octave_argv() -> List[str]:
    if not OCTAVE_BIN:
        return []
    return [
        OCTAVE_BIN,
        "--no-gui",
        "--no-window-system",
        "--norc",
        "--no-history",
        "--quiet",
    ]


def run_matlab_code(
    code: str,
    verify_code: str = "",
    expect_error: Optional[str] = None,
    stdin_data: str = "",
) -> RunResult:
    """Kodu calistirir ve RunResult dondurur."""
    import time

    if not OCTAVE_BIN:
        return RunResult(
            ok=False,
            error="Octave bulunamadi. `sudo pacman -S octave` ile kurulmali.",
            engine="none",
        )

    workdir = tempfile.mkdtemp(prefix="mlab-")
    started = time.time()
    try:
        # 1) Ana calistirma dosyasi
        driver = _build_driver(code, verify_code, expect_error)
        # kullanici kodu uretilen dosyada bu satirdan basliyor; hata mesajindaki
        # satirlari kullanicinin koduna cevirmek icin offset tutuyoruz
        marker = driver.index("%__USER_CODE_START__")
        user_line_offset = driver[:marker].count("\n") + 1
        with open(os.path.join(workdir, "__mlab_run__.m"), "w", encoding="utf-8") as fh:
            fh.write(driver)
            fh.write("\n")
            fh.write(HELPERS)

        # 2) Ana (script) dosya: fonksiyonu cagir, sonucu basil
        #    Not: mesajlardaki gercek satir sonlari iki karakterli '\\n' olarak
        #    kodlanir; aksi halde sentinel protokolu bozulur.
        main = r"""global __MLAB_RESULT__
__MLAB_RESULT__ = struct('ok', false, 'msg', '', 'err', '', 'errid', '', 'nfail', 0);
__mlab_run__();
__R__ = __MLAB_RESULT__;
__enc__ = @(s) strrep(s, sprintf('\n'), '\n');
fprintf('__MLAB_DONE__\n');
fprintf('__MLAB_OK__%d\n', __R__.ok);
fprintf('__MLAB_MSG__%s\n', __enc__(__R__.msg));
fprintf('__MLAB_ERR__%s\n', __enc__(__R__.err));
fprintf('__MLAB_ERRID__%s\n', __R__.errid);
"""
        with open(os.path.join(workdir, "main.m"), "w", encoding="utf-8") as fh:
            fh.write(main)

        env = dict(os.environ)
        env.update(
            {
                "OCTAVE_HISTFILE": os.devnull,
                "QT_QPA_PLATFORM": "offscreen",
                "GNUTERM": "dumb",
                "HOME": workdir,
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
            }
        )

        argv = _octave_argv() + ["--path", workdir, "--eval", "main;"]
        try:
            proc = subprocess.run(
                argv,
                cwd=workdir,
                env=env,
                input=stdin_data or "",
                capture_output=True,
                text=True,
                timeout=RUN_TIMEOUT,
                errors="replace",
            )
            stdout, stderr, timed_out = proc.stdout, proc.stderr, False
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout.decode("utf-8", "replace") if exc.stdout else ""
            stderr = exc.stderr.decode("utf-8", "replace") if exc.stderr else ""
            timed_out = True

        duration = int((time.time() - started) * 1000)
        return _interpret(stdout, stderr, timed_out, duration, verify_code, user_line_offset)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _extract(stdout: str, marker: str) -> Optional[str]:
    idx = stdout.find(marker)
    if idx < 0:
        return None
    rest = stdout[idx + len(marker) :]
    nl = rest.find("\n")
    return rest if nl < 0 else rest[:nl]


def _decode_newlines(text: str) -> str:
    """Sentinel protokolunda iki karakterli '\\n' gercek satir sonuna cevrilir."""
    return text.replace("\\n", "\n") if text else ""


def _octave_error(text: str, user_line_offset: int = 0) -> str:
    """Octave hata ciktisindan ilk 'error:' satirini temiz haliyle cikarir.

    `user_line_offset` verildiginde, uretilen dosyadaki satir numarasi
    kullanicinin kodundaki karsiliga cevrilir.
    """
    if not text:
        return ""
    for raw in text.split("\n"):
        line = raw.strip()
        if not line.lower().startswith("error:"):
            continue
        line = line[len("error:") :].strip()
        # gecici calisma dizinini gizle
        line = re.sub(r"/tmp/[\w.-]+/", "", line)
        line = re.sub(r"in file \S+", "", line).strip()

        def _remap(m):
            n = int(m.group(1)) - user_line_offset
            return "satir %d" % n if n >= 1 else m.group(0)

        line = re.sub(r"near line (\d+)", _remap, line)
        line = re.sub(r"\bline (\d+), column (\d+)", r"satir \1, sutun \2", line)
        return line.strip()
    return ""


def _interpret(
    stdout: str,
    stderr: str,
    timed_out: bool,
    duration: int,
    verify_code: str,
    user_line_offset: int = 0,
) -> RunResult:
    """Octave ciktisini ayristirir."""
    stdout = stdout or ""
    stderr = stderr or ""

    if timed_out:
        diag = diagnose("timeout") or {
            "title": "Zaman aşımı",
            "description": "Kod %d saniyede bitmedi ve çalıştırma durduruldu." % (duration // 1000),
            "fix": "Sonsuz döngü olabilir. `for`/`while` koşullarını ve `break` "
            "kullanımını kontrol et.",
        }
        return RunResult(
            ok=False,
            error="Zaman aşımı: kod %d saniyede tamamlanmadı." % (duration // 1000),
            stdout=stdout[:MAX_OUTPUT],
            stderr=stderr[:MAX_OUTPUT],
            timed_out=True,
            duration_ms=duration,
            diagnosis=diag,
        )

    ok_flag = _extract(stdout, "__MLAB_OK__")
    if ok_flag is None:
        # Motor seviyesinde bir sey ters gitti (ornegin sozdizimi hatasi:
        # dosya hic ayristirilamadigi icin sentinel yazilamadi).
        raw = _octave_error(stderr, user_line_offset) or _octave_error(stdout, user_line_offset)
        diag = diagnose(stderr or stdout) or {
            "title": "Kod çalıştırılamadı",
            "description": "Motor beklenen sonucu üretmedi. Aşağıdaki mesaja bak.",
            "fix": "Kodun sözdizimini kontrol et.",
        }
        return RunResult(
            ok=False,
            message=raw or "Çalıştırma sırasında beklenmeyen bir durum oluştu.",
            error=raw or "Çalıştırma sırasında beklenmeyen bir durum oluştu.",
            stdout=stdout[:MAX_OUTPUT],
            stderr=stderr[:MAX_OUTPUT],
            duration_ms=duration,
            diagnosis=diag,
        )

    ok = ok_flag.strip() == "1"
    msg = _decode_newlines((_extract(stdout, "__MLAB_MSG__") or "").strip())
    err = _decode_newlines((_extract(stdout, "__MLAB_ERR__") or "").strip())
    errid = (_extract(stdout, "__MLAB_ERRID__") or "").strip()

    # Kullaniciya ait stdout (sentinel oncesi kisim)
    cut = stdout.find("__MLAB_DONE__")
    user_out = stdout[:cut] if cut >= 0 else stdout
    user_out = user_out.strip()

    result = RunResult(
        ok=ok,
        message=msg,
        stdout=user_out,
        stderr=stderr[:MAX_OUTPUT],
        error=err,
        error_id=errid,
        duration_ms=duration,
    )
    if err:
        result.diagnosis = diagnose(err)
    return result


# ---------------------------------------------------------------------------
# Metin normalizasyonu / diff
# ---------------------------------------------------------------------------
def normalize_output(text: str) -> str:
    """Beklenen/gercek cikti karsilastirmasi icin normalizasyon."""
    if not text:
        return ""
    t = text.replace("\r\n", "\n").strip()
    lines = []
    for raw in t.split("\n"):
        line = raw.rstrip()
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def _numbers_in(text: str) -> List[float]:
    return [float(x) for x in re.findall(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?", text)]


def outputs_match(expected: str, actual: str, tol: float = 1e-6) -> bool:
    """Metinsel ve sayisal toleransli esitlik kontrolu."""
    e, a = normalize_output(expected), normalize_output(actual)
    if e == a:
        return True
    if not e and not a:
        return True
    e_lines, a_lines = e.split("\n"), a.split("\n")
    if len(e_lines) != len(a_lines):
        return False
    for le, la in zip(e_lines, a_lines):
        if le == la:
            continue
        ne, na = _numbers_in(le), _numbers_in(la)
        if not ne or not na or len(ne) != len(na):
            return False
        if any(abs(x - y) > tol * max(1.0, abs(x), abs(y)) for x, y in zip(ne, na)):
            return False
    return True


def diff_outputs(expected: str, actual: str) -> List[Dict[str, str]]:
    """Satir bazli fark listesi uretir."""
    import difflib

    e = normalize_output(expected).split("\n") if expected.strip() else []
    a = normalize_output(actual).split("\n") if actual.strip() else []
    out = []
    for line in difflib.unified_diff(e, a, "beklenen", "bulunan", lineterm="", n=1):
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("@@"):
            out.append({"type": "header", "text": line})
        elif line.startswith("-"):
            out.append({"type": "remove", "text": line[1:]})
        elif line.startswith("+"):
            out.append({"type": "add", "text": line[1:]})
    return out
