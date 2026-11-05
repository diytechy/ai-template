import ast, sys, pathlib, collections
root = pathlib.Path("/home/user/ai-template/project-trajectory/scripts")
rows = []
for p in sorted(list(root.glob("*.py")) + list((root/"kitlib").glob("*.py")) + list((root/"rendering").glob("*.py"))):
    try:
        tree = ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError as e:
        print("SYNTAX", p, e); continue
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            rows.append((node.name, str(p.relative_to(root)), node.lineno, node.end_lineno - node.lineno + 1))
        elif isinstance(node, ast.ClassDef):
            rows.append(("class " + node.name, str(p.relative_to(root)), node.lineno, node.end_lineno - node.lineno + 1))
out = pathlib.Path(sys.argv[1])
with out.open("w") as f:
    for r in rows:
        f.write("\t".join(map(str, r)) + "\n")
print(len(rows), "defs")
