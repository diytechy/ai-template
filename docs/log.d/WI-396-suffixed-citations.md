## 2026-08-01 — WI-396: a line-suffixed citation is the path it names

**Summary.** `check_doc_refs` decided path-shape by extension-suffix OR
prefix-list. A trailing `:40` / `:40-41` defeats the extension test, so every
suffixed token fell through to `PATH_PREFIXES` — a list of the *downstream*
layout (`registries/`, `skills/`, `ci/` appear there **without** the
`project-trajectory/` prefix they actually live under here). A suffixed
reference into `project-trajectory/`, the tree the kit's own product lives in,
therefore reached **no bucket at all**: not dangling, not untraced, never
classified. The suffix is now stripped before the shape test **and** before the
stat.

**Deliverables.**

- `project-trajectory/scripts/check_doc_refs.py` — `LINE_SUFFIX` +
  `_strip_line_suffix`, applied at **both** call sites: the predicate
  (`is_path_shaped`) and the resolver (`path_findings`, which derives `clean`
  from the stripped token before the stat, the untraced classification and the
  declared-absences lookup). Findings still quote the token as written.
  `PATH_PREFIXES` is untouched — stripping fixes every prefix at once, which is
  why the plan preferred it to a tenth entry.
- `tests/test_check_doc_refs.py` — four tests. The verdict pin
  (`…reaches_the_same_named_verdict_both_clean`, which also asserts a **zero**
  untraced count, so a later change that made the kit half pass by *exemption*
  rather than by resolving would fail it); the **mutation twin**
  (`…diverges_when_either_half_is_broken`, both directions); and two edge pins
  (a suffixed citation to a missing file still gates; only an all-digit trailing
  suffix is stripped).
- `project-trajectory/README.md` — the kit-contents row names the new shape.
  This is downstream-visible: an adopting repo citing a **deleted** file *with a
  line number* now reds under `--strict` where it was silent.

**Driven figures** (lane `wi-396`, at the pre-fix tip `19fddb7a`, command
`python project-trajectory/scripts/check_doc_refs.py --root . --strict`, with
`docs/test/report.md` generated first — see the finding below):

| run | dangling | untraced |
|---|---|---|
| before, clean | 0 | 928 |
| before, with a probe naming both halves `path:40-41` | **1** | **928** |
| half-fix (predicate only — the WI-394 trap, driven not inherited) | 0 | 971 |
| after, both sites | 0 | **829** |

The probe row is the defect: one half convicted, the other invisible, and the
untraced count unmoved. The 928 → 829 drop is suffixed citations to **live**
files that had been counted as explained-missing.

**Deviations from spec.** None. The row left the fix open between
"strip the suffix" and "add `project-trajectory/` to `PATH_PREFIXES`"; the first
was chosen, so the pinned verdict is BOTH CLEAN rather than BOTH DANGLING.

**Byte deltas on budgeted files.** None — `AGENTS.template.md`, `PROCESS.md` and
`PROCESS_OPTIONS.md` are untouched.

**Findings recorded as prose** (no id minted on a work branch — owner ruling R1):

1. **`check_doc_refs --strict` cannot pass on a fresh lane worktree.**
   `docs/test/report.md` is a generated, gitignored artifact that `README.md`
   cites twice; a new worktree does not have it, so a standalone run reads
   3 dangling until `trace.py` has run. It is invisible in the primary checkout
   (where the file exists) and invisible inside `check.py` (where the trace step
   runs first). A lane builder who runs the step alone reads a red that is not
   theirs. Candidates: teach the step to depend on the generator, or declare the
   generated report the way `docs/declared-absences` declares everything else.
2. **LLR-038's `Detail` describes the shape rule without the suffix clause.**
   Not false — a stripped token still needs an extension or a prefix — so it is a
   spine amendment for WI-390's batch, not an ordinary row's to take.
3. **The claim refused on trunk residue that was not session residue.** A single
   editor-preference line in `.vscode/settings.json` (the owner's, uncommitted)
   made `integrate.py claim` refuse. It was parked in a named `git stash` and
   restored after the merge. The refusal is right; worth noting that "dirty
   trunk" and "unfinished work" are not the same set.

**Bars.** The branch's `Bar-Green:` refresh trailer and this row's REVIEW-A
carry the figures with the commands and revisions that produced them.
