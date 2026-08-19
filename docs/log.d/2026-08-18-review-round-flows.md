## 2026-08-18 — the flows gate could not fail on a doc named "Runtime flows" (review finding M1)

**The defect.** `check_flows.flows_section` selected the FIRST heading whose
title merely *started with* "runtime flows", at ANY level, and ran the section
to the next heading of the same-or-higher level. Both flows docs in existence
are TITLED for the section they contain — this repo's
`docs/runtime-flows.md:1` (`# Runtime flows — the kit meta-repo
(self-adoption)`) and the shipped `RUNTIME_FLOWS.template.md:1` (`# Runtime
flows (authored at DevStg-Tests)`). So the H1 title shadowed the real `##
Runtime flows` section, and with no later level-1 heading the "section" was the
**whole file**. The DevStg-Tests gate therefore could not fail on any document
named for the obligation: delete the flows section outright and the check still
passed as long as one id-citing mermaid block survived anywhere in the doc.

**Measured before/after**, on scratchpad copies of the real doc with the entire
`## Runtime flows` section (all four flows) deleted and one unrelated mermaid
block grafted into *Shape of the product*:

| fixture | before | after |
| --- | --- | --- |
| real doc, unchanged | `OK - 4 flow diagram(s), 40 ids` | `OK - 4 flow diagram(s), 37 ids` |
| section deleted, H1 still "Runtime flows…" | **`OK - 1 flow diagram(s)`** (false green) | `FAIL - no "Runtime flows" section heading` |
| section deleted **and** H1 renamed | `FAIL` | `FAIL` |

The middle row is the finding. The third row is the reviewer's isolation: only
the H1 title kept the old check green. (The 40→37 id drop on the unchanged doc
is the same bug's other face: ids cited in the intro and *Shape of the product*
were being validated as though they sat in the flows section. They are now out
of scope, which is what the check claims to do.)

**The rule now.** The document's own TITLE never counts as the section — the
first heading in the file is skipped, and among the remaining candidates an
exact `Runtime flows` heading wins over a longer `Runtime flows …` one, ties
going to file order. The section still runs to the next heading of the same or
higher level, and severity is untouched (still a hard fail at the DevStg-Tests
bar). The alternatives considered were: pin the section to a fixed level (`##`)
— rejected, it dictates an adopter's document shape; prefer exact over prefix
alone — rejected, it re-shadows the moment a doc titles itself exactly
"Runtime flows"; take the deepest/last match — rejected, it still falls back to
the title when the section is *gone*, which is the whole finding. Skipping the
title is the only rule that makes a **deleted section** unrepresentable as a
pass, and it reads as one sentence: *a doc named for the section must still
contain the section.*

**The template shipped the shadow**, so a scaffolded repo was born with a dead
gate. `RUNTIME_FLOWS.template.md` now carries a document title (`# Runtime
flows — <project> (authored at DevStg-Tests)`) plus a real `## Runtime flows`
section above the example diagram, mirroring this repo's own instance. The
authored flow content is byte-identical; only the heading structure moved.
`docs/runtime-flows.md` needed no change — it already had the H2 the H1 was
shadowing.

**The tests could not have caught it.** The WI-455 merge re-pointed every
positive case onto `"# Runtime flows\n" + FLOWS_OK` — the shadow shape, where
the H1 *is* the section — and the negatives onto a non-shadowing `"# Doc\n"`.
No assertion was weakened; the fixture shape simply removed the doc-title layer
the bug lives in. Fixtures now use a real title + section, and
`test_titled_runtime_flows_with_deleted_section_fails` plants the reviewer's
exact scenario. Both directions observed: against the pre-fix
`check_flows.py` it fails with `AssertionError: check_flows: OK - 1 flow
diagram(s), 2 requirement id(s) cited, all known.`; against the fix it passes.
Two more cases pin the chosen semantics (exact heading beats a longer prefix
sibling; a section under an unrelated document title still resolves).

**Verified.** `check_flows.py` on the real repo: `OK - 4 flow diagram(s), 37
requirement id(s) cited, all known.` A fresh `bootstrap.py --dest` scaffold:
`OK - 1 flow diagram(s)`, and deleting that scaffold's `## Runtime flows`
section (leaving the title and a stray mermaid block) now FAILs — the shadow is
not shipped. `pytest -q tests/test_check_flows.py tests/test_bootstrap.py
tests/test_dogfood_sync.py` → 103 passed, 1 skipped; `tests/test_registry_checks.py
tests/test_complexity_ratchet.py` → 27 passed; `ruff format --check` and `ruff
check` clean on both touched files.

### Proposed RESYNC_PACK entry (NOT applied here — that file is another lane's)

An adopter who already followed the previous entry ("MOVE your authored
'Runtime flows' section there, heading included") may have landed a doc whose
only "Runtime flows" heading is its H1 title. That repo's `design-flows` step is
green and unfailable today, and after this change it flips to a hard FAIL — so
the range needs an entry. Exact text proposed:

> ### The flows gate stops matching your document TITLE [since <landing sha>]
>
> `check_flows.py` used to select the first heading whose title *started with*
> "Runtime flows", at any level. In a doc **named** for the section — which is
> how `RUNTIME_FLOWS.template.md` shipped, and what the architecture-retirement
> entry above told you to build — the H1 title shadowed the real section and ran
> to end-of-file. The gate could not fail: delete your entire Runtime-flows
> section and the step stayed green so long as one id-citing mermaid block
> survived anywhere in the doc.
>
> **The document title no longer counts as the section.** The first heading in
> `docs/runtime-flows.md` is skipped; the section is a matching heading *inside*
> the doc (an exact "Runtime flows" wins over a longer "Runtime flows …").
>
> - **Check your `docs/runtime-flows.md` shape.** If its only "Runtime flows"
>   heading is line 1, the step now fails with `no "Runtime flows" section
>   heading`. Fix: keep line 1 as the document title (name your project in it)
>   and add a `## Runtime flows` heading above your first diagram — the shape
>   `RUNTIME_FLOWS.template.md` now ships. No diagram content changes.
> - **Content outside the section is no longer scanned.** Ids cited in an intro
>   or a neighboring section are neither counted nor validated now (they never
>   should have been). If a diagram relied on the doc-wide sweep to look green,
>   move it under the section, where it belongs.
> - This is a **hard fail at the DevStg-Tests bar** — unchanged severity, only
>   the selection rule moved. A repo below that bar pays nothing.
