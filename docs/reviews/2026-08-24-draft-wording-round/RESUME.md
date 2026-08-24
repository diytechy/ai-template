# Adjudication - the wording round on the approval-pending Drafted spine text

Every suggestion the cross-family reviewer returned is dispositioned below.
**38 suggestions over 19 rows: 21 ACCEPTED (5 of them amended), 17 REJECTED.**
The reviewable population fell from **29,441 to 25,564 characters (-13.2%)**,
with the nine LLR titles down 28-67% and the seven re-worded LLR `Detail` cells
down 10-42%.

- Provider: **`OPENAI-TERRA`** - `gpt-5.6-terra` via `codex exec`, the OpenAI
  row `docs/agents.toml` declares and `docs/agents-enabled` lists. No
  substitution: the owner asked for "openai terra" and that entry exists.
  Probed live before dispatch.
- Brief and batching: [BRIEF.md](BRIEF.md). Raw returns:
  [1](RAW-BATCH1-LLR-A.md) · [2](RAW-BATCH2-LLR-B.md) ·
  [3](RAW-BATCH3-TC-A.md) · [4](RAW-BATCH4-TC-B.md).
- Editable population: the **19 `Drafted` rows only**. They carry no approval,
  so re-wording them needs no warrant. The nine anchor SRs are `Approved` and
  were sent as intent context only; `LLR-041` is `Approved` with a drifted
  `Detail` cell and was likewise not touched (see "Findings for the owner").
- Acceptance gate for every accepted text: `trace.py --strict-integrity`
  unchanged at **integrity=0, provenance-findings=1** (the pre-existing
  `LLR-197`) and **paraphrase-advisories=3** (the pre-existing `LLR-007`,
  `LLR-020`, `LLR-027`). Shortening a child `Detail` raises its lexical overlap
  with the parent, so the paraphrase count was the specific number watched: it
  did not move.

## The three rejection classes, stated once

Fourteen of the seventeen rejections fall into three classes rather than
seventeen separate judgements.

1. **Every `Expected` suggestion made the cell heavier (10 rejections).** The
   registry's 181 test rows carry a one-line pointer - `Satisfies the acceptance
   folded into LLR-nnn (parent SR-nnn)` - and the reviewer replaced each with a
   400-600 character restatement of its own `Method`. That is the opposite of
   what the owner asked for, it duplicates the cell beside it, and it would
   leave 19 rows written in a form the other 162 are not.
2. **A suggestion that asserts a test the row does not run (5 rejections).**
   The reviewer was given each row's anchor SR and repeatedly promoted the SR's
   *acceptance criteria* into the `Method` as though they were executed steps -
   a network-disabled fetch assertion and a missing-source-registry case in
   `TC-195`, launcher presence / one-step / execute-bit / "invites reuse" cases
   in `TC-188`, a `Critique` verification case and a literal 50-line composer
   span in `TC-197`. None appears in the row's `Evidence` list. A test case that
   claims coverage it does not have is the exact defect this spine's checks
   exist to catch, so these were refused whole rather than trimmed.
3. **A suggestion that contradicts the design row it verifies (1 rejection,
   and the sharpest).** `TC-182`'s rewrite adds "two joined seams with
   incompatible signal types" as a driven case. `LLR-187` - the row `TC-182`
   verifies - states in terms that the clause **has no executable form**: the
   carriage cell is the tier's only seam-to-seam edge and carries no signal
   vocabulary. Accepting it would have written a test for machinery that does
   not exist, over the design row's own explicit statement that it cannot.

The remaining three rejections are per-row and recorded in the table.

## The ledger

`old -> new` is characters. "amended" means the reviewer's text was taken with
a stated correction to its CONTENT; the amendment is spelled out in the reason.
Every accepted text was additionally normalized to house punctuation (ASCII
hyphens for the reviewer's double-hyphen dashes, straight quotes) and to the
emphatic capitals the row already used; that normalization changes no claim and
is not counted as an amendment.

### LLR `Title` - all nine ACCEPTED

The house convention was measurable and it argued for the reviewer: over the
**175 approved LLR rows the title median is 36 characters**, 146 are under 60
and only 4 reach 90. The nine `Drafted` titles ran 63-137, six of them at or
above 90. The shortening restores the convention rather than breaking it.

| Row | old -> new | disposition |
|---|---|---|
| LLR-187 | 137 -> 51 | ACCEPTED - "Frame-reference resolver and interface-cell checker" names both delivered mechanisms; the severity split it drops is a `Detail` fact, not a name. |
| LLR-193 | 109 -> 41 | ACCEPTED - "Loop-resume launcher interpreter selector" keeps "loop-resume", so the title still does not imply the environment-preparation half is delivered. |
| LLR-194 | 113 -> 48 | ACCEPTED (amended) - the reviewer's "SN scope schema-tier validation seam" reads as though an SN check exists, a risk it flagged itself; taken as "Scope's schema-tier seam, not yet extended to SN", which keeps the negative. |
| LLR-196 | 90 -> 55 | ACCEPTED - "unaggregated" carries the build gap into the title. |
| LLR-198 | 75 -> 54 | ACCEPTED - names the read model and the shim, which is what the row delivers. |
| LLR-199 | 100 -> 47 | ACCEPTED - drops "the approval it may never carry"; the no-approval rule survives in `Detail` as an observable. |
| LLR-200 | 63 -> 33 | ACCEPTED - accurate and the shortest honest name. |
| LLR-201 | 82 -> 51 | ACCEPTED - keeps the below-the-engine siting, which is the row's decomposition choice. |
| LLR-202 | 95 -> 31 | ACCEPTED - "Staged Hat-Refs amendment guard" is the mechanism exactly. |

### LLR `Detail` - seven ACCEPTED, two REJECTED

| Row | old -> new | disposition |
|---|---|---|
| LLR-187 | 2502 -> 1441 | ACCEPTED. Every guard survives: the FAILURE severity, the vacuity guard **with** its false-green reason, the HARD/advisory split, "one advisory each and never gate", the interface-cell ownership boundary, the NOT DISCHARGED seam-join clause and the cross-side residual. What went is one analogy and the restated obligation. |
| LLR-193 | 1796 -> 1542 | ACCEPTED (amended). The reviewer dropped "so the front door reports clearly instead of dying deep inside the engine at an obscure import" - that clause is the row's link to its parent's "does not crash cryptically" acceptance, so it was restored. Everything else taken. |
| LLR-194 | 1019 -> 802 | ACCEPTED (amended). The reviewer **invented** a sentence describing what the future SN entries would require and which registries the extension would scan - decisions this row has not made. Dropped; the two failure classes, the closed-vocabulary shape and every NOT DISCHARGED clause were taken as offered. |
| LLR-196 | 1393 -> 1122 | ACCEPTED (amended). The reviewer added a closing sentence importing SR-177's own "reported and never gated, no declared improvement target" contract into the child. Correct as a fact, wrong as a home - it is the parent's obligation and re-stating it in the child is the paraphrase this tier is checked against. Dropped; the compression of the telemetry columns and the grouping gap was taken. |
| LLR-198 | 1713 -> 1535 | ACCEPTED. All three sources, the fail-closed pause, the typed model, `pending_block`/`owner_cards`, the three consumers, the re-export shim and the byte-identity claim all survive. |
| LLR-199 | 2370 -> 1730 | ACCEPTED (amended). Two clauses restored over the reviewer's cut because they are the row's guards, not its rhetoric: "and that judgement has no place in shipped machinery" on the unplaced edge, and "so the view never implies exclusive ownership" on the shared edge. `NO APPROVAL CELL APPEARS, EVER` kept in the emphatic form. |
| LLR-202 | 2015 -> 1621 | ACCEPTED. The cell-class comparison, the structural tier scope, both vacuities, warn-first-never-an-exit-code and the whole NOT DISCHARGED paragraph survive; what went is a citation of the ruling the baseline decision rode, which a living cell must not carry anyway. |
| LLR-200 | REJECTED | The rewrite opens "traj_parse.frame_context inserts the declared external frame above derived structure" - it does not. `frame_context` is the read model; this row's `Module` is `traj_context.py` and its symbol is `context_block`, which renders and splices. A misattributed mechanism for a 10% saving. |
| LLR-201 | REJECTED | Two defects. It inverts the siting - "Module beneath the engine **composes** every checker rule" - when the point of the row is that the module HOLDS the rules and the engine composes them; and it imports the parent's whole strict/advisory gating contract into the child. Saving was 15%. |

### TC `Method` - five ACCEPTED, five REJECTED

| Row | old -> new | disposition |
|---|---|---|
| TC-189 | 789 -> 713 | ACCEPTED. Both behaviours, the "IF today because no SN entry exists" scoping and the `--strict-schema`/`--strict` split all survive. |
| TC-191 | 888 -> 850 | ACCEPTED. Small saving, nothing lost - including the clause that no test here exercises the lanes grouping, which is what stops this case reading as coverage of the report. |
| TC-192 | 994 -> 816 | ACCEPTED. The four named tests survive by name; what went is three parenthetical asides. |
| TC-194 | 1206 -> 1154 | ACCEPTED. Faithful: both claims, the fail-closed malformed pause, the function-body import graph, and the IF-138 loader arm. |
| TC-198 | 1111 -> 1046 | ACCEPTED. Faithful across all five cases, including both vacuity shapes and the tier-scoping case. |
| TC-182 | REJECTED | Rejection class 3 above - it drives a seam-signal-compatibility case that `LLR-187` states has no executable form. |
| TC-188 | REJECTED | Rejection class 2 - imports SR-160's acceptance (root presence, one-step launch, the Linux execute-bit step, the guide "invites reuse") into a case whose eleven cases and `Evidence` are all interpreter selection. |
| TC-195 | REJECTED | Rejection class 2 - adds a network-disabled fetch assertion and a missing-source-registry case that no listed test runs. |
| TC-196 | REJECTED | Misreads the row: "the three tiers come back id-ordered" means the frame's entities, crossings and relationships, and the rewrite renders it "reads return SR, LLR, and TC in id order". Wrong subject. |
| TC-197 | REJECTED | Rejection class 2 - invents a `Critique`-plus-unknown-verification case, and turns the row's "measured line span" into a literal 50-line claim the row never made. |

### TC `Expected` - all ten REJECTED

`TC-182`, `TC-188`, `TC-189`, `TC-191`, `TC-192`, `TC-194`, `TC-195`, `TC-196`,
`TC-197`, `TC-198` - rejection class 1 above, one reason for all ten.

## Findings for the owner - not applied, because the text is APPROVED

Nothing in this round touched an approved cell. Two things surfaced that are
the owner's to weigh rather than a worker's to edit:

1. **The reviewer's `CUT-REDUNDANT` lines repeatedly point at the anchor SR,
   not at the child.** On seven of the nine LLR rows its answer to "what would
   you cut" was some form of "the general contract - the parent already states
   it". That is the reviewer independently reporting that the SR tier and the
   LLR tier overlap on these chains. Nothing was cut from an SR on that basis.
   If the owner wants that overlap acted on, it is a decomposition question at
   the requirement tier, not a wording pass.
2. **`LLR-041`'s drifted `Detail` was left alone.** The row is `Approved` and
   its amendment is 322 characters that already read plainly, so no
   simplification was sought and none is proposed. It stays on the owner's
   brief exactly as it was.

Neither needs a ruling to proceed, so neither was filed as an open item.

## What did NOT change

No `Status` cell moved. Nothing was approved. The snapshot under
`docs/archive/last_approved` was not re-seeded. The nineteen rows are still
`Drafted` and still owe the owner's act - they are only shorter to read.
