"""How much of each LLR detail is already in its module's docstring?
Share = |significant words of detail that also occur in the module docstring(s)| / |significant words of detail|
(significant word = alphabetic run >= 4 chars, lowercased: the kit's own paraphrase-advisory tokenization,
 project-trajectory/scripts/trace_text.py paraphrase_advisories). Docstring = module docstring + all function/class
 docstrings of every module in the row's `module` cell.
Usage: python -I overlap.py <repo-root> [SR-xxx ...]  (no SR -> whole registry summary)
"""
import ast, re, sys, tomllib
from pathlib import Path
from collections import defaultdict
ROOT = Path(sys.argv[1])
llr = {k:v for k,v in tomllib.load(open(ROOT/"docs/requirements/low-level-requirements.toml","rb"))["design"].items() if not k.endswith("-000")}
WORD = re.compile(r"[A-Za-z]{4,}")
def words(s): return {w.lower() for w in WORD.findall(s)}
_cache = {}
def docwords(mod):
    if mod in _cache: return _cache[mod]
    p = ROOT / mod
    out = set()
    if p.suffix == ".py" and p.exists():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
            out |= words(ast.get_docstring(tree) or "")
            for n in ast.walk(tree):
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    out |= words(ast.get_docstring(n) or "")
        except Exception: pass
    _cache[mod] = out; return out
kids = defaultdict(list)
for l, r in llr.items():
    for s in r.get("sr_refs", []): kids[s].append(l)
def share(lid):
    r = llr[lid]; w = words(str(r.get("detail","")))
    dw = set()
    for m in str(r.get("module","")).split(";"):
        dw |= docwords(m.strip())
    return (len(w & dw) / len(w)) if w else 0.0, len(w)
if len(sys.argv) > 2:
    for sr in sys.argv[2:]:
        print(f"== {sr}")
        for lid in kids[sr]:
            s, n = share(lid)
            print(f"  {lid}: {s:.0%} of {n} significant detail words already in module docstrings  ({llr[lid]['module']})")
else:
    shares = sorted((share(l)[0], l) for l in llr)
    import statistics
    vals = [s for s, _ in shares]
    print(f"LLR rows: {len(vals)}; median share {statistics.median(vals):.0%}; >=50%: {sum(v>=0.5 for v in vals)}; >=70%: {sum(v>=0.7 for v in vals)}; <30%: {sum(v<0.3 for v in vals)}")
