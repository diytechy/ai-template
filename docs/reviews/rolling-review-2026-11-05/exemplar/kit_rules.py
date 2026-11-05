"""Run the kit's OWN pure text rules (trace_text.*, absolute_terms.*) over the BEFORE subtree rows
(live registries, filtered to the subtree) and the AFTER rows (proposal TOML). Read-only: imports the
kit modules with -B so no bytecode is written into the repository.
Usage: python -B -I kit_rules.py <repo-root> <after-dir> SR-xxx ...
"""
import sys, tomllib
from pathlib import Path
ROOT = Path(sys.argv[1]); AFTER = Path(sys.argv[2])
sys.path.insert(0, str(ROOT / "project-trajectory" / "scripts"))
import spine_carrier, trace_text, absolute_terms  # noqa: E402

def rows(text, id_col):
    out = spine_carrier.rows_from_toml(text, id_col) or {}
    return [r for rid, r in out.items() if not rid.endswith("-000")]

LIVE = {
    "SR-ID": rows((ROOT/"docs/requirements/system-requirements.toml").read_text(encoding="utf-8"), "SR-ID"),
    "LLR-ID": rows((ROOT/"docs/requirements/low-level-requirements.toml").read_text(encoding="utf-8"), "LLR-ID"),
    "TC-ID": rows((ROOT/"docs/test/test-cases.toml").read_text(encoding="utf-8"), "TC-ID"),
}
def refs(cell): return [x for x in str(cell or "").replace(";", " ").replace(",", " ").split() if x]

def subtree_before(sr_id):
    srs = [r for r in LIVE["SR-ID"] if r["SR-ID"] == sr_id]
    llrs = [r for r in LIVE["LLR-ID"] if sr_id in refs(r.get("SR-Refs"))]
    kid_ids = {r["LLR-ID"] for r in llrs} | {sr_id}
    tcs = [r for r in LIVE["TC-ID"] if kid_ids & set(refs(r.get("Verifies")))]
    return srs, llrs, tcs
def subtree_after(sr_id):
    text = (AFTER / f"{sr_id}.toml").read_text(encoding="utf-8")
    return rows(text, "SR-ID"), rows(text, "LLR-ID"), rows(text, "TC-ID")

RULES = [
    ("form_findings (GATING)", lambda s,l,t: trace_text.form_findings(s,l,t)),
    ("provenance_findings (GATING)", lambda s,l,t: trace_text.provenance_findings(s,l,t)),
    ("ears_advisories", lambda s,l,t: trace_text.ears_advisories(s)),
    ("paraphrase_advisories", lambda s,l,t: trace_text.paraphrase_advisories(s,l)),
    ("ac_advisories", lambda s,l,t: trace_text.ac_advisories(s)),
    ("sr_artifact_advisories", lambda s,l,t: trace_text.sr_artifact_advisories(s)),
    ("sr_fanout_advisories", lambda s,l,t: trace_text.sr_fanout_advisories(s,l)),
    ("absolute_advisories", lambda s,l,t: absolute_terms.absolute_advisories([], s, l)),
]
def count(x):
    if x is None: return 0, []
    if isinstance(x, dict): x = list(x.values())
    try: items = list(x)
    except TypeError: return 1, [repr(x)]
    flat = []
    for it in items:
        if isinstance(it, (list, tuple)): flat.extend(it if it and not isinstance(it[0], str) else [it])
        else: flat.append(it)
    return len(flat), [str(f)[:300] for f in flat]

for sr_id in sys.argv[3:]:
    print(f"\n===== {sr_id}")
    for label, fn in RULES:
        for side, (s,l,t) in (("before", subtree_before(sr_id)), ("after", subtree_after(sr_id))):
            try:
                n, items = count(fn(s,l,t))
            except Exception as e:  # noqa: BLE001
                n, items = -1, [f"ERROR {type(e).__name__}: {e}"]
            print(f"{label:32s} {side:6s} {n}")
            if side == "after":
                for it in items[:12]: print("      ", it)
