# WI-407 REVIEW-A — independent, hunt-to-break (branch wi-407-… @ 1bb14720 vs ConcurrencyTrainRewrite)

Method: severity-ordered per the intake. (1) THE GUARD: re-drove the WI-400 REVIEW-A
finding-1 fixture both ways — post-fix through the shipped test, pre-fix by swapping
`bddc8e67^`'s `integrate.py` into the tree and watching the alias test fail the
reviewer's exact way — and read the unit pin line-by-line for payload honesty. (2) THE
WIDENING: drove the residue+report.html lane and the `out/` boundary, then verified
the code half of the evidence citation directly against `check.py`/`trace.py` and
hunted the measurement half through every artifact I may read (mint commit body,
spec, ledger; `docs/log.d/` is off-limits to this review by charter). (3) THE RECORD
CORRECTION: diffed the WI-400 amendment, read both commit bodies for the disclosure,
checked the ledger's own header rules, ran the dogfood-sync policing suite. (4) THE
SWEEP LOCK: drove the non-ignored-empty-dir survival and confirmed the ignored-husk
sweep via the lane cleans. (5) Mechanical: module tests, ratchet, smoke, strict
checks, figures, docs/work delta, ruff — all watched on this box.

1. [NIT] docs/declared-absences:74 -> the new LIFECYCLE row's measurement
   parenthetical inverts holder and held: "declared tool-residue since WI-407
   (measured holding the wi-402 lane at unload, 2026-08-02)" reads as the FILE
   holding the LANE; every other record of the same fact (the WI-407 Deliverable,
   the `_RESIDUE_FILES` comment, the WI-400 amendment, the build commit body) says
   it straight — "the wi-402 lane was measured holding exactly that file at
   unload". The ledger is the one durable home prose references resolve through,
   so the garbled copy is the one a future reader lands on. One-word fix:
   "measured held by the wi-402 lane at unload". Record accuracy only; nothing
   mechanical reads the sentence. -> @owner

THE GUARD held, re-driven. Post-fix, the shipped fixture passes:
`test_a_posix_backslash_name_no_longer_aliases_onto_a_tracked_path` builds the
reviewer's exact lane (force-added tracked `x/__pycache__/evil.pyc`, git-ignored
neighbor literally named `x\__pycache__\evil.pyc`) and asserts refusal
("UNLOAD INCOMPLETE" + "DIRTY"), the twin byte-identical, the alias surviving as
evidence, the branch intact — 5/5 new-and-widened tests green on this box. Pre-fix,
with `bddc8e67^`'s `integrate.py` swapped into the tree, the same test fails exactly
the reviewer's way — `FileNotFoundError: … /worker/x/__pycache__/evil.pyc` on the
tracked twin, i.e. the shed deleted it through the mangled alias — so the red half of
the watched-red claim is independently reproduced, not taken on faith. The gate lands
at the ONE shared site: `ignored_files` (integrate.py:1520-1525) is consumed by BOTH
sheds — `_shed_declared_residue` at :1357 and `_shed_residue`'s baseline/now pair at
:1571/:1717 — and the fix is `if os.name == "nt": …replace… / return {p …}`
untouched on POSIX. The unit pin
(`test_the_backslash_normalization_is_windows_only`) is honest about the payload,
not just the platform: it fakes the `ls-files -z` return as
`(0, "x\\__pycache__\\evil.pyc\0sub/cache.pyc\0")` — a literal backslash byte beside
a normal path — forces `os.name` each way, and asserts the EXACT output sets (raw
name preserved on posix, normalized on nt, the normal path identical on both), so
POSIX CI genuinely drives the nt arm and vice versa. Two other
`.replace("\\", "/")` sites remain in the module (`_name_status` :341, the audit
path :2064) — checked, neither feeds a file deletion: `_name_status` authorises a
branch delete/merge refusal off non-`-z` porcelain (where git QUOTES backslash
names, so a mangle there fails the conviction and the fail direction is
refuse-to-act), and the audit only prints. Out of scope, bounded, no finding.

THE WIDENING held, and the evidence citation is judged SUFFICIENT — here is the
honest split. The code half I verified directly and it is load-bearing:
check.py:449-455 builds the trace step as
`trace_cmd = [sys.executable, str(_SCRIPTS / "trace.py"), "--strict",
"--no-placeholders", "--html"]` — `--html` unconditional — and check.py:562
registers it `("traceability", (), trace_cmd, {"G2", "G3"}, "process")`, so the
declared bar runs it at G2/G3 (this repo derives G3); trace.py:2906-2909 then writes
it: `if args.html: html_out = docs / "test" / "report.html";
html_out.write_text(html_document(forest), …)`. So the declared bar provably writes
`docs/test/report.html` in whatever lane it runs in — same generator, same
`.gitignore` block (root .gitignore:12-13 covers both reports), rebuilt
deterministically from tracked registries, sole-copy evidence never. The measurement
half — "on 2026-08-02 the wi-402 lane was measured holding exactly that file at
unload (station measurement, relayed at WI-407 intake)" — exists in no artifact I
may read: the trunk-side mint commit b9250c04 is subject-only, and the spec title's
own widening instruction is the CODE-half test ("if the bar can write it in a lane
… take it only with a test"). Judged sufficient anyway, for three reasons stated in
severity order: the intake's own criterion is the verified code half, and it was
taken WITH the test it demanded; the citation is dated, lane-specific, phrased
honestly as relayed rather than dressed up as an artifact, and is now recorded in
three durable homes; and the safety of the widening never rested on the measurement
— the double-lock admits only a path git IGNORES and the enumerated set names, and
this path's membership in the bar's-own-leavings class is established by the code I
quoted, so a misremembered measurement could not have admitted evidence. Driven:
`test_a_lane_holding_the_bars_html_report_unloads_clean` runs the six measured
paths plus `report.html` beside a TRACKED `docs/test/test-cases.csv` neighbor
through the real `_unload_branch` — unloads clean, worker gone, one worktree left —
and the repo-root `out/run-logs/refresh-refused-wi-401.log` planted OUTSIDE the lane
survives byte-identical in the same test, re-pinning the WI-398 boundary. The
declared-set data test pins membership; the negative list (`.env`,
`out/run-logs/session.md`, …) is unchanged, so nothing was quietly unpinned to make
room.

THE RECORD CORRECTION is the WI-394 shape, verified: the amendment is target-only
and in place (`docs/work/complete/WI-400-…md`, the one hunk), quotes the original
false text ("the bar never generates it" — FALSE), dates the correction 2026-08-02,
attributes it (WI-407, REVIEW-A finding 2), states the true narrower fact, and keeps
the decision/reason split ("The exclusion DECISION stood … widen only on
measurement" retained verbatim). No history rewritten — the amendment rides the new
build commit; WI-400's own commits are untouched. The disclosure is in BOTH commit
bodies: bddc8e67 carries a "RECORD CORRECTION, disclosed loudly" paragraph; 1bb14720
states "The fragment discloses the WI-400 record correction loudly for the
reviewer". The stale `<!-- path-ok: … it exists in no tracked tree by design -->`
escape is removed with the sentence it excused, replaced by the ledger row — the
right direction, per-line excuse to declared fact — and the row is consistent with
the ledger's own header rules (one line, `<path> — <reason>`, reason opening
`LIFECYCLE:`, beside `report.md`'s row; LIFECYCLE correctly chosen, since the file's
presence after any bar run is a legal state and the materialize-guard must not fire
on it). `tests/test_dogfood_sync.py` (the policing suite): 25 passed.
`check_doc_refs --strict` rc=0, so prose naming the path now resolves through the
declaration with no escapes.

THE SWEEP LOCK held, both directions. Survival:
`test_the_sweep_leaves_a_non_ignored_empty_cache_directory_alone` builds a repo with
NO ignore rules, plants an empty untracked `x/__pycache__/keep/`, runs
`_shed_declared_residue`, and the directory survives — green here (and red pre-fix,
consistent with the watched-red five). Sweep: the residue-lane cleans (the html-lane
test above and the measured-paths tests among the 122) run under LANE_IGNORE, whose
rules DO claim the cache dirs, and unload clean — so the emptied ignored husks are
rmdir'd through the new lock and nothing re-refuses. The guard line itself
(integrate.py:1393) fails closed on both non-zero shapes: `check-ignore` rc=1
(not ignored — the lane's emptiness) and rc=128 (git cannot answer) both skip the
rmdir, matching the docstring's stated fail direction; an unremovable husk is still
re-refused loudly by the caller's re-read.

Mechanical re-runs on this box (HEAD 1bb14720): `tests/test_integrate.py` 122 passed
in 40.71s (Deliverable: 122 in 41.17s — matches; the ratchet test beside it makes
123); smoke 625 passed / 2 skipped in 10.84s (close commit: 625/2 — matches; the
build commit's 621/6 is the same 627 total under the environment-variant skip split
the WI-400 review already recorded); `check_trajectory --strict` rc=0 (no WI-407
finding; residual WARNs are the pre-existing connectivity and WI-389/390
SpecRef-clock ones); `check_doc_refs --strict` rc=0; `check_figures` OK — 47
declared figure(s), every one carrying command and revision; spot-check re-drive of
the spec's `python -m pytest -q tests/test_integrate.py` figure reproduced its 122.
Size ratchet 2125 == `wc -l` 2125 exact, with a dated, reasoned +22 stamp naming all
three findings. Ruff lint + format clean on the three touched .py files. R-A: strict
rc=0 and the Deliverable's claims re-driven here; R-F: the terminal spec's
frontmatter carries no `specref` key. docs/work delta is exactly WI-407 (claim dir
removed, spec active→complete, log fragment) plus the DISCLOSED WI-400 amendment —
nothing else; status.md's WI-407 token sits inside the GENERATED ready-frontier
block that regenerates at integrate, the accepted shape.

I re-drove the breach this WI exists to close and watched it both red and green; the
guard sits at the one site both sheds share, the pin forces both arms over the
adversarial byte, the widening is driven and its evidence honestly weighed
(sufficient — the verified code half is the load-bearing half), the record
correction is loud, dated, and target-only, and the sweep lock fails closed. The one
finding is a garbled sentence in the ledger row.

VERDICT: APPROVE findings=1
