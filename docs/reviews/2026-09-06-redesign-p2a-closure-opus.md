# redesign-p2a-closure — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `940b4dda72b16b666e3a0e9f24b857c80faa6865bc3cb02af7b344f771f47999`

Tracked invocation: [session log](../iteration/call_ebb61e1faa6142f793b11bf4dd6b18eb-20260906-104926.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

## CHANGES_REQUESTED

No tests executed; findings are from the supplied diff, records and excerpts only. This is not an artifact approval, queue close or cutover.

### Withdrawn: the late-refusal blocker

The prior review's BLOCKER 1 does not survive the evidence now supplied. Three separate reasons, and the third is the one that matters:

- **The predicted ids are load-bearing only for grouping.** `_apply_supersedes` partitions by *which drafts absorbed which rows*; substituting different successor ids permutes labels, not the partition. Inside `_replace_needs_value`, `expected["needs"] = new_needs` is compared against a candidate built from that same `new_needs`, so span locatability is independent of the id strings. A drifted prediction therefore cannot turn a locatable span into an unlocatable one.
- **The allocator is proved serial for this shape.** `test_the_mint_handles_new_successors_across_multiple_repoint_groups` asserts `successors == ["WI-021", "WI-022", "WI-023"]` off a `WI-020` high-water — the prediction and the allocation, checked against each other rather than asserted in a docstring.
- **The apply-only population is now exercised.** That test's three successors each carry `needs` naming the rows they absorb, and the assertion `[rows[wi_id]["Predecessors"] for wi_id in successors] == ["", "", ""]` proves `_replace_needs_value` located and edited **canonical-writer output** — the exact population prevalidation structurally cannot see. Two distinct successor tuples (`WI-005 → 021,022`; `WI-006 → 022,023`) also make the second group re-locate a span in a file the first group had already rewritten, and `rows["WI-010"]["Predecessors"] == "WI-021;WI-022;WI-023"` shows it landed the union.

What remains is an unsupported concurrent external writer, which does not justify adding `reset --hard` + `clean -fd` to a path that would then erase unrelated dirty work on a failure mode nothing can reach. Declining it is correct.

### 1 — the ratchet record's head entry contradicts the value it annotates

This file's convention is unambiguous in the diff itself: the trailing comment opens with the *current* delta and pushes the rest behind `Earlier:` (`"intake.py": 1397,  # +18 (1379 -> 1397 SLOC) …`). After the change, `"intake.py": 1453` still leads with `+18 (1379 -> 1397 SLOC)`, and the `+56` reason sits detached in three comment lines *above* the row. `"bootstrap.py": 1663` has the identical shape against `+1 (1660 -> 1661)`.

The brief's own claim is that the baseline was deliberately restamped rather than silently waived. At the one place a future author reads to decide the next bump, the record now says 1397. `P2A-EXECUTION.md` compounds it by asserting "the reason beside the value" — it is not beside the value. Prepend into the inline chain with `Earlier:` and delete the detached block. (The `bootstrap.py` row is P0a's, outside this subject; I name the shape, I do not approve that restamp.)

Also confirm nothing parses the trailing comment to enforce "a bump carries a reason on the line" — a detached comment would evade such a check silently.

### 2 — the execution record's evidence cites a test the final diff does not contain

`P2A-EXECUTION.md` § Evidence, bullet 3, names `test_an_unwritable_dependency_edit_refuses_before_any_mint_effect` and describes it as *injecting* the failure. The final diff adds `test_a_cr_only_dependency_edit_refuses_before_any_mint_effect`, which injects nothing — it drives real CR-only input, which is precisely the improvement the dispositions accepted. The record still describes the superseded monkeypatch test.

This is not cosmetic: re-driving the cited evidence by name collects zero tests and reports green on an empty scan. Correct the bullet to the shipped test and its actual mechanism.

### 3 — the refusal message misattributes the CR-only cause

For a CR-only spec, `_NEEDS_SOURCE_RE` and the fence regex use `re.M`, whose anchors need `\n`; `fences` is empty, so `content_start = limit = 0` and the candidate scan never runs. The operator is then told the **array span** is not unique — when the real cause is that no frontmatter delimiter was found at all. That refusal aborts an entire mint and a human must act on it, so the diagnosis has to name the newline style, not imply ambiguity. One branch on `len(fences) < 2`, not a new guard.

### 4 (minor) — two undocumented couplings on one boundary

- `expected = dict(data)` compares a `tomllib.loads` result against whatever `ac.parse_spec_frontmatter` returns. If that function ever normalizes, defaults or drops a key, **every** re-point on a row exercising that path becomes a hard mint refusal, silently until a mint hits it. Cheapest fix keeps one owning boundary: derive `expected` by parsing the original `text[content_start:limit]` slice locally, so both sides of the equality come from the same parser.
- The fence regex is a second, stricter frontmatter delimiter reader than the one that already validated this file. Any tolerance the real parser has and this lacks (trailing whitespace on `+++`, for instance) converts a previously-working re-point into a hard refusal. State the assumed invariant or read the fences through the owning parser.

### 5 (minor) — `agent_loop.py`

`bool(commits)` is equivalent to the old `committed` (the f-string always contains `..`, so it is falsey exactly when `before == after`) — that substitution is sound. The `return a, b if c else ""` parse is also correct, though parenthesizing would cost nothing.

Unverified from the supplied diff: dropping `wi_label` is behavior-preserving only if `current_wi` is never rebound between the old alias point and the `session_meta` / `session_bookkeeping` consumers. That interval is not in the hunks. The alias's prior existence is weak evidence it was freezing the value. Confirm no rebinding, or keep the alias.

### Not faulted

Byte preservation is right end to end (`newline=""` on both read and write, edit confined to the value span, parse on a normalized copy). Bounded candidate spans plus full-dict `tomllib` equality genuinely defeats the multiline-string, nested-table, quoted-key and comment decoys, and the `len(spans) != 1` refusal is the correct response to ambiguity rather than a guess. Removing `_OI_ID_RE` is a real dead-reader deletion.
