/* ==========================================================================
   MATLAB Lab — uygulama mantigi
   ========================================================================== */
(function () {
  "use strict";

  var STATE = {
    questions: [],
    notes: [],
    glossary: [],
    engine: { available: false, octave: "" },
    filtered: [],
    current: null,
    progress: {},      // id -> "solved" | "failed"
    drafts: {},        // id -> kod metni
    lastResult: null,
    running: false
  };

  var LS_PROGRESS = "mlab.progress";
  var LS_DRAFTS = "mlab.drafts";
  var LS_THEME = "mlab.theme";

  var $ = function (id) { return document.getElementById(id); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* ------------------------------------------------------------------ */
  /* markdown (kucuk)                                                     */
  /* ------------------------------------------------------------------ */
  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function inline(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, function (_, c) { return "<code>" + c + "</code>"; })
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  }

  /** Satirlari markdown bloklarina cevirir (tablolar, listeler, paragraf). */
  function renderMd(text) {
    if (!text) return "";
    var lines = String(text).split("\n");
    var html = [];
    var i = 0;

    while (i < lines.length) {
      var line = lines[i];

      // tablo
      if (/^\s*\|/.test(line)) {
        var rows = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) {
          rows.push(lines[i].trim());
          i++;
        }
        html.push(tableHtml(rows));
        continue;
      }

      // alinti / cagri kutusu
      if (/^>\s?/.test(line)) {
        var buf = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) {
          buf.push(lines[i].replace(/^>\s?/, ""));
          i++;
        }
        html.push('<div class="callout">' + inline(buf.join(" ")) + "</div>");
        continue;
      }

      // liste
      if (/^\s*[-*]\s+/.test(line)) {
        var items = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
          items.push(lines[i].replace(/^\s*[-*]\s+/, ""));
          i++;
        }
        html.push("<ul>" + items.map(function (it) {
          return "<li>" + inline(it) + "</li>";
        }).join("") + "</ul>");
        continue;
      }

      // bos satir
      if (!line.trim()) { i++; continue; }

      // paragraf
      var para = [line];
      i++;
      while (i < lines.length && lines[i].trim() && !/^\s*(\||>|[-*]\s)/.test(lines[i])) {
        para.push(lines[i]);
        i++;
      }
      html.push("<p>" + inline(para.join(" ")) + "</p>");
    }

    return html.join("");
  }

  function tableHtml(rows) {
    if (!rows.length) return "";
    var cells = function (r) {
      return r.replace(/^\s*\|/, "").replace(/\|\s*$/, "").split("|").map(function (c) {
        return c.trim();
      });
    };
    var head = cells(rows[0]);
    var body = rows.slice(1).filter(function (r) {
      return !/^[\s|:-]+$/.test(r); // ayirici satiri atla
    });
    var out = '<div class="table-wrap"><table><thead><tr>';
    head.forEach(function (h) { out += "<th>" + inline(h) + "</th>"; });
    out += "</tr></thead><tbody>";
    body.forEach(function (r) {
      out += "<tr>";
      cells(r).forEach(function (c) { out += "<td>" + inline(c) + "</td>"; });
      out += "</tr>";
    });
    out += "</tbody></table></div>";
    return out;
  }

  function codeBlock(matlab, cikti) {
    var html = '<div class="code-block">';
    html += '<div class="code-block__head"><b>MATLAB</b><span>kod</span></div>';
    html += "<pre>" + highlightCode(matlab) + "</pre>";
    if (cikti) {
      html += '<div class="code-block__head"><b>Çıktı</b><span>sonuç</span></div>';
      html += '<pre class="out">' + highlightCode(cikti) + "</pre>";
    }
    html += "</div>";
    return html;
  }

  function highlightCode(src) {
    if (!src) return "";
    return esc(src)
      .replace(/(^|\n)(&gt;&gt;|%)/g, '$1<span class="t-com">$2</span>')
      .replace(/&#39;[^&]*?&#39;/g, function (m) { return '<span class="t-str">' + m + "</span>"; });
  }

  /* ------------------------------------------------------------------ */
  /* depolama                                                            */
  /* ------------------------------------------------------------------ */
  function loadLocal() {
    try {
      STATE.progress = JSON.parse(localStorage.getItem(LS_PROGRESS) || "{}");
      STATE.drafts = JSON.parse(localStorage.getItem(LS_DRAFTS) || "{}");
    } catch (e) {
      STATE.progress = {};
      STATE.drafts = {};
    }
  }

  function saveLocal() {
    try {
      localStorage.setItem(LS_PROGRESS, JSON.stringify(STATE.progress));
      localStorage.setItem(LS_DRAFTS, JSON.stringify(STATE.drafts));
    } catch (e) { /* kota dolu olabilir, yoksay */ }
  }

  /* ------------------------------------------------------------------ */
  /* yonlendirme                                                         */
  /* ------------------------------------------------------------------ */
  var ROUTES = ["notlar", "sorular", "sozluk"];

  function route() {
    var parts = (location.hash || "#/notlar").replace(/^#\//, "").split("/");
    var hash = parts[0];
    var arg = parts[1] || "";
    if (ROUTES.indexOf(hash) < 0) hash = "notlar";
    ROUTES.forEach(function (r) {
      $("page-" + (r === "sorular" ? "quiz" : r === "notlar" ? "notes" : "glossary")).hidden = (r !== hash);
    });
    $$(".topnav a").forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("data-nav") === hash);
    });
    if (hash === "notlar") renderNotes();
    if (hash === "sorular") {
      renderQuiz();
      if (arg && /^\d+$/.test(arg)) {
        var qid = parseInt(arg, 10);
        if (!STATE.current || STATE.current.id !== qid) openQuestion(qid);
      }
    }
    if (hash === "sozluk") renderGlossary();
    window.scrollTo({ top: 0 });
  }

  /* ------------------------------------------------------------------ */
  /* NOTLAR                                                              */
  /* ------------------------------------------------------------------ */
  function renderNotes() {
    var nav = $("notesNav");
    var content = $("notesContent");

    if (!nav.dataset.built) {
      nav.innerHTML = '<div class="notes-nav__title">Konular</div>' +
        STATE.notes.map(function (m, idx) {
          return '<a href="#/notlar" data-note="' + m.id + '">' + esc(m.title) + "</a>";
        }).join("");
      nav.dataset.built = "1";
    }

    var hashNote = (location.hash.split("=")[1] || "");
    var current = STATE.notes.filter(function (m) { return m.id === hashNote; })[0] || STATE.notes[0];
    if (!current) { content.innerHTML = "<p>Not bulunamadı.</p>"; return; }

    $$("#notesNav a").forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("data-note") === current.id);
    });

    var html = '<div class="note-hero">';
    html += "<h1>" + esc(current.title) + "</h1>";
    html += '<div class="note-source">Kaynak: ' + esc(current.source) + "</div>";
    html += '<p class="note-summary">' + inline(current.summary) + "</p>";
    html += "</div>";

    if (current.keypoints && current.keypoints.length) {
      html += '<div class="keypoints"><h2>Özet Noktalar</h2><ul>';
      current.keypoints.forEach(function (k) { html += "<li>" + inline(k) + "</li>"; });
      html += "</ul></div>";
    }

    (current.sections || []).forEach(function (sec) {
      html += '<section class="note-section">';
      html += "<h2>" + esc(sec.title) + "</h2>";
      if (sec.points && sec.points.length) {
        html += '<ul class="points">';
        sec.points.forEach(function (p) { html += "<li>" + inline(p) + "</li>"; });
        html += "</ul>";
      }
      if (sec.code) html += codeBlock(sec.code.matlab, sec.code.cikti);
      (sec.notes || []).forEach(function (n) {
        html += '<div class="callout callout--info">' + inline(n) + "</div>";
      });
      html += "</section>";
    });

    content.innerHTML = html;
    content.scrollIntoView({ block: "start" });
  }

  /* ------------------------------------------------------------------ */
  /* SORU BANKASI                                                        */
  /* ------------------------------------------------------------------ */
  function levelDots(level) {
    var out = '<span class="q-level">';
    for (var i = 1; i <= 5; i++) out += '<i class="' + (i <= level ? "on" : "") + '"></i>';
    out += "</span>";
    return out;
  }

  function moduleOptions() {
    var mods = [];
    STATE.questions.forEach(function (q) {
      if (mods.indexOf(q.module) < 0) mods.push(q.module);
    });
    return mods;
  }

  function applyFilters() {
    var term = ($("qSearch").value || "").trim().toLowerCase();
    var mod = $("qModule").value;
    var lvl = $("qLevel").value;

    STATE.filtered = STATE.questions.filter(function (q) {
      if (mod && q.module !== mod) return false;
      if (lvl && String(q.level) !== lvl) return false;
      if (term) {
        var hay = (q.prompt + " " + q.topic + " " + q.module + " " + q.solution).toLowerCase();
        if (hay.indexOf(term) < 0) return false;
      }
      return true;
    });
    renderQList();
  }

  function renderQList() {
    var list = $("qList");
    if (!STATE.filtered.length) {
      list.innerHTML = '<li class="q-item" style="cursor:default"><span class="q-item__title">Eşleşen soru yok.</span></li>';
      return;
    }
    list.innerHTML = STATE.filtered.map(function (q) {
      var st = STATE.progress[q.id] || "";
      var active = STATE.current && STATE.current.id === q.id ? " active" : "";
      return '<li class="q-item' + active + '" data-qid="' + q.id + '" role="option">' +
        '<span class="q-item__num">' + q.id + "</span>" +
        '<span class="q-item__title">' + esc(q.topic) + "</span>" +
        levelDots(q.level) +
        '<span class="q-item__dot ' + (st === "solved" ? "solved" : st === "failed" ? "failed" : "") + '"></span>' +
        "</li>";
    }).join("");
  }

  function renderQuiz() {
    if (!$("qModule").dataset.built) {
      $("qModule").innerHTML = '<option value="">Tüm konular</option>' +
        moduleOptions().map(function (m) { return "<option>" + esc(m) + "</option>"; }).join("");
      $("qModule").dataset.built = "1";
      applyFilters();
    }
    renderQList();
    updateProgress();
  }

  function updateProgress() {
    var total = STATE.questions.length || 1;
    var solved = Object.keys(STATE.progress).filter(function (k) {
      return STATE.progress[k] === "solved";
    }).length;
    var pct = (solved / total) * 100;
    $("progressFill").style.width = pct + "%";
    $("progressText").textContent = solved + " / " + STATE.questions.length;
    $("quizProgressFill").style.width = pct + "%";
    $("quizProgressText").textContent = solved + " / " + STATE.questions.length + " çözüldü";
    $("navCount").textContent = String(STATE.questions.length);
  }

  /* ------------------------------------------------------------------ */
  /* SORU MODALI                                                         */
  /* ------------------------------------------------------------------ */
  function openQuestion(qid) {
    var q = STATE.questions.filter(function (x) { return x.id === qid; })[0];
    if (!q) return;
    STATE.current = q;

    $("qModalBadge").textContent = q.id;
    $("qModalMeta").textContent = q.module + " · " + levelLabel(q.level);
    $("qModalTitle").textContent = q.topic;
    $("qModalPrompt").innerHTML = renderMd(q.prompt);

    var draft = STATE.drafts[q.id];
    editor.setValue(draft !== undefined ? draft : (q.starter || ""));

    $("console").hidden = true;
    $("feedback").hidden = true;
    $("diagnosis").hidden = true;
    $("modalExtra").hidden = true;
    $("modalExtra").innerHTML = "";

    $("questionModal").hidden = false;
    document.body.style.overflow = "hidden";

    renderQList();
    editor.focus();
    updateNavButtons();
  }

  function levelLabel(l) {
    return ["", "Temel", "Başlangıç", "Orta", "Zor", "Çok zor"][l] || "";
  }

  function closeQuestion() {
    $("questionModal").hidden = true;
    document.body.style.overflow = "";
  }

  function updateNavButtons() {
    var q = STATE.current;
    if (!q) return;
    var idx = STATE.filtered.map(function (x) { return x.id; }).indexOf(q.id);
    $("btnPrev").disabled = idx <= 0;
    $("btnNext").disabled = idx < 0 || idx >= STATE.filtered.length - 1;
  }

  function goRelative(dir) {
    var q = STATE.current;
    if (!q) return;
    var ids = STATE.filtered.map(function (x) { return x.id; });
    var i = ids.indexOf(q.id) + dir;
    if (i >= 0 && i < ids.length) openQuestion(ids[i]);
  }

  /* ------------------------------------------------------------------ */
  /* CALISTIR                                                            */
  /* ------------------------------------------------------------------ */
  function runCode() {
    if (STATE.running || !STATE.current) return;
    var q = STATE.current;
    var code = editor.getValue();

    STATE.drafts[q.id] = code;
    saveLocal();

    STATE.running = true;
    var btn = $("btnRun");
    btn.disabled = true;
    btn.textContent = "Çalışıyor…";

    $("console").hidden = false;
    $("feedback").hidden = true;
    $("diagnosis").hidden = true;
    $("consoleBody").innerHTML = '<span class="sys">Kod Octave motorunda çalıştırılıyor…</span>';
    $("consoleMeta").textContent = "";

    fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: code, qid: q.id })
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        STATE.lastResult = data;
        renderResult(data, q);
      })
      .catch(function (err) {
        $("consoleBody").innerHTML = '<span class="err">Sunucuya ulaşılamadı: ' + esc(err.message) + "</span>";
        showFeedback("bad", "Bağlantı hatası", "Yerel sunucu çalışıyor mu? `python3 server.py` ile başlat.");
      })
      .finally(function () {
        STATE.running = false;
        btn.disabled = false;
        btn.textContent = "Çalıştır";
      });
  }

  function renderResult(data, q) {
    var parts = [];
    if (data.stdout) parts.push({ cls: "", text: data.stdout });

    if (data.error) parts.push({ cls: "err", text: "HATA: " + data.error });

    // stderr ek bilgi tasiyorsa goster (ayni hatayi tekrarlamadan)
    if (data.stderr) {
      var extra = String(data.stderr)
        .replace(/\/tmp\/[\w.-]+\//g, "")      // gecici dizin yolunu gizle
        .split("\n")
        .filter(function (ln) {
          // hata zaten ayri olarak gosteriliyorsa ayni hata satirini atla
          if (data.error && /^\s*error:/i.test(ln)) return false;
          return ln.trim() !== "";
        })
        .join("\n")
        .trim();
      if (extra) parts.push({ cls: "sys", text: extra });
    }

    $("consoleBody").innerHTML = parts.length
      ? parts.map(function (p) {
          return p.cls ? '<span class="' + p.cls + '">' + esc(p.text) + "</span>" : esc(p.text);
        }).join("\n")
      : '<span class="sys">(çıktı yok)</span>';
    $("consoleMeta").textContent = data.durationMs + " ms · " + (data.engine || "octave");

    if (data.ok) {
      showFeedback("ok", "Doğru!", data.message || "Çözümün beklenen sonucu verdi.");
      STATE.progress[q.id] = "solved";
      toast("✓ Soru " + q.id + " çözüldü");
    } else {
      showFeedback("bad", data.error ? "Kod bir hata verdi" : "Sonuç beklenen değil", data.message || "");
      STATE.progress[q.id] = "failed";
    }
    saveLocal();
    updateProgress();
    renderQList();
  }

  function showFeedback(kind, title, msg) {
    var fb = $("feedback");
    fb.hidden = false;
    fb.className = "feedback feedback--" + (kind === "ok" ? "ok" : "bad");
    $("feedbackIcon").textContent = kind === "ok" ? "✓" : "✕";
    $("feedbackTitle").textContent = title;
    var m = $("feedbackMsg");
    m.textContent = msg || "";
    // deger karsilastirmasi olan mesajlar mono, dugun mesajlar duz metin
    m.className = "feedback__msg" + (msg && msg.indexOf("\n") >= 0 ? " feedback__msg--mono" : "");

    var diag = $("diagnosis");
    var d = STATE.lastResult && STATE.lastResult.diagnosis;
    if (d) {
      diag.hidden = false;
      $("diagTitle").textContent = d.title;
      $("diagDesc").textContent = d.description;
      $("diagFix").textContent = d.fix;
    } else {
      diag.hidden = true;
    }
  }

  /* ------------------------------------------------------------------ */
  /* IPUCU / COZUM                                                       */
  /* ------------------------------------------------------------------ */
  function showHint() {
    var q = STATE.current;
    if (!q) return;
    var box = $("modalExtra");
    if (!box.hidden && box.dataset.kind === "hint") { box.hidden = true; return; }
    box.dataset.kind = "hint";
    box.innerHTML = '<div class="extra-inner"><h3>İpucu</h3><p>' + renderMd(q.hint || "Bu soru için ipucu yok.") + "</p></div>";
    box.hidden = false;
    $("btnHint").textContent = "İpucuyu gizle";
  }

  function showSolution() {
    var q = STATE.current;
    if (!q) return;
    var box = $("modalExtra");
    if (!box.hidden && box.dataset.kind === "solution") { box.hidden = true; return; }
    box.dataset.kind = "solution";
    box.innerHTML =
      '<div class="extra-inner"><h3>Çözüm</h3>' +
      "<pre>" + esc(q.solution || "") + "</pre>" +
      (q.explanation ? "<p>" + renderMd(q.explanation) + "</p>" : "") +
      "</div>";
    box.hidden = false;
    $("btnSolution").textContent = "Çözümü gizle";
  }

  /* ------------------------------------------------------------------ */
  /* SOZLUK                                                              */
  /* ------------------------------------------------------------------ */
  function renderGlossary() {
    var term = ($("gSearch").value || "").trim().toLowerCase();
    var items = STATE.glossary.filter(function (g) {
      if (!term) return true;
      return (g.fn + " " + g.desc + " " + g.ex).toLowerCase().indexOf(term) >= 0;
    });
    $("glossaryGrid").innerHTML = items.map(function (g) {
      return '<div class="g-card">' +
        '<div class="g-card__fn">' + esc(g.fn) + "</div>" +
        '<div class="g-card__desc">' + esc(g.desc) + "</div>" +
        '<div class="g-card__ex">' + esc(g.ex) + "</div>" +
        "</div>";
    }).join("") || '<p style="color:var(--text-muted)">Eşleşen fonksiyon yok.</p>';
  }

  /* ------------------------------------------------------------------ */
  /* yardimcilar                                                         */
  /* ------------------------------------------------------------------ */
  var toastTimer = null;
  function toast(msg) {
    var t = $("toast");
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.hidden = true; }, 2200);
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem(LS_THEME, theme); } catch (e) {}
  }

  /* ------------------------------------------------------------------ */
  /* BASLATMA                                                            */
  /* ------------------------------------------------------------------ */
  var editor = null;

  function boot() {
    loadLocal();

    var savedTheme = "dark";
    try { savedTheme = localStorage.getItem(LS_THEME) || "dark"; } catch (e) {}
    applyTheme(savedTheme);

    editor = MatlabEditor.create({
      textarea: $("editorInput"),
      highlight: $("editorHighlight"),
      gutter: $("editorGutter"),
      onRun: runCode
    });

    fetch("/api/bootstrap")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        STATE.questions = data.questions || [];
        STATE.notes = data.notes || [];
        STATE.glossary = data.glossary || [];
        STATE.engine = data.engine || { available: false };

        updateProgress();
        applyFilters();
        route();

        if (!STATE.engine.available) {
          toast("Octave bulunamadı — kod çalıştırma kapalı. Kurulum: sudo pacman -S octave");
        }
      })
      .catch(function (err) {
        document.getElementById("quizMain").innerHTML =
          '<div class="empty-state"><div class="empty-state__icon">!</div>' +
          "<h2>Sunucuya ulaşılamadı</h2><p>" + esc(err.message) + "</p></div>";
      });

    /* olaylar */
    window.addEventListener("hashchange", route);

    $("themeToggle").addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme");
      applyTheme(cur === "dark" ? "light" : "dark");
    });

    $("qSearch").addEventListener("input", applyFilters);
    $("qModule").addEventListener("change", applyFilters);
    $("qLevel").addEventListener("change", applyFilters);
    $("qReset").addEventListener("click", function () {
      $("qSearch").value = "";
      $("qModule").value = "";
      $("qLevel").value = "";
      applyFilters();
    });

    $("qList").addEventListener("click", function (ev) {
      var li = ev.target.closest(".q-item");
      if (li && li.dataset.qid) {
        var qid = parseInt(li.dataset.qid, 10);
        if (location.hash !== "#/sorular/" + qid) {
          location.hash = "#/sorular/" + qid;   // route() soruyu acacak
        } else {
          openQuestion(qid);
        }
      }
    });

    $$("#questionModal [data-close]").forEach(function (el) {
      el.addEventListener("click", closeQuestion);
    });

    $("btnRun").addEventListener("click", runCode);
    $("btnHint").addEventListener("click", showHint);
    $("btnSolution").addEventListener("click", showSolution);
    $("btnPrev").addEventListener("click", function () { goRelative(-1); });
    $("btnNext").addEventListener("click", function () { goRelative(1); });

    $("gSearch").addEventListener("input", renderGlossary);

    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && !$("questionModal").hidden) closeQuestion();
    });

    // ilk yuklemede karsilama ekrani goster
    setTimeout(function () {
      if (!STATE.current && location.hash === "#/sorular") {
        $("quizMain").innerHTML = welcomeHtml();
      }
    }, 400);
  }

  function welcomeHtml() {
    var solved = Object.keys(STATE.progress).filter(function (k) {
      return STATE.progress[k] === "solved";
    }).length;
    return '<div class="quiz-start">' +
      "<h2>MATLAB soru bankası</h2>" +
      "<p>100 soru; matrislerden operatörlere, dizi türlerinden matematiksel " +
      "ifade çevrimeye. Kodunu yaz, <strong>Çalıştır</strong>'a bas — yanlışsa " +
      "hatayı ve düzeltme yolunu gösterelim.</p>" +
      '<div class="quiz-stats">' +
      '<div class="quiz-stat"><b>' + STATE.questions.length + "</b><span>soru</span></div>" +
      '<div class="quiz-stat"><b>' + solved + "</b><span>çözüldü</span></div>" +
      '<div class="quiz-stat"><b>' + moduleOptions().length + "</b><span>konu</span></div>" +
      "</div>" +
      '<button class="btn btn--primary" onclick="document.getElementById(\'qList\').firstElementChild.click()">İlk soruyu çöz →</button>' +
      "</div>";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
