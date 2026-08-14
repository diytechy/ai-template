+++
id = "WI-454"
title = "Land SN-033's declared need-cell checker as a PLACEHOLDER, while the tier is clean (owner-ruled 2026-08-13u, sitting-2 decision 7 rider 2). SN-033 is RATIFIED and its acceptance commissions a check that does not exist: 'A declared check reports the row and phrase when a need cell contains an internal path, implementation-only identifier or process citation; a reviewed exception list distinguishes names that are themselves user-facing interfaces.' Measured 2026-08-13: 0 of 27 need cells carry such a token (the prose batch cleaned them) and 16 of 27 ACCEPTANCE cells do — correctly exempt, since SN-033 scopes itself to need cells only. So the check would report ZERO findings today, which is exactly why it lands NOW: it locks the clean state in ahead of the SR re-tier's churn rather than trusting a large pass not to dirty it. Shape (the kit's existing pattern, not a new one): a stdlib check_need_form.py in the check_* lint family, wired into check.py's step table WARN-FIRST (the DEFAULTED tier), scanning each need cell for path-like and implementation-identifier tokens against a declared exception list that ships EMPTY; the first row to dirty the tier is the one that reports. Verification: a unit test that constructs a dirty need cell and asserts the row AND the offending phrase are both named (the acceptance requires both), one asserting a user-facing interface name on the exception list passes, and one asserting the live registry is clean at zero findings. Mint the spine chain with it — this check is a shipped kit script and every other check_* in the kit is named by an SR; landing it chainless would make it the only unrequirement-backed check in the kit. The SR cites SN-033 (one of the eight ratified needs with zero children — uncovered=8, so this row delivers SN-033's first coverage); the LLR names check_need_form.py; the TC is the constructed dirty-cell case. Rows land Draft/Planned per the ladder — no re-attest window. Scope guard: warn-first only — do not gate on it without an owner ruling, and do not scan acceptance or engineering-requirement cells (SN-033 exempts them by its own text)."
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Deliverable

Completed 2026-08-14. SN-033's declared checker exists:
`project-trajectory/scripts/check_need_form.py` (stdlib, cross-platform,
sibling-imports `spine_carrier` so an unreadable needs registry refuses loudly
rather than scanning as a clean tier) scans each SN `need` cell — need cells
ONLY, per SN-033's own exemption of acceptance and engineering cells — for the
three commissioned token classes, and every finding names the ROW and the
OFFENDING PHRASE. The reviewed exception list is `docs/need-form-allow`
(`<token> — <reason>` per line; a separator-less line declares nothing — loud
direction) and SHIPS EMPTY: the file is not scaffolded and an absent file
declares nothing. Wired as `check.py`'s `need-form` step at every bar,
WARN-FIRST ALWAYS — no `--strict` promotion anywhere in the shipped wiring;
the step comment records that gating needs an owner ruling. Two documented
scope decisions: `SN-###` is not a process citation (a need citing a sibling
need stays at the stakeholder tier — the live SN-025 hand-off to SN-034), and
a single-slash dot-free token is a path only when it RESOLVES in the scanned
tree (`docs/archive` reports; live English pairs `subjective/perceptual`,
`requirement/test` resolve nowhere and stay exempt — REVIEW-A round 1 narrowed
the original blanket exemption, which swallowed real one-level paths).
REVIEW-A round 1 (cross-family) drove two further genuine finds, fixed on the
branch: a URL's path-shaped tail reported as an internal path (URL spans are
now suppressed whole), and a present-but-emptied registry scanned as a clean
tier (now reported VACUOUS; absent stays the pre-scaffold clean skip, and a
`-000`-only scaffold registry stays a blank form). Its allow-span challenge
was refuted as deliberate: an allow'd name suppresses only its own span, and
an independent citation outside it still reports. Round 2 drove four more,
fixed: a sentence-final path dragged its full stop into the phrase (misnaming
the token and defeating its reviewed exception — the stop is now stripped
before judging, which also kept a sentence-final either/or pair from reading
its punctuation as a file suffix); scheme-less `www.` addresses now suppress
like their `scheme://` forms; and LLR-170/IF-121 mis-stated the allow-list
separator as an ASCII hyphen where the parser requires the em-dash (the exact
silent-voiding confusion the loud-direction rule exists for) — both cells now
state the literal separator. Verification: 15 in-process smoke tests
(`tests/test_check_need_form.py`) covering the dirty-cell row+phrase case,
`--strict`, the exception list and its malformed-entry arm, the exemptions,
the resolving-path, URL and sentence-final arms, the vacuous-registry arms,
and the live registry clean at zero findings over 27 need cells.
Spine: SR-150 (Planned, cites SN-033 — its first coverage, orphans 10 → 9) →
LLR-170 (Draft, CMP-007) → TC-164 (Draft, Smoke), plus IF-121/IF-122
(approval=draft) and the id watermark at SR=150 LLR=170 TC=164 IF=122.
Scaffold surface: bootstrap MAPPING + manifest, kit README row,
test_bootstrap list, BUILTIN_STEP_NAMES; no RESYNC_PACK entry (additive,
warn-first — the check_figures precedent; check_vocab's entry documented a
break). Riders and finds: §6 item 16's SN comment block executed (the empty
Edge-case heading now records the OI-18 deletion; the IF-064 stray rides the
external.toml row, not this touch); minting exposed that `_offspine_ids` lost
the IF/CMP watermark spaces at the WI-443 TOML conversion — re-armed with two
registry rows in `trace.py` (+9, reviewed stamp). `docs/gate` regenerated on
the branch (basis tracks the rows; value unchanged at DevBar-Reqs — the
WI-392/393 precedent). Full unfiltered suite 2484 passed / 11 skipped;
smoke 1123 / 7; `trace.py` and `check_trajectory.py --strict` rc=0 (figures
carry their markers in the log fragment).
