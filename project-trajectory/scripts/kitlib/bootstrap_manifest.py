#!/usr/bin/env python3
"""The portable-kit scaffold inventory and its normalized reader.

The manifest is one behavior decision: which kit sources become which adopter
paths, with an optional requirement reference. File generation, profile
selection, policy migration, and writes remain in ``bootstrap``.

Contracts: IF-262 — the interface seam this file declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-262: ``bootstrap`` imports and re-exports ``MAPPING`` and
``mapping_entries`` from this module. Consumers receive the ordered scaffold
inventory as source/destination/reference triples; this module performs no I/O
and imports no command-layer sibling.
"""

# (source relative to KIT, destination relative to --dest)
# Implements: SR-010, SR-191, SR-192, LLR-010, LLR-218
MAPPING = [
    # Agent guide: full content in AGENTS.md, thin stubs for tools that prefer
    # their own filename. All three copied unconditionally (see module docstring).
    ("AGENTS.template.md", "AGENTS.md"),
    ("CLAUDE.stub.template.md", "CLAUDE.md"),
    ("GEMINI.stub.template.md", "GEMINI.md"),
    ("PROCESS.md", "docs/process.md"),
    ("PROCESS_OPTIONS.md", "docs/process-options.md"),
    # The kit glossary: every working term defined once, linked from process.md.
    ("GLOSSARY.md", "docs/glossary.md"),
    # The machine-readable derived STAGE — the rung the settled spine has
    # earned, its per-phase breakdown, and a fingerprint of the declared
    # derivation inputs that lets any reader tell a current record from a stale
    # one. check.py and CI select their plan from it, so a young project's CI
    # runs the checks it is actually ready for. DERIVED from the artifact states
    # by derive_stage.py, never hand-set. The scaffold ships a comment-only
    # placeholder rather than invented values; `python scripts/derive_stage.py`
    # writes the real one.
    #
    # IT REPLACED `gate.template` -> `docs/gate` AT WI-498 slice 5. That file
    # carried a three-value BAR — "the gate the repo must next PASS" — which was
    # a second axis over the same rows; the ladder now answers both questions
    # with one value. An adopter's `docs/gate` is DELETED at re-sync, not
    # migrated: nothing reads it.
    ("stage.template", "docs/stage", "SR-049"),
    # The id watermark (docs/id-watermark): the high-water mark per id space, so
    # a deleted row's number is never re-minted. REQUIRED, because trace.py
    # treats an absent mark as an error rather than as "no id is taken".
    # NOT all-zeros: the template covers the example rows the other templates
    # seed (OI=2), so it is generated from a real scaffold, never hand-written.
    # NEVER --force THIS ONE onto a live repo. Every other target here is a
    # template to fill or is regenerable from the tree (docs/stage <- derive_stage);
    # this file is the only record of ids that have been DELETED, so overwriting
    # it with the fresh-scaffold marks destroys information nothing can recover.
    # `copy_file` therefore exempts it from --force (see WATERMARK_DEST).
    ("id-watermark.template", "docs/id-watermark"),
    # THE ONE POLICY HOME (SN-028). Every process dial — gate authority, the
    # human-approval level, push authority, the reviewer count, the privacy
    # toggle, the secrets floor, guardrails, the blackout window — declared once
    # here instead of in ~10 one-word files. A FRESH SCAFFOLD GETS ONLY THIS
    # FILE: shipping both homes would hand every new repo the mixed-config
    # refusal on its first run. An EXISTING repo converts with
    # `bootstrap.py --migrate-config`, which bootstrap runs for you (see
    # `migrate_legacy_config`). The three --gate-policy/--push-policy/
    # --privacy-check flags now rewrite a KEY in this file rather than writing
    # their own file.
    ("process.toml.template", "docs/process.toml", "SR-137"),
    # THE PROMPTS (plan §8). Every brief the loop sends is a FILE now, not a
    # Python string constant, and `scripts/prompts.py` resolves them
    # SCRIPT-RELATIVELY — in a scaffolded repo `scripts/` sits at the root, so
    # the templates must land in `prompts/` or every worker, reviewer and
    # critique session downstream loses its brief. (Before this, the three
    # dual-plan hats were the only templates here and nothing copied them: the
    # opt-in round simply PAGEd "hat template unreadable". That degrade was
    # tolerable for an opt-in layer and is not for the ordinary session path.)
    # Kit-owned: a re-sync overwrites them, and a repo that wants different
    # prose wires its own file through --prompt-map instead of editing these.
    ("prompts/README.md", "prompts/README.md"),
    ("prompts/worker.template.md", "prompts/worker.template.md", "SR-146"),
    ("prompts/reviewer.template.md", "prompts/reviewer.template.md", "SR-146"),
    ("prompts/critique.template.md", "prompts/critique.template.md", "SR-146"),
    (
        "prompts/adjudicate-amendment.template.md",
        "prompts/adjudicate-amendment.template.md",
        "SR-146",
    ),
    (
        "prompts/adjudicate-first-approval.template.md",
        "prompts/adjudicate-first-approval.template.md",
        "SR-146",
    ),
    (
        "prompts/adjudicate-disposition.template.md",
        "prompts/adjudicate-disposition.template.md",
        "SR-146",
    ),
    (
        "prompts/adjudicate-consolidate.template.md",
        "prompts/adjudicate-consolidate.template.md",
        "SR-146",
    ),
    (
        "prompts/adjudicate-red-tc.template.md",
        "prompts/adjudicate-red-tc.template.md",
        "SR-146",
    ),
    (
        "prompts/adjudicate-rejudge.template.md",
        "prompts/adjudicate-rejudge.template.md",
        "SR-215",
    ),
    (
        "prompts/adjudicate-done-when.template.md",
        "prompts/adjudicate-done-when.template.md",
        "SR-156",
    ),
    (
        "prompts/adjudicate-combined.template.md",
        "prompts/adjudicate-combined.template.md",
        "SR-156",
    ),
    (
        "prompts/adjudicate-dispute.template.md",
        "prompts/adjudicate-dispute.template.md",
        "SR-146",
    ),
    # The ONE home of the adjudicator's per-tier questions: the first-approval
    # and amendment briefs compose it at render time (an absent copy refuses
    # them), and the spine-authoring skill points at it.
    ("prompts/spine-questions.md", "prompts/spine-questions.md", "SR-146"),
    (
        "prompts/dual-plan-planner.template.md",
        "prompts/dual-plan-planner.template.md",
        "SR-146",
    ),
    (
        "prompts/dual-plan-critic.template.md",
        "prompts/dual-plan-critic.template.md",
        "SR-146",
    ),
    (
        "prompts/dual-plan-arbiter.template.md",
        "prompts/dual-plan-arbiter.template.md",
        "SR-146",
    ),
    # The model REGISTRY the coordinator's router reads (WI-059, S8): one row per
    # usable model keyed [PROVIDER]-[MODEL_NAME]-[VERSION], with example rows for
    # the verified headless shapes. Present but INERT until docs/agents-enabled
    # (the ordered enable-list / consent surface, deliberately NOT scaffolded) is
    # created — routing then selects from that pool (process-options.md
    # "Unattended operation" -> routing/escalation). Absent both files = today's
    # single AGENT_CMD/AGENT_MODEL behavior.
    ("agents.template.toml", "docs/agents.toml"),
    # (The gate-policy / push-policy / review-policy / privacy-check / blackout
    # one-word files folded into docs/process.toml at SN-028 — see the
    # process.toml.template row above. Their `*.template` files stay in the kit
    # marked RETIRED, as a HUMAN's reference for the legacy vocabulary when
    # reading an un-migrated adoption. `migrate_legacy_config` does NOT read
    # them: it reads the adopting repo's own `docs/<file>`, so the templates
    # are documentation, not an input.)
    ("STATUS.template.md", "docs/status.md"),
    # The owner decision briefs status.md's Needs-<human> bullets link to
    # (process-options.md "Trajectory / work-items layer"): one OI-N section
    # per pending decision, deleted when the ruling lands in log.md Decisions.
    ("registries/open-items.template.toml", "docs/requirements/open-items.toml"),
    # (SN-029's separate attestation ledger was scaffolded here until it was
    # retired, and the on-row anchor that was to replace it was ruled
    # unnecessary complexity in turn — owner directive 2026-08-15. What an
    # approval blessed is recorded by COPYING the registries, and the README
    # below is the only part of that mechanism a fresh scaffold receives.)
    #
    # The `last_approved` snapshot's prose stamp. THE DIRECTORY IS SCAFFOLDED
    # WITH ONLY THIS FILE, deliberately: an empty snapshot is the HONEST state
    # for a repo that has approved nothing yet, and shipping pre-filled copies
    # would hand every new project a record claiming a human blessed text they
    # have never seen. The registries land in it at the project's first signing
    # (`intake.py snapshot --seed`), and not before.
    (
        "registries/last-approved-README.template.md",
        "docs/archive/last_approved/README.md",
    ),
    # The append-only history status.md points at (Thread 36, process.md §5):
    # sign-offs, verdicts, and approved decisions append here, keeping the
    # per-session status.md reload cheap.
    ("LOG.template.md", "docs/log.md"),
    # The sequenced work-plan the plan/build cadence runs on (WI-1.29,
    # process-options.md "Unattended operation" → Plan/build cadence): PLAN
    # sessions write blocks here, BUILD sessions execute them; status.md stays
    # the lean resume surface and points at it.
    ("PLAN.template.md", "docs/plan.md"),
    # The authored-narrative half of the architecture record (sitting-2
    # decision 8, WI-455): the Runtime flows check_flows.py verifies from
    # DevStg-Tests on. The structural half is DERIVED (dashboard + checks read
    # the registries and source AST), so no docs/architecture.md is scaffolded.
    ("RUNTIME_FLOWS.template.md", "docs/runtime-flows.md"),
    ("INTERFACES.template.md", "docs/interfaces.md", "SR-159"),
    (
        "registries/stakeholder-needs.template.toml",
        "docs/requirements/stakeholder-needs.toml",
        "SR-147",
    ),
    (
        "registries/system-requirements.template.toml",
        "docs/requirements/system-requirements.toml",
        "SR-147",
    ),
    (
        "registries/low-level-requirements.template.toml",
        "docs/requirements/low-level-requirements.toml",
        "SR-147",
    ),
    (
        "registries/interfaces.template.toml",
        "docs/requirements/interfaces.toml",
        "SR-159",
    ),
    ("registries/external.template.toml", "docs/requirements/external.toml"),
    # The assumptions registry beside the frame it lands on (SR-191, SR-192):
    # every profile that scaffolds the frame scaffolds it, inert until its
    # `-000` rows are replaced.
    ("registries/assumptions.template.toml", "docs/requirements/assumptions.toml"),
    (
        "registries/performance-budgets.template.csv",
        "docs/requirements/performance-budgets.csv",
        "SR-015",
    ),
    (
        "registries/procurement.template.csv",
        "docs/requirements/procurement.csv",
    ),
    (
        "registries/assets.template.csv",
        "docs/requirements/assets.csv",
    ),
    (
        "registries/components.template.toml",
        "docs/requirements/components.toml",
    ),
    # The HATS ROSTER (SN-036, ruled at OI-19 2026-08-13): the declared expert
    # perspectives a decomposition must face, injected into the planner brief by
    # `plan_briefs.hat_surface`. It ships with CONTENT rather than as a blank
    # form — the roster itself is the census — because an empty roster is a
    # form with nothing behind it, only useful if it says something on day one.
    # OWNER TEXT: adopters are expected to EDIT it (cut, add, rewrite every
    # `applies_when` against their own vocabulary), which is the only thing that
    # keeps a roster inherited from a template honest. Deleting the file is a
    # supported opt-out; the composers proceed without hats.
    ("registries/hats.template.toml", "docs/requirements/hats.toml", "SR-161"),
    # registries/work-items.template.csv is deliberately NOT mapped: since the
    # Phase 2c authority flip the work-item registry scaffolds as the docs/work/
    # spec folder below, and the CSV template survives only as the legacy-format
    # reference wi_convert.py migrates from (RESYNC_PACK.md §3).
    # The work-item registry's home (docs/concurrency-restructure.md §2):
    # one Markdown spec per work item, its STATUS encoded as the directory. Ships
    # ADDITIVE beside the CSV — the readers resolve to the folder only once it
    # holds a REAL spec, so a fresh scaffold's CSV stays authoritative and the
    # `-000` example is documentation, exactly like the `-000` row it mirrors.
    # The status directories themselves are created below (GITKEEP_DIRS).
    ("work/WI-000.template.md", "docs/work/queued/WI-000-example.md"),
    # The delegated-decisions record's format, as the -000 example beside where
    # each run's record lands (SR-225); inert, since its one entry is -000.
    ("decisions.template.toml", "docs/decisions/run-000-example.toml", "SR-225"),
    # ...and the location->status contract, stated INSIDE the registry it governs.
    # The WI-000 exemplar documents the SPEC FORMAT; this README documents the
    # FOLDER — the eight status directories, and the one rule a reader keeps
    # re-deriving wrongly: a terminal row (complete/cancelled/partial/
    # restructured) STAYS in
    # the registry, because it is still a DAG predecessor and a trace link, so
    # `docs/work/archive/` must never materialize. That is the half `docs/specs/`
    # answers the other way (rule R-F archives a spec-of-record at close), and a
    # reader with only the specs README in hand generalizes the wrong lifecycle.
    ("work/README.template.md", "docs/work/README.md"),
    # ...and the declaration that makes it green: a work spec is a REGISTRY
    # ENTRY that happens to be Markdown, not a page anyone navigates to, so
    # `docs/work/*` is a declared expected-live-orphan class rather than a wall
    # of check_docs warnings (WI-228's census idiom, one glob with its reason).
    ("orphans-allow.template", "docs/orphans-allow"),
    ("registries/test-cases.template.toml", "docs/test/test-cases.toml"),
    # Specs-of-record (process-options.md "Trajectory / work-items layer"): the
    # per-WI spec directory the work-items.csv `SpecRef` column points at (rule
    # R-E). A README explaining the layer + an inert WI-000 example carrying the
    # Done-when checklist. Nothing gates on the -000 file (check_trajectory
    # ignores the WI-000 row), so a fresh scaffold stays vacuously clean.
    ("specs/README.template.md", "docs/specs/README.md"),
    ("specs/WI-000.template.md", "docs/specs/WI-000.md"),
    # Durable, hand-owned project knowledge: one topic per pack, indexed by this
    # README so documentation checks discover every pack. Packs are advisory;
    # requirements remain authoritative in the spine.
    ("knowledge/README.template.md", "docs/knowledge/README.md"),
    # Critique rubrics (process-options.md "Critique verification & the critique
    # loop", WI-068): the judgment reference a Verification=Critique requirement is
    # scored against — written from the SN/SR intent (not the possibly-lax TC),
    # carrying numbered good/bad anchors that accumulate at rework. A README
    # explaining the convention + an inert rubric-000 example. Nothing gates on the
    # -000 file, so a fresh scaffold that never uses Critique carries it for free.
    ("rubrics/README.template.md", "docs/rubrics/README.md"),
    ("rubrics/rubric-000.template.md", "docs/rubrics/rubric-000.md"),
    # THE SHARED-HELPER PACKAGE (owner ruling D-8, `OI-16`, executed WI-448) —
    # AND THIS BLOCK IS THE WHOLE DOWNSTREAM RISK SURFACE OF THAT RULING.
    #
    # `kitlib/` holds the behaviours that used to be copied into script after
    # script: the declared-policy line reader (five homes), the `docs/work/`
    # spec-folder registry reader (three verbatim 270-line copies) and the
    # best-effort-off-git subprocess pattern (three homes). Eleven shipped
    # scripts now import it, INCLUDING `bootstrap.py` itself, so a scaffold
    # that receives the scripts without the package ImportErrors on its first
    # check — the `trace_text.py` rule above, with a bigger blast radius.
    #
    # COPIED ATOMICALLY, AND THE MANIFEST IS TESTED IN A REAL SCAFFOLD. Every
    # module of the package is listed here explicitly rather than walked,
    # because MAPPING is a declaration an adopter can read; the completeness of
    # the list is held by `tests/test_bootstrap.py` —
    # `test_the_common_package_ships_complete` bootstraps a scaffold and
    # asserts the copied package imports and matches the kit's file set. That
    # test exists because THIS IS THE LINE THE REPO HAS ALREADY GOT WRONG ONCE:
    # MAPPING omitted `schedule.py`, and every fresh scaffold died on its first
    # claim while this repo stayed green, invisible to re-sync because an
    # already-adopted repo carries the file from an older kit.
    ("scripts/kitlib/__init__.py", "scripts/kitlib/__init__.py"),
    ("scripts/kitlib/config.py", "scripts/kitlib/config.py"),
    ("scripts/kitlib/git.py", "scripts/kitlib/git.py"),
    ("scripts/kitlib/registry.py", "scripts/kitlib/registry.py"),
    # WI-483 added `station`: the lane-close terminal-outcome vocabulary, which
    # `integrate` used to define and every reader of it had to import the merge
    # coordinator to reach. It ships for the same reason as the rest — the
    # scripts that import it are in this list, so the package must be whole.
    ("scripts/kitlib/station.py", "scripts/kitlib/station.py"),
    # WI-498 slice 0 added `ladder`: the eight-rung DevStg stage vocabulary,
    # which `spine_rules` defined and `agent_common`/`traj_status` each restated
    # as a literal. `spine_rules`, `agent_common` and `traj_status` are all in
    # this list and all import it now, so — the rule above, again — the package
    # must be whole or a fresh scaffold ImportErrors on its first check.
    ("scripts/kitlib/ladder.py", "scripts/kitlib/ladder.py"),
    # WI-498 slice 1 added `stage`: the DECLARED derivation inputs, their
    # fingerprint, the `docs/stage` format and THE COMMON READER every consumer
    # of "what stage is this repo in" calls. `derive_stage.py` below is the half
    # that needs the registry carrier and cannot live in the package; it imports
    # this one, so the same must-be-whole rule applies.
    ("scripts/kitlib/stage.py", "scripts/kitlib/stage.py"),
    # WI-500 added `evidence`: the `docs/test/evidence` record's format and the
    # declared source surface its claim is bound to. `kitlib/stage.py` above
    # imports it (the Release rung's one input is its verdict) and
    # `record_test_evidence.py` below writes through it, so the same
    # must-be-whole rule applies — a scaffold missing it ImportErrors on the
    # first stage read, not on some later Release-only path.
    ("scripts/kitlib/evidence.py", "scripts/kitlib/evidence.py"),
    # WI-579 added `verdict` (OI-76): the verdict record — the non-record tree
    # identity, the `Review-Verdict:` trailer grammar and the round-file /
    # session-log join. `integrate.py` (the merge gate) and `agent_loop.py` (the
    # C2 review-owed derivation) both import it, and both are in this list, so
    # the must-be-whole rule applies: a scaffold missing it ImportErrors on the
    # first merge attempt, not on some rare path.
    ("scripts/kitlib/verdict.py", "scripts/kitlib/verdict.py"),
    # WI-621 added `done_when`: a spec's Done-when as comparable items (S13).
    # `integrate.py` (the claim warning), `intake.py` (the merge-time flag) and
    # `agent_loop.py` (the reviewer's brief) import it, all three in this list.
    ("scripts/kitlib/done_when.py", "scripts/kitlib/done_when.py"),
    # WI-841 round 2 added `sitting`: a combined lane-checkpoint sitting's
    # scope tokens and verdict sections; `adjudicate_brief.py`,
    # `acceptance_record.py` and `intake.py` import it, all three in this list.
    ("scripts/kitlib/sitting.py", "scripts/kitlib/sitting.py"),
    # WI-865 added `dispute`: a contested review finding's findings file and
    # verdict grammar; `adjudicate_brief.py`, in this list, imports it.
    ("scripts/kitlib/dispute.py", "scripts/kitlib/dispute.py"),
    # WI-834 added `shell_line`: the one reading of a shell command line, with
    # the shell's quoting; `coordinator_guard.py`, in this list, imports it.
    ("scripts/kitlib/shell_line.py", "scripts/kitlib/shell_line.py"),
    # WI-834 round 7 added `guard_hooks`: which hook commands are the
    # coordinator guard's own and how its opt-in merges them;
    # `coordinator_guard.py`, in this list, imports it.
    ("scripts/kitlib/guard_hooks.py", "scripts/kitlib/guard_hooks.py"),
    # WI-448 slice 3 added `spine`: the spine ROW vocabulary — the Status
    # predicates, the LLR-exemption set, the phase parse, the SN id scrapes and
    # the registry CSV loader — which `trace.py` and `spine_rules.py` each
    # carried a copy of under the retired F5 rule. Both of those are in this
    # list, and `trace_text.py` re-exports three of the names for `trace.py`, so
    # the must-be-whole rule bites on the FIRST check a scaffold runs.
    ("scripts/kitlib/spine.py", "scripts/kitlib/spine.py"),
    # WI-520 added `secret_classes`: the credential CLASS vocabulary —
    # `check_privacy.py`'s enforcement floor and `agent_common.py`'s
    # transcript redactor each compiled their own credential patterns until
    # the WI-508 alignment pass measured them disagreeing, in both
    # directions, on the same classes. Both of those are in this list and
    # both import it now, so the must-be-whole rule applies on the very first
    # secrets-floor scan a scaffold runs.
    ("scripts/kitlib/secret_classes.py", "scripts/kitlib/secret_classes.py"),
    # WI-632 added `observation`: the observation record's format, strict reader
    # and atomic write (SR-199). `kitlib/evidence.py` above imports it (the
    # records lie outside a release claim's surface), and `trace.py` and
    # `record_observation.py` read and write through it, so the must-be-whole
    # rule applies on the first check a scaffold runs.
    ("scripts/kitlib/observation.py", "scripts/kitlib/observation.py"),
    # WI-557 added `decisions`: the delegated-decisions record's path, format
    # and obligation (SR-225); `integrate.py`, `agent_loop.py` and
    # `agent_common.py` import it, so the package must stay whole.
    ("scripts/kitlib/decisions.py", "scripts/kitlib/decisions.py", "SR-225"),
    # WI-636 added `provenance` and `authority`: the loop's `Loop-Session`
    # trailer and marker, and the approval-rung tables with the one dial
    # comparison. `agent_common.py`, `integrate.py`, `check.py` and
    # `check_trajectory.py` are all in this list and import them, so the
    # must-be-whole rule applies on the first check or claim a scaffold runs.
    ("scripts/kitlib/provenance.py", "scripts/kitlib/provenance.py"),
    ("scripts/kitlib/authority.py", "scripts/kitlib/authority.py"),
    ("scripts/trace.py", "scripts/trace.py"),
    # WI-329: trace.py imports its spine-row TEXT layer from this sibling, so a
    # scaffold missing it gets an ImportError on the first check. Copied
    # together, always.
    ("scripts/trace_text.py", "scripts/trace_text.py"),
    # The absolute-term rule, trace_text.py's pure sibling: trace.py imports it
    # unguarded and it imports trace_text.py's waiver marker, so the two ship
    # together or the first check ImportErrors.
    ("scripts/absolute_terms.py", "scripts/absolute_terms.py", "SR-157"),
    # OI-12: the spine's registry CARRIER — the one home
    # for the TOML tier tables, the key->column vocabulary and both readers.
    # Imported by trace.py and check_trajectory.py (and by the rest of the
    # spine readers as they convert), so the trace_text.py rule applies
    # verbatim: a scaffold missing it ImportErrors on the first check.
    ("scripts/spine_carrier.py", "scripts/spine_carrier.py"),
    # The one-shot CSV/markdown -> TOML converter (SR-147). Shipped because
    # EVERY adopting repo migrates too, and the round-trip proof is the
    # migration's evidence — an adopter that cannot run --check has to take the
    # conversion on faith, which is what SR-129's 140-cell lesson forbids.
    ("scripts/migrate_carrier.py", "scripts/migrate_carrier.py"),
    # The decisions-record migrator (WI-818): every adopter with records runs
    # it once at the resync that retires the `reviewed` key, since no reader
    # of that key is kept. Imports `kitlib.decisions` alone.
    ("scripts/migrate_decisions.py", "scripts/migrate_decisions.py", "SR-225"),
    ("scripts/spine_rules.py", "scripts/spine_rules.py"),
    # The STAGE axis's producer (WI-498 slice 1). Imports `spine_rules` for the
    # spine load and its rung predicates — so that the two axes can never
    # disagree about what a Drafted row is — and `kitlib.stage` for the carrier;
    # both are in this list, and all three must ship together.
    ("scripts/derive_stage.py", "scripts/derive_stage.py"),
    # The test-evidence PRODUCER (WI-500): the only sanctioned writer of
    # `docs/test/evidence`, and therefore the only way an adopter can reach
    # `DevStg-Release`. Shipped for that reason — a rung whose producer stayed in
    # the kit repo would be a rung no adopter could ever earn.
    ("scripts/record_test_evidence.py", "scripts/record_test_evidence.py"),
    # The observation writer (SR-199): the only sanctioned writer of
    # `docs/test/observations/`, and `trace.py` imports its inputs digest
    # unguarded, so a scaffold without it can neither record a result nor run
    # the checker.
    ("scripts/record_observation.py", "scripts/record_observation.py"),
    # The retirement writer (SR-226): the one writer of `docs/log.d/retired/`,
    # and `trace.py` and `gen_trajectory.py` import its readers unguarded, so a
    # scaffold without it can run neither.
    ("scripts/retire.py", "scripts/retire.py"),
    ("scripts/check.py", "scripts/check.py"),
    ("scripts/check_flows.py", "scripts/check_flows.py"),
    ("scripts/check_docs.py", "scripts/check_docs.py"),
    ("scripts/check_doc_refs.py", "scripts/check_doc_refs.py"),
    ("scripts/check_figures.py", "scripts/check_figures.py"),
    ("scripts/check_perf.py", "scripts/check_perf.py"),
    ("scripts/check_stubs.py", "scripts/check_stubs.py"),
    ("scripts/check_coverage.py", "scripts/check_coverage.py"),
    # The per-change readability report (WI-639): the stack profile's
    # [step:readability] runs it on every scaffold. Its complexity measure calls
    # check_complexity's census and comparison through an unguarded import, so
    # the census ships beside it — a scaffold with the report and not the
    # census could not run the one measure the profile declares. The flag-axis
    # measure is imported unguarded too, so it ships whether or not declared.
    ("scripts/check_readability.py", "scripts/check_readability.py", "SR-216"),
    ("scripts/check_complexity.py", "scripts/check_complexity.py", "SR-183"),
    ("scripts/flag_axis.py", "scripts/flag_axis.py", "SR-216"),
    # The test-first order (WI-640): check.py's built-in `test-first` step runs
    # it at every rung, so a scaffold without it would fail that step.
    ("scripts/check_test_first.py", "scripts/check_test_first.py", "SR-217"),
    # The assumption gate's four steps (SR-205, SR-206, SR-212): check.py's
    # built-in `assumption-gate`, `crossing-allocation`, `interface-allocation`
    # and `assumption-evidence` steps run it, so a scaffold without it would
    # fail each of them.
    ("scripts/check_assumption_gate.py", "scripts/check_assumption_gate.py", "SR-205"),
    ("scripts/check_privacy.py", "scripts/check_privacy.py"),
    ("scripts/check_vendored.py", "scripts/check_vendored.py"),
    # The retired-vocabulary enforcer (OI-21). Shipped, not kit-only: an adopter
    # re-syncing across the conversion has their OWN authored surfaces carrying
    # the retired `G*` tags (their WI `bar:` values, their `stack.ini` `gates=`,
    # their status prose), and the recipe that tells them to convert is worth
    # exactly as much as the check that tells them they missed one.
    ("scripts/check_vocab.py", "scripts/check_vocab.py"),
    # The need-form check (SN-033, WI-454): warn-first lint keeping SN `need`
    # cells in stakeholder language. Shipped because the registry it scans is
    # the adopter's own, and check.py's step table names it at every bar.
    ("scripts/check_need_form.py", "scripts/check_need_form.py"),
    ("scripts/check_trajectory.py", "scripts/check_trajectory.py"),
    ("scripts/trajectory_arch.py", "scripts/trajectory_arch.py"),
    # The `last_approved` snapshot reader/writer (owner directive 2026-08-15).
    # Shipped because it is a SIBLING IMPORT of `intake.py` — the adjudication
    # flip copies the registries in the same act — and because `trace.py` reads
    # it for the drift overlay. A scaffold without it cannot run either.
    ("scripts/baseline_snapshot.py", "scripts/baseline_snapshot.py"),
    # The ready-frontier/safety-classification library (IF-053). Shipped
    # because it is a SIBLING IMPORT of the integration seam, not a nicety:
    # integrate.py's claim refusal ladder and dispatch.py's cycle both
    # `import schedule` UNGUARDED, so a scaffold without it cannot claim work
    # or run the walk-away loop at all (WI-379 — a fresh scaffold raised
    # ModuleNotFoundError from the frontier check). check_trajectory and the
    # dashboard read it too.
    ("scripts/schedule.py", "scripts/schedule.py"),
    ("scripts/subagent_gate.py", "scripts/subagent_gate.py"),
    ("scripts/gen_arch_map.py", "scripts/gen_arch_map.py"),
    ("scripts/gen_release_checklist.py", "scripts/gen_release_checklist.py"),
    ("scripts/gen_cases.py", "scripts/gen_cases.py"),
    ("scripts/gen_trajectory.py", "scripts/gen_trajectory.py"),
    # The display reader and P9R HTML package ship with the facade. The status
    # path needs only traj_display/parse/status; an enabled dashboard imports
    # the rendering package. A scaffold missing either fails its applicable
    # public command, so every concrete module is mapped here.
    ("scripts/traj_display.py", "scripts/traj_display.py"),
    ("scripts/traj_parse.py", "scripts/traj_parse.py"),
    ("scripts/traj_status.py", "scripts/traj_status.py"),
    ("scripts/rendering/__init__.py", "scripts/rendering/__init__.py"),
    ("scripts/rendering/traj_graph.py", "scripts/rendering/traj_graph.py"),
    ("scripts/rendering/traj_render.py", "scripts/rendering/traj_render.py"),
    ("scripts/rendering/traj_views.py", "scripts/rendering/traj_views.py"),
    ("scripts/rendering/traj_panels.py", "scripts/rendering/traj_panels.py"),
    ("scripts/rendering/traj_context.py", "scripts/rendering/traj_context.py"),
    ("scripts/gen_open_items.py", "scripts/gen_open_items.py"),
    ("scripts/gen_components.py", "scripts/gen_components.py"),
    ("scripts/gen_okf.py", "scripts/gen_okf.py"),
    # The per-review-scope verdict rollup (OI-76). It ships with `trunk_step.py`
    # rather than optionally: the trunk step's REGEN_STEPS names it, and a
    # scaffold whose regen halts at a missing generator leaves every LATER
    # generated family stale too (regen stops at the first failure).
    ("scripts/gen_verdict_rollup.py", "scripts/gen_verdict_rollup.py"),
    # check.py runs this generator's --check arm, so its producer must ship
    # beside the prompt templates rather than remain kit-local.
    ("scripts/gen_prompt_catalog.py", "scripts/gen_prompt_catalog.py"),
    ("scripts/plan_coverage.py", "scripts/plan_coverage.py"),
    ("scripts/plan_round.py", "scripts/plan_round.py"),
    ("scripts/plan_briefs.py", "scripts/plan_briefs.py"),
    # The hats-roster reader plan_briefs imports (SN-036 / OI-19). Ships with
    # its importer, not optionally: a scaffold that got the roster and not its
    # reader would fail to compose a planner brief at all.
    ("scripts/hats.py", "scripts/hats.py"),
    # The prompt-template loader + strict single-brace fill (plan §8): every
    # brief the loop sends resolves through it, so it ships wherever
    # agent_loop.py does.
    ("scripts/prompts.py", "scripts/prompts.py"),
    # The adjudicator briefs' evidence assemblers: without it an
    # ADJUDICATE session composes from the worker assignment, which is
    # the WI-424 defect this ships to close.
    ("scripts/adjudicate_brief.py", "scripts/adjudicate_brief.py"),
    ("scripts/plan_coverage_step.py", "scripts/plan_coverage_step.py"),
    ("scripts/plan_artifacts.py", "scripts/plan_artifacts.py"),
    # The work-item registry's CSV <-> spec-folder converter (§2 of
    # docs/concurrency-restructure.md). plan_artifacts imports it as a sibling
    # when the folder home is authoritative, so the two copy together — a
    # scaffold with the filer and not the converter files nothing.
    ("scripts/wi_convert.py", "scripts/wi_convert.py"),
    # The serial trunk step (docs/concurrency-restructure.md §5.1/§5.5): compiles
    # the log fragments in git-derived merge order and re-derives the generated
    # artifacts. Ships with the kit because the rule it enforces — no work branch
    # writes docs/log.md or commits a generated artifact — is the process, not
    # this repo's local habit; its drop-box scaffolds as docs/log.d/ below.
    ("scripts/trunk_step.py", "scripts/trunk_step.py"),
    # The local integrator (concurrency-restructure §1.2, Phase 4): the §2.3
    # claim, the serial fail-closed merge queue over finished claimed branches,
    # and the RULING-6 window audit. The default backend of the one integration
    # flow; the forge backend is the same flow with server-side enforcement.
    ("scripts/integrate.py", "scripts/integrate.py"),
    # The S8 routing/scoring half of the unattended coordinator (WI-059): the
    # model-registry router + fixed escalation policy, and the substance scorer.
    # agent_loop imports them as siblings when the docs/agents-enabled enable-list
    # opts routing in; absent, they are inert (process-options.md "Unattended
    # operation" -> routing/escalation).
    ("scripts/agent_route.py", "scripts/agent_route.py"),
    ("scripts/score_reviews.py", "scripts/score_reviews.py"),
    ("scripts/setup.sh", "scripts/setup.sh"),
    ("scripts/setup.ps1", "scripts/setup.ps1"),
    ("scripts/check.sh", "scripts/check.sh"),
    ("scripts/check.ps1", "scripts/check.ps1"),
    # Onboarding-ladder helpers (Thread 15, process.md §7): a Stage-0 onboarder
    # (one readable entry point per platform) and the developer-workstation
    # dev-setup. Optional + consent-first; a project fills the onboarder's clone
    # URL and dev-setup's EDIT-FOR-YOUR-STACK block, and may serve the onboarder
    # as a Release asset.
    ("scripts/onboard.template.sh", "scripts/onboard.sh"),
    ("scripts/onboard.template.command", "scripts/onboard.command"),
    ("scripts/onboard.template.cmd", "scripts/onboard.cmd"),
    ("scripts/dev-setup.template.sh", "scripts/dev-setup.sh"),
    ("scripts/dev-setup.template.ps1", "scripts/dev-setup.ps1"),
    ("scripts/dev-setup.template.command", "scripts/dev-setup.command"),
    ("scripts/dev-setup.template.cmd", "scripts/dev-setup.cmd"),
    # The evaluator's rungs (WI-1.12): a README skeleton the kickoff agent
    # builds out from the project brief (never overwritten — an adopted repo
    # keeps its own README), and root double-clickable product launchers, one
    # per platform, so running the product never requires recalling a command.
    # They delegate to scripts/run_menu.py (capabilities declared in the
    # docs/stack.ini [run] section) and ship inert (an absent/empty [run] section
    # prints guidance); a pure library deletes
    # them. Root, not scripts/: the double-click use case is "open the checkout
    # folder and click" — one hop shallower matters for a non-code evaluator.
    ("README.template.md", "README.md"),
    # The owner's private scratchpad (FB3, owner-feedback-2026-07-11): a root
    # file for the human owner to keep free-form notes. Its loud header tells LLM
    # agents not to read/cite/act on it, and check_docs.py exempts it entirely
    # (links, orphans, stale hints) — owner notes never gate. Always scaffolded
    # like the README front door; a repo that doesn't want it just deletes it.
    ("OWNER_SCRATCHPAD.template.md", "OWNER_SCRATCHPAD.md"),
    # The capability-menu reader the launchers delegate to (WI-067): reads the
    # docs/stack.ini [run] section and presents a menu / launches by name /
    # lists for an agent, so the launch commands live once in stack.ini instead
    # of duplicated across the platform launchers.
    ("scripts/run_menu.py", "scripts/run_menu.py"),
    ("scripts/run.template.cmd", "run.cmd"),
    ("scripts/run.template.sh", "run.sh"),
    ("scripts/run.template.command", "run.command"),
    # The work-resume counterpart (Thread 33): root agent launchers over the
    # unattended-coordinator engine. Inert until AGENT_CMD is filled (seeded
    # when --agents chose an agent); deletable like run.* — see the module
    # docstring and process-options.md "Unattended operation".
    ("scripts/agent_loop.py", "scripts/agent_loop.py"),
    # The scheduling front end (WI-374; renamed drive.py -> dispatch.py with
    # lane.py extracted at WI-381, concurrency-v2 §A4.2): the dispatcher a
    # plain agent-resume launch runs — agent_loop.py imports it as a sibling
    # when no role flag is given. Composes schedule.py / integrate.py / the
    # lane.py worker launch; admission (the §A8 policy table + spine barrier)
    # is its scheduling decision, every other refusal stays where it lives.
    ("scripts/dispatch.py", "scripts/dispatch.py"),
    # One lane's mechanics (WI-381): ensure the lane worktree, launch the
    # worker subprocess, run the §A2 refresh as its own subprocess. dispatch.py
    # imports it unguarded, so a scaffold without it cannot run the loop.
    ("scripts/lane.py", "scripts/lane.py"),
    # The two lane closes that are NOT a merge (WI-387, concurrency-v2 §A3):
    # handback (the work so far committed as-is, the specs back in queued/) and
    # its ruled red arm, quarantine. drive.py imports it unguarded, so a
    # scaffold without it cannot run the walk-away loop at all.
    ("scripts/handback.py", "scripts/handback.py"),
    # The link-aware spec-move ritual (WI-393, rehoming WI-288/WI-353): move a
    # spec and relink the repo in ONE operation. integrate.py's claim and
    # handback.py's return import it unguarded; workers run its CLI for the
    # terminal close moves and the spec-of-record archival.
    ("scripts/spec_move.py", "scripts/spec_move.py"),
    # The ONE trunk bookkeeping commit (WI-612): stage exactly what the claim or
    # the mint wrote, restore only that on a refusal, advance trunk without a
    # whole-tree reset. integrate.py and intake.py import it unguarded, so a
    # scaffold without it cannot claim or mint.
    ("scripts/bookkeeping.py", "scripts/bookkeeping.py"),
    # The unified trunk-side intake mint (WI-388, concurrency-v2 §A5.2;
    # rulings R1/R3): a WI id is created only by a human trunk commit or this
    # helper. integrate.py's post-merge arm and dispatch.py's empty-frontier
    # ladder import it unguarded, so a scaffold without it cannot merge or
    # run the walk-away loop; agent_loop.py imports it lazily (the worker
    # prompt's advisory context block).
    ("scripts/intake.py", "scripts/intake.py"),
    # The registry-gap census (WI-483 slice 2): the read model that answers
    # "which gaps do the registries name right now?" off trace.analyze. It used
    # to live inside dispatch.py, which made intake.py import the scheduling
    # composer back — a cycle edge. dispatch.py, intake.py and
    # adjudicate_brief.py all import it, and the first two unguarded, so a
    # scaffold without it cannot run the walk-away loop.
    ("scripts/census.py", "scripts/census.py"),
    # The CONSOLIDATION census (the 2026-09-02 restructure plan §1.3): the
    # decision half of "which queued rows are one work item wearing several
    # ids". `intake.py` imports it unguarded for its lineage refusal and its
    # mint arm, so a scaffold without it cannot run the mint at all.
    ("scripts/consolidate.py", "scripts/consolidate.py"),
    # The CHECKPOINT RE-JUDGE decision (SR-215): which observation test cases a
    # merge or release preparation finds due. `intake.py`, `adjudicate_brief.py`
    # and `gen_release_checklist.py` import it unguarded, so a scaffold without
    # it can neither mint at a merge nor print its release checklist.
    ("scripts/rejudge.py", "scripts/rejudge.py", "SR-215"),
    ("scripts/observation_cadence.py", "scripts/observation_cadence.py", "SR-215"),
    # The pending-owner-action read model (WI-483 slice 3): the other half of
    # the same question the census asks — what the OWNER owes, rather than what
    # the registries lack. It used to live in traj_status.py, which made the
    # dispatcher and gen_open_items.py import the gen_trajectory render facade
    # for a state query. traj_status.py, gen_open_items.py and dispatch.py all
    # import it, the first two unguarded, so a scaffold without it cannot render
    # the owner surface.
    ("scripts/pending.py", "scripts/pending.py"),
    # The checker's cross-row coherence rules (WI-483 slice 4): does every id a
    # row cites name a row that exists, and does every row have the children its
    # tier requires. Split out of trace.analyze, which composed the join rules,
    # the carrier sweeps and the report in one 553-line function. trace.py
    # imports it unguarded, so a scaffold without it cannot run the checker.
    ("scripts/coherence.py", "scripts/coherence.py"),
    # The frame and need-tier rules (WI-627): a crossing's system of interest and
    # a requirement's derived one, pure joins beside coherence.py. trace.py
    # imports it unguarded, so a scaffold without it cannot run the checker.
    ("scripts/frame_rules.py", "scripts/frame_rules.py"),
    # The assumption tier's rules (WI-629), the same kind of pure sibling: trace.py
    # imports it unguarded, so a scaffold without it cannot run the checker.
    ("scripts/assumption_rules.py", "scripts/assumption_rules.py"),
    # The acceptance record (WI-521 slice 1): the two-tree spine comparison and
    # the snapshot mirror — which cells are attested, whether their text has
    # moved away from the copy recording its acceptance, and that the copy is
    # only ever written by copying live text. Split out of check_trajectory.py,
    # which imports it UNGUARDED and joins its findings to the failure set, so a
    # scaffold without it cannot run the checker — let alone report drift.
    ("scripts/acceptance_record.py", "scripts/acceptance_record.py"),
    # The WI-218 split of the coordinator engine: the headless session layer,
    # the shared primitives, and the dual-plan runner agent_loop.py imports as
    # siblings. (The parallel dispatcher retired at concurrency-restructure
    # Phase 5; integrate.py is the serial integration seam.)
    ("scripts/agent_session.py", "scripts/agent_session.py"),
    # One adapter per provider runner (flags, final text, usage, occupancy);
    # the session layer imports it as a sibling.
    ("scripts/session_adapters.py", "scripts/session_adapters.py"),
    # The session service: the one path every model call takes (act, keep,
    # record); the loop and the dual-plan runner import it as a sibling.
    ("scripts/session_service.py", "scripts/session_service.py"),
    ("scripts/session_keep.py", "scripts/session_keep.py"),
    # The coordinator's adjudication entry point (WI-835): a thin caller of the
    # session service's keep operation; temporary until WI-801's `ask`.
    ("scripts/coordinator_adjudicate.py", "scripts/coordinator_adjudicate.py"),
    # The coordinator context guard (WI-822): integrate.claim imports it;
    # dormant at the shipped `[coordinator] context_guard_pct = 0`.
    ("scripts/coordinator_guard.py", "scripts/coordinator_guard.py"),
    # An attended launcher's review and critique briefs, rendered from the
    # kit templates, and its review filed as a round file (WI-852).
    ("scripts/review_brief.py", "scripts/review_brief.py"),
    # WI-545's behavior seams keep the session briefs and declared-policy
    # decisions behind the small coordinator facades that consume them.
    ("scripts/agent_brief.py", "scripts/agent_brief.py"),
    ("scripts/agent_common.py", "scripts/agent_common.py"),
    ("scripts/agent_policy.py", "scripts/agent_policy.py"),
    ("scripts/plan_runner.py", "scripts/plan_runner.py"),
    # The scaffold inventory itself is package-owned so bootstrap stays a
    # command facade over one manifest decision surface.
    (
        "scripts/kitlib/bootstrap_manifest.py",
        "scripts/kitlib/bootstrap_manifest.py",
    ),
    ("scripts/agent-resume.template.cmd", "agent-resume.cmd"),
    ("scripts/agent-resume.template.sh", "agent-resume.sh"),
    ("scripts/agent-resume.template.command", "agent-resume.command"),
    # Agent-neutral enforcement: POSIX hooks (opt-in via
    # `git config core.hooksPath .githooks`, which setup.sh/ps1 set). commit-msg
    # scans the message; pre-push is the privacy-review backstop (Thread 39) —
    # the identity review is inert under the default `false` privacy-check (the
    # always-on secrets floor still runs), like the policy files.
    ("hooks/pre-commit", ".githooks/pre-commit"),
    ("hooks/commit-msg", ".githooks/commit-msg"),
    ("hooks/pre-push", ".githooks/pre-push"),
    # The one interpreter probe the three hooks source (WI-880), shipped
    # beside them so a hook and its probe travel together.
    ("hooks/kit-python.sh", ".githooks/kit-python.sh"),
    # The declared product toolchain (Thread 30, process.md §7): the single home
    # for the format/lint/test commands, src/tests paths, tiers, and coverage
    # threshold. check.py/CI/hook/setup.* read it. Copied UNCONDITIONALLY (unlike
    # pytest.ini) with the Python-reference values — it's the one file a stack
    # swap edits, so every scaffold gets it (a non-Python scaffold's OI checklist
    # points here). Deleting it falls back to check.py's identical built-ins.
    ("stack.ini.template", "docs/stack.ini"),
    ("pytest.ini", "pytest.ini"),
    ("gitignore.template", ".gitignore"),
    # eol=lf pin for the sh-based git hook (a CRLF shebang breaks it under
    # Windows autocrlf). Skipped if the repo already has a .gitattributes —
    # merge the .githooks/pre-commit rule in by hand (ADOPTING.md §1).
    ("gitattributes.template", ".gitattributes"),
    ("ci/check.yml", ".github/workflows/check.yml", "SR-151"),
]


def mapping_entries():
    """`MAPPING` normalized to `(src, dst, requirement_ref)` triples.

    A row may carry an OPTIONAL third element — a system-specification id stating
    why the file ships (SR-163). The reader is TOLERANT: a bare `(src, dst)` pair
    is accepted and yields `ref = None`, and a bare pair is by definition an
    unmapped-entry warning. So a downstream inventory keeps working with no flag
    day and the reference burn-down IS the migration — references are filled row
    by row, each one retiring one warning, rather than all at once behind a gate.
    `gen_arch_map.mapping_purpose_findings` is the checker that reads these."""
    return [(row[0], row[1], row[2] if len(row) > 2 else None) for row in MAPPING]
