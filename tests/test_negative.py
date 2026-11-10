import os, sys, concurrent.futures
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from mlab.questions import QUESTIONS
from mlab.runner import run_matlab_code

def check(q):
    if q['kind'] == 'mcq':
        return (q['id'], True, 'mcq')
    # bilerek yanlis cevap: sonuc 0 + beklenen degiskenler bos
    bad = "sonuc = 0;\n"
    r = run_matlab_code(bad, q['verify'], q['expectError'] or None, q['stdin'] or '')
    msg = r.message or r.error or ''
    return (q['id'], (not r.ok) and len(msg) > 0, msg[:150])

bad = []
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    for qid, good, msg in ex.map(check, QUESTIONS):
        if not good:
            bad.append((qid, msg))
print(f"Yanlis cevap testi -> Sorular: {len(QUESTIONS)} | Beklendigi gibi reddedilen: {len(QUESTIONS)-len(bad)} | Sorunlu: {len(bad)}")
for qid, msg in bad:
    print(f"  [PROBLEM] #{qid}: {msg!r}")
