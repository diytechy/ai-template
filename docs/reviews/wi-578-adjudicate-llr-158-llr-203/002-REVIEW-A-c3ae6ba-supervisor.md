### REVIEW-A — WI-578 — Round 002 — 2026-09-03 — supervisor-drawn (independent Opus, hostile brief)

Lane worktree `wi-578-adjudicate-llr-158-llr-203`, HEAD `c3ae6ba0`, integration
base `921f947abd47`, trunk `contract_split`. An ADJUDICATE session, not a build:
the failure classes it admits are (1) a lane taking an approval act it may not
take, (2) a wrong MEANING/CLARITY ruling absorbing unblessed text, (3) a false
"I was blocked" claim covering an act the adjudicator could have taken, and
(4) a successor that misroutes the corrective work. Hunted in that order.

## What I verified

**1. THE ABSOLUTE CONSTRAINT — clean, both ways.** No `Status` flip, no
snapshot byte. Driven at both scopes, because a lane can smuggle a write in
either the authored commits or the refresh:

```
$ git diff contract_split...HEAD --name-only | grep -E 'docs/requirements/|docs/test/|last_approved|docs/archive'
  (none)
$ git diff 921f947abd47..HEAD --name-only | grep -E 'docs/requirements/|docs/test/|last_approved|docs/archive'
  (none)
```

No registry file and no `docs/archive/last_approved/` path appears in either
diff, so there is no `Status` cell to diff. The verdict's closing claim — "No
registry CELL was edited by this session, and no snapshot byte moved" — is
true. Working tree clean (`git status --porcelain` empty).

**2. THE THREE MEANING RULINGS — all correct.** I did not take the verdict's
word for the before/after text; I re-derived it in-process from the ledger the
mechanism itself builds (`baseline_snapshot.refresh_ledger(root)`), which
returns the snapshot/live pairs for exactly the cells at issue, and read all
five. The row's own `## Context` names five cells across three rows; the ledger
carries the same five (LLR-158 `Detail`; LLR-203 `Detail`, `Rationale`,
`Title`; LLR-204 `Detail`). `rows=3` is the right counter and the excluded 26
are correctly excluded.

- **LLR-158 `Detail` — MEANING, correct.** The old text is preserved verbatim
  and an entire second half is APPENDED: `_spine_row_sides` as one shared
  two-tree walk with four named consumers, the exempts-vs-reports invariant
  with its single de-approval subtraction, `_approval_act` as the one home of
  the per-row judgement, and a declared parameterised universe
  (`SPINE_CSVS` / `APPROVAL_ACT_CSVS` / `OUTSIDE_THE_APPROVAL_ACT`) pinned as
  an exhaustive disjoint partition. A design in which each reader does its own
  walk and no registry bound is declared satisfies the old text and violates
  the new one. Obligations added, not reworded.
- **LLR-203 `Detail` — MEANING, correct, and the strongest of the three.** The
  old text makes three explicit NEGATIVE claims; the new text falsifies all
  three by construction — "no cell joins an inventoried file to a requirement
  id" against the optional third cell normalized by `mapping_entries`; "every
  arm above walks the DESTINATIONS the inventory declares, never the shipped
  tree" against `delivery_inventory`, which walks the shipped tree; and the
  installer excluded "in prose at its module" against its being a parsed row.
  A reader holding the old text reads a delivered mechanism as absent.
- **LLR-203 `Title` — MEANING, correct.** "carrying no purpose reference" ->
  "and its tolerant purpose reference" is a direct contradiction of the row's
  own scope statement, not a rewording.
- **LLR-203 `Rationale` — MEANING, correct.** Beyond the ownership redraw, the
  new text adds a POSITIVE design constraint absent from the old: the cell must
  be optional and its class must warn rather than gate. A mandatory-reference
  design satisfies the old rationale and violates the new one.
- **LLR-204 `Detail` — MEANING, correct.** The old text closes "the grammar and
  the dial are what the parent's join and its policy WOULD RIDE"; the new adds
  "AND THE PARENT DID NOT COME THIS WAY" and re-bounds the two gaps to this
  mechanism only. A builder acting on the old text discharges SR-163 by
  widening this grammar; under the new text that is wrong work. The obligation
  is redirected — the sharpest form of MEANING.

Every code citation the verdict offers as its re-drive is exact, checked one by
one: `acceptance_record.py` `SPINE_CSVS`:124, `APPROVAL_ACT_CSVS`:144,
`OUTSIDE_THE_APPROVAL_ACT`:165, `_spine_row_sides(..., registries=SPINE_CSVS)`
:422, `staged_approval_acts` passing `APPROVAL_ACT_CSVS`:557-558;
`tests/test_acceptance_record.py:233` pinning the partition against
`baseline_snapshot.SNAPSHOTTED`; `bootstrap.py` `mapping_entries`:2262,
`_mapping_source_exclusions`:2331, `delivery_inventory`:2346;
`gen_arch_map.mapping_purpose_findings`:2085; and
`project-trajectory/mapping-source-exclusions:19` is indeed the installer row
(`scripts/bootstrap.py — installer/generator run from the kit; deliberately not
scaffolded`). No citation drift.

**3. "THE RE-ANCHOR IS BLOCKED" — TRUE, and reproduced exactly.** Read-only,
in-process, through the same parser the CLI uses (my first probe passed a raw
filename and mis-scoped itself; `parse_approves` resolves it to the rel path,
which is what `refresh_refusal`'s `rel not in named` compares):

```
$ ap = baseline_snapshot.parse_approves("low-level-requirements.toml=<ref>")
  parsed keys: ['docs/requirements/low-level-requirements.toml']
$ baseline_snapshot.refresh_refusal(root, ap)
baseline_snapshot: REFUSED — this refresh would ABSORB approved text into the record of what a human blessed...
  docs/requirements/system-requirements.toml SR-024: Rationale
  ... (+12 more row(s))
  docs/test/test-cases.toml TC-138: Method
  docs/test/test-cases.toml TC-147: Method
  docs/test/test-cases.toml TC-194: Method
```

`low-level-requirements.toml` is ABSENT from the refusal — the `--approves`
authorised it — and every listed row is an `SR-###`/`TC-###` the adjudicator
did not judge. The verdict's quoted output is accurate. The measured ledger
matches its table exactly:

```
docs/requirements/system-requirements.toml     absorbed_rows=17 flips=0
docs/requirements/low-level-requirements.toml  absorbed_rows= 7 flips=0
docs/test/test-cases.toml                      absorbed_rows= 3 flips=0
interfaces / external / components             absorbed_rows= 0 flips=0
```

The LLR registry's 7 absorbed rows are LLR-058/136/144/158/198/203/204 — the
exact set the verdict names when it says blessing the file would carry four
other already-ruled rows. The claimed CONTRADICTION is real in the source, not
inferred: `_authorised_registries` returns `set(approves)` plus registries with
an approving `Status` move (docstring: "an untouched registry is not written"),
while `blocked` is built over the WHOLE ledger — `[(rel, e) for rel, e in
sorted(ledger.items()) if e["absorbed"] and not e["flips"] and rel not in
named]`. WI-571 scoped the writer and left the gate global.

**The adjudicator could NOT have taken the act, and did not work around it.**
Of `refresh_refusal`'s three documented routes: (1) amend-plus-flip is
unavailable — all three rows are `Approved` on both sides, so there is no
`Status` to move; (2) `--approves` naming only the ruled registry is refused,
as reproduced above; (3) reverting the amendment is not an adjudicator's act.
Naming the other two registries would have recorded into the snapshot's README
stamp that WI-578 authorised twenty cells it never read. Declining that is the
correct call, not a dodge, and the file says so with its evidence. Taking NO
act was right.

**5. The machine line.** Exactly one `VERDICT:` line
(`grep -c '^VERDICT:'` -> `1`), it is the last line of the file, and it reads
`VERDICT: MEANING rows=3` — matching
`adjudicate_brief.VERDICT_GRAMMAR["amendment"] = ("VERDICT", ("MEANING",
"CLARITY"), ("rows",))`. The line 13 mention of `VERDICT:` is inside prose and
does not match the `^\s*VERDICT:` anchor. N=3 matches the in-scope rows.

**6. Scope — clean.** The lane's own authorship (`921f947abd47..2329f28c`) is
three files: the telemetry log, the verdict record, and the spec it added
`## Dispositions` to. The brief's reading scope confirms it:

```
$ git diff contract_split...HEAD --stat -- . ':(exclude)docs/iteration' ':(exclude)docs/reviews' ...
 docs/status.md                                        |   1 -
 .../WI-578-adjudicate-llr-158-llr-203.md              |  27 -----
 .../complete/WI-578-adjudicate-llr-158-llr-203.md     | 109 +++++++++++++
```

The `docs/log.d` deletions and the +370 in `docs/log.md` visible in the two-dot
stat are trunk's own merged work arriving via the refresh, not this lane's. The
single `docs/status.md` deletion is the done-WI-id scrub the close requires. No
code file is touched at any scope. No creep.

**7. Harness.**

```
$ .venv/bin/python project-trajectory/scripts/trace.py --strict-integrity | tail -1
Traceability: SN=27 SR=76 LLR=188 TC=187 orphans=2 integrity=0 verified-mechanized=72 verified-demonstrated=3 verified-attested=0 drafts=9 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=162 interface-findings=0 provenance-findings=1 paraphrase-advisories=3. Report -> docs/test/report.md

$ .venv/bin/python project-trajectory/scripts/check_trajectory.py --strict 2>&1 | grep -c ERROR
1
```

`integrity=0`. The one ERROR is `cross-component import scripts/schedule
(CMP-008) -> scripts/trace (CMP-006) has no declared IF-### seam` — INHERITED,
not caused: this lane's diff contains zero Python files at either scope, so the
import graph is byte-identical to trunk's. Not a finding against WI-578.

**4. The drafted successor.** `intake.parse_dispositions` on the closed spec
returns exactly one draft and NO refusal string. `safety_class = "spine"` is a
valid `schedule.SAFETY_CLASSES` member; `bar = "DevStg-Impl"` is a valid WI bar;
`specref` pointing at a registry file is the kit's own mint idiom
(`intake.py:742`, `:861`). The scope is stated as a reproducible OBSERVABLE
with a measured ledger and a named contradiction in two functions, and it
refuses to presume the ruling — offering (a) and (b) with the same acceptance
shape either way. That is a well-built disposition, not frustration, and I
tried hard to read it as venting; it isn't.

On `safety_class = "spine"`: I judged it and it is RIGHT for the mechanism half,
though for a reason the draft does not state. The row authors no spine cell text
— it says so in OUT OF SCOPE — so on an "authors spine text" reading `ordinary`
would look defensible. It is not: `ordinary` maps to
`CONCURRENCY_PARALLEL`, and `refresh_ledger` is a whole-tree comparison whose
outcome changes if any concurrent lane amends any registry mid-act. `spine`
buys `CONCURRENCY_EXCLUSIVE` and rank 0, which this work genuinely needs. Not a
misdeclaration.

But the row's SECOND half is misrouted, which is finding 1 below.

## Findings

- [MAJOR] docs/work/complete/WI-578-adjudicate-llr-158-llr-203.md:99 -> the successor's "THEN, AND ONLY THEN, the anchor. Once the act is takeable, re-anchor `low-level-requirements.toml`" is in scope for a `safety_class = "spine"` row (line 38), and a spine row is a WORKER LANE, which may not take that act — re-anchoring writes `SNAPSHOT_DIR`, and `acceptance_record.lane_approval_refusal` refuses precisely that ("in those four spine registries it does not flip a `Status` ... and it does not write `SNAPSHOT_DIR`"), with `merge_approval_refusal` routing there because `integrate._adjudication_lane` is true only for `safety_class = "adjudication"` — which `intake.py:1349` forbids a disposition draft from declaring; so as drafted the row's closing step is unmergeable in the very lane the mint creates, and the successor cannot deliver the outcome it exists for (this is not a missing guard — the guard exists and already makes the bad state unrepresentable at merge; the defect is the draft's scope statement, so no unrepresentability clause is owed) -> split the disposition: keep the ruling on (a)/(b) plus the `refresh_refusal` change and its test as this `spine` row's whole scope, and restate the re-anchor as the act the trunk-side amendment-adjudication rung takes AFTER this row lands (the same rung that minted WI-578), naming it as a successor condition rather than a step of this row -> @owner
- [MINOR] docs/work/complete/WI-578-adjudicate-llr-158-llr-203.md:36 -> the drafted `title` is 140 characters, over `check_trajectory._TITLE_CONCISE_MAX` (120), so the row emits the concise-title WARN (`check_trajectory.py:773`) from the moment it is minted and open; the advisory's own comment says its purpose is to "nudge a Title toward concise AT THE SOURCE" and the exemption it describes is for owner-authored text already filed — this is new text at the source, so it takes the nudge rather than the exemption -> shorten to the contradiction itself, e.g. "The snapshot's scoped writer and unscoped refusal disagree on registry scope" (75 chars), leaving the full statement to the scope body where it already appears -> @owner

The adjudication itself — the three rulings, the refusal to take an
unauthorised act, and the evidence behind both — is correct and I could not
break it. What is wrong is where the corrective work was pointed.

VERDICT: CHANGES-REQUESTED findings=2
