"""Before/after metrics for the re-tier exemplar. Same counting code as dump_subtree.py.
Usage: python -I compare.py <repo-root> <after-dir> SR-xxx ...
"""
import re, sys, tomllib
from pathlib import Path
from collections import defaultdict
ROOT = Path(sys.argv[1]); AFTER = Path(sys.argv[2])
def load(rel, section, base=ROOT):
    with (base / rel).open("rb") as fh: data = tomllib.load(fh)
    return {k: v for k, v in data.get(section, {}).items() if not k.endswith("-000")}
SR = load("docs/requirements/system-requirements.toml", "requirement")
LLR = load("docs/requirements/low-level-requirements.toml", "design")
TC = load("docs/test/test-cases.toml", "test")
IDENT = re.compile(r"\b[A-Za-z_][A-Za-z_0-9]*\(|\b[a-z][a-z0-9]*_[a-z0-9_]+\b|\b[\w./-]+\.(?:py|toml|md|csv|ini|html|cmd|sh|json|txt)\b|--[a-z][a-z0-9-]+|\b[A-Z][A-Z0-9_]{3,}\b|\b[a-z]+\.[a-z_]+\.[a-z_]+\b")
PASS1 = re.compile(r"\b[a-z]+_[a-z_]+\(?|\b[A-Z][A-Z_]{3,}\b|\.py\b")
def prose_sr(r): return str(r.get("requirement","")) + " " + str(r.get("acceptance_criteria",""))
def prose_llr(r): return str(r.get("title","")) + " " + str(r.get("detail",""))
def prose_tc(r): return " ".join(str(r.get(k,"")) for k in ("method","expected","evidence"))
def subtree(sr_id, srs, llrs, tcs):
    kids = [l for l, r in llrs.items() if sr_id in r.get("sr_refs", [])]
    ts = sorted({t for t, r in tcs.items() if sr_id in r.get("verifies", []) or any(k in r.get("verifies", []) for k in kids)}, key=lambda t: t.split("-")[1])
    return kids, ts
def metrics(sr_id, srs, llrs, tcs):
    kids, ts = subtree(sr_id, srs, llrs, tcs)
    sr_text = prose_sr(srs[sr_id]); llr_text = [prose_llr(llrs[k]) for k in kids]; tc_text = [prose_tc(tcs[t]) for t in ts]
    blob = "\n".join([sr_text] + llr_text + tc_text)
    nodes = sum(1 for t in ts for x in re.split(r"[;\s]+", str(tcs[t].get("evidence",""))) if "::" in x)
    vac = sum(1 for t in ts if re.match(r"Satisfies", str(tcs[t].get("expected",""))))
    longest_tc_method = max((len(str(tcs[t].get("method",""))) for t in ts), default=0)
    return dict(rows=1+len(kids)+len(ts), llr=len(kids), tc=len(ts), chars=len(blob), sr_chars=len(sr_text),
                llr_chars=sum(map(len, llr_text)), tc_chars=sum(map(len, tc_text)),
                idents=len(IDENT.findall(blob)), pass1=len(PASS1.findall(blob)), nodes=nodes, vac=vac,
                max_llr_detail=max((len(str(llrs[k].get("detail",""))) for k in kids), default=0), max_tc_method=longest_tc_method)
print("| SR | metric | before | after | change |\n|---|---|---|---|---|")
for sr_id in sys.argv[3:]:
    a_sr = load(f"{sr_id}.toml", "requirement", AFTER); a_llr = load(f"{sr_id}.toml", "design", AFTER); a_tc = load(f"{sr_id}.toml", "test", AFTER)
    b = metrics(sr_id, SR, LLR, TC); a = metrics(sr_id, a_sr, a_llr, a_tc)
    for key, label in [("rows","rows (SR+LLR+TC)"),("llr","LLR rows"),("tc","TC rows"),("chars","prose chars (SR req+AC, LLR title+detail, TC method+expected+evidence)"),("sr_chars","  of which SR"),("llr_chars","  of which LLR"),("tc_chars","  of which TC"),("idents","code identifiers in prose (broad regex)"),("pass1","code identifiers (first-pass regex)"),("nodes","evidence node ids (path::test)"),("vac","TC expected opening 'Satisfies'"),("max_llr_detail","longest LLR detail (chars)"),("max_tc_method","longest TC method (chars)")]:
        bv, av = b[key], a[key]
        ch = f"{(av-bv)/bv:+.0%}" if bv else "n/a"
        print(f"| {sr_id} | {label} | {bv} | {av} | {ch} |")
    print(f"| {sr_id} | TCs leaving the subtree by re-pointing `verifies` | — | {len(set(subtree(sr_id, SR, LLR, TC)[1]) - set(a_tc)) - 0 if False else ''} | |") if False else None
