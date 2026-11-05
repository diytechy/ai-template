import ast, pathlib, collections
root = pathlib.Path("/home/user/ai-template/project-trajectory/scripts")
hits = []
for p in sorted(list(root.glob("*.py")) + list((root/"kitlib").glob("*.py")) + list((root/"rendering").glob("*.py"))):
    tree = ast.parse(p.read_text(encoding="utf-8"))
    seen = collections.defaultdict(list)
    for node in tree.body:
        targets = []
        if isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            targets = [node.name]
        for t in targets: seen[t].append(node.lineno)
    for name, lines in seen.items():
        if len(lines) > 1 and not name.startswith("__"):
            hits.append((str(p.relative_to(root)), name, lines))
print("module-level names bound more than once (later binding silently wins):", len(hits))
for h in hits[:20]: print("  ", h)
