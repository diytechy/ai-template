+++
id = "WI-520"
title = "One home for the credential class vocabulary: the hook scanner and the transcript redactor disagree both ways"
specref = "docs/plans/2026-08-25-remap-alignment.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "high-risk"
priority = 1
+++

## Context

Filed by `WI-508`'s alignment pass. This is the divergence **both** blind
derivations predicted from the requirements alone — A merged the classes into a
foundation module and B into the content guard, and both cited `SR-176`'s own
rationale as evidence that the duplicated class list had *already* diverged in
the field. The alignment pass then measured it, and it is worse than the
requirement records.

### The measurement — driven, not inferred

Two credential-pattern sets exist, compiled independently in two modules:

- `project-trajectory/scripts/check_privacy.py` — `KEY_RE` + `TOKEN_RES`
  (`LLR-017`/`LLR-018`, realizing `SR-017`/`SR-018`): the hook floor that
  refuses a commit or push.
- `project-trajectory/scripts/agent_common.py` — `_SECRET_RES`
  (`LLR-177`, realizing `SR-176`): `redact_secrets`, applied before a session
  transcript is committed to tracked history.

Driven against five samples, **four disagree, in both directions**:

| sample | hook scanner | transcript redactor |
| --- | --- | --- |
| PEM private key block (`-----BEGIN RSA PRIVATE KEY-----`) — privacy-ok: a documented example of the pattern class, not a key | catch | **MISS** |
| `Bearer <30 chars>` | **MISS** | catch |
| `ghp_` + 36 chars | catch | catch |
| `ghp_` + 24 chars | **MISS** | catch |
| `sk-` + 22 chars | **MISS** | catch |

fig: cmd="load check_privacy and agent_common by path, then evaluate KEY_RE + TOKEN_RES against _SECRET_RES over the five samples in the table" rev=754870db

**The first row is the one that matters, and it inverts the protection.** A PEM
private-key block is refused at the commit hook and passes **unredacted into a
committed transcript** — so the durable artifact is less protected than the
ephemeral one. `SR-176` exists precisely because "the finding record is the one
artifact guaranteed to contain the personal data it reports"; a redactor that
does not know a class its sibling scanner compiles is that hazard with a
different subject.

The threshold rows are the ordinary cost of two hand-maintained lists: the
redactor matches at 20 characters where the scanner requires 24 or exactly 36,
and the scanner anchors on non-token boundaries the redactor does not. Neither
set is a superset of the other.

### The original rationale, read first — and what it does and does not license

`redact_secrets`' own docstring says it is **"deliberately imperfect — unknown
token shapes pass through, and the raw unredacted stream stays in gitignored
`out/run-logs/` for debugging."** That is a real, recorded design decision and
this row does not overturn it: best-effort redaction stays best-effort, and the
gitignored raw stream stays.

What it does **not** license is the gap this row fixes. A PEM private key is not
"an unknown token shape" — it is a known class with a compiled pattern in a
sibling module of the same package. The docstring argues for accepting the
patterns nobody has written; it does not argue for ignoring the ones already
written twenty files away.

### Done when

1. **One home for the class vocabulary.** The pattern table — class name and
   pattern — lives in exactly one module, and both the scanner and the redactor
   read it. A pure pattern table has no dependencies, so the shipped helper
   package is the natural home; that keeps `agent_common` from importing a
   checker, which would be a new and unwanted edge.
2. **The union is deliberate, per class, and recorded.** Each class is present
   or absent on each side by a written decision, not by which list it happened
   to be added to. The redactor's threshold may legitimately stay looser than
   the scanner's (over-redacting a transcript costs a reader nothing; a
   false-positive commit refusal costs a contributor a lot) — but that
   asymmetry must be STATED, not left as a side effect of two literals.
3. **The PEM class reaches the redactor.** That is the one gap with a concrete
   disclosure path, and it is the row's minimum.
4. **A test drives the two sides against a shared sample set** and fails when
   they disagree on a class either side claims. The table above is the starting
   fixture. Asserting that one list "contains" the other is NOT the test — the
   thresholds differ deliberately, so the pin is on class coverage.
5. **The declared behaviour is unchanged where it is already right:** the hook
   still refuses, the redactor still lets unknown shapes through, and
   `SR-176`'s never-by-value rule is untouched.

### Watch for

- **`agent_common` must not import `check_privacy`.** The scanner is a checker;
  `agent_common` is imported by the loop and by many siblings. The extraction
  goes down into the shared package, not sideways.
- **The kit ships both modules**, so a new shared module is a `MAPPING` row, a
  `tests/test_bootstrap.py` file-list entry and a `RESYNC_PACK.md` entry.
- **`tests/test_rule_sync.py` pins duplicated literals across modules.** Check
  whether either pattern set is already pinned there before moving it; a pin
  whose subject moves must move or die in the same commit.
- Priority is `1` and `safety_class` is `high-risk` because the failing
  direction publishes a credential into tracked history.
