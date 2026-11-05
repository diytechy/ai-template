"""Words an LLM is handed per sitting: stripped brief body + composed {questions}.
Reproduces prompts.strip_dispatcher_block (leading <!-- --> removed) and
amendment_brief.tier_questions (sections whose tiers line matches, '*' always).
Usage: python -I words_per_sitting.py <repo-root>
"""
import pathlib, re, sys
root = pathlib.Path(sys.argv[1]) / "project-trajectory"
P = root / "prompts"

def strip(text):
    body = text.lstrip()
    if body.startswith("<!--"):
        end = body.find("-->")
        if end != -1:
            return body[end + 3:].lstrip()
    return body

def wc(s):
    return len(s.split())

q = strip((P / "spine-questions.md").read_text(encoding="utf-8"))
sections = []
for chunk in re.split(r"(?m)^(?=## )", q)[1:]:
    heading, _, rest = chunk.partition("\n")
    marker, _, body = rest.partition("\n")
    m = re.fullmatch(r"<!--\s*tiers:\s*(.*?)\s*-->", marker.strip())
    tiers = frozenset(m.group(1).split()) if m else frozenset()
    sections.append((heading.strip(), tiers, wc(heading + "\n" + body)))
print("spine-questions.md sections (words):")
for h, t, n in sections:
    print(f"  {n:5d}  {sorted(t)}  {h}")
print(f"  total composable: {sum(n for _,_,n in sections)}")

def questions_for(tiers):
    return sum(n for _, t, n in sections if "*" in t or (t & set(tiers)))

for label, tiers in [("SN only", {"SN"}), ("SR only", {"SR"}), ("LLR only", {"LLR"}), ("TC only", {"TC"}), ("LLR+TC", {"LLR", "TC"}), ("SR+LLR+TC", {"SR", "LLR", "TC"}), ("SN+SR+LLR+TC", {"SN","SR","LLR","TC"})]:
    print(f"  {{questions}} for {label:14s}: {questions_for(tiers):5d} words")

print("\nbrief bodies after the dispatcher-notes strip (words), and raw file words:")
for f in sorted(P.glob("*.template.md")):
    raw = f.read_text(encoding="utf-8")
    print(f"  {wc(strip(raw)):5d} stripped / {wc(raw):5d} raw  {f.name}")

fa = wc(strip((P / "adjudicate-first-approval.template.md").read_text(encoding="utf-8")))
am = wc(strip((P / "adjudicate-amendment.template.md").read_text(encoding="utf-8")))
print("\nper-sitting totals (brief body + {questions}; chain/rows slots NOT counted):")
for label, tiers in [("first-approval, SR+LLR+TC", {"SR","LLR","TC"}), ("first-approval, LLR+TC", {"LLR","TC"}), ("first-approval, SN only", {"SN"}), ("first-approval, all four", {"SN","SR","LLR","TC"})]:
    print(f"  {label:28s}: {fa} + {questions_for(tiers)} = {fa + questions_for(tiers)} words")
for label, tiers in [("amendment, SR+LLR+TC", {"SR","LLR","TC"}), ("amendment, all four", {"SN","SR","LLR","TC"})]:
    print(f"  {label:28s}: {am} + {questions_for(tiers)} = {am + questions_for(tiers)} words")

# the skill an authoring session reads, and what it points at
sk = root / "skills/spine-authoring"
skill = wc((sk / "SKILL.md").read_text(encoding="utf-8"))
inlane = wc((sk / "references/in-lane.md").read_text(encoding="utf-8"))
print(f"\nauthoring session: spine-authoring SKILL.md {skill} + references/in-lane.md {inlane} + spine-questions composable {sum(n for _,_,n in sections)} = {skill+inlane+sum(n for _,_,n in sections)} words")
# template -000 guidance words (what an author copying the form reads)
for t in ["system-requirements", "low-level-requirements", "test-cases", "stakeholder-needs"]:
    txt = (root / "registries" / f"{t}.template.toml").read_text(encoding="utf-8")
    print(f"  template {t}: {wc(txt)} words, {len(txt)} bytes")
