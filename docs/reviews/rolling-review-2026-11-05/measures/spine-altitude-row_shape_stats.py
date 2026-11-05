"""Row-shape facts not in the first-pass measure.py (stdlib only).
Usage: python -I row_shape_stats.py <repo-root>"""
import pathlib, re, statistics, sys, tomllib
root = pathlib.Path(sys.argv[1])
def rows(path, table):
    d = tomllib.load(open(path, "rb"))
    return {k: v for k, v in d[table].items() if re.match(r"^[A-Z]+-\d+$", k)}
sr = rows(root/"docs/requirements/system-requirements.toml", "requirement")
llr = rows(root/"docs/requirements/low-level-requirements.toml", "design")
tc = rows(root/"docs/test/test-cases.toml", "test")
def words(s): return {w for w in re.findall(r"[a-z_]{4,}", str(s or "").lower())}
def num(r): return int(r.split("-")[1])

print("== TC method cell shapes ==")
m_run = sum(1 for v in tc.values() if re.match(r"\s*(Run|Drive|Invoke) the .*(suite|tests?)\b", str(v.get("method",""))))
m_testnames = [k for k, v in tc.items() if re.search(r"\btest_[a-z0-9_]+", str(v.get("method","")))]
m_funcs = [k for k, v in tc.items() if re.search(r"\b[a-z][a-z0-9]*_[a-z0-9_]+\(|\b[a-z][a-z0-9_]*_[a-z0-9_]+ (called|invoked|is called)\b", str(v.get("method","")))]
m_inmem = sum(1 for v in tc.values() if re.search(r"in[- ]memory", str(v.get("method","")), re.I))
print(f"TC total {len(tc)}; method opens 'Run/Drive the ... suite/tests': {m_run}")
print(f"method names pytest test functions (test_xxx): {len(m_testnames)}  e.g. {m_testnames[:8]}")
print(f"method names an internal function by identifier (foo_bar( / foo_bar called): {len(m_funcs)}  e.g. {m_funcs[:8]}")
print(f"method says 'in memory': {m_inmem}")
ml = [len(str(v.get("method",""))) for v in tc.values()]
print(f"method chars: median {statistics.median(ml):.0f}, >500: {sum(1 for x in ml if x>500)}, >1000: {sum(1 for x in ml if x>1000)}, max {max(ml)}")

print("\n== TC expected vs LLR detail (copy, not outcome) ==")
copies = []
for k, v in tc.items():
    exp = words(v.get("expected"))
    if len(exp) < 15: continue
    for l in v.get("verifies", []):
        if l in llr:
            det = words(llr[l].get("detail"))
            if det and len(exp & det)/len(exp) > 0.7:
                copies.append((k, l, round(len(exp & det)/len(exp),2), len(str(v.get("expected")))))
                break
print(f"TC expected (>=15 content words) whose words are >70% contained in a verified LLR's detail: {len(copies)}")
for c in copies[:12]: print("  ", c)
el = [len(str(v.get("expected",""))) for v in tc.values()]
print(f"expected chars: median {statistics.median(el):.0f}, >=400: {sum(1 for x in el if x>=400)}, max {max(el)}")
sat = sum(1 for v in tc.values() if re.match(r"Satisfies ", str(v.get("expected",""))))
sat_only = sum(1 for v in tc.values() if re.fullmatch(r"Satisfies [^:]{0,120}", str(v.get("expected","")).strip()))
print(f"expected opens 'Satisfies': {sat}; is ONLY a pointer (no colon-continuation, <=120 chars): {sat_only}")

print("\n== TC-N shadows LLR-N ==")
shadow = [k for k, v in tc.items() if f"LLR-{k.split('-')[1]}" in v.get("verifies", [])]
print(f"TCs whose verifies names the LLR with the same number: {len(shadow)} of {len(tc)}  (e.g. {shadow[:10]})")
one_llr = sum(1 for v in tc.values() if sum(1 for x in v.get("verifies", []) if x.startswith("LLR-")) == 1)
print(f"TCs verifying exactly one LLR: {one_llr}")
fanin = [(k, len(v.get("verifies", []))) for k, v in tc.items() if len(v.get("verifies", [])) >= 5]
print(f"TCs with >=5 verifies entries: {len(fanin)}  max {max(fanin, key=lambda x: x[1]) if fanin else None}")
ifs = sum(1 for v in tc.values() if any(x.startswith("IF-") for x in v.get("verifies", [])))
print(f"TCs whose verifies names an IF- row: {ifs}")
multi_llr_per_llr = {}
for k, v in tc.items():
    for l in v.get("verifies", []):
        if l.startswith("LLR-"): multi_llr_per_llr.setdefault(l, []).append(k)
print(f"LLRs with 0 TC: {sum(1 for l in llr if l not in multi_llr_per_llr)}; LLRs with exactly 1 TC: {sum(1 for l in llr if len(multi_llr_per_llr.get(l, []))==1)}; with >=3: {sum(1 for l in llr if len(multi_llr_per_llr.get(l, []))>=3)}")

print("\n== LLR module / code_symbol cells ==")
mods = [len([m for m in str(v.get("module","")).split(";") if m.strip()]) for v in llr.values()]
print(f"LLR total {len(llr)}; module cell lists >=2 modules: {sum(1 for x in mods if x>=2)}; >=4: {sum(1 for x in mods if x>=4)}; max {max(mods)}")
syms = [len([s for s in re.split(r"[;/,\s]+", str(v.get("code_symbol",""))) if s.strip()]) for v in llr.values()]
print(f"code_symbol tokens: total {sum(syms)}, median {statistics.median(syms):.0f}, >=5: {sum(1 for x in syms if x>=5)}, >=10: {sum(1 for x in syms if x>=10)}, >=20: {sum(1 for x in syms if x>=20)}, max {max(syms)}")
top = sorted(((len([s for s in re.split(r'[;/,\s]+', str(v.get('code_symbol',''))) if s.strip()]), k) for k, v in llr.items()), reverse=True)[:5]
print(f"largest symbol lists: {top}")
sym_main = sum(1 for v in llr.values() if str(v.get("code_symbol","")).strip() == "main")
print(f"code_symbol == 'main' exactly: {sym_main}")
nonpy = sum(1 for v in llr.values() if str(v.get("module","")) and not any(m.strip().endswith(".py") for m in str(v.get("module","")).split(";")))
print(f"LLRs whose module names only non-.py files: {nonpy}")
det_fn = sum(1 for v in llr.values() if re.search(r"\b[a-z][a-z0-9_]*_[a-z0-9_]*\(", str(v.get("detail",""))))
print(f"LLR detail containing a call-syntax token foo_bar(: {det_fn}")
rat = sum(1 for v in llr.values() if str(v.get("rationale","")).strip())
print(f"LLRs with a rationale: {rat}")

print("\n== SR requirement shape ==")
rl = [len(str(v.get("requirement",""))) for v in sr.values()]
print(f"SR total {len(sr)}; requirement chars: median {statistics.median(rl):.0f}, >300: {sum(1 for x in rl if x>300)}, >500: {sum(1 for x in rl if x>500)}, max {max(rl)}")
semi = [str(v.get("requirement","")).count(";") for v in sr.values()]
print(f"requirement with >=2 semicolons: {sum(1 for x in semi if x>=2)}; >=4: {sum(1 for x in semi if x>=4)}")
shalls = [len(re.findall(r"\bshall\b", str(v.get("requirement","")))) for v in sr.values()]
print(f"requirement with >1 'shall': {sum(1 for x in shalls if x>1)}; 0 'shall': {sum(1 for x in shalls if x==0)}")
ears = sum(1 for v in sr.values() if re.match(r"\s*(When|While|If|Where)\b", str(v.get("requirement",""))))
print(f"requirement opening on a conditional EARS keyword: {ears}; ubiquitous (The/A ...): {len(sr)-ears}")
print("\n== fill rate of the SR template's keys (kit's own 138 SRs) ==")
for key in ["permutations","da_refs","coincident","delivered_with","form","aspect","hat_refs","boundary_refs","phase"]:
    n = sum(1 for v in sr.values() if v.get(key) not in (None, "", []))
    print(f"  {key:15s} filled in {n:3d} / {len(sr)}")
print("== fill rate of TC template keys ==")
for key in ["parameters","assumption_refs","inputs","max_age","sampling","rubric","trigger"]:
    n = sum(1 for v in tc.values() if v.get(key) not in (None, "", []))
    print(f"  {key:15s} filled in {n:3d} / {len(tc)}")
obs = sum(1 for v in tc.values() if str(v.get("automated","")).lower()=="no")
print(f"TC automated=No (observation/inspection): {obs}")
print("== verification methods across SRs ==")
import collections
print(collections.Counter(str(v.get("verification")) for v in sr.values()))
print("== TC level ==", collections.Counter(str(v.get("level")) for v in tc.values()))
print("== TC tier ==", collections.Counter(str(v.get("tier")) for v in tc.values()))
