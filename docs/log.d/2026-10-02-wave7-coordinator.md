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
