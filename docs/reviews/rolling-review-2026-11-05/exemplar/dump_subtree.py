"""Dump an SR subtree verbatim (SN excerpt, SR, LLRs, TCs) and its metrics.
Usage: python -I dump_subtree.py <repo-root> <out-dir> SR-xxx [SR-yyy ...]
Metrics counted over the PROSE cells a re-tier rewrites:
  SR: requirement + acceptance_criteria      LLR: title + detail      TC: method + expected + evidence
  rows   = 1 SR + n LLR + n TC
  chars  = len of those cells
  idents = matches of IDENT (broad: snake_case, call(), file.ext, --flag, ALL_CAPS, dotted.path)
  pass1  = matches of the first-pass regex from docs/reviews/rolling-review-2026-11-05/measure.py
"""
import re, sys, tomllib
from pathlib import Path
from collections import defaultdict

ROOT = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
def load(rel, section):
    with (ROOT / rel).open("rb") as fh:
        data = tomllib.load(fh)
    return {k: v for k, v in data.get(section, {}).items() if not k.endswith("-000")}
SN = load("docs/requirements/stakeholder-needs.toml", "need")
SR = load("docs/requirements/system-requirements.toml", "requirement")
LLR = load("docs/requirements/low-level-requirements.toml", "design")
TC = load("docs/test/test-cases.toml", "test")
children = defaultdict(list); tcs_of = defaultdict(list)
for lid, r in LLR.items():
    for s in r.get("sr_refs", []): children[s].append(lid)
for tid, r in TC.items():
    for ref in r.get("verifies", []): tcs_of[ref].append(tid)

IDENT = re.compile(
    r"\b[A-Za-z_][A-Za-z_0-9]*\("          # call syntax foo(
    r"|\b[a-z][a-z0-9]*_[a-z0-9_]+\b"       # snake_case
    r"|\b[\w./-]+\.(?:py|toml|md|csv|ini|html|cmd|sh|json|txt)\b"  # filenames
    r"|--[a-z][a-z0-9-]+"                   # --flags
    r"|\b[A-Z][A-Z0-9_]{3,}\b"              # ALL_CAPS constants
    r"|\b[a-z]+\.[a-z_]+\.[a-z_]+\b"        # dotted.module.path
)
PASS1 = re.compile(r"\b[a-z]+_[a-z_]+\(?|\b[A-Z][A-Z_]{3,}\b|\.py\b")
ID_TOKEN = re.compile(r"\b(?:SN|SR|LLR|TC|WI|OI|IF|CMP|DA|B|D)-\d{1,3}\b")

def prose_llr(r): return str(r.get("title","")) + " " + str(r.get("detail",""))
def prose_tc(r): return " ".join(str(r.get(k,"")) for k in ("method","expected","evidence"))
def prose_sr(r): return str(r.get("requirement","")) + " " + str(r.get("acceptance_criteria",""))

def metrics(sr_id):
    kids = children[sr_id]
    tcs = sorted(set(tcs_of[sr_id]) | {t for k in kids for t in tcs_of[k]}, key=lambda t:int(t.split('-')[1]))
    texts = [prose_sr(SR[sr_id])] + [prose_llr(LLR[k]) for k in kids] + [prose_tc(TC[t]) for t in tcs]
    blob = "\n".join(texts)
    return dict(rows=1+len(kids)+len(tcs), llr=len(kids), tc=len(tcs), chars=len(blob),
                idents=len(IDENT.findall(blob)), pass1=len(PASS1.findall(blob)),
                idrefs=len(ID_TOKEN.findall(blob)), tcs=tcs)

for sr_id in sys.argv[3:]:
    r = SR[sr_id]; m = metrics(sr_id)
    lines = [f"# BEFORE — subtree of {sr_id} (verbatim from the registries at HEAD)", ""]
    lines.append(f"## SN excerpt ({', '.join(r.get('sn_refs', []))})")
    for sn in r.get("sn_refs", []):
        n = SN.get(sn, {})
        lines += [f"### {sn} — {n.get('title','')}", f"need: {n.get('need','')}", f"acceptance: {n.get('acceptance','')}", ""]
    lines += [f"## {sr_id} — {r.get('title','')}"]
    for k in ("sn_refs","boundary_refs","hat_refs","requirement","rationale","acceptance_criteria","priority","verification","status","phase","coincident","delivered_with","da_refs"):
        if k in r: lines.append(f"{k} = {r[k]!r}")
    lines.append("")
    lines.append(f"## LLRs ({len(children[sr_id])})")
    for k in children[sr_id]:
        l = LLR[k]
        lines.append(f"### {k} — {l.get('title','')}  [sr_refs={l.get('sr_refs')}, module={l.get('module')}, code_symbol={l.get('code_symbol')}, component={l.get('component')}, test_refs={l.get('test_refs')}]")
        lines.append(f"detail ({len(str(l.get('detail','')))} chars): {l.get('detail','')}")
        if 'rationale' in l: lines.append(f"rationale ({len(str(l['rationale']))} chars): {l['rationale']}")
        lines.append("")
    lines.append(f"## TCs ({len(m['tcs'])})")
    for t in m['tcs']:
        c = TC[t]
        lines.append(f"### {t}  [verifies={c.get('verifies')}, level={c.get('level')}, tier={c.get('tier')}, automated={c.get('automated')}, status={c.get('status')}]")
        lines.append(f"method: {c.get('method','')}")
        lines.append(f"expected: {c.get('expected','')}")
        lines.append(f"evidence: {c.get('evidence','')}")
        lines.append("")
    lines += ["## METRICS (before)", f"rows={m['rows']} (1 SR + {m['llr']} LLR + {m['tc']} TC)", f"chars={m['chars']} (SR requirement+AC, LLR title+detail, TC method+expected+evidence)", f"identifiers (broad IDENT)={m['idents']}; first-pass regex matches={m['pass1']}; spine-id tokens={m['idrefs']}"]
    (OUT / f"{sr_id}-before.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{sr_id}: rows={m['rows']} LLR={m['llr']} TC={m['tc']} chars={m['chars']} idents={m['idents']} pass1={m['pass1']} idrefs={m['idrefs']} -> {OUT / (sr_id + '-before.md')}")
