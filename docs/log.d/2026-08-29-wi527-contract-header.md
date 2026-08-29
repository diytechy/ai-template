## 2026-08-29 — WI-527: the component-side contract header, built and adversarially reviewed

Deferred open items: none.

`OI-66` ruled (a) GO. The mechanism is built, shipped and gated; a cross-family
adversarial round ran against the design decisions mid-build and its confirmed
findings are applied. The 71-row cell pass is NOT in this slice — see "What is
not done" below.

### What landed

**The harvester fix, the ruling's binding precondition.** The `Contracts:`
marker must now OPEN its line AND parse as an id list — `Contracts:` then a
comma- or semicolon-separated `IF-###` list, optionally then prose. Line-start
alone was not enough and the review proved it: `Contracts: not IF-080; an
example, not a declaration` opens correctly and still leaked `IF-080` under a
"harvest every IF token on the line" rule. The kit's own false positive is gone —
`gen_arch_map.module_contracts` returned `['IF-080']` for `handback.py`, whose
docstring denied a declaration, and now returns `[]`.

**The body grammar.** After the marker, a module states each contract as a block
opening `Contract IF-###:`. The opener is not a bare `IF-###:` deliberately: a
bare id-colon is ordinary docstring prose (`IF-001: legacy identifier retained`,
a mapping row, an example) and only a form nobody writes by accident is safe to
hard-fail on. Four refusals — a body before the marker, a body for an undeclared
id, a second body for one id, and a body carrying an HTML comment (the text is
spliced into generated Markdown and must not be able to close its own end
marker).

**The reference and its gate.** `gen_arch_map.py --contracts-doc` harvests into
`docs/interface-reference.md`, spliced between markers, `--check` red on drift.
Wired as a `check.py` step, a `docs/stack.ini` `[generated]` row, a
`trunk_step.py --regen` step, and a member of the pre-commit hook floor. Stated
contracts lead the document; the declared-but-unstated seams are one compact
line per module rather than 135 placeholder paragraphs.

**A false green closed for the whole kit, not just this artifact.** A
`[generated]` row naming a file that does not exist read GREEN, because every
freshness step is deliberately vacuous on an absent target — so deleting a
declared artifact disarmed its own gate in silence. `staged_divergence` now
fails on an absent declared FILE row. Prefix rows (`docs/okf/`, `docs/ratify/`)
are exempt: `docs/okf/` is legitimately absent because its dial is off.

**No adopter loses a declaration in silence.** Tightening a shipped grammar may
not drop seams quietly, so `check_trajectory` reports both lossy forms by name —
a marker-shaped line whose id list will not parse, and a `Contracts:` carrying
ids mid-line. Driven on this tree: **0 findings**. The detector was proved to
fire by planting a mid-line marker in `census.py` and watching the harness name
it.

**Two real declarations the tightening exposed, both fixed rather than
absorbed.** `plan_artifacts.py` separates its ids with SEMICOLONS, which the
first draft of the grammar rejected — the finding caught it, and the grammar was
widened, because this tightens against prose and never against a separator style
the tree already writes. `handback.py`'s denial was reworded to say the same
thing without carrying the marker token, so the detector stays strict and the
kit's own tree reports nothing.

**Registry work.** `IF-138` gains its declaring module (`pending.py`); `IF-144`
gains one (`check.py`) and the first two real contract bodies. Adopter surfaces:
PROCESS.md section 8, `interfaces.template.toml`, and a `RESYNC_PACK.md` entry
carrying the grammar migration with a search recipe.

### What is NOT done, and why it is not hidden

**The 71-row cell pass has not run.** `OI-66` priced it and this slice built the
mechanism it needs; moving the contract text out of 71 registry cells and into
module headers is authoring work, one row at a time, and it is the item the
price explicitly left unmeasured. Two rows are done (`IF-013`, `IF-144`) as the
proof that the pipeline works end to end. **The reference therefore reads as
mostly debt today — 137 seams declared, 2 stated — which is the honest picture
and the reason the debt list is a first-class section of the document.**

**`IF-134` and `IF-135` still have no declaring module.** They are the git hooks
(`pre-commit`, `pre-push`), which are extensionless files, so a `*.py` scan
structurally cannot see them. Recorded, not papered over.

**The reverse check is still id-global, not provider-exact.** `IF-021` declared
on the wrong module passes. The review named it; it is a real gap and it is not
this slice's.

### The adversarial round

Record: `docs/reviews/2026-08-29-oi66-build-round/`. OPENAI-SOL at medium
reasoning effort, run mid-build against four named design decisions. Every
testable claim it made was re-verified here before being acted on, and four
parser defects it demonstrated were real: a line-start denial still leaked, a
body before the marker was harvested, duplicate bodies silently kept the last,
and a body could inject the reference's own end marker. All four are fixed and
each has a test.

### Gates

Smoke **1,363 passed, 6 skipped**. Full suite and the commit bar recorded with
the commit. Three module-size baselines and three complexity entries re-stamped
deliberately, each with its reason in the table — no baseline was bumped to
green a step.
