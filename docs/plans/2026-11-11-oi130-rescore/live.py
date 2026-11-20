"""OI-130 re-score, step 1: the live module inventory, LLR-derived component tags, declared kernel and
bare-stem import edges. Run from the repo root: python live.py <out>/live.json"""

import sys, json, collections
from pathlib import Path

root = Path(".").resolve()
sys.path.insert(0, str(root / "project-trajectory/scripts"))
import trajectory_arch as ta
from kitlib import spine as kitspine

names, contracts, imports = ta.arch_inventory(root)
raw = kitspine.module_components(ta.spine_carrier.load(root / ta.LLR_CSV, "LLR-ID"))  # one home since WI-1005
kernel = ta.read_kernel_modules(root)
inv = {}
for m in names:
    n = ta._norm_module(m)
    inv[n] = m
print("inventory", len(inv))
print("kernel", sorted(kernel))
mem = {n: sorted(raw.get(n, set())) for n in inv}
by = collections.Counter(len(v) for v in mem.values())
print("tagcount dist", by)
for n, v in sorted(mem.items()):
    if len(v) != 1:
        print("  ", n, v)
percmp = collections.defaultdict(list)
for n, v in mem.items():
    for c in v:
        percmp[c].append(n)
for c in sorted(percmp):
    print(c, len(percmp[c]))
by_stem = collections.defaultdict(set)
for n in inv:
    by_stem[n.rsplit("/", 1)[-1]].add(n)
edges = set()
unres = collections.Counter()
for src, stems in imports.items():
    s = ta._norm_module(src)
    for st in stems:
        t = by_stem.get(st, set())
        if len(t) == 1:
            edges.add((s, next(iter(t))))
        else:
            unres[(st, len(t))] += 1
print("edges", len(edges), "unresolved", dict(unres))
json.dump(
    {"mem": mem, "edges": sorted(edges), "kernel": sorted(kernel), "inv": inv},
    open(sys.argv[1], "w"),
    indent=1,
)
