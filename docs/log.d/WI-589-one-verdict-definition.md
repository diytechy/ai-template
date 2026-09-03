## 2026-09-03 — WI-589: the one verdict definition, actually singular (the unpinned `REVIEW_PHASES` duplicate and the undeclared `score_reviews` seam)

Two defects verified while reading the WI-586 chain and queued at its merge
(the verdict this continues is
[`../reviews/wi-586-adjudicate-llr-207-llr-208/009-ADJUDICATE-082b9e1.md`](../reviews/wi-586-adjudicate-llr-207-llr-208/009-ADJUDICATE-082b9e1.md)).
Neither was a fault in the four rows adjudicated there, which is why neither
could be cured by returning them. Both are about `IF-175`'s central claim —
that there is exactly ONE definition of the verdict — being true in the
registry and not yet true in the tree.

### 1. The duplicate span and the magic ceiling (`agent_loop.py`)

`agent_loop.py` declared its own `REVIEW_PHASES = ("REVIEW-A", "REVIEW-B")`, a
byte-identical copy of `kitlib/verdict.py`'s, pinned by nothing, and
`_clamped_review_rounds` clamped the reviewer dial with `min(2, rp_int)` — that
tuple's length restated as a literal. **The failure that shape admits, stated
concretely because a duplicate is only worth deleting if it can bite:** add a
`REVIEW-C` to the verdict leaf and `kverdict.declared_phases(3)` returns three
phases while `_clamped_review_rounds("3")` still answers `2`, so the loop
schedules two rounds against a merge slot demanding three — the lane draws what
will not clear, which is the exact wedge `declared_phases`' own docstring says
the shared span exists to prevent ("a policy the two read to different lengths
is a lane that draws what will not clear or refuses what will never be drawn").

Remedy is the kit's settled one (LLR-182: drift is better made unrepresentable
than detected). The local tuple is DELETED — not aliased — and its two use
sites (`NON_BUILD_PHASES`, `draw_session_route`) plus the clamp ceiling read
`kverdict.REVIEW_PHASES`. The ceiling is now `len(kverdict.REVIEW_PHASES)`, so
the three readers move together or not at all. Behaviour is unchanged today
(the span is 2, so every clamp answer is identical) — this buys the future
edit, not a present bug fix.

Pinned in `tests/test_agent_loop_policy.py`:
`test_the_loop_keeps_no_second_copy_of_the_review_phase_span` asserts the
module has no `REVIEW_PHASES` attribute at all (the `not hasattr` shape
`tests/test_seam_resolution.py` already uses for a retired symbol), that the
declared span is inside `NON_BUILD_PHASES`, and that an over-dialled policy
round-trips through the clamp into `declared_phases` as the whole span. The
existing `test_clamped_review_rounds_is_lenient_then_clamped` keeps its
literal-`2` case (that IS the shipped span, and a test that only computes
asserts nothing about today) and gains a `span + 1` case that survives a
change to the tuple.

`tests/test_module_size_ratchet.py` re-stamped agent_loop.py DOWNWARD
2587 -> 2586 in the same commit, per that file's rule.

### 2. The undeclared span reader (`IF-175.requestors`)

`scripts/score_reviews.py:72` holds a hard `from kitlib.verdict import
declared_phases` and calls it in `latest_phase_verdicts`, but no `requestors`
entry named it. Added.

**On the justification, and a correction taken from the lane's own review.**
The minting disposition rested this on `IF-175`'s sentence "a second reader of
round evidence anywhere else is a finding against this row". Round 012 of the
WI-586 lane
([`012-REVIEW-A-51fb3e8.md`](../reviews/wi-586-adjudicate-llr-207-llr-208/012-REVIEW-A-51fb3e8.md),
MINOR) is right that the clause does not establish this omission and, read
carelessly, licenses REMOVING the legitimate import rather than declaring it:
`score_reviews` reads the phase SPAN, not round evidence. So the row's amended
notes rest the naming on the completeness rule — an import no `requestors`
entry carries is an undeclared seam — and keep the round-evidence clause only
where it belongs, in the sentence saying this addition is a requestor and NOT a
fourth reader of the verdict. The remedy the disposition asked for is
unchanged; only its stated ground is.

The `data` cell also now names `REVIEW_PHASES` as a crossing, because after
part 1 the span crosses this seam as a CONSTANT and not only through
`declared_phases`, and the notes say which caller asks it that way.

### Surfaced, not fixed (separate findings, per the working agreement)

- **Nothing detects this class.** `tests/test_seam_resolution.py` checks that a
  seam row's shape is well-formed — owner resolves, exactly one far side, a
  closed channel set — and never joins `requestors` to the modules that
  actually import the owner. So the omission part 2 fixes was invisible to
  every check, and the next one will be too. A detector is buildable (the kit
  already walks imports in `gen_arch_map`/`gen_components`), but it is a new
  mechanism with its own false-positive surface and is outside this row.
- **`LLR-207.code_symbol` omits `REVIEW_PHASES` and `TRAILER_LABEL`** although
  `kitlib/verdict.py`'s `__all__` exports both, and part 1 makes the first of
  them a symbol a second module now imports by name. Deliberately NOT touched
  here: `LLR-207`/`TC-205` are `WI-587`'s scope on this same branch, and two
  sessions editing one cell is the collision the lane discipline exists to
  avoid.
