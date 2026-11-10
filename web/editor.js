/* ==========================================================================
   MATLAB kod editoru — textarea uzerine vurgulama katmani.
   Bagimlilik yok, tamamen yerel. Satir numaralari, girinti, kisa yollar.
   ========================================================================== */
(function (global) {
  "use strict";

  const KEYWORDS = new Set([
    "function", "end", "if", "else", "elseif", "for", "while", "switch", "case",
    "otherwise", "break", "continue", "return", "try", "catch", "global",
    "persistent", "classdef", "properties", "methods", "events", "parfor",
    "spmd", "do", "until", "unwind_protect", "unwind_protect_cleanup"
  ]);

  const BUILTINS = new Set([
    "abs", "acos", "acosh", "asin", "asinh", "atan", "atan2", "atanh", "balance",
    "bar", "bar3", "cell2mat", "cellfun", "ceil", "char", "class", "clock",
    "colon", "compan", "compinv", "cond", "conv", "corrcoef", "cross", "cumprod",
    "cumsum", "deal", "delete", "det", "diag", "diff", "disp", "dot", "eig",
    "eigs", "error", "exist", "exp", "eye", "factor", "feval", "fft", "fill",
    "find", "fliplr", "fliplu", "floor", "fopen", "fprintf", "fread", "fscanf",
    "fullfile", "func2str", "gamma", "gcd", "gradient", "grid", "hankel", "help",
    "hess", "hist", "hold", "horzcat", "imag", "inv", "isempty", "isequal",
    "isfield", "isfinite", "isinf", "islogical", "ismember", "isnan", "isnumeric",
    "isreal", "isscalar", "isstruct", "isvector", "kron", "lcm", "length",
    "linspace", "load", "log", "log10", "log2", "loglog", "lookfor", "lu",
    "magic", "mat2str", "max", "mean", "median", "mesh", "min", "mod", "nargin",
    "nargout", "nnz", "norm", "num2str", "numel", "nthroot", "ones", "pinv",
    "plot", "poly", "polyfit", "polyval", "prod", "qr", "quad", "rand", "randi",
    "randn", "randperm", "rank", "real", "regexp", "rem", "repmat", "reshape",
    "roots", "save", "schur", "sec", "sech", "set", "sign", "sin", "sind",
    "size", "sort", "sortrows", "sprintf", "sqrt", "std", "str2double", "str2num",
    "strcat", "strcmp", "strcmpi", "strfind", "strrep", "strsplit", "struct",
    "subplot", "sum", "svd", "tan", "tand", "tic", "toc", "title", "trapz",
    "triu", "tril", "unique", "upper", "lower", "var", "vertcat", "warning",
    "who", "whos", "xlabel", "ylabel", "zeros", "isvector", "atan2", "nchoosek",
    "isprime", "primes", "sign", "factorial", "deg2rad", "rad2deg", "asin",
    "acos", "atan", "input", "disp", "double", "single", "int8", "uint8", "logical",
    "cell", "fieldnames", "rmfield", "isfield", "exist", "numel", "randsample"
  ]);

  const IDENT_TAIL = /[A-Za-z0-9_]/;
  const TRANSPOSE_PREV = /[A-Za-z0-9_\)\]\}]/;

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function span(cls, text) {
    return '<span class="' + cls + '">' + escapeHtml(text) + "</span>";
  }

  /** MATLAB kaynak kodunu renklendirilmis HTML'e cevirir. */
  function highlightMatlab(src) {
    var out = "";
    var i = 0;
    var n = src.length;

    while (i < n) {
      var ch = src[i];

      // --- yorum ---
      if (ch === "%") {
        var nl = src.indexOf("\n", i);
        var end = nl < 0 ? n : nl;
        out += span("t-com", src.slice(i, end));
        i = end;
        continue;
      }

      // --- metin / transpoz ---
      if (ch === "'" || ch === '"') {
        var prev = i > 0 ? src[i - 1] : "";
        var isTranspose = ch === "'" && TRANSPOSE_PREV.test(prev);
        if (!isTranspose) {
          var j = i + 1;
          while (j < n) {
            if (src[j] === ch) {
              if (src[j + 1] === ch) { j += 2; continue; } // kacisli tirnak
              break;
            }
            if (src[j] === "\n") break;
            j++;
          }
          var endStr = Math.min(j + 1, n);
          out += span("t-str", src.slice(i, endStr));
          i = endStr;
          continue;
        }
        out += span("t-op", "'");
        i++;
        continue;
      }

      // --- sayi ---
      if (/[0-9]/.test(ch) || (ch === "." && /[0-9]/.test(src[i + 1] || ""))) {
        var k = i;
        while (k < n && /[0-9.eE+\-]/.test(src[k])) {
          if ((src[k] === "+" || src[k] === "-") && !/[eE]/.test(src[k - 1] || "")) break;
          k++;
        }
        if (k === i) k = i + 1;
        out += span("t-num", src.slice(i, k));
        i = k;
        continue;
      }

      // --- tanimlayici ---
      if (/[A-Za-z_]/.test(ch)) {
        var m = i;
        while (m < n && IDENT_TAIL.test(src[m])) m++;
        var word = src.slice(i, m);
        if (KEYWORDS.has(word)) out += span("t-kw", word);
        else if (BUILTINS.has(word)) out += span("t-fn", word);
        else out += escapeHtml(word);
        i = m;
        continue;
      }

      // --- operator ---
      if (/[+\-*/\\^=<>~!&|:]/.test(ch)) {
        var p = i;
        while (p < n && /[+\-*/\\^=<>~!&|:]/.test(src[p])) p++;
        out += span("t-op", src.slice(i, p));
        i = p;
        continue;
      }

      out += escapeHtml(ch);
      i++;
    }

    return out;
  }

  /**
   * Editoru olusturur.
   * @param {object} o  { textarea, highlight, gutter, onRun }
   */
  function createEditor(o) {
    var ta = o.textarea;
    var pre = o.highlight;
    var code = pre.querySelector("code") || pre;
    var gutter = o.gutter;
    var gutterInner = document.createElement("div");
    gutterInner.className = "gutter__inner";
    gutter.appendChild(gutterInner);

    function render() {
      var src = ta.value;
      var html = highlightMatlab(src);
      code.innerHTML = html + (src.endsWith("\n") ? "\n" : "");

      var lines = src.split("\n").length;
      if (src.endsWith("\n")) lines += 1;
      var nums = [];
      for (var i = 1; i <= lines; i++) nums.push(i);
      gutterInner.innerHTML = nums
        .map(function (n) { return "<div>" + n + "</div>"; })
        .join("");
    }

    function syncScroll() {
      pre.scrollTop = ta.scrollTop;
      pre.scrollLeft = ta.scrollLeft;
      gutterInner.style.transform = "translateY(" + (-ta.scrollTop) + "px)";
    }

    ta.addEventListener("input", render);
    ta.addEventListener("scroll", syncScroll);

    // Tab / Shift+Tab ile girinti
    ta.addEventListener("keydown", function (ev) {
      if (ev.key === "Tab") {
        ev.preventDefault();
        var start = ta.selectionStart;
        var end = ta.selectionEnd;
        var value = ta.value;

        if (ev.shiftKey) {
          // geri girinti
          var lineStart = value.lastIndexOf("\n", start - 1) + 1;
          var chunk = value.slice(lineStart, start);
          var trimmed = chunk.replace(/^ {1,4}/, "");
          ta.value = value.slice(0, lineStart) + trimmed + value.slice(end);
          ta.selectionStart = ta.selectionEnd = lineStart + trimmed.length;
        } else if (start !== end) {
          // secili satirlari girintile
          var s0 = value.lastIndexOf("\n", start - 1) + 1;
          var s1 = value.indexOf("\n", end);
          if (s1 < 0) s1 = value.length;
          var block = value.slice(s0, s1)
            .split("\n")
            .map(function (l) { return "    " + l; })
            .join("\n");
          ta.value = value.slice(0, s0) + block + value.slice(s1);
          ta.selectionStart = s0;
          ta.selectionEnd = s0 + block.length;
        } else {
          ta.value = value.slice(0, start) + "    " + value.slice(end);
          ta.selectionStart = ta.selectionEnd = start + 4;
        }
        render();
        return;
      }

      if (ev.key === "Enter" && !ev.ctrlKey && !ev.metaKey) {
        // otomatik girinti: onceki satirin girintisini koru
        var pos = ta.selectionStart;
        var before = ta.value.slice(0, pos);
        var ls = before.lastIndexOf("\n");
        var line = before.slice(ls + 1);
        var indent = (line.match(/^\s*/) || [""])[0];
        if (indent.length) {
          ev.preventDefault();
          var ins = "\n" + indent;
          ta.value = ta.value.slice(0, pos) + ins + ta.value.slice(ta.selectionEnd);
          ta.selectionStart = ta.selectionEnd = pos + ins.length;
          render();
        }
        return;
      }
    });

    // Ctrl+Enter
    ta.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) {
        ev.preventDefault();
        if (o.onRun) o.onRun();
      }
    });

    render();

    return {
      getValue: function () { return ta.value; },
      setValue: function (v) { ta.value = v || ""; render(); ta.scrollTop = 0; syncScroll(); },
      focus: function () { ta.focus(); },
      render: render,
      textarea: ta
    };
  }

  global.MatlabEditor = { create: createEditor, highlight: highlightMatlab };
})(window);
