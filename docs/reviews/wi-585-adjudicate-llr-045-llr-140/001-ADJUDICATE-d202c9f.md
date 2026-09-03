# WI-585 — ADJUDICATE amended-cell meaning/clarity — commit d202c9f

One line per amended row. Question judged: did the amendment change the
requirement's MEANING, or only its CLARITY? Basis: the live registries against
`docs/archive/last_approved` (copied 2026-08-30, commit `4824c0ba`).

**Scope, and why the count is three.** The material handed to me is the whole
drift set — thirty-two rows. This row's own generated `## Context` names
**three**: `LLR-045` `Detail`, `LLR-140` `Detail`, `TC-082` `Method`. The other
twenty-nine are carried by other rows; they are restated below as reading aid
and excluded from the counter — the correction WI-566's REVIEW-A finding 1
forced, WI-573 applied and WI-578 applied. The governing `VERDICT:` line is the
last line of this file and it is the only one.

I re-drove every load-bearing claim in the three in-scope cells against the tree
at this commit rather than reading the diff for plausibility; citations below are
what I read, not what the cells assert.

## In-scope amended rows — adjudicated here, counted (3)

- [MEANING] LLR-045 `Detail` -> schedule N reviewer sessions for a declared review policy of N, fail preflight on a broken prompt map, keep legacy behaviour when the enable-list is absent — and NOTHING about where the queued phase list comes from, so a scheduler that derived its own phases (or defaulted an unnamed list to the full declared span) satisfied the row -> the same, PLUS a positive constraint on that list: the queued phases are ALWAYS NAMED BY THE CALLER and NEVER DEFAULTED, a fresh round naming the declared span and a resume naming exactly the phases the branch's committed evidence still owes AT THE GOVERNING IDENTITY, an EMPTY list being an EMPTY round rather than a full one, and the untracked owed-round marker contributing ADVISORY FIELDS ONLY, never a round -> an implementation correct under the old text — `phases=None` falling back to the declared set, which is what this scheduler demonstrably used to do — is DEFECTIVE under the new one, and the empty-list clause reverses the answer in the one case (`[]`) where a falsey-defaulting implementation would queue a full round. Obligations added, not restated. Verified: `RoutingState.schedule_review_round(self, phases)` has no default (`project-trajectory/scripts/agent_loop.py:1205`), the body is an unconditional `self.review_queue = list(phases)` with no truthiness test (`:1227`), the fresh arm passes `kverdict.declared_phases(ctx.rp_int)` (`:2751`) and the resume arm passes `review_owed_by_evidence(...)` derived through `kverdict.governing_identity` / `branch_entries` / `phases_owed` (`:3452-3464`, `:3528`, `:3547`); the marker (`read_review_owed`) contributes only `base` and `family` (`:3529-3544`) and never an OR-arm into `owed`. No call site anywhere relies on an implicit list.
- [MEANING] TC-082 `Method` -> run the review-policy 0/1/2, prompt-map, redaction, selection-logging, verdict and unmanaged cases; the phase list is not a subject of the test at all -> the same, PLUS the phases driven AS A REQUIRED ARGUMENT across four named cases — fresh span, named owed subset, empty list queuing an EMPTY round, and OMITTING the argument RAISING — so that "the evidence owes nothing" and "the caller named nothing" cannot share one value -> a suite passing the old Method is silent on every one of those four, and the omission-raises case in particular can only pass against an implementation that has no default. The test's obligation moved with its parent's; this is the acceptance half of the same change. Verified: `tests/test_agent_loop_routing.py:273` `test_routingstate_schedule_review_round_by_policy` drives the fresh span (`:280`, `:284-287`), the named owed subset (`:296-297`), the empty list (`:304-305`) and `pytest.raises(TypeError)` on the zero-arg call (`:306-307`). That node is already on this row's `evidence` cell.
- [MEANING] LLR-140 `Detail` -> a verdict gate keyed to `review_rounds`, admitting a verdict via `score_reviews.parse_verdict` under a RECENCY/ORDERING rule — "the verdict's last branch commit required no older than the last non-review non-fragment commit" — with no statement about which round files count, no adjudication-owed question, no spec-copy precedence, no bound on the legacy hand-authored rollup, and no trailer cross-check -> a gate computed over THE BRANCH'S OWN round files, RESTRICTED to rounds a LOGGED reviewer session produced, and governed by TREE IDENTITY — a verdict counts only while it names the branch's current non-record tree at the work tip, with NO ordering rule and NO time comparison at all; PLUS whether an adjudication lane owes a verdict being `[attestation] adjudication_review` read through the ONE function the loop's round scheduler also reads, over the SAME input by a single declared spec-home precedence (terminal first); PLUS the legacy hand-authored `docs/reviews/WI-<n>-REVIEW-A.md` clearing the gate under that same identity rule, with a WARN, at a declared count of ONE ONLY; PLUS a trailer cross-check over the newest attestation at the tree under judgement, refusing on a differing verdict word or a count ABOVE the evidence and never on one below -> the admission rule is REPLACED, not reworded: a verdict that was fresh-enough under the old recency test but names a stale tree now fails, and a verdict older than the last work commit but naming the current tree now passes — the two texts admit different sets. Four further obligations exist only in the new text, each independently failable: a stale-tree round, a round file with no logged session, a hand-authored rollup at policy 2, and an over-stated trailer are all merges the old text permits and the new one refuses. Verified: `want = kverdict.governing_identity(root, branch)` and equality-only binding (`project-trajectory/scripts/integrate.py:1370`; `kitlib/verdict.py:653-657`), branch-scoped `base..branch` paths (`verdict.py:548-557`), the logged-session restriction discarding the filename's phase (`verdict.py:573-620`), the shared dial reader `agent_common.adjudication_review_owed` called by both `integrate._verdict_owed` (`integrate.py:1235`) and `agent_loop.schedule_adjudication_round` (`agent_loop.py:2816`), the one declared precedence `SPEC_HOMES` / `authoritative_spec` (`agent_common.py:1060-1090`) asked for by both callers (`integrate.py:1193-1197`, `agent_loop.py:2777-2780`), the legacy arm gated on `required == 1` with the same identity check and a stderr WARN (`integrate.py:1391-1396`, `1244-1289`), and the trailer's strict `stamped[1] > evidence_count` (`integrate.py:1443-1451`).

All three in-scope rows are MEANING, so §A5.2's "flip back to Approved" arm does
not apply to any of them; each row's `Status` is `Approved` on both sides and
stays untouched. No registry cell was edited by this session.

### The new text is text I would bless

Every claim above holds against the tree at `d202c9f3`. Two observations that do
NOT falsify a cell and therefore raise no `## Dispositions` draft, recorded so
the next reader does not have to re-derive them:

- `integrate._last_commit_time` (`integrate.py:1163-1167`) is the old recency
  rule's helper and still exists. A repo-wide grep finds NO caller: it is dead
  residue, not a live second rule, so the cell's "no ordering rule and no time
  comparison" is true of the gate.
- The declared precedence is HOME-level (`SPEC_HOMES = ("docs/archive/work",
  "docs/work")`), with a plain path sort inside a home. This repo carries
  terminal folders in BOTH homes (`docs/archive/work/complete` and
  `docs/work/complete`, six specs), so "terminal first" is guaranteed by the
  archive rank rather than by a terminal-vs-active rule, and inside `docs/work`
  an `active/` copy would sort ahead of a `complete/` one. The cell's
  load-bearing claim — ONE declared precedence both callers ask for, so the
  scheduler and the gate cannot be handed different drafts — holds exactly, and
  the gate reads the branch's own tree, where the close ritual has already
  moved the spec. Named as a narrow edge, not a defect in the row.

### THE RE-ANCHOR IS BLOCKED, and I did not work around it

The rung is released (`docs/process.toml` `human_approval_through =
"DevStg-Needs"` — only the Needs rung is human-held; SR/LLR/TC approval and
amendment proceed under ordinary review), so the re-attestation is this
session's to take. I ran the prescribed act, naming ONLY the two registries whose
rows I ruled on:

```
python3 project-trajectory/scripts/intake.py snapshot \
  --approves "low-level-requirements.toml=LLR-045/LLR-140 (WI-585 adjudication, MEANING rows=3);test-cases.toml=TC-082 (WI-585 adjudication, MEANING rows=3)"
```

It REFUSED, and every row in the refusal is a row I did not judge — both
registries I named are muted, and `system-requirements.toml` alone blocks:

```
baseline_snapshot: REFUSED — this refresh would ABSORB approved text into the
record of what a human blessed, and nothing in this working tree authorises it:
  docs/requirements/system-requirements.toml SR-024: Rationale
  … (+12 more row(s))
```

The measured ledger (`baseline_snapshot.refresh_ledger`) at this commit:

| registry | absorbed rows | flips |
|---|---|---|
| `docs/requirements/system-requirements.toml` | 17 | none |
| `docs/requirements/low-level-requirements.toml` | 9 | none |
| `docs/test/test-cases.toml` | 4 | none |
| interfaces / external / components | 0 | none |

This is WI-578's finding reproduced at a sharper point. `copy_live` is SCOPED
(`_authorised_registries`; an untouched registry is not written), while
`refresh_refusal` builds `blocked` from the WHOLE ledger
(`baseline_snapshot.py:633-637`) and so judges registries the refresh would not
write a byte of. Naming BOTH of my registries removes them from the refusal and
leaves exactly the 17 SR `Rationale` cells — WI-547's CLARITY verdict, which by
rule "owes nothing further", so nothing will EVER authorise them and the block
is permanent by construction, not transient.

I will not name `system-requirements.toml`. Doing so would record in the
snapshot's own prose stamp that WI-585 authorised seventeen cells it never
judged — the exact false claim this rung exists to prevent, and a worse one than
the drift it would clear. The tree is unchanged: the refusal raises before any
copy, and `git status` is clean after the run.

**No new `## Dispositions` draft.** The contradiction is already ruled-and-
queued as `WI-584` ("The snapshot's scoped writer and unscoped refusal disagree
on registry scope", `docs/work/queued/`, `safety_class = "spine"`, rank 0,
exclusive), drafted by WI-578 and minted at its merge. Its `## Context` already
names the successor condition: once WI-584 lands and the act is takeable, the
trunk-side amendment-adjudication rung takes the anchor. Drafting a second row
for the same defect would mint a duplicate and, under `adjudication_review =
"when-minting"`, arm a review round to carry it. What this verdict adds to
WI-584's record is the two rows above: `LLR-045` and `LLR-140` are re-driven,
blessable and owed on `low-level-requirements.toml`, and `TC-082` extends the
same condition to `docs/test/test-cases.toml`, which WI-584's context does not
yet name as a registry with a blessable, owed re-anchor of its own.

Until then `LLR-045`, `LLR-140` and `TC-082` stay drifted — visibly, on the
re-attestation surfaces (`trace.reattest_model` -> `gen_open_items.py`), and on
a loop-side surface, since this rung is released and no human signature is
pending on it.

## Restatement, excluded from the count (29)

Reproduced because they are in the drift set I was shown, not because they are
adjudicated here. I read each independently before checking whose verdict owns
it, and I concur with every one.

**Closed by WI-547 as CLARITY (17)** — SR-024, SR-033, SR-043, SR-052, SR-053,
SR-054, SR-111, SR-112, SR-129, SR-144, SR-146, SR-147, SR-149, SR-167, SR-175,
SR-176, SR-177, all `Rationale`. Every one is the removal of the `Hat-derived
(hat.X):` provenance label (de-tokenised rather than deleted at SR-175) and, at
SR-111 and SR-112, of the trailing sentence those cells themselves declared
removable ("the sentence above stands without the citation"). The token is now
absent from the live SR registry entirely — 0 hits live against 17 in the
anchor — so this is a registry-wide vocabulary retirement, a term made
consistent with the rest of the registry. No clause id is lost that the cell
does not still carry (C-DPR-2, C-PRF-1, C-MNT-3, C-SEC-2, C-SEC-5 all survive
in the surviving prose); no behaviour, limit, actor, scope or acceptance
condition moves; a builder or a test acting correctly on the old text acts
identically on the new.

**Closed by WI-566 as MEANING (6)** — LLR-058 `Detail`, LLR-144 `Detail`,
LLR-198 `Detail`, TC-138 `Method`, TC-147 `Method`, TC-194 `Method`; all turn on
the WI-553 retirement of the `queued`+`blockref` shape for the terminal
`partial/` move (the exclusion class, the anti-livelock property, the dropped
`blocked_pending` source and the three surviving re-exports).

**Closed by WI-573 as MEANING (1)** — LLR-136 `Detail`.

**Closed by WI-578 as MEANING (3)** — LLR-158 `Detail`, LLR-203
`Detail`/`Rationale`/`Title`, LLR-204 `Detail`.

**Not amendments of approved text (2)** — TC-199 and TC-200 are `Drafted` in
`docs/test/test-cases.toml`, so they carry no attestation for this rung to keep
and do not appear in the ledger's absorbed set. Their `Expected`/`Method`
narrowing is not adjudicable here.

VERDICT: MEANING rows=3
