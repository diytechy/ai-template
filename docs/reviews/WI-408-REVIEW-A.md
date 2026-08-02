# WI-408 REVIEW-A — independent, hunt-to-break (branch wi-408-… @ 467208df vs ConcurrencyTrainRewrite)

Method: severity-ordered per the intake. (1) THE FIX: re-drove the staging defect
both ways from extracted script trees — `d1dfb07d^`'s `spec_move.py` on the
link-free fixture stages the stale blob, `d1dfb07d`'s stages the working-tree
bytes, SHA-compared — then hunted the three interactions (claim precondition,
abandoned-claim oracle, deleted source) in code and by driving scratch repos.
(2) THE RIDERS: mutation-checked the new `sn_all_ids` pin (one copy altered in
place, watched red, reverted), verified the §8.3 exhibit against the committed
caches by `git show`, read the vacuous-G1 branch behind the `uncovered=`
softening, and drove the §2.1 prose-mention sharp edge through `compute()` on a
scratch spine. (3) THE DOGFOOD: reproduced the close blob and read the reflog
for the construction order. (4) Mechanical: module tests, smoke, strict checks,
figures, ratchet, dupes census, ruff, docs/work delta — all watched on this box.
`docs/log.d/` unread per charter (one targeted `grep -c` existence probe for a
SHA string, zero content read).

1. [MINOR] project-trajectory/scripts/spec_move.py:293 -> the fix's
   unconditional `ac.git(root, "add", "--", dest_rel)` also changes the
   UNTRACKED-source fallback (the WI-287 shape): driven both ways on a scratch
   repo, pre-fix the plain-rename fallback left the destination untracked
   (`?? docs/`), post-fix it is staged as a new file
   (`A  docs/work/complete/WI-9-x.md`). Benign-to-positive in every kit caller
   (the claim requires a clean tree and a tracked queued spec; the handback's
   `new_text` arm always added), and the new docstring's "Both arms end by
   `git add`ing the destination" covers it at the function level — but the
   Deliverable and both commit bodies frame the add purely as the mv-arm
   stale-blob fix, no test pins the fallback's staging in either direction, and
   a downstream CLI user moving a deliberately-uncommitted draft now gets it
   silently staged. Fail direction is visible (`git status`), no content loss.
   Fix: one line in the Deliverable-of-record naming the side effect deliberate,
   and/or a two-assert pin on the untracked fixture. -> @owner
2. [NIT] dogfood verification record -> the builder-quoted staged-blob SHA
   `b68a9d1d73ac` is not reproducible: the close commit's actual spec blob is
   `7125b52e30df83d947bd90a90fb124ebc2ed8b41`
   (`git rev-parse 467208df:docs/work/complete/WI-408-…md`), `git cat-file -t
   b68a9d1d73ac` says "Not a valid object name" in the shared object DB — and
   since `git add` writes blob objects immediately, a blob ever staged in this
   repo would still exist — and the string appears in no tracked surface (0
   hits repo-wide, including a content-unread existence probe of the WI-408 log
   fragment). The dogfood SUBSTANCE verified independently (finding is the
   quote, not the claim — see the dogfood section). Likely a hash taken in the
   builder's scratch reproduction or a transcription slip in the session
   report; nothing durable carries it, so record-hygiene only. -> @owner
3. [NIT] docs/registry-machinery-reference.md:390 -> the §8.3 exhibit is now a
   verbatim quote of a real committed cache (byte-matched here against
   `72587dc1:docs/gate`, the WI-401 close), which is exactly what WI-401
   REVIEW-A finding 1 prescribed — but the doc still nowhere says that `as-of`
   stamps HEAD AT REGENERATION TIME (`derive_gate.py:589`, `rev-parse --short
   HEAD`) while the counts come from the working tree, i.e. a committed cache's
   `as-of` names the commit's parent. A reader who re-does what this review did
   (`git show d35c3b93:docs/requirements/low-level-requirements.csv` → 129 real
   rows, TC → 126) will conclude the exhibit is wrong AGAIN, when it is the
   stamp's semantics — the precise confusion class finding 1 arose from. Half a
   sentence beside the exhibit retires it for good. -> @owner

THE FIX held, re-driven both ways with the SHA compare the builder described.
From extracted trees (`git archive d1dfb07d^` / `d1dfb07d`), the exact field
shape — committed spec whose only links are a fragment and an external URL (so
the rebase half cannot re-add the destination as its own rewrite), an unstaged
`## Deliverable` appended, `move_spec` — gives: pre-fix, staged blob sha256
`0b35ffdfaefa6203` vs on-disk `f9a69a3eeac28394`, Deliverable ABSENT from the
staged copy (the stale pre-edit bytes reproduced verbatim); post-fix, staged ==
on-disk `f9a69a3eeac28394`, Deliverable riding. The shipped test pins the same
contract (`git show :dest` carries the edit AND equals the on-disk file) and the
fix sits where the module's own contract sentence ("never a staged move with
dirty relink residue beside it") always claimed it should: for a linked spec the
destination re-enters `touched` after the rebase and is re-added post-rewrite
(spec_move.py:~360), so the new add cannot strand pre-rewrite bytes either.

The three interactions, hunted and bounded. (a) The claim: `integrate.claim`
runs `_claim_refusal` first (integrate.py:614), whose rung — `if
ac.working_tree_dirty(root): return "the trunk working tree is dirty - a claim
is a clean serial commit"` (integrate.py:539) — genuinely fronts every claim;
`working_tree_dirty` reads full `git status --porcelain` (unstaged, staged and
untracked lines all count, agent_common.py:1215), so no unstaged edit can exist
at claim time and the new add stages bytes identical to the index. (b) The
abandoned-claim oracle: `_claim_delta` (integrate.py:402) classifies the
destination spec as the A of the commit's own move pair (`moved_in, dest =
True, path`) and only `M`-status `.md` paths OUTSIDE the pair enter `relinked`
— the set `_relinked_exactly`/`expected_relink` judges — so the destination's
content is never oracle-compared and the new staging cannot make a genuine
claim convict. (c) Source deleted from the working tree but present in the
index: refused LOUDLY before `_place_moved_file` by the `is_file()` guard
(`"no file to move at …"`, spec_move.py:317) — driven on scratch repos,
identical pre- and post-fix, destination never created, nothing staged. The one
behavior change found outside the defect is the untracked fallback (finding 1).

THE RIDERS held. `sn_all_ids` pin: mutation-checked — `derive_gate.py`'s copy
altered in place to a table-rows-only scrape and
`test_rule_sync::test_sn_all_ids_agrees` failed on the exact regression class
(`AssertionError: SN-001 mentioned in prose, no table row at all — assert
{'SN-001'} == set()`), then reverted (tree clean). The pin's semantics asserts
are real teeth: whole-text (prose == table row), draft-section ids in, only
`-000` out. §8.3 exhibit: now byte-identical to the committed
`72587dc1:docs/gate` (`SN=25 SR=136 LLR=130 TC=127 … uncovered=0 computed=G3 …`
/ `computed 2026-08-02 (as-of d35c3b93)` / `G3`) — the "paste the final
committed cache line" fix finding 1 asked for, taken exactly (residual stamp
subtlety filed as finding 3). `uncovered=` softening: accurate — `_raw_level`
returns `G1` at `if not srs:` (derive_gate.py:263-ish) BEFORE the `min()` that
includes `sn_gate`, so with zero real SRs the count is nonzero with nothing
capped, precisely as §8.3 and the `compute()` comment now say. §2.1 sentence:
present ("an SN id mentioned only in ratified *prose* and cited by no SR caps
the derived gate at G0 … exactly as an uncovered table row does") and DRIVEN
true on a scratch spine through this tree's `compute()`: one Verified SR
covering SN-001 plus a prose-only ratified SN-002 → `raw=G0, uncovered=1,
gate=G1`; control without the prose sentence → `raw=G3, uncovered=0`.

THE DOGFOOD substance verified; the quoted SHA is finding 2. The close commit's
spec blob (`7125b52e30df…`) carries this exact Deliverable — and since a commit
snapshots the index, the committed blob IS the staged blob at close, so "the
destination's staged blob …contain[s] this text" is proven by the commit
itself. Construction order from the reflog: branch cut at dd3947ff → ONE work
commit d1dfb07d (the fix already in the tree) → ONE close commit 467208df, no
resets, no amends — so the close move ran the fixed ritual, and with the
pre-fix code an unstaged Deliverable would have needed exactly the amend the
reflog does not show. "No pre-stage" is not strictly provable post-hoc
(staging leaves no history), but every observable is consistent with the
claimed ritual and nothing contradicts it.

Mechanical re-runs on this box (HEAD 467208df): `tests/test_spec_move.py` 17
passed in 0.60s (Deliverable: 17 — matches); `test_rule_sync` +
`test_derive_gate` 37 passed (matches); smoke 627 passed / 2 skipped in 10.59s
(build commit's 623/6 is the same 629 total under the environment-variant skip
split prior reviews recorded); `check_trajectory --strict` rc=0 with zero
R-A/R-F lines (Deliverable-iff-terminal and spec-lifecycle rungs silent);
`check_doc_refs --strict` rc=0; `check_figures` OK — 50 declared figure(s),
every one carrying command and revision; spot-check re-drive of the spec's
`tests/test_spec_move.py` figure reproduced its 17. `derive_gate --check` rc=0
(gate up to date, G3). Size ratchet: `wc -l` 2930 == baseline 2930 exact, with
a dated, reasoned +11 stamp naming the rider. Dupes: `check_dupes --src
project-trajectory/scripts --allowlist docs/dupes-allow` OK over 49 files;
census 20 → 21 stamped with the new `5d6159709c2c` derive_gate==trace row and a
dated comment; `test_dupes_census_audit` 12 passed. Ruff lint + format clean on
all six changed .py files. docs/work delta across the whole branch
(7a893e7e..467208df) is exactly the WI-408 pair (`D queued/… / A complete/…`);
the work commit touches no docs/work path.

I re-drove the field defect red and green with the builder's own SHA-compare,
bounded all three named interactions in code and on scratch repos, killed a
mutation against the new pin, byte-verified the exhibit against the cache it
quotes, and drove both doc claims live. The fix is one line at the one site the
module's own contract always implied; the findings are a silently-changed
fallback staging (unpinned, undisclosed), an unreproducible SHA in the
builder's verification quote, and the half-sentence that would stop §8.3's
as-of trap from firing a third time.

VERDICT: APPROVE findings=3
