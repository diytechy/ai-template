## 2026-08-02 — WI-403: the abandoned-claim oracle convicts EOL-margin hand edits

**Summary.** WI-393 REVIEW-A finding 1, driven not reasoned: the reviewer
forged claim-shaped commits carrying (a) a trailing-newline-only edit and
(b) a whole-file CRLF relay of an otherwise-relinked doc, and
`integrate._abandoned_claim` excused BOTH — returned True, branch deleted with
the edit — while one mid-file byte correctly convicted. Cause:
`_relinked_exactly`'s two reads went through `ac.git`, whose text-mode
subprocess folds `\r\n`/`\r` to `\n` on decode and `.strip()`s the success
path, so the docstring's "byte-for-byte" was actually
stripped-text-for-stripped-text. Harm ceiling stated honestly, per the spec:
deletion of a whitespace/EOL-only hand edit riding a forged claim-shaped
commit — never a false merge, never a false conviction of genuine relinks —
which is why the finding was APPROVE-non-blocking and rode its own row. But
this repo's own discipline (WI-234/WI-337) treats line endings as
load-bearing, so an EOL relay is real content the oracle must see.

**The fix (confined to the oracle's two reads, as specced).** `_blob_bytes`
(raw `git cat-file blob` — plumbing: no text mode, no strip, no textconv)
feeds a strict-decode/re-encode compare: the expected new bytes are literally
`utf8(expected_relink(utf8_strict(parent bytes)))`, and UTF-8 strict
decode/encode round-trips exactly, so "byte-for-byte" in the
`_relinked_exactly` docstring, LLR-145's Detail cell and commit `9b91e04f`'s
message is now the implemented property — fixed FORWARD (the wording was
right, the code was wrong), so no spine cell needed amending. Two consequences
pinned deliberately: a parent that does not decode as UTF-8 convicts outright
(`_rewrite_md_links` SKIPS such a file, so a modification to it cannot be the
ritual's write), and a genuine relink on a CRLF checkout still matches
WITHOUT the accidental fairness the EOL fold used to buy, because `spec_move`
preserves line endings (`newline=""`).

**Evidence — the reviewer's drives as fixtures** (`forged_relink_claim`:
exact `_claim_subject`, real `spec_move.move_spec` move pair, one commit past
trunk, so only the relinked file's bytes are left to convict on). Watched red
first, on the claim tree with the tests applied and the oracle untouched:
`2 failed, 5 passed` — trailing-newline-only and CRLF-relay EXCUSED
(`assert not True` on `_abandoned_claim`), the guards green. After the fix
the same selection is green: 7 passed
<!-- fig: cmd="python -m pytest -q tests/test_integrate.py -k 'trailing_newline_only or crlf or mid_file_byte or ritual_would_have_skipped or relinked_docs or not_the_relink'" rev=3844cfd9 -->,
with the genuine-relink excusal
(`test_a_crashed_claim_that_relinked_docs_is_still_re_cut`), the
one-extra-mid-file-byte conviction (now pinned as its own test) and the
non-relink conviction staying green throughout. Module suites: 148 passed in
44.45s
<!-- fig: cmd="python -m pytest -q tests/test_integrate.py tests/test_spec_move.py tests/test_handback.py" rev=3844cfd9 -->.
Smoke tier 616 passed / 6 skipped in 11.57s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=3844cfd9 -->;
full suite 1875 passed / 10 skipped in 0:04:41
<!-- fig: cmd="python -m pytest -q -n auto" rev=3844cfd9 -->.

**Judgment calls / deviations.**

- **Finding-3 adjacency judged, LEFT RECORDED** (the spec: take it only if
  the same two reads cover it without new machinery). They do not: the moved
  spec's legitimate destination content is the OUTBOUND rebase composed with
  the inbound relink, `spec_move.expected_relink` covers only the inbound
  half, and the spec pair sits outside the `relinked` loop entirely
  (`_claim_delta` classifies it into `moved_in`/`src`/`dest`; the loop reads
  the SAME path on both sides, the pair needs `tip^1:src` vs `tip:dest`).
  Closing it needs a public outbound oracle in spec_move — new machinery —
  so finding 3 stays recorded in `docs/reviews/WI-393-REVIEW-A.md`, advisory,
  harm direction deletion-only.
- **Registration: none owed — internal of the WI-393 rows.** LLR-145's
  Detail already registers the property ("compares byte-for-byte to excuse a
  crashed claim's own relink writes without widening its conviction to any
  .md edit") and this WI makes that registered sentence true; LLR-140/TC-132
  own the integrate.py claim ladder and TC-132's Evidence
  (`tests/test_integrate.py`) is where all five new tests live. No new row,
  no cell amended.
- **Two guard tests beyond the reviewer's three drives** (new behavior needs
  new tests): the CRLF-checkout genuine-relink excusal (the fairness the old
  fold bought by accident, now held deliberately by `spec_move`'s
  EOL-preserving writes) and the undecodable-parent conviction (the new
  strict-decode branch).
- **integrate.py 2079 → 2103**
  <!-- fig: cmd="wc -l project-trajectory/scripts/integrate.py" rev=3844cfd9 -->
  (+24, mostly the two docstrings stating the property honestly); reviewed
  baseline bump in `tests/test_module_size_ratchet.py` naming this WI.
- **Byte-budgeted docs untouched** (AGENTS.template.md / PROCESS.md /
  PROCESS_OPTIONS.md — no delta owed). `check_docs --stale` stays at the
  pre-existing trunk red of 4 broken links (complete/-archive corners this WI
  never touched).
