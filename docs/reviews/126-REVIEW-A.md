# 126-REVIEW-A — the rationale rewrite, the decomposition, and the new rows

**Trigger:** three surfaces had reached the attestation window unreviewed — the
nine fixes applied after the previous review (a fix pass nothing checked), the
six rows added to close the untraced-checker gap, and the 47 cells of S5 that a
premature completion tick had hidden. The owner asked whether any review was
outstanding before grinding through the spine; the honest answer was three.
Dispatched as **one** review over all three rather than three dispatches.

**Critic:** a fresh **OpenAI/`codex`** strong-tier session (`gpt-5.6-sol`),
family-heterogeneous. Sandbox held **only** the BEFORE/AFTER material (~100 KB,
53 items) and the four claims under test. No repo, no commit messages, no spec,
no self-assessment. It was told a previous review of a different batch returned
six findings, and told explicitly **not** to assume this batch clean or dirty.

**Verdict:** `CHANGES-REQUESTED findings=27` over 21 of 53 items — 16 BLOCKER,
11 MAJOR. **All 27 confirmed and fixed.**

The failure class the brief asked it to hunt first — a silently dropped scope
narrowing — is exactly what it found six of.

---

## Dropped normative content (6)

Each is a constraint that existed in the BEFORE cell and appeared **nowhere** in
the AFTER pair. All six widen a claim without looking like a change.

| Item | Lost | Restored as |
|---|---|---|
| `SR-029` | *"the dispatcher, each worker, and an interactive sitting take it"* | the lock's participating scope, back in the rationale |
| `SR-041` | *"path-ok lines are exempt"* | named as the deliberate escape hatch |
| `SR-042` | *"stdlib"*, *"no runtime dependency"* | the implementation boundary, restated |
| `LLR-026` | *"the status.md-resume read is retired"* | the exclusion, not just the positive scope |
| `LLR-104` | `12px/9.5px/13px/13px` | the four measured values |
| `LLR-109` | `sw external/component 8.6, SR/phase[3] 9.5, Interface/phase[7] 10.5` | identities and deltaE, not just the count |

The last two are measurements, which the brief named as legitimate to keep. I
generalised them away while "tidying" — the same instinct the previous review
caught as scope creep, running in the opposite direction.

## False or overreaching reasoning (8)

The more uncomfortable half: **claims I wrote that are not true.**

- **`SR-017`** — *"a committed secret cannot be un-published"*. A local commit is
  not published and history can be rewritten. Rewritten to the claim that
  survives: a credential reaching a shared branch must be treated as disclosed,
  and expunging it is a rewrite every clone must follow.
- **`SR-029`** — the pid-reuse mechanism was **backwards**. A reused pid makes a
  liveness check see a live process and *retain* a dead lock; I wrote that it
  clears a live one. Now states both horns.
- **`SR-018`** — straw man. An always-on identity layer that *kept* the author
  exemptions would not "flag every legitimate authorship line". The real
  objection is that the exemption list is project-specific.
- **`SR-039`** — *"exemptions are fingerprinted and count-aware"* is false of the
  permitted legacy bare file pair, which has no fingerprint. (Inherited from the
  BEFORE text, not introduced here — and still wrong in a row about to be signed.)
- **`SR-042`** — *"cannot disagree with the registries"*. A derived artifact can
  disagree through generator defects or staleness. Narrowed to what holds: it can
  only be **stale**, which `--check` detects.
- **`SR-053`** — *"a build judging its own visual output passes by construction"*.
  It can fail itself. The real argument is shared assumptions, not automatic passage.
- **`SR-109`** — *"which is how that backlog formed"* asserts a cause the
  material never establishes. Replaced with what is defensible: the prose rule was
  the control already in place while the backlog accumulated.
- **`SR-126`** — *"the citation is a second copy that rots"*. A citation is a
  pointer, not a copy.

## Requirement broader than its mechanism (2)

The finding with the longest reach, and it is structural rather than textual.

- **`SR-127`** claimed the checker fails a requirement stating *"more than one
  obligation"*. It counts obligation keywords. Two obligations can share one
  keyword through coordination, and two keywords need not be two obligations —
  **the requirement promised semantics the mechanism cannot deliver.**
- **`SR-128`** guaranteed an advisory for *"a child cell"*, unrestricted, while
  the criteria name two specific relationships.

Both requirements were narrowed to what is actually checked, and `SR-127`'s
rationale now says plainly that each rule is a **lexical proxy** scoped to what
it can decide. A requirement that overclaims is worse than a narrow one: it is
the readout an attestation trusts.

## Incomplete rationale on new rows (8)

Every one of `LLR-133`/`134`/`135` explained a *sub-decision* (why all three
registries, why Draft is skipped, why a separate counter) without ever stating
what breaks if the rule is absent — so each still had to borrow its parent SR's
reason, which is precisely what the contract forbids. `SR-126` never justified
the process-doc half of its own ban. `LLR-135`'s `Detail` did not define the
overlap operation, so two reasonable implementations would disagree; it now names
the denominator.

## Misplaced content (3)

`LLR-055`'s `Detail` still stated T1's one-switch obligation **while declaring T1
had left the row entirely** — internally contradictory, and duplicated ownership
of an anchor. `LLR-100` kept critic-routing governance in `Detail`, where it is
not the mechanism.

---

## The transferable lesson

Three reviews now, three distinct failure modes: **124** found things left behind
when text was removed; **125** found things added when text was rewritten; **126**
found *claims that are simply false* — reasoning that reads fluently and does not
survive being checked.

That third class is the one a self-review cannot catch, because the author
believes the reasoning. It is also the class that gets attested: a wrong
mechanism in a rationale is a wrong mechanism a human then signs. Two of these
(the pid-reuse inversion, the "cannot disagree" guarantee) would have entered the
record as fact.

**The tick that hid the work was the root cause of the exposure.** S5 was marked
done on a gating signal rather than against its own checklist, so 47 cells
reached an attestation window with no review at all. The checklist is the
contract; the green is not.
