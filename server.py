#!/usr/bin/env python3
"""MATLAB Ogrenim Sitesi — yerel HTTP sunucusu.

Bagimlilik yoktur (yalnızca Python 3 standart kütüphanesi).
Kod calistirma istegi `mlab.runner` uzerinden GNU Octave'a gonderilir.

Kullanim:
    python3 server.py [--port 8787] [--host 127.0.0.1]
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import posixpath
import socket
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mlab.notes import GLOSSARY, NOTES
from mlab.questions import QUESTIONS
from mlab.runner import OCTAVE_BIN, run_matlab_code

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

RUN_TIMEOUT = 20
MAX_CODE_BYTES = 64 * 1024


class Handler(BaseHTTPRequestHandler):
    server_version = "MATLABLab/1.0"
    protocol_version = "HTTP/1.1"

    # ------------------------------------------------------------------ #
    # yardimcilar
    # ------------------------------------------------------------------ #
    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, body: bytes, content_type: str, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return None
        if length <= 0 or length > MAX_CODE_BYTES:
            return None
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    def log_message(self, fmt, *args):  # gürültüyü azalt
        if "--verbose" in sys.argv:
            super().log_message(fmt, *args)

    # ------------------------------------------------------------------ #
    # rotalar
    # ------------------------------------------------------------------ #
    def do_GET(self):
        path = urlparse(self.path).path
        try:
            if path in ("/", "/index.html"):
                return self._serve_file("index.html")
            if path == "/api/bootstrap":
                return self._send_json(
                    {
                        "questions": QUESTIONS,
                        "notes": NOTES,
                        "glossary": GLOSSARY,
                        "engine": {
                            "octave": OCTAVE_BIN or "",
                            "available": bool(OCTAVE_BIN),
                        },
                    }
                )
            if path == "/api/health":
                return self._send_json(
                    {"status": "ok", "octave": OCTAVE_BIN or "", "available": bool(OCTAVE_BIN)}
                )
            return self._serve_static(path)
        except BrokenPipeError:
            pass
        except Exception:
            traceback.print_exc()
            self._send_json({"error": "Sunucu hatasi"}, 500)

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/run":
            return self._send_json({"error": "Bilinmeyen uc nokta"}, 404)
        payload = self._read_json()
        if payload is None:
            return self._send_json({"error": "Gecersiz istek govdesi"}, 400)

        code = payload.get("code") or ""
        if not isinstance(code, str):
            return self._send_json({"error": "code alani metin olmali"}, 400)
        if len(code.encode("utf-8")) > MAX_CODE_BYTES:
            return self._send_json({"error": "Kod cok uzun (en fazla 64 KB)"}, 400)

        qid = payload.get("qid")
        question = next((q for q in QUESTIONS if q["id"] == qid), None)
        if question is None:
            return self._send_json({"error": "Soru bulunamadi"}, 404)

        # MCQ sorulari calistirilmaz
        if question["kind"] == "mcq":
            return self._send_json(
                {
                    "ok": False,
                    "message": "Bu coktan secmeli sorudur; kod calistirilmaz.",
                    "stdout": "",
                    "stderr": "",
                    "error": "",
                    "engine": "octave",
                    "timedOut": False,
                    "durationMs": 0,
                }
            )

        result = run_matlab_code(
            code,
            verify_code=question.get("verify", ""),
            expect_error=question.get("expectError") or None,
            stdin_data=payload.get("stdin") or question.get("stdin") or "",
        )
        return self._send_json(result.to_dict())

    # ------------------------------------------------------------------ #
    # statik dosyalar
    # ------------------------------------------------------------------ #
    def _serve_file(self, name: str):
        path = os.path.join(WEB_DIR, name)
        if not os.path.isfile(path):
            return self._send_json({"error": "Dosya bulunamadi"}, 404)
        with open(path, "rb") as fh:
            body = fh.read()
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript",):
            ctype += "; charset=utf-8"
        return self._send_bytes(body, ctype)

    def _serve_static(self, url_path: str):
        # dizin listelemeyi engelle
        clean = posixpath.normpath(url_path).lstrip("/")
        if clean.startswith("..") or os.path.isabs(clean):
            return self._send_json({"error": "Yasakli yol"}, 403)
        path = os.path.join(WEB_DIR, clean)
        if not os.path.isfile(path):
            return self._send_json({"error": "Dosya bulunamadi: " + clean}, 404)
        with open(path, "rb") as fh:
            body = fh.read()
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype == "application/javascript":
            ctype += "; charset=utf-8"
        return self._send_bytes(body, ctype)


def main():
    parser = argparse.ArgumentParser(description="MATLAB ogrenim sitesi")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--open", action="store_true", help="tarayiciyi otomatik ac")
    args = parser.parse_args()

    if not OCTAVE_BIN:
        print("UYARI: GNU Octave bulunamadi. Kod calistirma ozelligi devre disi kalir.")
        print("      Kurulum: sudo pacman -S octave")
    else:
        print(f"Engine : {OCTAVE_BIN}")

    try:
        httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    except OSError as exc:
        print(f"Port {args.port} acilamadi: {exc}")
        print("Farkli bir port dene:  python3 server.py --port 8788")
        sys.exit(1)

    url = f"http://{args.host}:{args.port}/"
    print(f"Sunucu : {url}")
    print(f"Durdurmak icin: Ctrl+C")
    if args.open:
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruldu.")
        httpd.shutdown()


if __name__ == "__main__":
    main()
