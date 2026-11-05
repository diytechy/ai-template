import ast, pathlib, re, collections
root = pathlib.Path("/home/user/ai-template/project-trajectory/scripts")
tests = pathlib.Path("/home/user/ai-template/tests")
hooks = pathlib.Path("/home/user/ai-template/project-trajectory/hooks")
files = sorted(list(root.glob("*.py")) + list((root/"kitlib").glob("*.py")) + list((root/"rendering").glob("*.py")))
texts = {p: p.read_text(encoding="utf-8", errors="replace") for p in files}
prod = "\n".join(texts.values()) + "\n".join(p.read_text(errors="replace") for p in hooks.iterdir() if p.is_file())
# also count docs/stack.ini, process.toml, check steps referencing CLI entry? we only care about python symbol references
test_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in tests.glob("*.py"))
dead = []; dead_test_only = []
for p, text in texts.items():
    tree = ast.parse(text)
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)): continue
        name = node.name
        if name in ("main",) or name.startswith("test_"): continue
        pat = re.compile(r"\b%s\b" % re.escape(name))
        # references in production: occurrences minus the def line itself
        n_prod = len(pat.findall(prod)) - 1
        # subtract docstring/comment mentions roughly? keep raw: a name mentioned only in a comment still counts as "referenced" (conservative)
        if n_prod <= 0:
            n_test = len(pat.findall(test_text))
            size = node.end_lineno - node.lineno + 1
            (dead_test_only if n_test else dead).append((str(p.relative_to(root)), node.lineno, name, size, n_test))
print("top-level functions with ZERO references anywhere in scripts/hooks (conservative: comments count as refs)")
print("  unreferenced everywhere:", len(dead), "functions,", sum(d[3] for d in dead), "lines")
print("  referenced ONLY from tests:", len(dead_test_only), "functions,", sum(d[3] for d in dead_test_only), "lines")
by_mod = collections.Counter(d[0] for d in dead_test_only)
print("  test-only by module (top 12):", by_mod.most_common(12))
print("  sample test-only:", [(d[0], d[1], d[2]) for d in sorted(dead_test_only, key=lambda d: -d[3])[:12]])
print("  sample unreferenced:", [(d[0], d[1], d[2]) for d in sorted(dead, key=lambda d: -d[3])[:12]])
