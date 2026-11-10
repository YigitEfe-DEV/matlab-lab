#!/usr/bin/env python3
"""Chrome DevTools Protocol ile arayuz testi: kod yaz -> calistir -> ekran goruntusu."""

import base64
import json
import os
import subprocess
import sys
import time
import urllib.request

import websocket

CHROME = "/usr/bin/google-chrome-stable"
PORT = 9400 + (os.getpid() % 300)
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8787/#/sorular/4"
CODE = sys.argv[2] if len(sys.argv) > 2 else "A = [1 2; 3 4];\nB = [5 6; 7 8];\nsonuc = A*B;"
OUT = sys.argv[3] if len(sys.argv) > 3 else "/tmp/cdp_shot.png"
WIDTH = int(sys.argv[4]) if len(sys.argv) > 4 else 1440
HEIGHT = int(sys.argv[5]) if len(sys.argv) > 5 else 1050

profile = "/tmp/cdp-profile-%d" % os.getpid()
subprocess.run(["rm", "-rf", profile], check=False)
proc = subprocess.Popen(
    [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--remote-allow-origins=*",
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={profile}",
        f"--window-size={WIDTH},{HEIGHT}",
        URL,
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
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


def cmd(method, params=None):
    _id[0] += 1
    ws.send(json.dumps({"id": _id[0], "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == _id[0]:
            if "error" in msg:
                raise RuntimeError(msg["error"])
            return msg.get("result", {})


def evaluate(expr):
    res = cmd(
        "Runtime.evaluate",
        {"expression": expr, "awaitPromise": True, "returnByValue": True},
    )
    return res.get("result", {}).get("value")


try:
    cmd("Page.enable")
    cmd("Runtime.enable")
    time.sleep(3.5)

    # Editor icerigini yaz
    code_js = json.dumps(CODE)
    evaluate(
        "(function(){"
        "var ta=document.getElementById('editorInput');"
        f"ta.value={code_js};"
        "ta.dispatchEvent(new Event('input',{bubbles:true}));"
        "return ta.value.length;})()"
    )
    time.sleep(0.3)

    # Calistir
    evaluate("document.getElementById('btnRun').click();")
    time.sleep(6)

    # Konsol + geri bildirim metnini oku
    info = evaluate(
        "(function(){"
        "return JSON.stringify({"
        "console:(document.getElementById('consoleBody')||{}).textContent||'',"
        "feedback:(document.getElementById('feedbackTitle')||{}).textContent||'',"
        "msg:(document.getElementById('feedbackMsg')||{}).textContent||'',"
        "diag:document.getElementById('diagnosis').hidden===false"
        "  ? (document.getElementById('diagTitle')||{}).textContent : ''"
        "});})()"
    )
    print("UI:", info)

    shot = cmd("Page.captureScreenshot", {"format": "png"})
    with open(OUT, "wb") as fh:
        fh.write(base64.b64decode(shot["data"]))
    print("Yazildi:", OUT)
finally:
    ws.close()
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
