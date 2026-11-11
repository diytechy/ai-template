"""Re-score candidate partitions on today's tree. Usage: score.py live.json [behaviours.json]"""

import json, sys, collections

d = json.load(open(sys.argv[1]))
mods = sorted(m.replace("scripts/", "") for m in d["inv"])
KERNEL = {k.replace("scripts/", "") for k in d["kernel"]}
# ---- import edges, resolving dotted/relative names the live check drops ----
sys.path.insert(0, "project-trajectory/scripts")
import trajectory_arch as ta
from pathlib import Path

names, _c, imports = ta.arch_inventory(Path(".").resolve())
modset = set(mods)
edges, unres = set(), collections.Counter()
for src, stems in imports.items():
    s = ta._norm_module(src).replace("scripts/", "")
    pkg = s.rsplit("/", 1)[0] if "/" in s else ""
    for st in stems:
        if st.startswith("."):
            t = (pkg + "/" if pkg else "") + st.lstrip(".")
        elif "." in st:
            t = st.replace(".", "/")
        else:
            t = st
        if t not in modset and pkg and (pkg + "/" + t) in modset:
            t = pkg + "/" + t
        if t in modset and t != s:
            edges.add((s, t))
        else:
            unres[st] += 1


def fam(prefixes, exact=()):
    return {m for m in mods if m in exact or any(m.startswith(p) for p in prefixes)}


W = {}
W["W1"] = {
    "absolute_terms",
    "acceptance_record",
    "assumption_rules",
    "baseline_snapshot",
    "census",
    "check_trajectory",
    "coherence",
    "derive_stage",
    "frame_rules",
    "gen_arch_map",
    "held_status",
    "id_carrier",
    "migrate_carrier",
    "plan_coverage",
    "record_observation",
    "retire",
    "spine_carrier",
    "spine_rules",
    "trace",
    "trace_text",
    "trajectory_arch",
    "wi_convert",
    "kitlib/spine",
    "kitlib/secret_classes",
    "kitlib/observation",
    "kitlib/authority",
}
W["W2"] = fam(["check"], {"flag_axis", "record_test_evidence", "subagent_gate"}) - {
    "check_trajectory"
}
W["W4"] = fam(
    ["gen_", "traj_", "rendering"],
    {"bootstrap", "run_menu", "kitlib/bootstrap_manifest", "kitlib/guard_hooks"},
) - {"gen_arch_map"}
W["K"] = set(KERNEL)
W["W3"] = set(mods) - set().union(*W.values())
P = {}
P["B"] = {
    "spine_carrier",
    "trace",
    "trace_text",
    "derive_stage",
    "plan_coverage",
    "spine_rules",
    "coherence",
    "frame_rules",
    "absolute_terms",
    "assumption_rules",
    "acceptance_record",
    "baseline_snapshot",
    "census",
    "held_status",
    "id_carrier",
    "retire",
    "record_observation",
    "kitlib/spine",
    "kitlib/authority",
    "kitlib/observation",
}
P["A"] = {
    "bootstrap",
    "migrate_carrier",
    "wi_convert",
    "run_menu",
    "gen_skills_index",
    "gen_cases",
    "gen_release_checklist",
    "kitlib/bootstrap_manifest",
    "migrate_decisions",
}
P["C"] = fam(
    ["check"],
    {
        "gen_arch_map",
        "trajectory_arch",
        "flag_axis",
        "record_test_evidence",
        "kitlib/secret_classes",
        "kitlib/red_mark",
    },
)
P["D"] = fam(
    ["traj_", "rendering"],
    {
        "gen_trajectory",
        "gen_open_items",
        "gen_okf",
        "gen_prompt_catalog",
        "gen_components",
        "gen_verdict_rollup",
        "pending",
    },
)
P["K"] = set(KERNEL)
P["E"] = set(mods) - set().union(*P.values())
F = {}
F["F1"] = {
    "spine_carrier",
    "trace_text",
    "migrate_carrier",
    "wi_convert",
    "id_carrier",
    "kitlib/spine",
    "retire",
    "record_observation",
    "kitlib/observation",
}
F["F2"] = {
    "trace",
    "check_trajectory",
    "derive_stage",
    "plan_coverage",
    "gen_arch_map",
    "trajectory_arch",
    "spine_rules",
    "coherence",
    "frame_rules",
    "absolute_terms",
    "assumption_rules",
    "acceptance_record",
    "baseline_snapshot",
    "census",
    "held_status",
    "kitlib/authority",
}
F["F3"] = {"check", "check_coverage", "record_test_evidence", "check_assumption_gate"}
F["F5"] = {
    "check_privacy",
    "subagent_gate",
    "kitlib/secret_classes",
    "kitlib/commit_hooks",
    "kitlib/guard_hooks",
    "coordinator_guard",
}
F["F4"] = fam(["check_"], {"flag_axis"}) - F["F2"] - F["F3"] - F["F5"]
F["F6"] = fam(["gen_", "traj_", "rendering"], {"pending"}) - {"gen_arch_map"}
F["F7"] = {
    "schedule",
    "dispatch",
    "lane",
    "intake",
    "integrate",
    "trunk_step",
    "spec_move",
    "handback",
    "bookkeeping",
    "consolidate",
    "kitlib/station",
    "kitlib/done_when",
    "kitlib/adoption",
    "adoption_record",
    "kitlib/red_mark",
    "review_set",
    "plan_gate",
}
F["F9"] = {"bootstrap", "run_menu", "kitlib/bootstrap_manifest"}
F["K"] = set(KERNEL)
F["F8"] = set(mods) - set().union(*F.values())


def check_partition(name, part):
    seen = collections.Counter(m for s in part.values() for m in s)
    dup = [m for m, c in seen.items() if c > 1]
    miss = [m for m in mods if m not in seen]
    assert not dup and not miss, (name, dup, miss)
    return {m: c for c, s in part.items() for m in s}


cands = {
    "P5* narrow-waist": check_partition("P5", W),
    "P3* actor": check_partition("P3", P),
    "P4* functional": check_partition("P4", F),
}
live = {m.replace("scripts/", ""): set(v) for m, v in d["mem"].items()}
beh = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}


def score(a):
    cut = [(s, t) for s, t in edges if a[s] != a[t] and a[t] != "K"]
    cut_all = [(s, t) for s, t in edges if a[s] != a[t]]
    bnd = {tuple(sorted((a[s], a[t]))) for s, t in cut}
    per = collections.Counter()
    for s, t in cut:
        per[a[s]] += 1
        per[a[t]] += 1
    strad = {
        b: sorted({a[m] for m in ms})
        for b, ms in beh.items()
        if len({a[m] for m in ms}) > 1
    }
    sizes = collections.Counter(a.values())
    return dict(
        cut=len(cut),
        cut_incl_kernel=len(cut_all),
        boundaries=len(bnd),
        per_cmp=dict(per),
        sizes=dict(sizes),
        straddle=len(strad),
        straddling=strad,
    )


print(
    "modules", len(mods), "resolved edges", len(edges), "unresolved stems", dict(unres)
)
out = {}
for n, a in cands.items():
    out[n] = score(a)
    r = out[n]
    print(
        f"\n{n}: cut={r['cut']} (incl. into-kernel {r['cut_incl_kernel']}) boundaries={r['boundaries']} straddle={r['straddle']}/{len(beh)}"
    )
    print("  sizes", r["sizes"])
    print("  crossings/cmp", r["per_cmp"])
    for b, cs in r["straddling"].items():
        print("   straddles:", b, cs)
# live as tagged: hard edges vs silenced by multi-tag
hard = sil = 0
for s, t in edges:
    if t in KERNEL:
        continue
    if (
        live[s]
        and live[t]
        and len(live[s]) == 1
        and len(live[t]) == 1
        and live[s] != live[t]
    ):
        hard += 1
    elif live[s] & live[t] and (live[s] | live[t]) != (live[s] & live[t]):
        sil += 1
print(
    f"\nLIVE tags: single-tag cross edges={hard}; edges with a multi-tagged endpoint whose tags differ (advisory only)={sil}"
)
lstr = {
    b: ms
    for b, ms in beh.items()
    if len(set().union(*(live[m] for m in ms))) > 1
    and not set.intersection(*(live[m] for m in ms))
}
print("LIVE straddle (no common tag):", len(lstr), list(lstr))
json.dump(
    out,
    open(sys.argv[1].replace("live.json", "scores.json"), "w"),
    indent=1,
    default=list,
)

# ---- seam coverage of LIVE single-tag cross edges, split by whether the live check can see them ----
root = Path(".").resolve()
cov = {
    (a.replace("scripts/", ""), b.replace("scripts/", ""))
    for a, b in ta._declared_seam_pairs(root)
}
by_stem = collections.defaultdict(set)
for m in mods:
    by_stem[m.rsplit("/", 1)[-1]].add(m)
seen_by_live = set()
for src, stems in imports.items():
    s = ta._norm_module(src).replace("scripts/", "")
    for st in stems:
        t = by_stem.get(st, set())
        if len(t) == 1:
            seen_by_live.add((s, next(iter(t))))
rows = collections.Counter()
unc = []
for s, t in sorted(edges):
    if t in KERNEL or not live[s] or not live[t]:
        continue
    if live[s] & live[t]:  # shares a tag -> live treats as internal or silenced
        if live[s] != live[t]:
            rows["multi-tag silenced"] += 1
        continue
    vis = (s, t) in seen_by_live
    c = (s, t) in cov
    rows[("visible" if vis else "INVISIBLE", "covered" if c else "UNCOVERED")] += 1
    if not c:
        unc.append(
            (s, t, sorted(live[s]), sorted(live[t]), "visible" if vis else "invisible")
        )
print("\nLIVE cross-component edges by visibility/coverage:", dict(rows))
for u in unc:
    print("  uncovered:", u)
