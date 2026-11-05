import ast, pathlib, collections
root = pathlib.Path("/home/user/ai-template/project-trajectory/scripts")
to_kitlib = to_script = 0; chains = 0; per_target = collections.Counter()
for p in sorted(list(root.glob("*.py")) + list((root/"rendering").glob("*.py"))):
    tree = ast.parse(p.read_text(encoding="utf-8"))
    kit_aliases = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                nm = a.asname or a.name
                src = (node.module or "") if isinstance(node, ast.ImportFrom) else a.name
                if "kitlib" in src or "kitlib" in a.name: kit_aliases.add(nm.split(".")[0])
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0], ast.Name):
            v = node.value
            if isinstance(v, ast.Attribute) and isinstance(v.value, ast.Name):
                base = v.value.id
                if base in kit_aliases: to_kitlib += 1
                else:
                    to_script += 1; per_target[base] += 1
print("aliases pointing at kitlib:", to_kitlib, "| pointing at a sibling SCRIPT module (hop chain):", to_script)
print("most-aliased sibling targets:", per_target.most_common(10))
