+++
id = "WI-403"
title = "The abandoned-claim oracle excuses EOL-only hand edits (WI-393 REVIEW-A finding 1, minted trunk-side at intake per the R3 invariant). DRIVEN, NOT REASONED: the reviewer forged a claim-shaped commit carrying (a) a trailing-newline-only edit and (b) a whole-file CRLF relay in an otherwise-relinked doc, and _abandoned_claim excused BOTH (returned True, branch destroyed with the edit) while one mid-file byte correctly convicted - because _relinked_exactly's two reads go through ac.git, whose text-mode output is .strip()ed, so byte-for-byte is actually stripped-text-for-stripped-text. HARM CEILING, stated honestly: deletion of a whitespace/EOL-only hand edit riding a forged claim-shaped commit - never a false merge and never a false conviction of genuine relinks - which is why the finding was APPROVE-non-blocking and rides its own row instead of a rework. THE FIX IS CONFINED: make _relinked_exactly's two reads binary-clean (git show/cat-file raw bytes, no strip; integrate.py, the oracle clause WI-393 added) so the byte-for-byte claim in its comment becomes literally true. Tests: drive both forged shapes red (excused today, convicted after), keep the genuine-relink excusal green, and keep the one-extra-mid-file-byte conviction green - the reviewer's three drives in docs/reviews/WI-393-REVIEW-A.md finding 1 are the fixture recipe. While in the file, judge (do not silently take) the reviewer's finding 3 adjacency: the oracle never reads the moved spec's OWN content, closable with spec_move.expected_relink over the spec pair - take it only if the same two reads cover it without new machinery, else leave it recorded."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit 3844cfd9. The fix is exactly the specced
confinement: `_relinked_exactly`'s two reads are binary-clean — a new
`_blob_bytes` helper (raw `git cat-file blob`; no text mode, no strip, no
textconv) replaces the `ac.git` text-mode reads, and the compare becomes
`utf8(expected_relink(utf8_strict(parent bytes))) == new bytes`, so the
docstring's "byte-for-byte" is literally the implemented property. A parent
that does not decode as UTF-8 convicts outright (`_rewrite_md_links` skips
such files, so a modification to one cannot be the ritual's write); a genuine
relink on a CRLF checkout still matches because `spec_move` preserves line
endings (`newline=""`).

**Driven red-then-green** on the reviewer's fixture recipe (exact
`_claim_subject`, real `spec_move.move_spec` pair, one commit past trunk):
before the fix the trailing-newline-only edit and the whole-file CRLF relay
were EXCUSED (watched: `2 failed, 5 passed`); after, the same selection is
7 passed
<!-- fig: cmd="python -m pytest -q tests/test_integrate.py -k 'trailing_newline_only or crlf or mid_file_byte or ritual_would_have_skipped or relinked_docs or not_the_relink'" rev=3844cfd9 -->
— both forged shapes convict, the genuine-relink excusal and the
one-extra-mid-file-byte conviction stay green (the latter now pinned as its
own test), plus two guards for the new mechanics (CRLF-checkout genuine
excusal; undecodable-parent conviction). Module suites 148 passed in 44.45s
<!-- fig: cmd="python -m pytest -q tests/test_integrate.py tests/test_spec_move.py tests/test_handback.py" rev=3844cfd9 -->;
smoke 616 passed / 6 skipped in 11.57s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=3844cfd9 -->;
full suite 1875 passed / 10 skipped in 0:04:41
<!-- fig: cmd="python -m pytest -q -n auto" rev=3844cfd9 -->.

**Finding-3 adjacency judged, LEFT RECORDED:** the moved spec's destination
content is the outbound rebase composed with the inbound relink;
`expected_relink` covers only the inbound half and the spec pair sits outside
the `relinked` loop's same-path reads (`tip^1:src` vs `tip:dest`), so closing
it needs a public outbound oracle in spec_move — new machinery, not these two
reads. It stays advisory in docs/reviews/WI-393-REVIEW-A.md.

**Registration:** none owed — internal of the WI-393 rows (LLR-145's Detail
already states the byte-for-byte property this WI makes true; the new tests
join TC-132's evidence file `tests/test_integrate.py`). integrate.py
2079 → 2103
<!-- fig: cmd="wc -l project-trajectory/scripts/integrate.py" rev=3844cfd9 -->;
reviewed ratchet bump names this WI. The frontmatter `specref` is deleted at
close (R-F): the ref was WI-393's review — a shared record, not a per-WI
spec-of-record — so nothing archives.
