"""Join per-test junit times (smoke + slow) with AST facts: takes `scaffold`, module class, spawns."""
import xml.etree.ElementTree as ET, csv, ast, pathlib, re, collections, sys
root = pathlib.Path('/home/user/ai-template/tests')
cls = {r["module"]: r["class"] for r in csv.DictReader(open("classes.csv"))}
spawn = {(r['module'], r['test']): int(r['subprocess']) for r in csv.DictReader(open('pertest.csv'))}
scaf = {}
for p in root.glob('test_*.py'):
    src = p.read_text(encoding='utf-8', errors='replace'); tree = ast.parse(src)
    for t in ast.walk(tree):
        if isinstance(t, ast.FunctionDef) and t.name.startswith('test_'):
            scaf[(p.stem, t.name)] = int('scaffold' in {a.arg for a in t.args.args})
slow = set(re.findall(r'^\s*"(test_[a-z_0-9]+)"', open('/home/user/ai-template/tests/conftest.py').read(), re.M))
tot = collections.Counter(); n = collections.Counter(); per_mod = collections.Counter(); per_mod_n = collections.Counter()
for name in sys.argv[1:]:
    for tc in ET.parse(name).iter('testcase'):
        mod = [p for p in tc.get('classname').split('.') if p.startswith('test_')][0]
        fn = tc.get('name').split('[')[0]; t = float(tc.get('time'))
        tier = 'slow' if mod in slow else 'smoke'
        tot[('tier', tier)] += t; n[('tier', tier)] += 1
        tot[('class', cls.get(mod, '?'))] += t; n[('class', cls.get(mod, '?'))] += 1
        s = scaf.get((mod, fn), 0); tot[('scaffold', s)] += t; n[('scaffold', s)] += 1
        sp = spawn.get((mod, fn), 0); tot[('spawn', sp)] += t; n[('spawn', sp)] += 1
        per_mod[mod] += t; per_mod_n[mod] += 1
        if mod in slow and sp == 0: tot[('slow-noswpawn', 1)] += t; n[('slow-noswpawn', 1)] += 1
T = sum(v for k, v in tot.items() if k[0] == 'tier')
print(f"whole suite: {sum(v for k, v in n.items() if k[0]=='tier')} tests, per-test time sum {T:.0f}s")
for k in sorted(tot):
    print(f"  {k}: {n[k]:5d} tests  {tot[k]:7.1f}s  ({100*tot[k]/T:4.1f}%)")
print("top 25 modules by time (both tiers):")
for m, s in per_mod.most_common(25):
    print(f"  {s:7.1f}s {per_mod_n[m]:4d} tests {1000*s/per_mod_n[m]:6.0f} ms/test  {'slow ' if m in slow else 'smoke'} {cls.get(m,'?'):8s} {m}")
with open('permodule_both.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['module', 'tests', 'seconds', 'tier', 'class'])
    for m, s in per_mod.most_common(): w.writerow([m, per_mod_n[m], f"{s:.2f}", 'slow' if m in slow else 'smoke', cls.get(m, '?')])
