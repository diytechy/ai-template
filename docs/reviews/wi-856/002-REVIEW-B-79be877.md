Reviewed: 79be877e3e2e7cf82bfd2b2157df496698e23a9a

Verified. `git rev-parse HEAD` in the lane printed 79be877e3e2e7cf82bfd2b2157df496698e23a9a. I read the full scoped diff (consolidate.edged_text, the two handback refusal strings, the four new tests and the reworked refused-edge close test, the LLR-210 detail, the TC-208 and TC-254 method and evidence cells, the RESYNC entry, the stack.ini max-tests re-stamp, docs/decisions/wi-856.toml), the WI-856 spec, SR-220 and LLR-312, the kitlib.registry spec reader, and the rubric docs/rubrics/kit-change-review.md.

Failure classes I hunted first, worst first: (1) silent wrong content, meaning an edge written somewhere the registry reader never sees, or bytes outside the frontmatter changed; (2) fail-open, meaning a frontmatter that cannot be read gets edged instead of refused; (3) a close that refuses what it should edge.

Real-path evidence:
- The new close test drives `handback.close_adjudication` and a merge on a real repository and lane. The waiter ends up `queued` with Predecessors `WI-401`, and the rest of its spec is byte-identical.
- Red before the fix: I loaded trunk's `consolidate.py` (3b9f2b44f), patched its `edged_text` into the test modules with a scratch plugin, and ran the five new or changed tests. The two new-behaviour tests fail on the old code, as they must: `test_the_edge_write_inserts_a_missing_needs_line[lf]` and `[crlf]` ("a spec with no needs line was refused"), and `test_queue_with_edge_gives_a_waiter_with_no_needs_line_one` ("cannot add the WI-404 -> WI-401 edge ... nothing written"). The extension and refusal characterizations, and the refused-edge close test, pass on the old code. That is correct for characterizations.

Pure-function probes, old code against new:
- A `needs = [...]` line inside a body code block, with none in the frontmatter, was silently rewritten IN THE BODY by the old code. The new code edges the frontmatter and leaves the body alone. This is an unstated improvement, because the regex is now confined to the frontmatter.
- A multi-line `needs` list that already holds the blocker is now a no-op instead of a refusal.
- An unterminated `needs = [` and a missing fence still refuse.

Spine and rubric checks:
- K3: SR-220 is unchanged and stays true. It promises no refusal for a row with no needs line. The ruling is to retain it with no carried change.
- LLR-312 (handback's close) is unchanged, and its detail never mentions the needs line. The ruling is to retain it. TC-254, which verifies both LLR-210 and LLR-312, carries the change.
- Every approved sentence of LLR-210, TC-208 and TC-254 survives. The one exception is TC-254's refusal clause, which the spec's Done-when dictates. No Status flips.
- K2: no SN or SR text changed.
- docs/work, 971 specs: none has a table in its frontmatter, none has a multi-line `needs`, and none is CRLF in the repository. 457 have no `needs` key, which confirms how often the gap occurs.
- The max-tests re-stamp (3276 + 5 = 3281, ceiling 3410) matches the five new in-process test ids. tests/conftest.py SLOW_MODULES lists test_consolidate_close.

Done-when map:
- (1) Insert, extend as before with idempotence, refuse an unreadable frontmatter. Covered by tests/test_consolidate.py::test_the_edge_write_inserts_a_missing_needs_line, ::test_the_edge_write_extends_an_existing_needs_line_as_before, ::test_the_edge_write_refuses_a_frontmatter_it_cannot_read and the existing ::test_the_edge_write_is_surgical_and_idempotent.
- (2) Covered by tests/test_consolidate_close.py::test_queue_with_edge_gives_a_waiter_with_no_needs_line_one, the in-process insert test (the inserted line parses, the rest is unchanged) and the extend test.
- (3) LLR-210 and its TCs are amended. The in-lane adjudication half has not yet been discharged at this tip. The coordinator cycle sits it at the checkpoint after a counted round, so it is not counted as a finding here.
- (4) The RESYNC entry is anchored at trunk commit 3b9f2b44f.

Coverage-extension note, no severity: a multi-line `needs` list that lacks the blocker is refused, which fails closed. The refusal text ("has no frontmatter the edge can read") misdescribes it, but no supported writer produces that shape.

Commands:
- `git rev-parse HEAD` -> 79be877e3e2e7cf82bfd2b2157df496698e23a9a
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-24a-leg17/r1/opus/wi-856 tests/test_consolidate.py tests/test_consolidate_close.py` -> `118 passed in 271.08s (0:04:31)` (posix-shell gate unsatisfied, 0 tests skipped by it)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (970 work item(s), 858 done (88%), 34 cancelled, graph acyclic).` exit 0
- red-before run: the same pytest with `-p prefix_plugin` (trunk's edged_text patched in), basetemp .../r1/opus/prefix, on the five new or changed test ids -> `3 failed, 4 passed in 114.12s` (the three new-behaviour cases fail, the characterizations pass)
- `python .../r1/opus/probe.py` -> old and new edged_text on no-needs (LF/CRLF), needs-in-body, a frontmatter subtable, multi-line needs, CRLF extension (outputs quoted in the findings)
- `git status --short` in the lane -> empty (nothing written there)

- [MINOR] project-trajectory/scripts/consolidate.py:1445 -> The insert arm puts `needs = ["<blocker>"]` just before the closing fence. If a frontmatter ends in a TOML table (`[extra]` then `note = "x"`), the inserted line becomes `extra.needs`, not a top-level `needs`. The probe printed `top-level needs: None extra: {'note': 'x', 'needs': ['WI-401']}`. The function returns text, so the close reports success while the waiter gains no edge: silent wrong content (a fail-open). No supported writer and no spec on file carries a frontmatter table (0 of 971), so this is MINOR (K1). -> Insert the line directly after the OPENING fence (`lines[:1] + [inserted] + lines[1:]`). Every byte there is top-level TOML, so the bad placement cannot happen in the first place, and no check is added. -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:9772 -> The entry promises adopters the line is written "in the file's own line ending, and the rest of its spec stays byte for byte". The CRLF parametrization at tests/test_consolidate.py:1217 tests that, but the one caller never feeds CRLF text. handback.py:811 and :845 read with `Path.read_text`, which turns CRLF into LF (probed: `b'a\r\nb\r\n'` reads as `'a\nb\n'`), and handback writes with `newline="\n"`. So a CRLF hand-filed waiter is rewritten all-LF: in the working tree, and in the commit when autocrlf is off. That breaks the byte-for-byte claim for exactly the hand-filed rows this WI targets. Separately, the extend arm's `_NEEDS_RE` (`\s*$`) eats the `\r` on a raw CRLF input. The probe printed `needs = ["WI-1", "WI-401"]\n+++\r\n`, a mixed-ending line, but only through a direct call. Nothing is lost, and LF is the registry's own format (TC-254), so this is MINOR (K1). -> Either say the close writes the spec in the registry's LF format (and drop or relabel the CRLF case as a pure-function property), or have the close read and write with `newline=""` so the file's own line endings reach `edged_text`. -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:2226 -> For clarity: LLR-210's new sentence, and TC-208's method (docs/test/test-cases.toml:2132), say a spec is refused when its "`needs` line does not parse". The code refuses when ANY part of the frontmatter fails to parse (consolidate.py:1439), and when a `needs` list spans several lines. The Done-when ("A frontmatter it cannot read is still refused") and the RESYNC entry ("whose front matter does not parse") state it correctly. So the LLR and TC under-describe the refusal set, and a frontmatter whose `needs` line parses but whose other keys do not now refuses where it used to be edged (K1). -> Say "whose frontmatter does not parse, or whose `needs` list is not one line" in both cells at the pending in-lane sitting. -> @owner
- [MINOR] project-trajectory/scripts/consolidate.py:1439 -> A repeat (PROCESS.md section 3, "Consolidate, don't duplicate"). `edged_text` now parses the frontmatter itself (`_fence_close`, then `tomllib.loads` over `lines[1:close]`), a second home for the fence-and-TOML read that `kitlib.registry.parse_spec_frontmatter` owns. The two already differ on `\r` handling, and the close only ever feeds LF text. -> Take the parsed table from `parse_spec_frontmatter` (its ValueError is the refusal), and keep `_fence_close` only for the insert position. -> @owner

VERDICT: APPROVE findings=4
