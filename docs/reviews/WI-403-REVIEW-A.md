# WI-403 — REVIEW-A (2026-08-02)

Verdict: APPROVE — I re-drove both convictions red-then-green against trunk's
own integrate.py, forged three NEW shapes the builder never tried (BOM
prepend, trailing-space-only edit, and a `.gitattributes`-mediated CRLF
relay), and re-ran every registered bar. The docstring's promise — literal
byte-for-byte, anything non-identical convicts — held against everything I
threw at it. Findings below, severity-ordered; none blocks.

Reviewed: branch `wi-403-oracle-excuses-eol-only-hand-edits` at `c8f92b3d`
(work `3844cfd9` + close), trunk `ConcurrencyTrainRewrite`. All commands run
under `/Users/diytechy/Documents/ai-template/.venv/bin/python` from the
worktree. Per the brief, `docs/log.d/` fragments were not read.

## What I verified before hunting

**The two convictions, re-driven red.** I checked trunk's pre-fix
`integrate.py` into the worktree (`git checkout ConcurrencyTrainRewrite --
project-trajectory/scripts/integrate.py`) and ran the branch's own 7-test
selection against it:

```
FAILED tests/test_integrate.py::test_a_trailing_newline_only_hand_edit_in_a_claim_shape_convicts
FAILED tests/test_integrate.py::test_a_whole_file_crlf_relay_in_a_claim_shape_convicts
2 failed, 5 passed, 111 deselected in 1.98s
```

— exactly the deliverable's watched red (the two forged shapes excused by the
old text-mode reads, the five holds green). Restored the branch code and
re-ran the same selection: `7 passed, 111 deselected in 1.90s`. All four
keep-greens are in that seven and pass: genuine relink excused
(`test_a_crashed_claim_that_relinked_docs_is_still_re_cut`), genuine
CRLF-checkout relink excused
(`test_a_crashed_claim_that_relinked_a_crlf_doc_is_still_excused`), non-relink
conviction (`test_an_md_edit_that_is_not_the_relink_still_convicts`), and the
mid-file-byte conviction now pinned as its own test
(`test_one_extra_mid_file_byte_still_convicts`).

**Two NEW forged shapes of my own.** Using the branch's own
`forged_relink_claim` recipe (exact `_claim_subject`, real
`spec_move.move_spec` pair, one commit past trunk, mangle applied to the
genuinely-relinked `docs/log.md` before the commit), I drove two shapes the
builder never tried:

- *BOM prepend* — `log.write_bytes(b"\xef\xbb\xbf" + log.read_bytes())` →
  `_abandoned_claim` → **False** (convicts).
- *Trailing-space-only edit* —
  `log.write_bytes(log.read_bytes().rstrip(b"\n") + b" \n")` →
  `_abandoned_claim` → **False** (convicts).

Both non-identical byte shapes convict, as the rewritten docstring promises.
(Probes were transient test files, deleted after the runs; recipes above are
complete.)

**The fixture cannot self-satisfy.** `forged_relink_claim` performs a GENUINE
`spec_move.move_spec` and asserts `docs/log.md` was actually relinked before
mangling, so the relinked file's bytes are the only degree of freedom left —
a compare that loosened again would go green on these tests only by excusing
the mangle itself. The fixture is as tight as its docstring claims.

**The code is what the spec confined it to.** `_blob_bytes`
(integrate.py:436) is a raw `git cat-file blob` — binary `subprocess.run`, no
text mode, no strip, no `--textconv`; a failed read returns None and both
None-arms of `_relinked_exactly` convict (fail-closed). The compare is
`spec_move.expected_relink(old.decode("utf-8"), doc_dir, remap).encode("utf-8")
== new` — and valid UTF-8 round-trips decode/encode byte-identically (BOM,
lone-`\r`, mixed EOLs all preserved; `bytes.decode` does no newline
translation), so the only text-domain step introduces no fold. Nothing else in
the oracle chain changed: `_abandoned_claim`'s four facts and `_claim_delta`'s
classification are untouched by the diff.

## Findings

**1. MINOR (advisory; corrects the review brief's premise) — the kit DOES
ship `.gitattributes` EOL rules over `.md`, and under them git's own clean
filter re-opens a hairline version of the fixed harm; the direction is safe
and I drove it.** The brief's premise ("the kit's own repo has no such
attributes") is false: this repo's root `.gitattributes` and the scaffolded
`project-trajectory/gitattributes.template` both open with the catch-all
`* text=auto eol=lf`, which covers `.md`. Since `git cat-file blob` reads
post-clean repository bytes while `spec_move` writes worktree bytes, I drove
the interaction in probe repos carrying the shipped attributes:

- *Genuine relink under `* text=auto eol=lf`* → excused (True). With `eol=lf`
  checkout conversion is a no-op and the relink preserves the parent's EOL
  mix, so clean's `text=auto` renormalize guard leaves the new blob matching
  `expected_relink` over the parent blob.
- *Genuine relink of a legacy CRLF blob in a repo that adopted the attributes
  later* → excused (True) — the `text=auto` guard (index copy already CRLF)
  keeps the re-add unconverted.
- *Forged whole-file CRLF relay under the attributes* → **excused (True)**,
  but `_blob_bytes(root, "refs/heads/wi-401:docs/log.md")` contains no
  `\r`: git's clean filter erased the relay at `git add`, so the committed
  blob IS the genuine relink and the branch deletion loses nothing the
  repository ever stored. The worktree-only relay is still destroyed with the
  branch — the WI's harm class resurfacing one layer down — but it is
  destroyed by the repo's own declared content policy (the attributes say
  CRLF-vs-LF is not content there), before the oracle ever runs; no blob read
  can see bytes git refused to store, so this is not an oracle bypass and no
  code change is owed.

Residual downstream exposure, mapped honestly: a config where blob bytes and
ritual-written worktree bytes genuinely diverge (an explicit `*.md text` rule
over a mixed-EOL legacy blob, where checkout skips smudge but checkin
converts; or a content filter such as git-lfs on `.md`) makes a genuine
relink CONVICT — fail-closed friction (the branch is preserved and the claim
declines to re-cut), never a false excusal, which is exactly
`_abandoned_claim`'s documented failure direction ("It never deletes
something it should not; it declines to re-cut something it could have").
No remedy owed. -> @owner.

**2. MINOR (concur, pre-existing) — finding 3's leave-it-recorded call is
correct against the code.** The spec's condition was "take it only if the
same two reads cover it without new machinery." They don't: the oracle's loop
reads same-path pairs (`tip^1:path` vs `tip:path`) for paths in `relinked`,
while the spec pair is cross-path (`tip^1:src` vs `tip:dest`) and
`_claim_delta` records the `A` under `active/<branch>/` without ever reading
its content; the dest's expected content is the OUTBOUND rebase
(`_rebased_link_target`, private, applied via `_rebase_moved_spec_links` on
the worktree) for which spec_move exposes no pure oracle —
`expected_relink` covers only the inbound half. Closing it means a public
`expected_rebase` mirror plus a cross-path read: new machinery, exactly as
the deliverable says. The harm ceiling is the same hand-edit-deletion class
as finding 1 was (never a merge, never a false conviction), so advisory
stands. Now that this WI makes the fix shape crisp (one public pure function
+ one read pair, same conviction grammar), it is cheap enough to mint — but
per the R3 invariant that is trunk's intake call, not this branch's omission.
-> no remedy owed this row -> @owner.

**3. INFO — the undecodable-parent conviction's claimed invariant is real; no
false-conviction file class exists in a filter-free repo.**
`_rewrite_md_links` (spec_move.py:166-169) reads with strict
`encoding="utf-8"` and catches `(OSError, UnicodeDecodeError)` → `return
False` before any write, so the ritual structurally cannot have modified a
file whose bytes do not strict-decode — a claim-shaped `M` on such a file
(the latin-1 legacy doc of the brief's hypothetical) genuinely is somebody's
work, and the conviction is CORRECT, not a false-conviction class: it
preserves the branch and refuses the re-cut (the safe direction). The branch's
`test_a_relinked_doc_the_ritual_would_have_skipped_convicts` drives exactly
this, asserting the ritual itself skipped the `\xff` file before the forge
touches it. The only path to a decodable worktree over an undecodable blob is
a content filter, covered by finding 1's exposure map. Verified sound.

**4. INFO — fixed-forward was the right call, and it is clean.**
`check_trajectory.staged_spine_amendments(".", "ConcurrencyTrainRewrite",
"HEAD")` → `[]`, and `git diff --name-only ConcurrencyTrainRewrite..HEAD --
docs/requirements docs/test` is empty — no spine cell was touched, let alone
amended. LLR-145's Detail ("expected_relink is the pure oracle
integrate._abandoned_claim compares byte-for-byte") stated the REQUIRED
property; the defect was the code under it, so making the code match the
Verified row — rather than amending a ratified cell down to
"stripped-text-for-stripped-text" and back up again — keeps the record stable
and true and never puts a false property through the WI-316/WI-388 amendment
machinery. WI-393's commit message remains historically wrong about `9b91e04f`
as all history does; the review record (WI-393-REVIEW-A finding 1) already
documents that, which is this repo's honest mechanism. Concur.

## Registered bars, re-run

- Module suites: `pytest -q tests/test_integrate.py tests/test_spec_move.py
  tests/test_handback.py` → `148 passed in 43.63s` (matches the declared 148).
- Smoke: `pytest -q -n auto -m smoke` → `620 passed, 2 skipped in 10.23s` —
  622 collected, exactly the deliverable's 616+6=622 with four
  environment-conditional skips passing on this machine.
- Full unfiltered suite: not independently observed by this review (a re-run
  was launched but had not completed at write time); the verdict rests on the
  module suites + smoke + strict checks above — the changed surface's own
  suites in full — and the refresh bar re-runs the unfiltered suite
  mechanically at integrate time. The deliverable's own declared figure is
  `1875 passed / 10 skipped` at `3844cfd9`.
- Strict checks: `check_figures.py --root . --strict` → rc=0, `33 declared
  figure(s)` (matches). Spot-checked two figures by re-driving: the 7-test
  selection cmd → `7 passed` (matches the deliverable's prose), and
  `wc -l project-trajectory/scripts/integrate.py` → `2103` (matches the
  ratchet figure). `check_trajectory.py --root . --strict` → rc=0; its 11
  WARN lines are byte-identical to trunk's own strict run (diffed, `WARN SETS
  IDENTICAL`) — none introduced by this branch.
- Ratchet: BASELINE `integrate.py: 2103` exact against `wc -l`; the bump
  comment names WI-403 and the reason per the escape-hatch rule.
- R-A/R-F: `check_trajectory --strict` reports neither; the closed spec's
  frontmatter carries no `specref` and the close commit records why nothing
  archives (a shared review record is not a spec-of-record).
- docs/work delta: `git diff --name-status ConcurrencyTrainRewrite..HEAD --
  docs/work` → exactly the WI-403 `D` (active) + `A` (complete) pair; the
  only other doc touched on the branch is WI-403's own log fragment.
- Ruff: `ruff check` over the three touched files → `All checks passed!`.

VERDICT: APPROVE findings=4
