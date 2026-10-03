# TC-279 sample, round 2 — sampled new-reader inspection of DA-011, drawn at f2bc66c1

The round-2 sample record the [sampled new-reader inspection](../../test/inspection-procedures.md#sampled-new-reader-inspection)
asks for: the draw, and each reader's statement beside the part's linked
requirement and design rows, with the adjudicator's agreement ruling. The
verdict is [002-ADJUDICATE-f2bc66c.md](002-ADJUDICATE-f2bc66c.md). Rubric:
[sampled-new-reader](../../rubrics/sampled-new-reader.md), unchanged since
round 1 (anchors R1, R2, B1, B2). Round 1's sample, drawn from a defective
frame and recording no result, is [SAMPLE-f2bc66c.md](SAMPLE-f2bc66c.md); none
of its five parts recurs here.

## The draw

Taken by the unattended coordinator, not by any part's author. Judged by an
independent Claude Opus 5.5 adjudicator that directed none of it.

- **Population.** Every distinct (file, enclosing symbol) pair that the kit's
  own back-link harvest, `gen_arch_map.declaration_sites`, reports for a `.py`
  file under the readability roots `docs/stack.ini` `[paths]` declares
  (`src = project-trajectory/scripts`, `tests = tests`), the surface
  `[readability]` says it measures. A site with no enclosing symbol is keyed
  `<module header>`. **516 parts.** This is the frame round 1 said was owed.
- **Seed.** `int("f2bc66c12fc8b8702af6d93568ddba01dbb00278", 16)`, the trunk
  HEAD this lane was cut from, fixed by rule rather than chosen.
- **Draw.** The population sorted, then `random.Random(seed).sample(pop, 5)`.
- **Reproduced.** The adjudicator re-ran both scripts with that seed (the
  population at this lane's tip is identical: round 1 changed only `docs/`) and
  got both outputs exactly.

**Unrestricted draw (`draw_parts_v2.py`, population 516):**

1. `project-trajectory/scripts/gen_arch_map.py:2011` `MAPPING_FINDING_POLICY` → SR-163, LLR-276
2. `project-trajectory/scripts/session_service.py:469` `KeepWarmer` → SR-227, LLR-270
3. `tests/test_trajectory_arch.py:1494` `<module header>` → LLR-900, LLR-901
4. `project-trajectory/scripts/consolidate.py:1204` `close_refusal` → SR-220, LLR-210
5. `project-trajectory/scripts/gen_release_checklist.py:114` `_rejudge_checklist_line` → SR-215, LLR-255

**Restricted draw (`draw_parts_v3.py`, population 515, 1 dropped):** the same
seed over the sites naming at least one live SR/LLR/IF id. Picks 1, 2, 4 and 5
above, and in place of pick 3:

- `project-trajectory/scripts/rendering/traj_render.py:1001` `_render_drill` → SR-054, LLR-100

The coordinator stated this restriction AFTER seeing the unrestricted draw.

### Ruling on the restriction: the sample stands, on a different ground than the one stated

**Pick 3 is not a part.** Line 1494 of `tests/test_trajectory_arch.py` sits
inside `MOD_A_SRC`, a module-level string that is the source text of a
synthetic module a test writes to a temporary directory. The `Implements:`
there declares the back-link of that fixture's `method_a`, not of anything in
the test file. It names LLR-900 and LLR-901, which no registry holds.
`declaration_sites` scans lines, so it reports the hit, and it keys it to
`<module header>` because no def or class encloses the line. That is the only
site in that file, so the drawn key stands for no back-link. The procedure's
part is "one function, class or module-level block with its own back-link".
This key is a frame blank: an entry in the list that is not a member of the
population.

**Dropping a drawn blank and taking the next seeded draw is a population
rule, not a selection.** I checked what the restricted draw actually did. The
dropped key sorts last (index 515 of 516). The unrestricted stream's first six
draws, in order, are picks 1–5 above and then `_render_drill`. The restricted
draw is exactly that stream with pick 3 skipped. So the round-2 sample is what
a rule fixed before any draw would give: "draw in seeded order and skip a key
that is not a part". Under that rule the coordinator had no discretion. The
replacement is the next seeded draw, not a part anyone picked, and the four
parts that were already drawn did not move.

**The stated live-id criterion is NOT adopted as the population definition.**
It is a proxy that happens to drop only this one blank. It does not define a
back-link. The frame still holds fixture-string hits that name LIVE ids, and
the proxy keeps them:

- `tests/test_gen_arch_map.py` `<module header>`: line 580 is inside the
  `PROSE_MOD` fixture text, `Implements: SR-070, LLR-071`.
- `tests/test_gen_arch_map.py`
  `test_reverse_coverage_reads_non_python_source_but_not_unlisted_types`:
  lines 687 and 690 are string arguments written to fixture files.

Neither was drawn. Under the skip rule the sample is the same whatever else
the frame holds, because every one of picks 1, 2, 4, 5 and 6 is a genuine
back-linked part. I confirmed each one below: each part carries its own
`Implements:` line, in its docstring or as the comment directly above it.

**Not B2.** No author of a part chose any part. The post-hoc restriction
changed one draw, and only one way, to exactly the part that a pre-stated
skip-blank rule yields. The redraw that would have been correct, had I
rejected the restriction, is this same sample.

### Reader kind and procedure

Reader kind, all five: a fresh Claude Sonnet 5.5 session, told that it did not
author its part. Each read only the part's code and the rows its `Implements:`
names, and did not ask the author. Each read the rows **from the registry
files** (`docs/requirements/*.toml`), not "through the generated views" as the
procedure says. Ruling: this does not break R1. R1 requires a random part, a
fresh non-author reader, and the reader kind and statement recorded beside the
rows, and all of those hold. The views are generated from these same files, so
the readers read the same cells in their source form. Reading the raw rows
gives a reader no more help than the views would, so the deviation cannot have
produced the pass. It is a deviation from the procedure's letter, and it is
recorded here as one.

## The parts, the statements and the rows

The adjudicator read each part's code at `f2bc66c1` and each linked row from
the registry.

### 1. `project-trajectory/scripts/gen_arch_map.py:2011` `MAPPING_FINDING_POLICY`

- **Back-link:** `# Implements: SR-163, LLR-276`, the comment directly above
  the assignment (a module-level block).
- **Linked rows.**
  - SR-163: every shipped file maps to a requirement reaching a need, "with
    missing files, stale inventory entries, unresolved references and unmapped
    files reported under the declared warning-to-gating policy". Its
    acceptance criteria say "the declared policy assigns warn versus gate per
    class".
  - LLR-276 (CMP-006): "MAPPING_FINDING_POLICY maps missing_file and
    stale_entry to gate and unresolved_reference and unmapped_file to warn";
    the inventory fails exactly when a gate-class finding is present. The
    rationale is a table read in one place rather than branches spread through
    the checker. Missing and stale gate because each is a one-edit defect.
    Unmapped and unresolved warn because they are a burn-down, and gating them
    would force a flag day.
- **Statement (reader 1).**
  - What it does: a four-entry dict giving each coverage-finding class a
    severity. `missing_file` and `stale_entry` gate; `unresolved_reference` and
    `unmapped_file` warn. The checker beneath reads the table, and the
    inventory fails only on a gate-class finding. Moving a warn class to gate
    is a reviewed commit once that class reaches zero.
  - Why it exists: SR-163's declared warn-versus-gate policy. LLR-276 puts that
    decision in one table rather than in branches, so the unmapped and
    unresolved classes can burn down without a flag day.
  - Could not explain: what "OI-72, 2026-08-31" is, and whether the phrase "the
    SHIPPED default for unmapped stays warn-only" implies overrides elsewhere.
- **Ruling: AGREES.**
  - The mapping is exactly the code's.
  - "Fails only on a gate-class finding" is `mapping_purpose_report`'s
    `ok = not any(policy.get(cls, "warn") == "gate" ...)`.
  - The purpose is LLR-276's rationale nearly word for word.
  - Both open notes concern references outside the part: an open-item id, and
    the `policy=` parameter of the consumer, whose one call site, line 2267,
    passes the default. Neither is the part's behaviour or purpose.

### 2. `project-trajectory/scripts/session_service.py:469` `KeepWarmer`

- **Back-link:** `Implements: SR-227, LLR-270` in the class docstring.
- **Linked rows.**
  - SR-227: retained adjudicator sessions, and "make any keep-warm call one
    bounded turn that never blocks the scheduler". Its acceptance criteria add
    that a keep-warm call is recorded like any other call and never runs while
    another call holds the session.
  - LLR-270 (CMP-008), the KEEP-WARM clause:
    - built by `keep_warmer` only when `keepwarm_minutes` is on, and ticked
      once per dispatcher poll;
    - only routes whose adapter bounds a call to one turn are pinged;
    - `take_warm_lease`;
    - the ping (role KEEP-WARM, one turn, a 300 s wall) runs on its own thread
      through `act`, so the tick never waits;
    - one ping at a time, a due ping in flight skipped and said;
    - the log is committed by the dispatcher's thread, over a clean trunk only,
      else held;
    - at the run's end a ping is waited out and, over a dirty trunk, its log is
      not written and the reason is printed and returned.
    The rationale: off the dispatcher's thread so a slow ping cannot stall the
    merges, and the record on that thread so its commit is serialised with them.
- **Statement (reader 2).**
  - What it does:
    - the dispatcher-side one-turn keep-warm ping;
    - routes are chosen at construction (command buildable, one-turn adapter);
    - `tick` records a finished ping only over a clean trunk, else holds and
      says so; with none in flight it takes a warm lease and starts the ping
      on a daemon thread through `act`;
    - the thread only launches and accounts;
    - `_once` suppresses repeated messages;
    - `finish`, registered at exit, waits and then records, or returns "not
      recorded (trunk dirty)";
    - `keep_warmer` returns None unless both dials are on.
  - Why it exists: to keep a retained session's prompt cache warm without
    stalling the scheduler, racing an adjudication, or committing beside a
    merge or uncommitted work (SR-227, LLR-270).
  - Could not explain: helpers taken on trust. It noted that dirty-trunk logs
    are dropped rather than retried, "LLR-270 says so". It also read the
    `due_routes` call in the in-flight branch as a read-only check.
- **Ruling: AGREES.**
  - Every clause matches the code: the `bounds_one_turn` filter, the `tick`
    order, the `daemon=True` thread, `_ping` appending only, `_once`, and
    `finish` clearing over a dirty trunk.
  - Every clause matches LLR-270's keep-warm clause.
  - The `due_routes` reading is right: that branch takes no lease and only
    decides whether to say "skipped".

### 3. `project-trajectory/scripts/consolidate.py:1204` `close_refusal`

- **Back-link:** `Implements: SR-220, LLR-210` in the docstring. The function
  is defined at line 1160; 1204 is the back-link line.
- **Linked rows.**
  - SR-220's acceptance criteria:
    - "an outcome that moves an item no longer queued is refused, naming the
      item";
    - an absorbing outcome leaves each absorbed item naming "its one
      successor";
    - a set "never re-absorbs" an earlier enacted consolidation's successor.
  - LLR-210 (CMP-008):
    - "`parse_verdict` and `close_refusal` read the verdict's typed outcome
      block and refuse by name for any row it moves that is not queued";
    - the scope rides the typed `Adjudicates` cell, and the recursion guard
      the typed `Digests` cell;
    - a successor row neither seeds a cluster nor may be re-absorbed.
- **Statement (reader 3).**
  - What it does: decides, before the close writes anything, whether a
    consolidation verdict may be enacted, and returns a refusal or None.
    - It runs four rungs in a fixed order, first message wins:
      `_outcome_refusal`, `_scope_refusal`, `_queued_refusal`, `_drift_rung`.
    - It then returns `reabsorption_refusal`.
    - The six refusals: outcome and absorbed set agree; exactly one successor;
      every touched row in `Adjudicates` scope; `Digests` still match; every
      touched row still queued; reabsorption refused here.
    - Specific causes come before the generic drift so the message names the
      row.
  - Why it exists: SR-220's refusal by name, its one successor and its
    no-re-absorption rule; LLR-210 names this function as the pre-close gate.
  - Could not explain:
    - the rung helpers' full behaviour;
    - "unused-looking" `rows` and `where`;
    - the references "census guard", "plan §1.2/§1.5", "WI-572" and
      "first-approval sibling";
    - that LLR-210 does not spell out the digest or scope checks.
- **Ruling: AGREES.**
  - The order, the six refusals and the "order is the message" reason are the
    code's own.
  - The purpose is SR-220's acceptance and LLR-210's refuse-by-name clause.
  - The reader's note that LLR-210 does not detail the scope and digest rungs
    is accurate. LLR-210 names the `Adjudicates` and `Digests` cells but not
    these checks. It is an observation, not a contradiction.
  - One soft slip: `rows` and `where` are not unused, because the body forwards
    both to every rung and `rows` to `reabsorption_refusal`. The reader offered
    this as an uncertainty, not as a claim in its account, and it touches
    neither behaviour nor purpose.
  - The other open notes are external references.

### 4. `project-trajectory/scripts/gen_release_checklist.py:114` `_rejudge_checklist_line`

- **Back-link:** `Implements: SR-215, LLR-255` in the docstring (function at
  line 104).
- **Linked rows.**
  - SR-215: when a release is prepared, the harness files one re-judge item
    per due observation case.
  - LLR-255 (CMP-008): "Release and stage-gate preparation are a person's
    acts, so each is prompted where that person works. The release checklist,
    a view that may not import intake, carries a required item from
    _rejudge_checklist_line naming the release command and the count of
    observation cases due at the release checkpoint, read through rejudge's
    pure decision."
- **Statement (reader 4).**
  - What it does: builds one **Required** checkbox line naming
    `python scripts/intake.py rejudge --checkpoint release`, to be run with
    every item it files closed before sign-off, and the count from
    `rejudge.due_cases(root, "HEAD", checkpoint="release")`. On `RejudgeError`
    it says the count could not be read and why, never zero. It files nothing
    itself.
  - Why it exists: SR-215's release checkpoint. LLR-255 makes release
    preparation a person's act prompted on their checklist. The checklist may
    not import the mint, so it counts through rejudge's pure decision, and an
    unreadable count is stated rather than shown as zero.
  - Could not explain: nothing (`due_cases` and `RejudgeError` taken from the
    docstring and the rows).
- **Ruling: AGREES.** It matches the code exactly, and its purpose is
  LLR-255's checklist clause. The never-zero reason is in the docstring ("zero
  would read as nothing to re-judge").

### 5. `project-trajectory/scripts/rendering/traj_render.py:1001` `_render_drill`

- **Back-link:** `Implements: SR-054, LLR-100` in the docstring (function at
  line 995).
- **Linked rows.**
  - SR-054: dashboard usability; "revealing detail preserves the return path
    to the parent context".
  - LLR-100 (CMP-009), T3 core: "descending a container never replaces the
    view with no way back — the drill emits a declared breadcrumb nav (<nav
    class="crumbs"> with a data-root-crumb root label) whose crumb click
    TRUNCATES the trail to that ancestor, restoring the parent view". Its
    code symbols are `_render_drill/DRILL_SCRIPT`.
- **Statement (reader 5).**
  - What it does: builds one drill view's HTML:
    - each `(layer_id, svg)` is wrapped in a `.layer` div, with every non-root
      layer hidden;
    - an empty `nav.crumbs` with `aria-label="<root crumb> breadcrumb"`, which
      the script fills;
    - the root id and crumb in data attributes;
    - for the `when` and `sw` drills only, a trace bar and `data-focused-trace`;
    - then `DRILL_SCRIPT`.
  - Why it exists: SR-054 and LLR-100's never-without-a-way-back breadcrumb.
    It emits that markup and its controller, and the distinct aria-label
    keeps several breadcrumb landmarks apart.
  - Could not explain: `DRILL_SCRIPT`'s internals; why only `when` and `sw`
    get the trace bar; what `data-descend` does beyond the docstring.
- **Ruling: AGREES.**
  - The markup is described exactly. The purpose is LLR-100's, with the
    `nav.crumbs` and `data-root-crumb` named.
  - The aria-label reason is the code's own WI-312 comment.
  - `DRILL_SCRIPT` and `data-descend` lie outside the part.
  - The trace-bar question is the one note that concerns the part's own code.
    The reader stated the branch's BEHAVIOUR correctly, but not its reason. No
    row the part links gives that reason. No row I could find in the SR or LLR
    registries names the focused trace either: `DRILL_STYLE`'s trace rules cite
    LLR-285, which is about de-emphasis contrast, not about which drills trace.
    The reason for this one branch lives outside the part's records. That is a
    small instance of DA-011's Obstacle ("a part whose reason lives only in its
    author's head").
  - Ruled not B1. The reader said what the part does, the branch included, and
    why the part exists, and contradicted nothing. Surfaced as a finding in the
    verdict.

## Bound

This pass bounds discovery to these five parts. It says nothing about the
parts the sample did not reach (rubric intent, B2), and it does not settle
round 1's part 3. A person may still overrule that ruling and record `fail` on
round 1's sample.
