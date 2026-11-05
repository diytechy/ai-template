"""Survey the kit's own spine: fan-out per SR, function-call syntax in LLR details, candidate SRs.
Usage: python -I survey.py /home/user/ai-template
"""
import re, sys, tomllib
from pathlib import Path
from collections import defaultdict

ROOT = Path(sys.argv[1])
def load(rel, section):
    with (ROOT / rel).open("rb") as fh:
        data = tomllib.load(fh)
    return {k: v for k, v in data.get(section, {}).items() if not k.endswith("-000")}

SN = load("docs/requirements/stakeholder-needs.toml", "need")
SR = load("docs/requirements/system-requirements.toml", "requirement")
LLR = load("docs/requirements/low-level-requirements.toml", "design")
TC = load("docs/test/test-cases.toml", "test")
print(f"rows: SN {len(SN)} SR {len(SR)} LLR {len(LLR)} TC {len(TC)}")
print("SN keys sample:", sorted(SN)[:5], "...", "non-SN keys:", [k for k in SN if not k.startswith('SN-')])

children = defaultdict(list)
for lid, r in LLR.items():
    for sr in r.get("sr_refs", []):
        children[sr].append(lid)
tcs_of = defaultdict(list)
for tid, r in TC.items():
    for ref in r.get("verifies", []):
        tcs_of[ref].append(tid)

CALL = re.compile(r"\b[A-Za-z_][A-Za-z_0-9]*\(")
IDENT_PASS1 = re.compile(r"\b[a-z]+_[a-z_]+\(?|\b[A-Z][A-Z_]{3,}\b|\.py\b")

print("\n=== top 12 SRs by direct LLR fan-out ===")
for sr, kids in sorted(children.items(), key=lambda kv: -len(kv[1]))[:12]:
    ntc = len(set(tcs_of[sr]) | {t for k in kids for t in tcs_of[k]})
    print(f"{sr}: {len(kids)} LLRs, {ntc} TCs  | {SR.get(sr, {}).get('title', '?')[:70]}")

for sr in ("SR-156", "SR-168", "SR-157", "SR-006"):
    kids = children[sr]
    ntc = len(set(tcs_of[sr]) | {t for k in kids for t in tcs_of[k]})
    calls = sum(len(CALL.findall(str(LLR[k].get("detail", "")))) for k in kids)
    print(f"\n{sr}: {len(kids)} direct LLRs, {ntc} TCs, {calls} call-syntax matches in LLR details | {SR[sr]['title']}")
    print("   sn_refs:", SR[sr].get("sn_refs"), " kids:", kids)

print("\n=== mid-size SRs (3-5 LLRs) whose LLR details contain function-call syntax, ranked by call count ===")
cands = []
for sr, kids in children.items():
    if 3 <= len(kids) <= 5:
        calls = sum(len(CALL.findall(str(LLR[k].get("detail", "")))) for k in kids)
        callrows = sum(1 for k in kids if CALL.search(str(LLR[k].get("detail", ""))))
        if calls:
            chars = sum(len(str(LLR[k].get("detail", ""))) for k in kids)
            cands.append((calls, callrows, len(kids), chars, sr, SR.get(sr, {}).get("title", "?")))
for calls, callrows, n, chars, sr, title in sorted(cands, reverse=True)[:20]:
    print(f"{sr}: {n} LLRs, {callrows} with call syntax, {calls} calls, {chars} detail chars | {title[:60]}")
