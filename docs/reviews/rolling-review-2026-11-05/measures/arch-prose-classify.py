"""Classify sentences in the architecture prose as METHOD (what an adopter does)
vs MACHINERY (this kit's scripts/flags/markers/dashboard/exit codes) vs PROVENANCE."""
import re, sys, pathlib
ROOT = pathlib.Path('/home/user/ai-template')
MACH = re.compile(r'gen_arch_map|gen_trajectory|gen_components|check_trajectory|check_flows|trace\.py|trace_text|plan_briefs|--\w|GENERATED|marker|dashboard|How-SW|How \(SW|PROJECT_STATE|\[checks\]|warn-first|warn-only|WARN\b|ERROR\b|exit code|exit-code|refus|REPORTED|finding|allowlist|interfaces_check|components_check|freshness|stale|opt-out|default-on|\.toml|\.csv|\.md\b|pre-commit|hook', re.I)
PROV = re.compile(r'WI-\d+|OI-\d+|\bruled\b|owner ruling|AXES|FB\d|\bD\d\b|sitting')
def sents(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    text = re.sub(r'\s+', ' ', text)
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z*`(])', text) if len(s.strip()) > 20]
def classify(label, text):
    ss = sents(text); m = p = 0
    for s in ss:
        if PROV.search(s): p += 1
        elif MACH.search(s): m += 1
    meth = len(ss) - m - p
    print(f'| {label} | {len(ss)} | {meth} | {m} | {p} | {100*meth//max(1,len(ss))}% |')
def lines(path, a, b):
    return '\n'.join(path.read_text(encoding='utf-8').splitlines()[a-1:b])
P = ROOT/'project-trajectory/PROCESS.md'; O = ROOT/'project-trajectory/PROCESS_OPTIONS.md'
print('| home | sentences | method | machinery | provenance | method share |'); print('|---|---|---|---|---|---|')
t = P.read_text(encoding='utf-8').splitlines()
# §3 architecture paragraphs: from "Architecture is derived" bullet to end of §3
start = next(i for i,l in enumerate(t) if 'Architecture is derived, never committed' in l)+1
end = next(i for i,l in enumerate(t) if l.startswith('## 4. Objectives'))
classify('PROCESS §3 (arch bullets→end)', '\n'.join(t[start-1:end]))
classify('PROCESS §8 Interface seams', lines(P,1298,1390))
classify('OPTIONS Intra-repo interfaces', lines(O,2486,2574))
classify('OPTIONS Component layer', lines(O,2623,2706))
classify('OPTIONS Complexity ratchet', lines(O,1681,1726))
classify('OPTIONS §10 several modules', lines(O,2776,2812))
classify('AGENTS.template Code we want + contract', '\n'.join(l for l in (ROOT/'project-trajectory/AGENTS.template.md').read_text(encoding='utf-8').splitlines()[73:132]))
classify('skill architecture-decomposition', (ROOT/'project-trajectory/skills/architecture-decomposition/SKILL.md').read_text(encoding='utf-8'))
classify('skill deep-module-design', (ROOT/'project-trajectory/skills/deep-module-design/SKILL.md').read_text(encoding='utf-8'))
classify('rubric architecture-decomposition', (ROOT/'docs/rubrics/architecture-decomposition.md').read_text(encoding='utf-8'))
classify('INTERFACES.template.md', (ROOT/'project-trajectory/INTERFACES.template.md').read_text(encoding='utf-8'))
