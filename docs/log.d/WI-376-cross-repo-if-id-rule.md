## 2026-07-31 — WI-376: the cross-repo IF-ID rule stops contradicting MULTI_REPO

**One line:** `INTERFACES.template.md`'s rules list told every adopter to
reuse identical `IF-` ids across repos — the exact collision MULTI_REPO.md
§3.3 exists to prevent, and the template's own worked snippet already did
the opposite; the bullet now states the repo-local rule, the qualified
reference form, and the honesty caveat.

**The defect (field-motivated):** an old multi-repo adoption (the homelab
group) hit IF- designation confusion across independent repos. The research
sweep found why: the scaffolded template's "Both sides reference the same
`IF-ID`" bullet mandates deliberate id collision, while MULTI_REPO.md §3.3
and EXAMPLE.md's multi-repo note state ids are owner-local with `CIF-###`
as the coordinator handle — two shipped rules that cannot both be followed,
and the wrong one ships in the file every repo scaffolds as
`docs/interfaces.md`. The no-coordinator peer case (two repos, no CIF
catalog) had no stated form at all, and `trace.py`'s `^IF-\d+$` integrity
pattern silently forbids any qualified id in the `IF-ID` column.

**The fix (one bullet, replacing the wrong one):** ids are repo-local; the
two ends of one contract carry different local ids (as the snippet shows);
a foreign seam is cited as the qualified pair (counterpart repo / `REPO-###`
+ its local `IF-###` + pinned version) in `Counterpart` + `Contract`/`Notes`,
never in the `IF-ID` column; under a coordinator the stable handle is
`CIF-###` (linked to MULTI_REPO.md §3.3); and the honesty note that no tool
validates the far side — it is a text convention.

**Not changed:** MULTI_REPO.md (already right), EXAMPLE.md (already right),
the registry template (no schema change — the qualified pair lives in
existing free-text cells), `trace.py` (the anchored pattern is correct;
qualification belongs in prose cells).

**Bars:** commit bar green (smoke standing-red only + check_docs OK); no
budgeted file touched.
