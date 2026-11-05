"""Control for overlap.py: the same share computed against the docstrings of a DIFFERENT module
(the module cell of the LLR 37 rows further down the registry, wrapping), so common-word noise is visible."""
import ast, re, sys, tomllib, statistics
from pathlib import Path
ROOT = Path(sys.argv[1])
llr = {k:v for k,v in tomllib.load(open(ROOT/"docs/requirements/low-level-requirements.toml","rb"))["design"].items() if not k.endswith("-000")}
WORD = re.compile(r"[A-Za-z]{4,}")
def words(s): return {w.lower() for w in WORD.findall(s)}
_c = {}
def docwords(mod):
    if mod in _c: return _c[mod]
    p = ROOT / mod; out = set()
    if p.suffix == ".py" and p.exists():
        try:
            t = ast.parse(p.read_text(encoding="utf-8")); out |= words(ast.get_docstring(t) or "")
            for n in ast.walk(t):
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)): out |= words(ast.get_docstring(n) or "")
        except Exception: pass
    _c[mod] = out; return out
ids = list(llr)
def share(lid, modcell):
    w = words(str(llr[lid].get("detail",""))); dw = set()
    for m in str(modcell).split(";"): dw |= docwords(m.strip())
    return len(w & dw)/len(w) if w else 0.0
real = [share(l, llr[l].get("module","")) for l in ids]
ctrl = [share(l, llr[ids[(i+37) % len(ids)]].get("module","")) for i,l in enumerate(ids)]
print(f"n={len(ids)}  own-module median {statistics.median(real):.0%} (>=70%: {sum(v>=0.7 for v in real)})   control (other module) median {statistics.median(ctrl):.0%} (>=70%: {sum(v>=0.7 for v in ctrl)})")
better = sum(1 for r,c in zip(real,ctrl) if r > c)
print(f"rows where own-module share exceeds the control: {better}/{len(ids)}; mean lift {statistics.mean(r-c for r,c in zip(real,ctrl)):+.0%}")
