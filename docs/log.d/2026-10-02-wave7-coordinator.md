## 2026-10-02 — wave 7 (coordinator): Sol 6.1 builds, Sonnet 5.5 reviews

Deferred open items: none — the owner ruled every question this session raised
(recorded in WI-541, WI-657, WI-667, WI-697 and WI-746, and as the new WI-747 and
WI-748).

### Setup and the owner's 2026-10-02 rulings

- The commit floor was red on trunk with nothing staged (skills-sync, derived-stage,
  approval-fresh, open-items, format); `f243a1eb` regenerated each by its own writer
  and formatted `tests/test_session_service.py`. `3e0a5f48` had amended the approved
  method cells of TC-262, TC-263, TC-264 and TC-267 outside a lane; they go to the
  next spine-acts adjudication.
- `880eff04`: `[attestation] complete_review = "off"` (owner). `2e13b2bd`: the
  rulings and WI-747/WI-748.
- `build/wi-722` (`d451cb64`), the other `build/*` branches and the `archive/lanes`
  ref were gone at session start; WI-722 is rebuilt from trunk and `archive/lanes`
  restarts at this wave's first landing.
- Builders: Codex Sol `gpt-6.1-sol` through the VS Code extension's codex 0.160.0;
  the npm codex 0.157.1 and the desktop app's 0.155 are refused for that model. The
  `elevated` Windows sandbox cannot read the user's Python install under 0.160.0, so
  builders run `windows.sandbox="unelevated"` with `-s workspace-write`; they still
  cannot commit, and the coordinator commits for them.

### WI-744 lands: the keep-warmer survives a refused routing row

Sol built it at `9d19e88d` (red then green; 148 passed over the session, dispatch and
ratchet modules). Sonnet 5.5: SOUND, one minor (a malformed template is skipped too),
accepted as built. Squash-landed with the bar below.

### WI-745 lands: the re-seed test plants its own Drafted LLR

Sol (low effort) built it; the first run could not start Python under the elevated
sandbox, and the continuation recovered the red by restoring HEAD's files (1 failed,
123 passed) before the green (124 passed). Sonnet 5.5: SOUND, two cosmetic minors
accepted. The shared fixture now forces SR/LLR/TC statuses to Approved in its temp
copy; the reviewer checked every caller and the regex's anchoring.

### WI-722 lands: the shrink floor is a 9 px rendered-label minimum

Rebuilt from trunk (the first build's commit was lost). Sol's first build ran its
tests on an improvised interpreter under the elevated sandbox; the coordinator
re-ran them with the repo venv. Three Sonnet rounds: NOT YET SOUND at e5e42767 (the
seam graph's literal 10 px label renders 8.57 px at the floor; the drill width
estimates were stale), NOT YET SOUND at ed57db9f (the estimates over-corrected to
1.0 em, halving label capacity), SOUND at 45a0bab2 (0.7/0.65 em pinned to a
0.65-0.85 em band; a seam budget of its own; a scan of every emitted SVG for
non-token text sizes). One 27-character component name now truncates at the 172 px
column cap, from the larger type; noted for WI-713. LLR-116 and TC-121 amended in
place for this merge's adjudication, which also carries TC-262/263/264/267.

### WI-713: TC-055 re-judged cross-family, RECORDED fail

The coordinator rendered the declared matrix at cafa07ab and cut it into 270
native-resolution tiles (Playwright clips at scale 1 over the scale-2 shots; no
image library is installed). Three independent Claude Opus 5.5 judges, one per width,
saw only the composed brief, the rubric, SR-054, LLR-055, its needs and the tiles.
T2 and T5 pass at every width. T4 fails at every width (the System-context crossing
captions clipped under the boxes, a 54-character cut sized for the type WI-722
raised). T8 fails at 1680 px (MAJOR) and 1280 px (MINOR): avoidable crossings in
three diagrams. Recorded `fail` through `record_observation.py`, naming the judges.
WI-722's floor itself held. Successor WI-750, filed by hand.

### WI-746 lands: a pending open item's wi_refs blocks a queued row

Sol built the owner's design. It found the kit already reads open-item ids in
`needs` (approved TC-253 requires the reader), so it kept the reader, stopped intake
writing them, and made `wi_refs` the gate. Sonnet 5.5: NOT YET SOUND at 56503928
(the shipped disposition prompt still said intake writes the id into `needs`; four
stale comments), SOUND at acc1e195. Retiring the legacy reader needs an adjudicated
amendment of TC-253, IF-176 and LLR-058; left for the owner. OI-98 and OI-99 now hold
WI-684 and WI-688 mechanically. Composed onto trunk, the smoke tier (which neither
the builder's module runs nor the review covered) failed three tests the lane caused;
the squash was backed out and a fix round cleared them: a `gates` name the ladder
guard reads, deferred imports 31 -> 29, and the dashboard (+13,231 bytes, 3,013,555
-> 3,026,786) re-stamped to 3,480,000, the file's ~15% headroom. SOUND at d1681906.
Lesson: a builder's bar includes the whole smoke tier, not only its modules.

### WI-749: spine-acts sitting, six rows re-attested (act seq 14)

An independent Claude Opus 5.5 adjudicator, working from the kit-composed brief in
its own worktree, ruled LLR-116 and TC-121 (WI-722's floor) and TC-262, TC-263,
TC-264 and TC-267 (`3e0a5f48`'s live recordings, carried in by the coordinator) all
MEANING, and re-attested all six; no Dispositions. Sonnet's cross-review: SOUND.
Because trunk had gained WI-746's Drafted rows since the lane was cut, the
coordinator retook the snapshot on the merged tree: `refresh_refusal` returned no
refusal for the same arguments, `last_approved/` was reset to trunk, and the exact
command re-run (seq 14). TC-264's cache-write clause is now WI-748's to amend.

### WI-751: first approval of the open-item gate's rows (act seq 15)

An independent Claude Opus 5.5 adjudicator approved LLR-288, LLR-289 and TC-301 and
returned TC-302 (archive resolution and the absent-registry case untested in its
Method), drafting one exact replacement row. Sonnet's cross-review: SOUND. The lane
was cut from the trunk tip, so its snapshot stands as taken.

### WI-752 lands: TC-302's return applied as drafted

Sol (low) applied WI-751's exact replacement to TC-302 and added the one assert; no
code change, nothing went red because the behaviour already held. Sonnet: SOUND. The
shared builder prompt had told builders not to run the whole smoke tier, against the
item prompts; it now requires the smoke tier at `-n 2`.

**A slip found here:** WI-722's landing ran four traj test modules, not
`tests/test_traj_graph.py`, and that slow-tier module still pinned the old floor:
`test_svg_frame_pads_only_the_side_that_carries_outboard_ink` is red on trunk from
6a40d7b2 (`1 failed, 30 passed`). WI-750's lane carries the fix. Lesson: a lane
touching `rendering/` runs every `test_traj_*` module before it lands.

### WI-750 lands: the System-context captions fit their lane; three crossings removed

Sol built it; Sonnet: SOUND at 9884f643 (two minors). T4's captions are fitted to
the measured lane from the token-derived estimate and painted after the boxes; T8's
Process, How and When crossings named by WI-713 are removed and tested over emitted
geometry, except the When roadmap's cyclic return routes, documented and pinned as
needing joint routing. It also repairs `tests/test_traj_graph.py`'s floor pin, red on
trunk since WI-722. TC-055 is due again at this merge (its rendering inputs changed).

### The disk filled; WI-753 approved TC-302 (act seq 16)

The C: drive (931 GB) reached 0 bytes free at about 00:20. Cause: this session's own
pytest scratch, 148 `--basetemp` directories of 250-420 MB each under `%TEMP%` (a new
path per run, never wiped) on a drive already near full; the full unfiltered suite
started on trunk died of it. All 148 and `C:\Projects\.pytest-tmp`'s runs were
deleted, back to ~3.6 GB free. Builders and the coordinator now use one fixed
`--basetemp` per lane, which pytest wipes per run. The full suite is NOT re-run:
it needs more free space than the drive has.

WI-753: the independent Opus adjudicator ruled TC-302 APPROVE, but its commit failed
on the full disk. The coordinator executed its recorded steps. A first attempt
chained a failed status flip into an empty snapshot act (seq 16, `approved = []`);
caught at once and reset on the unreviewed lane, then redone correctly. Sonnet's
cross-review: SOUND.

### WI-748 lands: codex cache writes read, compaction recorded reported or inferred

Sol built it; Sonnet: NOT YET SOUND at 72b035e5 (exec turn totals are per-turn sums
of requests, so the fallback could infer a false compaction; only the last request
pair was compared), SOUND at 630150c3 after the inference moved to rollout
per-request prompts only, across every new pair. TC-264 and LLR-268 amended; the
cache-write inclusion is hedged as unverified live.

### Spine-acts batch L (WI-755, WI-756): LLR-268 and TC-264 re-attested; LLR-290 and TC-303 returned

One independent Opus adjudicator sat over two briefs and took one act (seq 17):
LLR-268 and TC-264 MEANING and re-attested; LLR-290 and TC-303 returned (the sticky
inferred flag is unstated; reported-versus-inferred precedence untested), with an
exact draft. Sonnet's cross-review: SOUND. The open-items page's "2 rows drifted" is
a mislabel for two chains owing a first approval (SR-224; SR-227); the genuinely
drifted rows remain SN-003, SN-008, SN-009 and SN-025, owed to the owner.

### WI-754: TC-055 re-judged after WI-750, RECORDED fail on T8 only

Rendered at 6e89705b, 268 native tiles, three independent Opus judges told that an
anchor with only MINOR findings passes. T2, T4 and T5 pass at every width; WI-750
fixed T4. T8 fails at 1280 and 1680 px: distinct edges share segments and meet
end-to-end at the port fans (the How view's CMP-006 hub reads as a chain; 26
unrelated edge pairs overlap in the When roadmap). WI-758 filed by hand: separate
the lanes and bind the clause as a test, so T8's lane separation stops needing an
LLM judgement (the owner's WI-747 direction).

### WI-757 lands: LLR-290 and TC-303 state and test the sticky compaction source

Sol (low) applied batch L's exact return and wrote the second test so it exercises the
stored reported source (the drafted form passed trivially). Sonnet: SOUND. Sol
resumed at 02:30 after the usage limit.

### WI-759 lands: an example wi_refs entry is inert; the scaffold hook tests are green

Sol (low) reused `kitlib.spine.is_example`; the two hook tests red since WI-746 pass.
The hook modules fail inside the Codex sandbox (Git Bash), so the coordinator ran
them outside it: 34 passed. Sonnet: SOUND.
