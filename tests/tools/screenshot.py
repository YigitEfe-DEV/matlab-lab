#!/usr/bin/env python3
"""Belirtilen URL/theme/gorunum ile ekran goruntusu alir ve JS hatalarini raporlar."""

import base64
import json
import os
import subprocess
import sys
import time
import urllib.request

import websocket

CHROME = "/usr/bin/google-chrome-stable"
URL = sys.argv[1]
OUT = sys.argv[2]
WIDTH = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
HEIGHT = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
THEME = sys.argv[5] if len(sys.argv) > 5 else ""
PORT = 9500 + (os.getpid() % 400)
profile = "/tmp/cdp-shot-%d" % os.getpid()

proc = subprocess.Popen(
    [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
     "--remote-allow-origins=*", f"--remote-debugging-port={PORT}",
     f"--user-data-dir={profile}", f"--window-size={WIDTH},{HEIGHT}", URL],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)

ws_url = None
for _ in range(60):
    time.sleep(0.4)
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list", timeout=2) as r:
            tabs = json.load(r)
        pages = [t for t in tabs if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
        if pages:
            ws_url = pages[0]["webSocketDebuggerUrl"]
            break
    except Exception:
        continue

if not ws_url:
    print("Chrome baglantisi kurulamadi")
    proc.kill()
    sys.exit(1)

ws = websocket.create_connection(ws_url, timeout=30, suppress_origin=True)
_id = [0]
errors = []


def cmd(method, params=None):
    _id[0] += 1
    ws.send(json.dumps({"id": _id[0], "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("method") == "Runtime.exceptionThrown":
            errors.append(json.dumps(msg.get("params", {}))[:400])
        if msg.get("id") == _id[0]:
            return msg.get("result", {})


def evaluate(expr):
    return cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True}) \
        .get("result", {}).get("value")


try:
    cmd("Page.enable")
    cmd("Runtime.enable")
    time.sleep(4)
    if THEME:
        evaluate(f"document.documentElement.setAttribute('data-theme','{THEME}')")
        time.sleep(0.5)
    shot = cmd("Page.captureScreenshot", {"format": "png"})
    with open(OUT, "wb") as fh:
        fh.write(base64.b64decode(shot["data"]))
    print("Yazildi:", OUT)
    print("JS hatalari:", len(errors))
    for e in errors[:5]:
        print("  ", e)
finally:
    ws.close()
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
