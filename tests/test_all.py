import os, sys, concurrent.futures
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from mlab.questions import QUESTIONS
from mlab.runner import run_matlab_code

def check(q):
    if q['kind'] == 'mcq':
        return (q['id'], True, 'mcq - atlandi')
    r = run_matlab_code(q['solution'], q['verify'], q['expectError'] or None, q['stdin'] or '')
    return (q['id'], r.ok, (r.message or r.error or '')[:220])

fails = []
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    for qid, ok, msg in ex.map(check, QUESTIONS):
        if not ok:
            fails.append((qid, msg))
print(f"Toplam: {len(QUESTIONS)} | Gecen: {len(QUESTIONS)-len(fails)} | Kalan: {len(fails)}")
for qid, msg in fails:
    print(f"  [FAIL] #{qid}: {msg}")
