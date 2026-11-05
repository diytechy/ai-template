import ast, pathlib, collections
root = pathlib.Path("/home/user/ai-template/project-trajectory/scripts")
files = sorted(list(root.glob("*.py")) + list((root/"kitlib").glob("*.py")) + list((root/"rendering").glob("*.py")))
per = collections.Counter(); total = 0; examples = collections.defaultdict(list)
for p in files:
    tree = ast.parse(p.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            v = node.value
            # X = mod.attr  or  X = mod.sub.attr  (pure re-export alias)
            if isinstance(v, ast.Attribute) and isinstance(v.value, (ast.Name, ast.Attribute)):
                rel = str(p.relative_to(root)); per[rel] += 1; total += 1
                if len(examples[rel]) < 2: examples[rel].append("%s = %s" % (node.targets[0].id, ast.unparse(v)))
print("module-level re-export aliases (X = module.attr):", total, "in", len(per), "modules")
for rel, n in per.most_common(18):
    print("%4d  %-28s e.g. %s" % (n, rel, "; ".join(examples[rel])))
