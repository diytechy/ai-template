"""Pick every 10th SR by sorted id and dump its full LLR + TC subtree (stdlib only).

Usage: python -I sample_subtrees.py <repo-root> [stride] [offset]
Prints one block per sampled SR with the SR row, each LLR citing it, and each TC
verifying the SR or any of those LLRs. Also prints per-subtree lexical stats.
"""
import pathlib
import re
import sys
import tomllib

root = pathlib.Path(sys.argv[1])
stride = int(sys.argv[2]) if len(sys.argv) > 2 else 10
offset = int(sys.argv[3]) if len(sys.argv) > 3 else 0


def rows(path, table):
    data = tomllib.load(open(path, "rb"))
    return {rid: row for rid, row in data[table].items() if re.match(r"^[A-Z]+-\d+$", rid)}


sn = rows(root / "docs/requirements/stakeholder-needs.toml", "need")
sr = rows(root / "docs/requirements/system-requirements.toml", "requirement")
llr = rows(root / "docs/requirements/low-level-requirements.toml", "design")
tc = rows(root / "docs/test/test-cases.toml", "test")

IDENT = re.compile(r"\b[a-z]+_[a-z_0-9]+\(?|\b[A-Z][A-Z_]{3,}\b|\.py\b|--[a-z][a-z-]+|\.toml\b|\.md\b|\.ini\b")


def num(rid):
    return int(rid.split("-")[1])


srs = sorted(sr, key=num)
picked = [s for i, s in enumerate(srs) if i % stride == offset]
print(f"SR total {len(sr)}, LLR {len(llr)}, TC {len(tc)}, SN {len(sn)}; picked {len(picked)} SRs: {picked}\n")

for s in picked:
    r = sr[s]
    kids = sorted((k for k, v in llr.items() if s in v.get("sr_refs", [])), key=num)
    tcs = sorted(
        (k for k, v in tc.items() if s in v.get("verifies", []) or any(l in v.get("verifies", []) for l in kids)),
        key=num,
    )
    print("=" * 100)
    print(f"[{s}] {r.get('title')}  | sn_refs={r.get('sn_refs')} verification={r.get('verification')} status={r.get('status')}")
    for n in r.get("sn_refs", []):
        if n in sn:
            print(f"  SN {n}: {str(sn[n].get('need', ''))[:300]}")
    print(f"  REQUIREMENT ({len(str(r.get('requirement','')))}c): {r.get('requirement')}")
    print(f"  AC ({len(str(r.get('acceptance_criteria','')))}c): {r.get('acceptance_criteria')}")
    print(f"  RATIONALE ({len(str(r.get('rationale','')))}c): {str(r.get('rationale',''))[:600]}")
    print(f"  SR idents: {sorted(set(IDENT.findall(str(r.get('requirement','')) + ' ' + str(r.get('acceptance_criteria','')))))}")
    print(f"  --- {len(kids)} LLR children, {len(tcs)} TCs ---")
    for k in kids:
        v = llr[k]
        d = str(v.get("detail", ""))
        print(f"  {k} [{v.get('title')}] module={v.get('module')} symbol={v.get('code_symbol')} status={v.get('status')}")
        print(f"      DETAIL ({len(d)}c): {d[:900]}{' ...' if len(d) > 900 else ''}")
        print(f"      idents: {sorted(set(IDENT.findall(d)))[:25]}")
    for t in tcs:
        v = tc[t]
        print(f"  {t} verifies={v.get('verifies')} level={v.get('level')} tier={v.get('tier')} automated={v.get('automated')}")
        print(f"      METHOD ({len(str(v.get('method','')))}c): {str(v.get('method',''))[:500]}")
        print(f"      EXPECTED ({len(str(v.get('expected','')))}c): {str(v.get('expected',''))[:400]}")
        print(f"      EVIDENCE: {str(v.get('evidence',''))[:300]}")
    print()
