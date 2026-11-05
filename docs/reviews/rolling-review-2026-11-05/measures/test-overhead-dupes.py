"""Duplicate tests: (1) identical test names in two modules; (2) near-identical bodies (normalized token
Jaccard >= 0.8) across modules, families first."""
import ast, re, pathlib, collections, itertools, csv
root = pathlib.Path('/home/user/ai-template/tests')
tests = []
for p in sorted(root.glob('test_*.py')):
    src = p.read_text(encoding='utf-8', errors='replace'); lines = src.splitlines(); tree = ast.parse(src)
    for t in ast.walk(tree):
        if isinstance(t, ast.FunctionDef) and t.name.startswith('test_'):
            body = '\n'.join(lines[t.lineno-1:t.end_lineno])
            # strip docstring/comments, normalize identifiers lightly
            body_nd = re.sub(r'"""[\s\S]*?"""', '', body); body_nd = re.sub(r'#.*', '', body_nd)
            toks = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|"[^"]*"|\'[^\']*\'|\S', body_nd)
            toks = [x for x in toks if x not in ('def', t.name)]
            tests.append((p.stem, t.name, t.lineno, t.end_lineno - t.lineno + 1, set(zip(toks, toks[1:], toks[2:])), toks))
print("tests:", len(tests))
# (1) same name in two modules
byname = collections.defaultdict(list)
for m, n, ln, L, sh, toks in tests: byname[n].append((m, ln))
same = {n: v for n, v in byname.items() if len({m for m, _ in v}) > 1}
print(f"\n(1) test names present in >1 module: {len(same)}")
for n, v in sorted(same.items(), key=lambda kv: -len(kv[1]))[:40]:
    print(f"  {n}: " + ", ".join(f"{m}:{ln}" for m, ln in v))
# (2) near-identical bodies across modules
fams = ["test_trace", "test_trajectory", "test_traj_", "test_agent_loop", "test_integrate", "test_check_", "test_gen_", "test_id_", "test_plan_", "test_held_", "test_parent_first", "test_intake", "test_kitlib", "test_session", "test_codex", "test_overnight", "test_usage", "test_review_brief", "test_coordinator", "test_consolidate", "test_done_when", "test_decision", "test_dispatch", "test_retire", "test_rule_sync", "test_wi_"]
pairs = []
big = [t for t in tests if len(t[4]) >= 15]
for a, b in itertools.combinations(big, 2):
    if a[0] == b[0]: continue
    inter = len(a[4] & b[4])
    if inter == 0: continue
    j = inter / len(a[4] | b[4])
    if j >= 0.75:
        pairs.append((j, a, b))
pairs.sort(key=lambda x: -x[0])
print(f"\n(2) cross-module near-duplicate bodies (Jaccard>=0.75 on token trigrams, body>=15 trigrams): {len(pairs)} pairs")
mods = collections.Counter()
for j, a, b in pairs:
    mods[tuple(sorted((a[0], b[0])))] += 1
print("module pairs with most near-duplicates:")
for (x, y), c in mods.most_common(25): print(f"  {c:3d}  {x} <-> {y}")
with open('dupes.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(["jaccard", "mod_a", "test_a", "line_a", "len_a", "mod_b", "test_b", "line_b", "len_b"])
    for j, a, b in pairs: w.writerow([f"{j:.2f}", a[0], a[1], a[2], a[3], b[0], b[1], b[2], b[3]])
print("\nsample pairs (top 30):")
for j, a, b in pairs[:30]: print(f"  {j:.2f} {a[0]}::{a[1]} L{a[2]} ({a[3]} lines)  <->  {b[0]}::{b[1]} L{b[2]}")
# also within-module exact duplicates of bodies (same module, Jaccard >= 0.9)
within = 0
for a, b in itertools.combinations(big, 2):
    if a[0] != b[0]: continue
    inter = len(a[4] & b[4]); 
    if inter and inter / len(a[4] | b[4]) >= 0.9: within += 1
print("\nwithin-module near-identical pairs (J>=0.9):", within)
