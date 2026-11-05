"""Tests per shipped script: a test module 'exercises' a script when it load_script("name")s it, runs
scripts/<name>.py via run_py/subprocess, or imports kitlib.<name>. Each test in the module counts toward
every script the module exercises (so a module over 3 scripts credits each). Also a strict count: tests whose
own body names the script."""
import ast, re, pathlib, csv, collections
ROOT = pathlib.Path('/home/user/ai-template'); S = ROOT / 'project-trajectory/scripts'
scripts = {p.stem: p for p in S.glob('*.py')}
kitlib = {p.stem: p for p in (S / 'kitlib').glob('*.py') if p.stem != '__init__'}
def loc(p):
    n = 0
    for ln in p.read_text(encoding='utf-8', errors='replace').splitlines():
        s = ln.strip()
        if s and not s.startswith('#'): n += 1
    return n
loc_s = {k: loc(v) for k, v in scripts.items()}; loc_k = {k: loc(v) for k, v in kitlib.items()}
per_mod = collections.Counter(); per_body = collections.Counter(); mods_per = collections.defaultdict(set)
tests_total = 0
for p in sorted((ROOT / 'tests').glob('test_*.py')):
    src = p.read_text(encoding='utf-8', errors='replace'); lines = src.splitlines(); tree = ast.parse(src)
    names = set(re.findall(r'load_script\(\s*"([A-Za-z_0-9]+)"', src)) | set(re.findall(r'scripts/([A-Za-z_0-9]+)\.py', src)) | set(re.findall(r'SCRIPTS\s*/\s*"([A-Za-z_0-9]+)\.py"', src))
    names |= {'kitlib.' + k for k in re.findall(r'kitlib\.([a-z_]+)', src)} | {'kitlib.' + k for k in re.findall(r'from kitlib import ([a-z_, ]+)', src) for k in re.split(r'[ ,]+', k) if k}
    names = {n for n in names if n in scripts or (n.startswith('kitlib.') and n[7:] in kitlib)}
    tests = [t for t in ast.walk(tree) if isinstance(t, ast.FunctionDef) and t.name.startswith('test_')]
    tests_total += len(tests)
    for n in names:
        per_mod[n] += len(tests); mods_per[n].add(p.stem)
    for t in tests:
        body = '\n'.join(lines[t.lineno-1:t.end_lineno])
        for n in names:
            short = n[7:] if n.startswith('kitlib.') else n
            if re.search(r'\b' + re.escape(short) + r'\b', body): per_body[n] += 1
rows = []
for k, l in loc_s.items():
    rows.append((k, l, per_mod.get(k, 0), per_body.get(k, 0), len(mods_per.get(k, ()))))
for k, l in loc_k.items():
    rows.append(('kitlib.' + k, l, per_mod.get('kitlib.' + k, 0), per_body.get('kitlib.' + k, 0), len(mods_per.get('kitlib.' + k, ()))))
with open('perscript.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(["script", "loc", "tests_in_modules_exercising_it", "tests_naming_it_in_body", "modules"]); w.writerows(sorted(rows))
print("scripts with NO test module exercising them:")
print("  " + ", ".join(f"{k}({l} loc)" for k, l, a, b, m in sorted(rows, key=lambda r: -r[1]) if a == 0))
print("\ntop 12 by tests-per-100-LOC (module-credited count), loc>=100:")
for k, l, a, b, m in sorted([r for r in rows if r[1] >= 100], key=lambda r: -r[2] / r[1])[:12]:
    print(f"  {100*a/l:6.1f} tests/100loc  {a:5d} tests ({b} naming it) in {m:2d} modules  {l:5d} loc  {k}")
print("\nbottom 12 by tests-per-100-LOC among scripts with >0 tests, loc>=200:")
for k, l, a, b, m in sorted([r for r in rows if r[1] >= 200 and r[2] > 0], key=lambda r: r[2] / r[1])[:12]:
    print(f"  {100*a/l:6.1f} tests/100loc  {a:5d} tests ({b} naming it) in {m:2d} modules  {l:5d} loc  {k}")
print("\nlargest scripts:")
for k, l, a, b, m in sorted(rows, key=lambda r: -r[1])[:15]:
    print(f"  {100*a/l:6.1f} tests/100loc  {a:5d} tests ({b} naming it) in {m:2d} modules  {l:5d} loc  {k}")
print("\ntotal tests:", tests_total, " scripts:", len(scripts), " kitlib:", len(kitlib))
