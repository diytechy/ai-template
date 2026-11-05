"""Dump each test module's docstring + first two test function sources for classification."""
import ast, sys, pathlib
root = pathlib.Path('/home/user/ai-template/tests')
out = []
for p in sorted(root.glob('test_*.py')):
    src = p.read_text(encoding='utf-8', errors='replace')
    lines = src.splitlines()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        out.append(f"=== {p.name} ({len(lines)} lines) SYNTAX ERROR {e}")
        continue
    doc = ast.get_docstring(tree) or ''
    tests = [n for n in tree.body if isinstance(n, (ast.FunctionDef,)) and n.name.startswith('test_')]
    # also tests inside classes
    for n in tree.body:
        if isinstance(n, ast.ClassDef):
            for m in n.body:
                if isinstance(m, ast.FunctionDef) and m.name.startswith('test_'):
                    tests.append(m)
    out.append(f"=== {p.name} ({len(lines)} lines, {len(tests)} tests)")
    out.append("DOC: " + doc[:1200].replace('\n', ' '))
    for t in tests[:2]:
        body = '\n'.join(lines[t.lineno-1:min(t.end_lineno, t.lineno+30)])
        out.append(f"--- {t.name} L{t.lineno}")
        out.append(body)
    out.append("")
pathlib.Path(sys.argv[1]).write_text('\n'.join(out), encoding='utf-8')
print(len(out))
