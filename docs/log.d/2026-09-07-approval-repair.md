## 2026-09-07 — Exclusive primary approval repair and preserved-lane migration

Preparation for the existing bounded control retry; no control coordinator has
been launched in this repair session. The tracked pause remains. No push or
merge to main is authorized or performed. The control still carries zero
completions and 3050.255 active seconds from its earlier segments.
<!-- fig: derived="CONTROL-RETRY.md recorded segments: 1871.909 + 1178.346 = 3050.255 seconds; zero completions" rev=7ded8e5f -->

The authoring/judgment boundary preceded implementation. The separately
reviewed [repair contract](../ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md)
and immutable design/live-cell review artifacts record the exact LLR/TC
wording, stable-ID meaning rule and finite RETURN/reanchor path. Those reviews
approve neither the disputed preserved cells nor a live snapshot. Module and
CodeSymbol bindings subsequently describe the actual implementation.
The [Markdown reader binding](../reviews/2026-09-07-if077-binding-luna.md)
records the final cross-component call without granting artifact approval.

The runtime now separates immutable primary turn bindings, read-only approval
projection, queued close staging and publication. The existing session engine
runs in process while the coordinator holds its exclusive writer slot. The
publisher independently replays the exact candidate into a disposable checkout,
checks the proposed tree and records the decision-bound author, scope check and
publication identity. Snapshot metadata binds the candidate date, so later
replay is deterministic. A failed commit hook restores the exact candidate.
All WI branches refuse approval/snapshot writes; governing implementation
changes hand back to exclusive spine authoring. RETURN accepts zero cells and
can mint the explicitly reviewed correction/reanchor successors atomically.

[The supervisor migration](../reviews/2026-09-07-WI-605-supervisor-migration.md)
moves the same interrupted adjudication to queued primary ownership, with its
three exact scoped IDs. Its old branch/worktree and forensic patch remain
unchanged. The adjacent amendment and first-approval specs carry their actual
typed scopes and the publisher boundary; the dependency on the preserved
judgment remains. The absorption work's existing owner remains the same.
It stays queued: prior-verdict/UNJUDGED rendering in the brief and absorption
history consumption by the rollup/intake remain its obligations. The new
publication ledger does not silently close that broader work.

The first broad diagnostic produced 58 failures, 3643 passes and 22 skips in
797.00 seconds. Many failures were the source-restart guard correctly noticing
edits during that diagnostic run. Others exposed actual import cycles, obsolete
adjudication-claim fixtures, stale generated artifacts and missing bindings.
This is diagnostic evidence, not the final verification of the repair.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=7ded8e5f+approval-repair-diagnostic; out/run-logs/approval-repair-full-diagnostic.txt -->

The next full run completed with 3724 passes, 22 skips and six failures in
854.97 seconds. Four dispatcher fixtures omitted the new in-process primary
session callback; two harness-selection fixtures patched the former module
owner after extraction. These were migrated with their behavioral
assertions retained. A separate real-scaffold adversarial test exposed a
direct-publication bypass from a linked checkout; the writer now invokes the
existing primary identity validator before deriving or installing any tree.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=7ded8e5f+approval-repair-stable; out/run-logs/approval-repair-full-stable.txt -->

Decomposition removed the new import cycles without changing their empty
baseline. The lower verdict library has no import of a session or publication
writer. The unused publication-peel callback was removed after review; the ordinary
lane reader peels only its verified refresh. Publication completion uses its
separate exact verifier. Shared close and bar implementations moved out of the integrator;
they are not duplicated wrappers around an old workflow.

The existing large-module census, from the session's initial committed
baseline to this repair, is agent_common 1473 → 1459 (-14), agent_loop
2704 → 2731 (+27), bootstrap 1665 → 1677 (+12), intake 1453 → 1455 (+2),
integrate 1421 → 1358 (-63): net -36 SLOC. The increases are the session engine's
primary callback, completion/provenance adapter, shipped-file manifest and
stage-only mint option. The extracted operations stay below the module limit;
new functions retain the existing complexity ceiling. These are deliberate
exact restamps, with no headroom added to a complexity or cycle baseline.
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_module_size_ratchet.py tests/test_import_layers.py tests/test_complexity_ratchet.py" rev=7ded8e5f+approval-repair; out/run-logs/approval-ratchets-restamped.txt; baseline diff in tests/test_module_size_ratchet.py -->

Four new subprocess-heavy primary integration modules run in Full/CI: they
exercise real Git histories, clones, hooks and exact publication replay. Their
initial 23-case run took 9.12 seconds alone. The per-commit smoke test-count
ceiling and 90-second wall budget remain unchanged.

Budgeted byte deltas: PROCESS.md 89406 → 89355 (-51); PROCESS_OPTIONS.md
189535 → 190517 (+982); byte-budget-guard/SKILL.md 4594 → 4511 (-83).
The method replaces model-side approval with primary publication; the options
carry its stable-meaning and evidence contract. The capped guide stays at
9980 bytes and CLAUDE.md at 8009 bytes. All capped files remain below their
existing limits; the skill's mirrored baselines were restamped exactly.
<!-- fig: cmd="wc -c project-trajectory/AGENTS.template.md CLAUDE.md project-trajectory/PROCESS.md project-trajectory/PROCESS_OPTIONS.md project-trajectory/skills/byte-budget-guard/SKILL.md" rev=7ded8e5f+approval-repair; before sizes from git show 7ded8e5f:path -->

The [independent runtime review](../reviews/2026-09-07-approval-runtime-opus.md)
requested changes. The [dispositions](../reviews/2026-09-07-approval-runtime-dispositions.md)
record the exact-target copier, cached immutable proofs, current-judgment close,
optional telemetry and publication boundary fixes, plus the explicit dirty
staging recovery limit. The second frozen review manifest is
`26afd9f9e1fa1eff02216bf771972fc30dc5b21d14236ea97823cc617447d2ae`.

The [independent runtime follow-up](../reviews/2026-09-07-approval-runtime-opus-followup.md)
approved the repair with stated operational limits. A supervisor manifest
comparison found no altered files in its frozen copy. The isolated review
snapshot manifest is retained under out/run-logs; review and
repair costs are preparation, outside the measured control envelope. Launch
remains contingent on completing the checks, review and fresh preflight.

The reviewed-source full run completed with 3733 passes, 22 skips and two
failures in 780.26 seconds, both stale generated prompt-catalogue checks.
The catalogue was regenerated without changing runtime/template source; the
two affected test modules then passed all 31 tests in 17.28 seconds.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=7ded8e5f+frozen-26afd9f9; out/run-logs/approval-repair-full-final.txt -->
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_generated_freshness_wiring.py tests/test_routing_and_prompts.py" rev=7ded8e5f+catalog-regenerated; out/run-logs/approval-catalog-fix.txt -->

The final catalogue-corrected full suite passed: 3735 passed, 22 skipped in
785.31 seconds. This is the full verification of the broad runtime repair.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=7ded8e5f+catalog-final; out/run-logs/approval-repair-full-catalog-final.txt -->

A subsequent synthetic regression proved that the shared spec mover could read,
rewrite and stage an owner-only Markdown file during close. The final two-line
fix excludes the existing shared owner-only paths before content access. The
actual owner scratchpad was never opened. The strengthened test failed on the
read before the fix; the mover, primary publication and structural ratchets
then passed 39 tests in 32.34 seconds. This last bounded change is covered by
that targeted run and the fresh commit bar, not by the preceding full run.
[Luna's independent review](../reviews/2026-09-07-owner-relink-luna.md) approves
these exact source/test bytes. No privacy policy, module limit or check was
weakened to pass.
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_spec_move.py tests/test_primary_publication.py tests/test_module_size_ratchet.py tests/test_import_layers.py tests/test_complexity_ratchet.py" rev=7ded8e5f+owner-exclusion; out/run-logs/approval-owner-relink-green.txt; red proof out/run-logs/approval-owner-relink-red-read.txt -->

Final commit bar after the owner exclusion: smoke 1694 passed, 4 skipped in
49.64 seconds; enforcing smoke 1694 passed, 4 skipped in 49.67 seconds,
49.9-second wall against the unchanged 90-second budget. Documentation check:
1494 documents, 2388 links, zero broken and one pre-existing orphan warning.
Ruff passes. The strict trajectory check is clean with its standing title
warnings. The generated dashboard retains its generator's whitespace on the
empty active-row line; other changed files pass `git diff --check`.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=7ded8e5f+owner-exclusion; out/run-logs/approval-owner-smoke-commit.txt -->
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=7ded8e5f+owner-exclusion; out/run-logs/approval-owner-smoke-budget-commit.txt -->
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=7ded8e5f+owner-exclusion; out/run-logs/approval-owner-docs-commit.txt -->

The first hooks-enabled commit attempt was refused by the formatting check
on publication_verify.py. Ruff's correction changes only formatting; an AST
comparison against the staged reviewed source is identical. The rejection is
retained in out/run-logs/approval-repair-commit.txt. The commit bar is rerun
on the formatted tree before the next attempt: smoke 1694 passed, 4 skipped
in 59.39 seconds; enforcing smoke 1694 passed, 4 skipped in 54.94 seconds,
55.3-second wall against 90 seconds. The docs result remains 1494 documents,
2388 links, zero broken and one pre-existing orphan warning.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=7ded8e5f+formatted-final; out/run-logs/approval-formatted-smoke-commit.txt -->
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=7ded8e5f+formatted-final; out/run-logs/approval-formatted-smoke-budget-commit.txt -->
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=7ded8e5f+formatted-final; out/run-logs/approval-formatted-docs-commit.txt -->

Deferred open items: none — no new owner decision is requested; existing
queued absorption work and review follow-ups remain separately recorded.
