# Decisions taken without consulting the owner — 2026-08-29

**Why this exists.** The owner ruled `OI-66` (a) GO and directed this session to
take its own decisions, escalate anything high-risk to a cross-family reviewer,
and file the decisions needing review as their own document. This is that file.

**How to read it.** Each entry states what was decided, what the alternative was,
why this one was taken, and **what it would cost to reverse**. Ranked by how much
a different answer would change. Nothing here is a ruling — every one is
reversible, and the ones that would be expensive to reverse say so.

---

## 1. The `Contracts:` marker grammar is now anchored, and adopters can lose declarations

**Decided:** the marker must OPEN its line *and* parse as `Contracts:` followed
by a comma- or semicolon-separated `IF-###` list.

**The alternative:** target the negation specifically (refuse a line containing
"No", "not", …).

**Why not:** negation is unbounded — "does not declare", a quoted example, a
historical note — and each spelling recreates the defect. The reviewer agreed:
declaration syntax should be structural.

**What it costs adopters.** A module whose marker sits mid-line, or whose id list
uses an unrecognised separator, **stops declaring**. This is a real behaviour
change on a shipped grammar. Mitigations taken: both lossy forms are reported by
name (`check_trajectory`), the `RESYNC_PACK.md` entry carries a search recipe,
and the separator set was widened to `,` and `;` the moment the kit's own tree
proved semicolons were in use.

**Escalated?** Yes — this was the main item raised to OPENAI-SOL. Its verdict was
CHANGE-not-revert: keep line-start, but a warning alone is inadequate. **I went
further than the reviewer asked in one respect and less far in another:** I added
the anchored id-list parse (its finding, not its recommendation) and I did *not*
make the legacy finding blocking. A blocking finding would fail an adopter's
first post-upgrade commit on a form that was legal the day before; warn-plus-
migration-entry is the kit's own posture for every other grammar change.

**Reversal cost:** low. One regex and one helper.

**⚠️ This is the entry most worth a second opinion**, because it is the only one
where an adopter can be worse off after an upgrade than before.

---

## 2. Body opener is `Contract IF-###:`, and four malformed cases HARD-FAIL

**Decided:** bodies open `Contract IF-###:`. A body before the marker, for an
undeclared id, a duplicate, or one carrying an HTML comment raises
`ContractsGrammarError`.

**The alternative:** a bare `IF-###:` opener (my first implementation), and
warn-first rather than hard-fail.

**Why not:** the reviewer demonstrated that a bare id-colon collides with
ordinary docstring prose — `IF-001: legacy identifier retained`, mapping tables,
examples — and I confirmed all four collisions on the real parser. Hard-failing a
form that prose can produce by accident would be indefensible; hard-failing
`Contract IF-###:`, which nobody writes by accident, is safe. That is the trade
that makes the severity choice defensible, and it is why the two decisions are
one decision.

**Note on house style:** this harness warns first and gates under `--strict`
almost everywhere. These four refusals are deliberate exceptions, on the grounds
that they are malformed *explicit syntax*, not a judgement about content.

**Reversal cost:** low, but every already-written body would need re-keying.

---

## 3. A `[generated]` row naming an absent FILE now FAILS — for the whole kit

**Decided:** `staged_divergence` fails when `docs/stack.ini [generated]` declares
a file that git TRACKS and the worktree no longer has. Prefix rows
(`docs/okf/`, `docs/ratify/`) are exempt.

**Why:** every freshness step is vacuous on an absent target — that is what makes
the kit opt-in — so deleting a declared artifact disarmed its own gate silently.
The reviewer raised it against the new artifact; the hole was general.

**Why this is the entry with the widest blast radius.** It changes behaviour for
**all eleven declared artifacts in every adopting repo**, not just the new one. An
adopter who deleted a generated file and left its declaration standing has been
green until now and will go red on upgrade. I judged that correct — that repo's
gate was not running — but it is the change most likely to surprise someone.

**The prefix-row exemption is a judgement call:** `docs/okf/` is legitimately
absent because its dial is off, and I chose to exempt directory rows wholesale
rather than teach the check which dials disable which generator. A dial-aware
check would be stricter and more complex.

**Corrected mid-build, and the correction matters.** The first implementation
failed on *missing*, which fired in every fresh scaffold and broke 18 tests —
exactly the failure the module's own docstring warns about ("a detector that
died in a scaffold would be removed from the floor"). It now fails only on
**tracked but absent**: a file git knows about and the worktree no longer has.
A scaffold's never-created artifact is untracked and says nothing.

**Reversal cost:** low. One block in one function.

---

## 4. The generated reference leads with stated contracts; unstated ones are a compact debt list

**Decided:** stated contracts are the document; declared-but-unstated seams get
one line per module under "Declared, not stated".

**The alternative:** a placeholder paragraph per unstated seam (my first
implementation, 400+ lines), or omitting them.

**Why:** the reviewer's point was right — 135 repeated placeholders bury the
contracts a reader came for, and omitting them hides real debt. The document is
now 88 lines.

**What I did NOT do, and the reviewer asked for:** a separate *coverage finding*
for a declared seam with no body. Today a reference containing almost no contracts
is perfectly fresh and green. That is a real gap; the debt is visible in the
document but nothing fails on it. **Deliberately deferred**, because a coverage
gate would fire on 135 seams the moment it shipped and the cell pass that would
clear them has not run.

---

## 5. "Deliberately no contracts" gets no syntax

**Decided:** a module that does not open a line with `Contracts:` declares
nothing. No `Contracts: none` marker.

**Why:** the registry already knows which modules provide seams. An explicit
"none" would be a second, contradictable copy of that state — the reviewer's
phrasing was that another declaration "could lie". This was the one decision it
returned KEEP on.

**The consequence I accepted:** `handback.py`'s prose denial had to be reworded
so it no longer carries the marker token, or the mid-line detector would flag it
forever. The rewording preserves the meaning exactly.

**Reversal cost:** low.

---

## 6. IF-144 was declared on `check.py`

**Decided:** the cross-cutting reporting protocol's declaring module is
`check.py` — the module an adopter runs, and the one that composes the verdict.

**Why it was a judgement call:** `IF-144` has fourteen providers and a directory
as its `provider` cell. The precedent (`IF-025` on `gen_arch_map.py`, `IF-026` on
`check_stubs.py`) is that a directory-provider row is still declared by one
specific module, so the question was only *which*. `trace.py` was the other
candidate (it owns `exit_code`, and `SR-157` owns the row).

**Reversal cost:** trivial — move one id between two docstrings.

---

## 7. Scope: the 71-row cell pass was NOT run

**Decided:** this slice builds the mechanism and moves two rows as proof; the
other 69 stay in their cells.

**Why:** `OI-66`'s price explicitly left the authoring cost of the cell pass
unmeasured, and it is per-row judgement rather than mechanism. Doing it badly at
speed would produce 69 contracts nobody can trust, which is worse than 69 rows
that have not moved.

**What that means today:** the reference reads as mostly debt — 137 seams
declared, 2 stated. That is the honest picture, and it is why the debt list is a
first-class section rather than a footnote.

**This is the entry most likely to read as "unfinished".** It is a deliberate
stopping point, not an omission, but if the owner expected `OI-66` (a) to include
the content migration then this is the gap.

---

## 8. Two things left broken on purpose

- **`IF-134`/`IF-135` have no declaring module.** They are the git hooks —
  extensionless files a `*.py` scan structurally cannot see. Fixing it means
  widening the scan to non-`.py` sources, which is a bigger change than this
  slice.
- **The reverse check is id-global, not provider-exact.** `IF-021` declared on
  the wrong module passes. The reviewer flagged it; it is a real gap and
  pre-existing.

---

## What I disagreed with the reviewer about

The reviewer called the build "a mechanism prototype, not a complete
implementation of OI-66(a)", and listed the adopter migration as a release
blocker. **Two of its four supporting bullets were already false when written** —
it read the tree before the `PROCESS.md` paragraph and the `RESYNC_PACK.md` entry
landed. The other two (scaffold delivery via `stack.ini.template` and
`bootstrap.py`) are true, and I did **not** act on them: the shipped CLI
reference — the exact precedent this feature mirrors — is *also* absent from both,
because both references are opt-in by design. Matching the precedent is the
consistent choice; diverging from it to satisfy one review would have made the
two references behave differently for no stated reason.

**No arbitration was needed.** Every factual claim the reviewer made was
re-verified here before being acted on, and where it was right (four parser
defects, the presentation problem, the false green) it was right in a way I could
reproduce. The disagreement above is about scope and precedent, not fact.
