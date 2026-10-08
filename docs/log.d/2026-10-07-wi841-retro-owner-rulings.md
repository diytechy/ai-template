Deferred open items: OI-110 — pending only the owner's confirmation of option (b)

## 2026-10-07 — Owner rulings from the WI-841 retrospective

A retrospective of the WI-841 lane
([spec](../archive/work/complete/WI-841-done-when-blessed-in-lane.md)) asked
why it took as long as it did. Two causes were found:
- Code and spine work alternated, so every code fix re-opened rows and owed
  another sitting.
- The coordinator's hand path has become a second copy of the loop's cycle.
  It writes its own prompts, runs no plan, critique or findings gate, and its
  procedure lives in a chain of handoffs.

The working proposal, the skill drafts and their reviews are in
[`../plans/2026-10-07-wi841-retro/`](../plans/2026-10-07-wi841-retro/README.md).
The owner ruled:

1. **Spine editing stays in the lane.** The fix is the order inside it: rows
   are drafted once, the code iterates, and the rows are reconciled and judged
   at checkpoints. Rows are not re-sat after every code round.
2. **Scope is settled where a row is born**, filed by hand or minted from a
   lane, by a scope critique. There is no lane-size tripwire: size can be
   derived after a lane lands, and a large row may be kept whole on purpose.
3. **A spine grows in three modes.**
   - From the vision, tier by tier.
   - In a lane on released rungs: one connected change set, authored whole and
     judged in one sitting. It must be closed: every edge present, every arm a
     parent states verified.
   - In a lane touching a held rung: the set splits at the dial.
   A spine is decomposed consistently in all three.
4. **A child is approved only after its parent.** No check enforces this yet.
   LLR-281 and TC-291 are Approved under SR-224, which is still `Drafted`.
5. **Held-rung rows are protected by state alone:** the live registry, the
   snapshot and the dial. The rule judges what lands from a lane. A held row
   whose snapshot moved to match changed text is refused unless the change was
   CLARITY, recorded in the verdict. A direct trunk approval by the owner or an
   authorized approver is not judged.
6. **The approval act is kit-wide in the lane.** An independent adjudicator
   may take the act in the authoring lane. This supersedes the trunk-side
   clause of the 2026-09-01 ruling. PROCESS.md and the merge slot do not say
   so yet: one row changes both, carrying the S11 plan's unbuilt approval-act
   rung change, so the doc never runs ahead of the check.
7. **The two-hour Codex relaxation stands.** After two hours unavailable, a
   fresh independent Opus reviewer may review, recorded as a same-family
   relaxation.
8. **The verdict rollup stays generated on trunk.** A lane never commits it.
9. **The coordinator's procedure moves into one this-repo skill,**
   `coordinator-cycle`. Handoffs go back to holding state only.
10. **One authoring model for spine text.** Terra, or another declared author
    role, does the first authoring pass, and the adjudicator passes judgement.
    The adjudicator never drafts the text it judges. This re-scopes WI-812,
    which followed the design's "the adjudicator drafts" (OI-101 Q1's drafting
    half; README changes 4 and 14, now annotated as superseded).

Four further questions surfaced by the queue reconciliation are filed as open
items, each cited by the row that waits on it:
- OI-108, the two-hour relaxation under `ask`'s per-kind routing (WI-801);
- OI-109, the rollup when the trunk step runs lane-side (WI-800, WI-807);
- OI-110, where the token-file dial lives (WI-846);
- OI-111, WI-811's final-review family rule.

Already landed: `bec70dc5` corrects PROCESS.md §4's description of the dial,
which still called it a 0–4 ordinal, to the `DevStg-*` rung it has been since
OI-21 shape (ii).

Rows for the next coordinator session to file, each with its own lane:
- the `coordinator-cycle` skill, and the `spine-authoring` lane modes;
- ruling 6: PROCESS.md, process-options "Who performs the approval act" and
  the `spine-authoring` preamble, together with the merge slot's
  approval-act rung, after which coordinator landings go through the slot;
- ruling 4: the parent-first approval check, with SR-224's chain settled
  first;
- ruling 5: the state-based held-rung check, retiring the trailer-armed
  `held-status` arm and the act-ledger CLARITY arm;
- the coordinator renders its review and critique briefs from the kit
  templates, with the untracked coordinator tools brought into the repo;
- `plan_coverage --findings` wired into rework, on both the loop and the
  coordinator path;
- the adjudication briefs compose `spine-authoring`'s tier questions at
  render time;
- the verdict rollup reads the coordinator's review files.

Later the same day the owner ruled five open items. Each ruling is written
into the rows that cite it, in the registry's verbatim form:
- **OI-106 (a):** SN-029's two cells as the adjudicator gave them, plus the two
  older staleness fixes (WI-827, landed on trunk by the owner's act).
- **OI-107 (b):** a decisions record is named by its work item; a decision tied
  to no work item takes the next number above the highest such decision. A
  decision watermark is the deferred cleaner option (WI-832).
- **OI-108:** no second relaxation. The coordinator's relaxation is the kit's
  one alternative-agent rule, the reviewer ladder that ends same-family and
  records it, in whatever form later rows give it (WI-801, cited by WI-811).
- **OI-109 (a):** under the station authority, the rollup the lane-side trunk
  step writes is trunk's (WI-800, WI-807).
- **OI-111 (a):** the final reviewer's family is a preference, never an
  author's session, yielding only by the alternative-agent rule (WI-811).

OI-110 stays pending. The owner prefers (b), an environment variable naming
the token file, and asked how the path is held today: it is in no tracked
file, only in the coordinator's local agent memory outside the repository.
