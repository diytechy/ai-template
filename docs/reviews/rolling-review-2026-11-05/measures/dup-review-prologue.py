import ast, pathlib
root = pathlib.Path("/home/user/ai-template/project-trajectory/scripts")
mods = 0; dup_lines = 0; names_twice = 0
for p in sorted(list(root.glob("*.py")) + list((root/"rendering").glob("*.py"))):
    tree = ast.parse(p.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Try):
            for h in node.handlers:
                if h.type is not None and "ImportError" in ast.unparse(h.type):
                    body_imports = [n for n in node.body if isinstance(n, (ast.Import, ast.ImportFrom))]
                    handler_imports = [n for n in h.body if isinstance(n, (ast.Import, ast.ImportFrom))]
                    if body_imports and handler_imports:
                        mods += 1
                        dup_lines += sum(n.end_lineno - n.lineno + 1 for n in handler_imports)
                        names_twice += sum(len(n.names) for n in handler_imports)
print("modules with try/except-ImportError import prologue:", mods)
print("import statement lines repeated in the except arm:", dup_lines, "| imported names written twice:", names_twice)
