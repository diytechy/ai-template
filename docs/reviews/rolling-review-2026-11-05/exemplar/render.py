"""Render BEFORE (condensed, from the live registries) and AFTER (full, from the proposal TOML) as markdown."""
import re, sys, tomllib
from pathlib import Path
ROOT = Path(sys.argv[1]); AFTER = Path(sys.argv[2]); OUT = Path(sys.argv[3])
def load(p, section):
    with open(p, "rb") as fh: d = tomllib.load(fh)
    return {k: v for k, v in d.get(section, {}).items() if not k.endswith("-000")}
SN = load(ROOT/"docs/requirements/stakeholder-needs.toml", "need")
SR = load(ROOT/"docs/requirements/system-requirements.toml", "requirement")
LLR = load(ROOT/"docs/requirements/low-level-requirements.toml", "design")
TC = load(ROOT/"docs/test/test-cases.toml", "test")
IDENT = re.compile(r"\b[A-Za-z_][A-Za-z_0-9]*\(|\b[a-z][a-z0-9]*_[a-z0-9_]+\b|\b[\w./-]+\.(?:py|toml|md|csv|ini|html|cmd|sh|json|txt)\b|--[a-z][a-z0-9-]+|\b[A-Z][A-Z0-9_]{3,}\b|\b[a-z]+\.[a-z_]+\.[a-z_]+\b")
def esc(s): return str(s).replace("|", "\\|").replace("\n", " ")
def clip(s, n): s = esc(s); return s if len(s) <= n else s[:n].rstrip() + " …"
def base(mod): return "; ".join(Path(m.strip()).name for m in str(mod).split(";") if m.strip())
out = []
for sr_id in sys.argv[4:]:
    r = SR[sr_id]
    kids = [l for l, x in LLR.items() if sr_id in x.get("sr_refs", [])]
    tcs = sorted({t for t, x in TC.items() if sr_id in x.get("verifies", []) or any(k in x.get("verifies", []) for k in kids)}, key=lambda t: int(t.split("-")[1]))
    out.append(f"\n### {sr_id} — BEFORE (live registries at HEAD f17b62a30; condensed — verbatim text in the scratch dump)\n")
    out.append("SN excerpt: " + " · ".join(f"**{sn}** “{clip(SN[sn]['need'], 110)}”" for sn in r.get("sn_refs", [])) + "\n")
    out.append(f"**SR requirement** ({len(r['requirement'])} chars): {esc(r['requirement'])}\n")
    out.append(f"**SR acceptance_criteria** ({len(r['acceptance_criteria'])} chars): {clip(r['acceptance_criteria'], 600)}\n")
    out.append(f"\n| LLR | title | module (basename) | code_symbol tokens | detail chars | identifiers | opening of detail |\n|---|---|---|---|---|---|---|")
    for k in kids:
        l = LLR[k]; d = str(l.get("detail", ""))
        toks = len([s for s in str(l.get("code_symbol", "")).replace(";", "/").split("/") if s])
        out.append(f"| {k} | {esc(l.get('title',''))} | {base(l.get('module',''))} | {toks} | {len(d)} | {len(IDENT.findall(d))} | {clip(d, 110)} |")
    out.append(f"\n| TC | verifies | level/tier | method chars | expected (opening) | evidence files | node ids |\n|---|---|---|---|---|---|---|")
    for t in tcs:
        c = TC[t]; ev = [x for x in str(c.get("evidence", "")).replace(";", " ").split() if x]
        out.append(f"| {t} | {esc(', '.join(c.get('verifies', [])))} | {c.get('level')}/{c.get('tier')} | {len(str(c.get('method','')))} | {clip(c.get('expected',''), 90)} | {len({x.split('::')[0] for x in ev})} | {sum(1 for x in ev if '::' in x)} |")
    # AFTER
    a_sr = load(AFTER/f"{sr_id}.toml", "requirement"); a_llr = load(AFTER/f"{sr_id}.toml", "design"); a_tc = load(AFTER/f"{sr_id}.toml", "test")
    out.append(f"\n### {sr_id} — AFTER (proposed; full text)\n")
    ar = a_sr[sr_id]
    out.append(f"**SR requirement** ({len(ar['requirement'])} chars): {esc(ar['requirement'])}\n")
    out.append(f"**SR acceptance_criteria** ({len(ar['acceptance_criteria'])} chars): {esc(ar['acceptance_criteria'])}\n")
    # absorbs comments
    text = (AFTER/f"{sr_id}.toml").read_text(encoding="utf-8")
    absorbs = dict(re.findall(r"\[(?:design|test)\.([A-Z]+-\d+)\]\n# ([^\n]*)", text))
    for k, l in a_llr.items():
        out.append(f"\n**{k}** — *{esc(l['title'])}* ({absorbs.get(k,'')})  \nmodule: `{esc(l['module'])}` · code_symbol: `{esc(l['code_symbol'])}` · detail {len(l['detail'])} chars  \ndetail: {esc(l['detail'])}" + (f"  \nrationale: {esc(l['rationale'])}" if l.get('rationale') else ""))
    for t, c in a_tc.items():
        out.append(f"\n**{t}** ({absorbs.get(t,'')}) verifies {esc(', '.join(c['verifies']))} · {c['level']}/{c['tier']}  \nmethod: {esc(c['method'])}  \nexpected: {esc(c['expected'])}  \nevidence: `{esc(c['evidence'])}`")
OUT.write_text("\n".join(out), encoding="utf-8")
print(OUT, len("\n".join(out)), "chars")
