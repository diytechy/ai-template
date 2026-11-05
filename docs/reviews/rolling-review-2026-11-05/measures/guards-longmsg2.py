"""Context-aware census: longest REFUSAL/WARNING messages (stderr prints, sys.exit, raise,
returns from *refusal*/*hold*/*lines*/*fail* functions, REMEDY/FIX/HINT constants, hook echo blocks)."""
import ast, re, sys
from pathlib import Path
root = Path(sys.argv[1])
NAME_RE = re.compile(r"refus|hold|fail|_lines|warn|notice|remedy|hint|_cause|refusal|banner|die", re.I)
CONST_RE = re.compile(r"REMEDY|FIX|HINT|REFUS|WARN|NOTICE|NO_TERMINAL|ASK$|_MSG|MESSAGE|SQUASH", re.I)
rows = []
def text_of(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str): return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "format":
        return text_of(node.func.value)
    if isinstance(node, ast.BinOp): return (text_of(node.left) or "") + (text_of(node.right) or "")
    return None
def is_stderr_print(call):
    return isinstance(call.func, ast.Name) and call.func.id == "print" and any(
        k.arg == "file" and isinstance(k.value, ast.Attribute) and k.value.attr == "stderr" for k in call.keywords)
def is_exit(call):
    return (isinstance(call.func, ast.Attribute) and call.func.attr == "exit") or (isinstance(call.func, ast.Name) and call.func.id in ("exit","fail","_refusal","_say"))
for p in list((root/"project-trajectory/scripts").glob("*.py")) + list((root/"project-trajectory/scripts/kitlib").glob("*.py")):
    tree = ast.parse(p.read_text(encoding="utf-8"))
    for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.Module))]:
        fname = getattr(fn, "name", "<module>")
        for node in ast.walk(fn):
            cands = []
            if isinstance(node, ast.Call) and (is_stderr_print(node) or is_exit(node)):
                cands = [(a, "stderr/exit") for a in node.args]
            elif isinstance(node, ast.Raise) and node.exc is not None:
                exc = node.exc
                cands = [(a, "raise") for a in (exc.args if isinstance(exc, ast.Call) else [exc])]
            elif isinstance(node, ast.Return) and node.value is not None and NAME_RE.search(fname):
                cands = [(node.value, "return:"+fname)]
            elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and CONST_RE.search(t.id) for t in node.targets):
                cands = [(node.value, "const:"+",".join(t.id for t in node.targets if isinstance(t, ast.Name)))]
            for a, how in cands:
                s = text_of(a)
                if s and len(s) >= 80:
                    rows.append((len(s.split()), str(p.relative_to(root)), a.lineno, how, s))
for h in (root/"project-trajectory/hooks").iterdir():
    lines = h.read_text(encoding="utf-8").splitlines(); i = 0
    while i < len(lines):
        if re.match(r"\s*(echo|printf) ", lines[i]):
            j = i; buf = []
            while j < len(lines) and re.match(r"\s*(echo|printf) ", lines[j]):
                buf.append(re.sub(r"^\s*(echo|printf) '?\"?", "", lines[j]).rstrip("\\\" >&2;")); j += 1
            s = " ".join(buf); rows.append((len(s.split()), str(h.relative_to(root)), i+1, "hook-echo", s)); i = j
        else: i += 1
rows.sort(reverse=True); seen=set(); n=0
for words, path, line, how, s in rows:
    if (path,line) in seen: continue
    seen.add((path,line)); n+=1
    print(f"{words:4d}w {path}:{line} [{how}]\n      {s[:200].replace(chr(10),' ')}\n")
    if n>=30: break
print("messages >=80 chars in refusal/warning contexts:", len(rows))
import statistics
ws=[r[0] for r in rows]; print("median words:", statistics.median(ws), " >=60 words:", sum(1 for w in ws if w>=60), " >=40 words:", sum(1 for w in ws if w>=40))
