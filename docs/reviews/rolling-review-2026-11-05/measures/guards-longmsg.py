"""Rank the longest message string constants in kit scripts + hooks by word count."""
import ast, re, sys
from pathlib import Path
root = Path(sys.argv[1])
rows = []
KEY = re.compile(r"REFUS|refus|FAIL|WARN|Fix|fix:|nothing was merged|HOLD|held|STALE|cannot|must|never", re.I)
for p in list((root/"project-trajectory/scripts").glob("*.py")) + list((root/"project-trajectory/scripts/kitlib").glob("*.py")):
    try:
        tree = ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError:
        continue
    # skip docstrings: collect Expr-level string statements to exclude
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
                docs.add(id(node.body[0].value))
    # standalone string statements (comments-as-strings)
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            docs.add(id(node.value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs:
            s = node.value
            if len(s) >= 120 and KEY.search(s) and not s.lstrip().startswith(("#", "<!--", "<")):
                words = len(s.split())
                rows.append((words, str(p.relative_to(root)), node.lineno, s))
        if isinstance(node, ast.JoinedStr):
            s = "".join(v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str))
            if len(s) >= 120 and KEY.search(s):
                rows.append((len(s.split()), str(p.relative_to(root)), node.lineno, s))
# hooks: group consecutive echo/printf lines
for h in (root/"project-trajectory/hooks").iterdir():
    lines = h.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        if re.match(r"\s*(echo|printf) ", lines[i]):
            j = i; buf = []
            while j < len(lines) and re.match(r"\s*(echo|printf) ", lines[j]):
                buf.append(re.sub(r"^\s*(echo|printf) '?\"?", "", lines[j]).rstrip("\\\" >&2;"))
                j += 1
            s = " ".join(buf)
            if KEY.search(s):
                rows.append((len(s.split()), str(h.relative_to(root)), i+1, s))
            i = j
        else:
            i += 1
rows.sort(reverse=True)
seen = set()
n = 0
for words, path, line, s in rows:
    k = (path, line)
    if k in seen: continue
    seen.add(k); n += 1
    print(f"{words:4d} words  {path}:{line}\n      {s[:230].replace(chr(10),' ')}...\n")
    if n >= 25: break
print("total candidate messages >=120 chars:", len(rows))
