"""Per-test analysis: does the test drive a kit script as a SUBPROCESS (run_py/subprocess, directly or via a
module-level helper, one level), and does it assert on message WORDING (a str literal >= 25 chars with a space
inside an assert, or `in proc.stdout/stderr/out/err`)."""
import ast, re, csv, pathlib, collections
root = pathlib.Path('/home/user/ai-template/tests')
cls = {r["module"]: r["class"] for r in csv.DictReader(open("classes.csv"))}
SUBP = re.compile(r'\b(run_py|subprocess\.(run|Popen|check_output|check_call|call)|fixture_git|_git\(|run_git\(|git\(|\.run\(|run_session|run_hook|_run\()')
# conftest helpers known to spawn processes
CONF_SPAWN = {"run_py", "scaffold", "make_minimal_project", "hooked_checkout", "hooks_on", "trunk_repo", "lane_checkout",
              "fixture_git", "fixture_commit", "claimed_lane", "relocate_as_lane", "claim_on_trunk", "claim_on_branch", "declare_review_bar", "python_stand_ins", "sub_floor_interpreter"}
out = []
agg = collections.defaultdict(lambda: collections.Counter())
for p in sorted(root.glob('test_*.py')):
    src = p.read_text(encoding='utf-8', errors='replace'); lines = src.splitlines()
    tree = ast.parse(src)
    # module-level helper functions and fixtures and their spawn-ness
    helpers = {}
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and not n.name.startswith('test_'):
            body = '\n'.join(lines[n.lineno-1:n.end_lineno])
            calls = {c.func.id for c in ast.walk(n) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}
            attr = {c.func.attr for c in ast.walk(n) if isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute)}
            spawns = bool(SUBP.search(body)) or bool(calls & CONF_SPAWN) or ('run' in attr and 'subprocess' in body)
            helpers[n.name] = spawns
    # second pass: helper calling spawning helper
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and not n.name.startswith('test_') and not helpers[n.name]:
            calls = {c.func.id for c in ast.walk(n) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}
            if any(helpers.get(c) for c in calls): helpers[n.name] = True
    tests = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]
    for t in tests:
        body = '\n'.join(lines[t.lineno-1:t.end_lineno])
        calls = {c.func.id for c in ast.walk(t) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}
        args = {a.arg for a in t.args.args}
        direct = bool(SUBP.search(body))
        via_helper = any(helpers.get(c) for c in calls) or bool(calls & CONF_SPAWN)
        via_fixture = bool(args & CONF_SPAWN) or any(helpers.get(a) for a in args)
        subp = direct or via_helper or via_fixture
        # load_script in-process?
        inproc = ('load_script' in src) or ('from kitlib' in src) or ('import kitlib' in src)
        # wording asserts
        wording = False; nassert = 0; wassert = 0
        for n in ast.walk(t):
            if isinstance(n, ast.Assert):
                nassert += 1
                hit = False
                for c in ast.walk(n.test):
                    if isinstance(c, ast.Constant) and isinstance(c.value, str) and len(c.value) >= 25 and ' ' in c.value:
                        hit = True
                if hit: wassert += 1
        # pytest.raises(..., match=...)
        if re.search(r'match=\s*r?["\'][^"\']{25,}', body): wassert += 1; nassert += 1
        wording = wassert > 0
        m = p.stem
        out.append(dict(module=m, test=t.name, cls=cls[m], subprocess=int(subp), direct=int(direct), wording=int(wording), asserts=nassert, wording_asserts=wassert, lines=t.end_lineno - t.lineno + 1))
        a = agg[cls[m]]; a['tests'] += 1; a['subp'] += subp; a['direct'] += direct; a['wording'] += wording; a['asserts'] += nassert; a['wasserts'] += wassert
with open('pertest.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("| class | tests | spawn a process (any route) | direct run_py/subprocess in body | tests with a wording assert | asserts | wording asserts |")
print("|---|---|---|---|---|---|---|")
for k in ("PRODUCT", "PLUMBING", "META", "HISTORY"):
    a = agg[k]
    print(f"| {k} | {a['tests']} | {a['subp']} ({100*a['subp']/a['tests']:.0f}%) | {a['direct']} ({100*a['direct']/a['tests']:.0f}%) | {a['wording']} ({100*a['wording']/a['tests']:.0f}%) | {a['asserts']} | {a['wasserts']} ({100*a['wasserts']/a['asserts']:.0f}%) |")
# per-module subprocess share for PRODUCT, top wording modules
perm = collections.defaultdict(lambda: collections.Counter())
for r in out:
    a = perm[r['module']]; a['tests'] += 1; a['subp'] += r['subprocess']; a['wording'] += r['wording']; a['wasserts'] += r['wording_asserts']; a['asserts'] += r['asserts']
print("\ntop 20 modules by wording-assert count:")
for m, a in sorted(perm.items(), key=lambda kv: -kv[1]['wasserts'])[:20]:
    print(f"  {a['wasserts']:4d}/{a['asserts']:4d} wording asserts, {a['wording']:3d}/{a['tests']:3d} tests  {cls[m]:8s} {m}")
print("\nPRODUCT modules where every test spawns a process (count>=10):")
print("  " + ", ".join(f"{m}({a['tests']})" for m, a in sorted(perm.items()) if cls[m]=="PRODUCT" and a['tests']>=10 and a['subp']==a['tests']))
