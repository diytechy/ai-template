"""Row M: the counts the manifest reports, computed from _built.json (build.py's output)."""
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
B = json.load(open(OUT / "_built.json", encoding="utf-8"))
CLASSES = ["instrument", "open-input", "history-rederive", "spine-text", "regression", "defect", "process"]


def cohort_sets(name):
    """primary = base 2's rule; base1 = + WI-853/WI-870 legacy rounds; allfmt = + every legacy-alt round."""
    def keep(row):
        if row["cohort"] == "primary":
            return True
        if row["cohort"] != "legacy-alt":
            return False
        if name == "base1":
            return row["wi"] in ("WI-853", "WI-870")
        return name == "allfmt"
    files = [f for f in B["files"] if keep(f)]
    finds = [f for f in B["findings"] if keep(f)]
    return files, finds


def report(name):
    files, finds = cohort_sets(name)
    print(f"\n===== cohort {name}: {len(files)} rounds, {len({f['wi'] for f in files})} WIs, {len(finds)} findings "
          f"(verdict-n sum {sum(int(f['findings_n']) for f in files)})")
    rounds = Counter(f["wi"] for f in files)
    landed = {f["wi"] for f in files if f["wi_status"] == "landed in window"}
    flight = {f["wi"] for f in files if f["wi_status"] == "in flight"}
    lr = sorted(rounds[w] for w in landed)
    print(f"landed WIs {len(landed)}: rounds {sum(lr)}, mean {sum(lr)/len(lr):.2f}, median {statistics.median(lr)}, "
          f"distribution {dict(sorted(Counter(lr).items()))}")
    print("  per landed WI:", dict(sorted((w, rounds[w]) for w in landed)))
    print("in flight:", {w: rounds[w] for w in sorted(flight)})
    print("scope:", Counter(f["scope"] for f in files), " verdicts:", Counter(f["verdict"] for f in files))
    print(">=6 rounds:", sorted(w for w in rounds if rounds[w] >= 6))
    pc = Counter(f["primary_class"] for f in finds)
    print("primary class:", {c: pc[c] for c in CLASSES})
    sec = Counter(t for f in finds for t in f["secondary_tags"].split(";") if t)
    print("secondary tags:", dict(sec))
    anytag = {c: sum(1 for f in finds if f["primary_class"] == c or c in f["secondary_tags"].split(";")) for c in CLASSES}
    print("class as primary or secondary:", anytag)
    print("severity:", Counter(f["severity"] for f in finds))
    late = [f for f in finds if f["late"] == "yes"]
    lc = Counter(f["primary_class"] for f in late)
    print(f"late: {len(late)} of {len(finds)}; by class {{{', '.join(f'{c}: {lc[c]}' for c in CLASSES)}}}")
    lo = [f for f in late if f["primary_class"] == "open-input"]
    lo_l = [f for f in lo if f["wi_status"] == "landed in window"]
    print(f"late open-input: {len(lo)} (landed {len(lo_l)} over {len(landed)} landed WIs = {len(lo_l)/len(landed):.2f}/landed WI; "
          f"in flight {len(lo)-len(lo_l)}); by WI {dict(Counter(f['wi'] for f in lo))}")
    lo_any = [f for f in late if f["primary_class"] == "open-input" or "open-input" in f["secondary_tags"]]
    print("late open-input incl. secondary:", len(lo_any))
    fana = [f for f in finds if f["full_after_narrow_approve"] == "yes"]
    print("findings in a full review right after a narrow APPROVE:", len(fana), dict(Counter(f["wi"] for f in fana)),
          "major+:", sum(1 for f in fana if f["severity"] != "MINOR"))
    ins = [f for f in finds if f["primary_class"] == "instrument"]
    print("instrument primary:", len(ins), "dispositions", dict(Counter(f["disposition"] for f in ins)))
    ins2 = [f for f in finds if "instrument" in f["secondary_tags"].split(";")]
    print("instrument secondary (partial):", len(ins2))
    reg = [f for f in finds if f["regression_basis"] in ("operational", "strict")]
    print("regression any:", len(reg), dict(Counter(f["regression_basis"] for f in reg)),
          "late:", sum(1 for f in reg if f["late"] == "yes"))
    hist = [f for f in finds if f["primary_class"] == "history-rederive" or "history-rederive" in f["secondary_tags"]]
    print("history-rederive primary or secondary:", len(hist), "primary:", pc["history-rederive"])
    disp = Counter(f["disposition"] for f in finds)
    print("dispositions:", dict(disp))
    dpc = defaultdict(Counter)
    for f in finds:
        dpc[f["primary_class"]][f["disposition"]] += 1
    for c in CLASSES:
        print(f"   {c}: {dict(dpc[c])}")
    reopen = [f for f in files if f["full_reopen_after_checkpoint"] == "yes"]
    print("full reviews reopening after a checkpoint:", len(reopen),
          [(f["wi"], f["round_nnn"] or f["path"].rsplit('/', 1)[-1], f["after_narrow_approve"], f["after_spine_sitting"]) for f in reopen])
    print("   after narrow APPROVE:", sum(1 for f in reopen if f["after_narrow_approve"] == "yes"),
          " after spine sitting only:", sum(1 for f in reopen if f["after_narrow_approve"] != "yes"))
    print("tip states:", dict(Counter(f["tip_state"] for f in files)))
    print("reviewer test reports:", dict(Counter(f["reviewer_tests"] for f in files)))
    full_major = [f for f in files if f["scope"] == "full" and any(
        g["path"] == f["path"] and g["severity"] != "MINOR" for g in finds)]
    print("full reviews with MAJOR+ findings:", len(full_major))


for n in ("primary", "base1", "allfmt"):
    report(n)
