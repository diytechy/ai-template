# Rubric — Whole-registry contradiction audit (WI-206)

**Adjudicates:** the driven, recurring **old-vs-old** sweep the change-scoped
reviewer net structurally misses — contradictions between rows that both predate
any diff, and interpretation drift accumulated across many individually-sane
amendments. Judges the **standing registry as a whole**, all-vs-all, not one
diff. The continuous per-commit sweep (the embedded `REVIEWER_PROMPT`) is
untouched; this is its phase-close complement.
**Used by:** an independent whole-registry audit session — the WI-206 occasion
wired in PROCESS_OPTIONS ("Trajectory / work-items layer", Phase cadence), at
phase close (with the gate bar) and before G-Final.

**Scope.** All-vs-all over the **SN** rows
([`stakeholder-needs.md`](../requirements/stakeholder-needs.md)) and **SR** rows
([`system-requirements.csv`](../requirements/system-requirements.csv)); pull in an
**LLR/TC** row only where it *restates* a limit or attribute (a bound, default,
or vocabulary) an SN/SR also states — the audit is about meaning-level conflict,
not decomposition depth.

**Redaction (state it, it is load-bearing).** The auditor reads **only the
registries above + this rubric** — never `status.md`, `log.md`, the `docs/specs/`
session notes, or any self-assessment. A leaked narrative collapses an
independent reviewer's finding rate; the registry rows are the whole context.

## Anchors

**C1 — Direct contradiction.** Two rows cannot both hold: one requires what
another forbids, or asserts a fact its counterpart denies. *Bad:* SR-a mandates
fail-closed on a missing tool while SR-b mandates best-effort continue for the
same tool. The tripwire is a reader who tries to satisfy both and can't.

**C2 — Semantic overlap / double-home.** Two rows **own the same meaning** — the
[anti-duplication rule](../../project-trajectory/PROCESS.md#3-traceability--anti-duplication) ("one
fact, one home") applied to *meaning*, not text. *Bad:* two SRs each declare the
same limit in their own words, so an amendment can move one and leave the other
stale. *Good:* one owns it; the other references it by id. `check_dupes` catches
token overlap; a re-worded double-home is reviewer-class.

**C3 — Attribute / limit conflict.** Incompatible numbers, bounds, defaults, or
vocabularies across rows that constrain the same quantity: 8192 vs 4096 for one
budget, a default `human` in one row and `agent` in another, one term enumerated
with a value another row's enum omits.

**C4 — Drifted interpretation.** One term used in **incompatible senses** across
rows — "phase" as delivery version in one, lifecycle stage in another; "track"
as workstream vs. parallel lane. Each row is locally sane; the *set* is
incoherent because the word drifted.

**Severity.** A C1/C3 conflict that makes the spec genuinely unsatisfiable is
**BLOCKER**; a real but non-blocking overlap or drift is **MAJOR**; a wording
ambiguity that sharper SN/SR language would resolve — not a defect — is **MINOR**
(the "for clarity" grade the continuous sweep uses).

## Verdict

The auditor writes `docs/reviews/NNN-AUDIT.md` (the CRITIQUE verdict-file idiom),
one finding line per issue in the `log.md` block format, then **exactly one**
machine line:

```
- [BLOCKER|MAJOR|MINOR] <row-id vs row-id> -> issue -> the concrete change -> @owner
VERDICT: APPROVE|CHANGES-REQUESTED findings=N
```

**Disposition.** Findings route as **WIs / registry amendments through normal
change-intake** ([PROCESS.md §5](../../project-trajectory/PROCESS.md)); the audit **never edits the
spine itself** — it records the verdict and stops. `APPROVE findings=0` closes
the occasion; any finding is `CHANGES-REQUESTED` and the intake triage decides
each row's fix or explicit disposition.
