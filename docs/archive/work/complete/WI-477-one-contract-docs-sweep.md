+++
id = "WI-477"
title = "One authoritative contract: sweep the shipped and reference surfaces whose taught schema, delivery ledger, and posture claims drifted from enforcement (repo review 2026-08-19 H-06, H-07, H-08, L-01, M-13, L-03, M-15)"
workstream = "docs"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

One authoritative contract restored across the shipped and reference
surfaces, with the sweep PINNED rather than repeatable:
`tests/test_status_vocabulary_contract.py` reads the enforcement constants
(`trace.ENUM_FIELDS`/`STATUS_VALUES`) and reds any instructing surface
teaching a retired value or the retired `Approval` column —
mutation-verified. **SCOPED HONESTLY 2026-08-20** (closing review,
ROUND-OPUS MINOR-15 / ROUND-SOL MAJOR-7, which planted the cases): "any
instructing surface" was one channel, not any — the scan read
`status = "<word>"` ASSIGNMENTS over a hand-listed set of eleven files, so
a sentence ("Valid statuses are Drafted, Modified, and Approved") passed
clean, and a new instructing document landed outside the list unseen. The
covered channels are now THREE and are named as such: the assignment
channel; a narrow PROSE channel (a retired word on a line that also says
`status`, with a token-scoped historical exemption, measured
zero-to-zero on the live surfaces); and the surface list itself, which
every kit-root `.md` must now either join or be excluded from with a
stated reason. Two internal weaknesses went in the same pass — a
disjointness assertion that was true by construction, and a line-scoped
`retire` exemption that excused a whole table row. Still not covered,
stated rather than implied: a sentence that teaches a value without using
the word `status`. H-06 swept everywhere the checklist named (the
vocabulary re-verified FIRST: it had moved again at the signing — Approval
retired, {Drafted, Approved} enforced for IF/frame, {Drafted, Approved,
Founded} for spine), EXAMPLE.md's CSV IF block converted to the real TOML
carrier, plus two LIVE `Status=Modified` claims the review itself missed.
H-07: the three-category inventory (required spine / required-off-spine
frame, "inert until filled" / optional layers) with EXT/B/REL in the root
diagram and both inventories. H-08: the ledger restated shipped /
half-shipped / still-owed; the derive-from-row-states suggestion DECLINED
with evidence (SN-037 shipped with no LLR/TC while SN-040's chain calls
itself not-built — row state is not a delivery proxy in either direction).
L-01: three stale comments corrected. M-13: the gate renamed to its
measured posture (opt-in, fail-open supervision) with four
corruption-vs-absence tests including the fall-through-to-legacy pin; the
posture itself stays the owner's. L-03: both live commit-subject forms
stated once, enforcing nothing. M-15: status.md 139 → 120 lines (at
budget; the warning gone) by RELOCATING the standing-rules doctrine to
session-protocol §2 per its own header. Three RESYNC entries; tri-copied
skills swept whole. PROCESS.md +124 flagged; trace.py held exactly at its
baseline; max-tests re-stamped 1226→1240 for irreducible growth after
cutting 24 test ids by design. Full suite 2657/13; the worker caught its
own CRLF introduction via the very rule it had relocated.

## Context

The review's documentation cluster, every item re-verified against this tree
2026-08-19 (verification table in
`docs/log.d/2026-08-19-repo-review-triage.md`). One coordinated sweep, per the
review's own advice, because the drift accumulated exactly by being maintained
in ten places. Checklist, with the verified anchors:

- **H-06 — taught schema vs enforced schema.** Enforced: IF-row maturity is
  `Status = Drafted|Approved` (`trace.py:474`, `interfaces.template.toml`).
  Drifted surfaces: `PROCESS.md:1099,:1125` (`Approval`, lower-case values);
  `INTERFACES.template.md:22,:45` (an `Approval` column its OWN example at
  `:96,:107` does not use); `specs/README.template.md:31` +
  `specs/WI-000.template.md:36` (`Status=Proposed` rows — retired; also both
  still claim a "Proposed citation carries a rationale" checker arm that
  `check_trajectory.py:1616` says is GONE; the `IF-045 (Proposed)` plan-
  coverage CITATION notation is separate and legitimate — do not sweep it);
  `KICKOFF_PROMPT.md:146`, `EXAMPLE.md:500,:513`, `MULTI_REPO.md:167,:279`,
  `docs/registry-machinery-reference.md:653` (`Stable`/`Approval`);
  `README.md:201` CMP `State` vs implemented `status`/`standing`/
  `superseded_by` — plus the same retired words in `derive_gate.py:592,:634`
  comments. Prefer generating the schema tables from the enforcement
  constants, or add one cross-document contract test on a shared definition —
  do not hand-maintain this vocabulary in ten places again.
- **H-07 — the depth-0 frame taught as optional.** `README.md:140-141,:188`
  call everything off-spine optional and the root diagram omits EXT/B/REL,
  while `PROCESS.md` makes `DevStg-Boundary` rung 1 with
  `requirements/external.toml` its deliverable and `bootstrap.py:1648` always
  installs it. Adopt the review's three categories everywhere: required
  spine; required depth-0 frame (off-spine, NOT optional — inert-until-filled
  is the honest gloss, per `bootstrap.py:167-172`); optional layers. Add
  EXT/B/REL to the root diagram and both inventories.
- **H-08 — the commissioned-vs-shipped ledger is false in both directions.**
  `README.md:121-123` claims the SN-036 machine-readable record shipped
  (`hats.py:14-18` says it is DELIBERATELY NOT BUILT; SR-161 exists but is
  Drafted with no LLR/TC) and `:126-127` still owes SN-033's checker
  (delivered: `check_need_form.py`, wired at all three bars in `check.py`,
  traced SR-150 → LLR-170 → TC-164). State it straight: SN-036
  roster+injection shipped, record+missing-perspective check owed; SN-033
  checker shipped, warn-first. Prefer deriving the ledger from row states.
- **L-01 — stale operational comments.** `check_trajectory.py:61` module
  header says `status_forward_only_findings` is "not yet implemented — no
  status.md generator exists" while the function sits at `:2416` and its own
  docstring (`:2436`) records the correction the header never got;
  `skills/registry-hygiene/SKILL.md:30` teaches "+ Verified" (folded into
  Approved — the `--require-verified` FLAG stays valid; skills are
  tri-copied, sweep all three); `handback.py:56-57` claims integration "never
  the reverse"-imports while `integrate.py:2186` imports handback (the
  structural fix is WI-483's; the false sentence goes now).
- **M-13 — the subagent gate's headline contradicts its behavior.**
  `subagent_gate.py:2` says "deny-by-default"; absent/off/malformed policy
  ALLOWS by design (`:13-20,:57-85,:188-201`, pinned by tests). Rename the
  posture honestly ("opt-in, fail-open supervision") and test corruption
  separately from absence. Changing the fail posture itself is explicitly OUT
  of scope here — if wanted, that is an owner call to raise as its own item.
- **L-03 — two live commit-subject conventions.** The session-protocol skill
  prescribes `WI-<n>: <imperative>`; recent practice uses category prefixes
  for non-WI sessions. State the convention once in the skill: `WI-<n>:` for
  WI sessions, `<category>:` for sittings/sweeps/merges — enforce nothing.
- **M-15 — status.md over its own budget.** 167 lines against the declared
  120; the `check_docs --stale` warning has become background noise. Move
  durable doctrine to its process home and resolved countersign detail to
  log/decision evidence; much of the bulk is sitting instructions that
  dissolve at the sitting — coordinate, don't collide.

Constraints: `AGENTS.template.md` is byte-capped and `PROCESS.md`
byte-watched — run the byte-budget-guard skill before and after; edits to
shipped surfaces owe RESYNC entries; where a table can be generated from the
same constants enforcement reads, generate it.
