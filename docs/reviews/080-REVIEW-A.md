# 080-REVIEW-A — WI-166 (dev-setup.template.cmd — Windows double-click rung)

Independent review of commit `57b199b` (WI-166: ship Windows dev-setup
launcher), built session 079. Reviewed the diff against the spec-of-record
(`docs/specs/owner-intake-2026-07-14b.md#dev-setup-windows`), the WI-166 registry
row (SR-032, `WI-051;WI-160`), the macOS twin it mirrors
(`dev-setup.template.command`), the target it delegates to
(`dev-setup.template.ps1`), the bootstrap `MAPPING`, and the meta-repo dogfood
(`scripts/dev-setup.{cmd,ps1}`). No SN/SR/LLR/TC rows were added or changed
(off-spine `scripts` work; SR-032 text unchanged), so no registry sweep applies;
this is a BUILD commit, not a G1/G2 Status-change ratification, so no `--ratify`
hierarchy applies.

## Harness run (observed, not reported)

- `python project-trajectory/scripts/check.py` (derived gate **G3**, tier all) →
  `RESULT: PASS` — all 15 steps PASS incl. `tests+coverage` (210.2s), `format`,
  `lint`, `dupes`, `derived-gate`, `traceability`, `doc-navigability`,
  `arch-map`, `trajectory-map`, `okf`, `skills-sync`, `trajectory`.
- `python -m pytest -q tests/test_onboard_devsetup.py tests/test_bootstrap.py` →
  `54 passed, 1 skipped`.
- `python project-trajectory/scripts/trace.py` → `SN=24 SR=56 LLR=57 TC=57
  orphans=0 integrity=0 components=5 interfaces=52`.
- Line-ending/encoding: `git check-attr -a` confirms `*.cmd text eol=crlf` from
  the repo `.gitattributes` covers the new template — checkout normalizes to
  CRLF, so the batch file is Windows-safe. The file is ASCII-clean (no non-ASCII
  bytes), as its own comment and the shape test require. Both correct.

## Assessment

The scaffold plumbing is right: the `MAPPING` entry, the `test_bootstrap` file
list, the fresh-scaffold shape test, and the README kit-contents row all land,
and the whole G3 suite is green. But the suite never *executes* the
`.cmd → .ps1` handoff, and that is where the deliverable breaks.

The shim was copied verbatim from the meta-repo **dogfood** `scripts/dev-setup.cmd`,
whose sibling `scripts/dev-setup.ps1` is a meta-only two-switch script
(`param([switch]$Check, [switch]$Install)`). The **template** it now ships beside,
`dev-setup.template.ps1`, has a *different* interface —
`param([switch]$Check, [switch]$Baseline, [switch]$Full, [string]$Profile)` with
**no `-Install`**. So the consented install path `dev-setup.ps1 -Install`
(line 31) hands the scaffolded ps1 a switch it does not declare. I confirmed the
runtime behavior empirically: a `param()` block without `[CmdletBinding()]`
silently drops the unknown `-Install` into `$args` (no error, exit 0), leaving
all switches `$false`, so `$tier = ... else { "check" }` (ps1 line 55) — the
`-Check` "pure report, always green" branch (ps1 line 120-123). Net: a downstream
Windows adopter double-clicks, answers **y** to "Run the install step now?", sees
a green report, and **nothing is installed** — a silent no-op that reads as
success. That directly defeats the spec Done-when ("double-click on Windows
reports then offers install") and the macOS twin it claims parity with (the
`.command` correctly offers `--baseline`, not `--install`). The fix is a
mechanical switch swap (`-Install` → `-Baseline`), but the shape test currently
pins the wrong token, so it must move with it.

Everything else — status.md/next-wi forward-only bookkeeping (WI-166 dropped as
done, `next-wi` → WI-162), log.md, the regenerated `PROJECT_STATE.html`, the
work-items row — is coherent, and declared policies (`push-policy: human`) match.

## Findings

- [BLOCKER] project-trajectory/scripts/dev-setup.template.cmd:31 -> the consented install path runs `dev-setup.ps1 -Install`, but the scaffolded `dev-setup.template.ps1` declares only `-Check/-Baseline/-Full` (no `-Install`; `-Install` was the meta *dogfood* ps1's switch); PowerShell silently drops it into `$args`, so `$tier` falls to `"check"` and the double-click's "install" runs the report-only default and exits green — nothing installs, defeating the WI Done-when -> replace `-Install` with `-Baseline` (the template ps1's install switch, matching the macOS `.command`'s `--baseline`) at the install invocation (line 31) and the "install later" hint (line 33), and update the two comments (lines 7, 14) + the `[y/N]` prompt wording to match -> @owner
- [MINOR] tests/test_onboard_devsetup.py:235 -> the new `test_scaffold_ships_devsetup_cmd` asserts `"-Install" in text`, pinning the exact switch the scaffolded `dev-setup.ps1` rejects — the shape test locks in the defect instead of catching it (which is why G3 stays green) -> assert the install switch the scaffolded `dev-setup.ps1` actually declares (`-Baseline`), ideally cross-checking the shim's switch against the ps1 `param` block rather than a hard-coded string -> @owner
- [MINOR] project-trajectory/scripts/bootstrap.py:50 -> the scaffold-map docstring still reads `scripts/dev-setup.{sh,ps1,command}`, omitting the now-mapped `cmd` (contrast line 49's onboard row `{sh,command,cmd}`), so the in-code inventory drifts from the `MAPPING` it documents -> append `cmd` → `scripts/dev-setup.{sh,ps1,command,cmd}` -> @owner

VERDICT: CHANGES-REQUESTED findings=3
