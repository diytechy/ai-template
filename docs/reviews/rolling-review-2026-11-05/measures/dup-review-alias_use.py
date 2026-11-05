import ast, pathlib, re, collections
root = pathlib.Path("/home/user/ai-template/project-trajectory/scripts")
tests = pathlib.Path("/home/user/ai-template/tests")
def aliases(p):
    out = {}
    for node in ast.parse(p.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0], ast.Name):
            v = node.value
            if isinstance(v, ast.Attribute) and isinstance(v.value, (ast.Name, ast.Attribute)):
                out[node.targets[0].id] = ast.unparse(v)
    return out
test_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in tests.glob("*.py"))
script_text = {p.name: p.read_text(encoding="utf-8", errors="replace") for p in root.glob("*.py")}
for mod, short in [("check_trajectory.py", ["ct", "check_trajectory", "_ct"]), ("agent_loop.py", ["agent_loop", "al", "loop"]), ("agent_common.py", ["ac", "agent_common", "_ac"])]:
    al = aliases(root/mod)
    used_tests = used_scripts = 0
    for name in al:
        pat = re.compile(r"\b(?:%s)\.%s\b" % ("|".join(map(re.escape, short)), re.escape(name)))
        if pat.search(test_text): used_tests += 1
        if any(pat.search(t) for n, t in script_text.items() if n != mod): used_scripts += 1
    print("%-20s aliases=%3d  referenced-from-tests=%3d  referenced-from-other-scripts=%3d" % (mod, len(al), used_tests, used_scripts))
