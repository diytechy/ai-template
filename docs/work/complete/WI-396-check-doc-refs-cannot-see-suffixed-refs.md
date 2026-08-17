+++
id = "WI-396"
title = "`check_doc_refs` silently cannot see a SUFFIXED reference into `project-trajectory/` - the half of this repo that IS the product. DRIVEN, not reasoned: `is_path_shaped('project-trajectory/work/WI-000.template.md:40-41')` is False while `is_path_shaped('docs/work/queued/WI-000-example.md:40-41')` is True, and the counter proves the consequence - writing BOTH as `path:line` reports `1 dangling - 887 untraced`, the same 887 a clean run reports, so the shipped token was never counted in ANY bucket. It is not classified as kit-relative and exempted; it never reaches classification at all. MECHANISM (`check_doc_refs.py`, the `is_path_shaped` return at line 155): a token is path-shaped if it `endswith(PATH_EXTS)` OR `startswith(PATH_PREFIXES)`. Append `:40-41` and nothing ends in an extension any more, so everything turns on PATH_PREFIXES (lines 87-98), which enumerates the DOWNSTREAM layout: `scripts/`, `docs/`, `src/`, `tests/`, `.githooks/`, `.github/`, `registries/`, `skills/`, `ci/`, `hooks/`. The tell that this is the downstream layout and not an oversight of one entry: `registries/`, `skills/` and `ci/` are the KIT's own subdirectories, listed WITHOUT the `project-trajectory/` prefix they actually live under in this repo. So this is an ACCIDENTAL BLIND SPOT, not a deliberate exemption - the kit-relative rule is sound, but it only ever fires on tokens that are ALREADY path-shaped and resolve under the kit root, so it neither defends nor can close this gap. THE HONEST LIMITER, which keeps this small: `project-trajectory/` does not exist downstream - it is the directory an adopter COPIES FROM, not one they carry - so no adopting repo inherits the gap and no downstream bar is weakened. It bites THIS repo only, and only for suffixed references. That is still worth fixing here, because `project-trajectory/` is precisely where the kit's product lives, so the one tree where the blind spot exists is the tree whose product references go unchecked. WORKED EXAMPLE: WI-391 cited `docs/work/queued/WI-000-example.md` and `project-trajectory/work/WI-000.template.md` with a `:40-41` suffix on each, in one sentence naming two byte-identical halves of a dogfooded pair; --strict convicted the first and was structurally blind to the second, and the fix that satisfied the checker (move the line numbers into prose) happened to correct both, which is exactly how a blind spot stays invisible. THE ROW YOU ARE READING TRIPPED IT AGAIN while describing it - this sentence originally carried both suffixed forms, --strict convicted only the `docs/` one, and the asymmetry reproduced verbatim inside the row that documents it. Third occurrence on one branch. THE CONVENTION IS SURFACE-SCOPED, NOT REPO-WIDE - state it precisely or this row licenses churning every review file in the repo: `RECORD_PREFIXES` exempts `docs/log.md`, `docs/archive/`, `docs/reviews/`, `docs/plans/`, any `docs/repo-review-…` file and `docs/test/report.md`, so a `path:line` citation is perfectly legal there and this row's own REVIEW file uses the form dozens of times, correctly and with no consequence. Keep-it-out-of-the-path-token applies only to the surfaces the checker actually inspects. THE ADJACENT FACT, which is the evidence for the whole row because it explains the FIRST occurrence: `docs/log.md` is a record surface but `docs/log.d/` is NOT - the prefix tuple carries the compiled file, not the fragment directory - so the identical citation is LEGAL in `log.md` and ILLEGAL in the fragment that becomes `log.md` on the next trunk step. A writer cannot tell those two apart by looking at what they are writing. SCOPE, deliberately small: decide whether a suffixed `path:line` token should be path-shaped at all (the alternative is stripping a trailing `:<line>` / `:<line>-<line>` before the shape test), and if it should, add `project-trajectory/` to PATH_PREFIXES so the kit's own tree is covered. DONE-WHEN, and it must NAME THE VERDICT rather than only assert equality: the two byte-identical halves of a dogfooded pair, cited with the same suffix, must reach the SAME NAMED outcome - which outcome depends on the fix chosen (strip-the-suffix and suffixed-is-never-a-path both yield BOTH-CLEAN; adding `project-trajectory/` to PATH_PREFIXES yields BOTH-DANGLING), so the ruling fix determines the verdict the test pins. Equality alone is not enough for two reasons: three different fixes all satisfy it, and it cannot fail if the tool stops examining either half. So the guard needs the MUTATION TWIN this repo's WI-353 discipline already requires - break one half and assert the pair DIVERGES - which is what proves the test is still looking. Note why an absolute assertion cannot substitute: the defect is a DIFFERENTIAL, and both `a suffixed path is dangling` and `a suffixed kit path is not dangling` pass TODAY, so either one would ossify the bug as intended behaviour. Do NOT widen this into a general path-token rewrite."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

RULED: **strip the trailing line suffix**, the direction
[docs/archive/history/backlog-plan-2026-08-01.md](../../archive/history/backlog-plan-2026-08-01.md) row 2
prefers — one rule that fixes every prefix at once, rather than a tenth entry in
`PATH_PREFIXES` that would only ever cover the one tree somebody happened to
cite. `PATH_PREFIXES` is untouched; it stays a list of layout conventions.

THE VERDICT THIS PINS, named rather than merely asserted equal: **BOTH CLEAN**.
Once the suffix is off, each half of the dogfooded pair resolves on disk, so
neither is DANGLING and neither is EXCUSED as kit-relative —
`test_a_suffixed_pair_reaches_the_same_named_verdict_both_clean` asserts a
**zero** untraced count for exactly that reason, which is what would fail if a
later change made the kit half pass by exemption instead of by resolving.

TWO CALL SITES, because a predicate cannot hand a rewritten token back:
`is_path_shaped` strips before the extension/prefix test, and `path_findings`
derives `clean` from the stripped token before the stat, the untraced
classification and the declared-absences lookup. The finding still quotes the
token AS WRITTEN so a reader can find it in the doc. The half-fix was driven
here, not inherited from WI-394's measurement of it: the three new guard tests
go red against it, and on this repo it reads 971 untraced against 829 for the
full fix — 142 live files reclassified as explained-missing.

THE GUARD IS A MUTATION TWIN (WI-353), not an equality.
`test_the_suffixed_pair_diverges_when_either_half_is_broken` deletes each half
in turn and asserts the pair DIVERGES (broken → `DANGLING`, intact → `CLEAN`),
which is what proves the tool is still examining both; equality alone passes
trivially when the tool stops looking, which is the defect itself.

MEASURED, `check_doc_refs.py --root . --strict` on the lane tree: **0 dangling
before, 0 dangling after** — no prose repair is owed anywhere in this repo — and
untraced **928 → 829**, the drop being suffixed citations to LIVE files that had
been counted as explained-missing. Before the fix, a probe naming both halves
read `1 dangling · 928 untraced` beside a clean run's `928 untraced`: the kit
half was in no bucket at all.

DOWNSTREAM-VISIBLE, stated rather than implied: an adopting repo whose live
prose cites a DELETED file *with a line number* now reds under `--strict` where
it was silent. The kit-contents row in `project-trajectory/README.md` names the
new shape; the module docstring (which is also `--help`) states the rule.

NOT IN SCOPE, deliberately: the general path-token rewrite the row forbids, and
the spine cell LLR-038's `Detail`, which describes the shape rule without the
suffix clause. It is not FALSE — a stripped token still needs an extension or a
prefix — so it is a spine amendment for WI-390's batch, not this row's to take.
