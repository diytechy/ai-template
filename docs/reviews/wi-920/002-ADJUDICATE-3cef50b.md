# WI-920: TC-055 adjudicated at 3cef50b2

**Adjudicator:** claude-opus-5-5, independent, for TC-055 (verifies SR-054;LLR-055).
**Due because:** declared trigger `component:CMP-009` fired after its work-item floor.
**Judged:** TC-055's Method, against its Expected, on HEAD `3cef50b2`. The only commit
after the judges' render base `825dd47d` adds `docs/reviews/wi-920/001-REJUDGE-825dd47.md`.
None of the declared inputs (the rubric, SR-054, LLR-055, `gen_trajectory.py`, `rendering/`)
changed between the render and HEAD. I regenerated `PROJECT_STATE.html` at HEAD. Its only
difference from the committed file was the as-of stamp, which reads `825dd47de`, the base
that was shot. I then restored the committed file.

The Method's critique has to come from a fresh session of a different model family from the
dashboard's Claude-authored code. I am Claude, so I did not issue the APPROVE myself. I
checked the cross-family sitting against the Method from its retained raw material
(`review-tmp/2026-10-25a-leg19/rj920/`), not from the compiled record's summary. That material
is the operator brief, `tools/` (`briefs.py`, `tile.mjs`, `launch.sh`), six briefs, six
manifests, 328 tiles, six session logs, six verdicts, `launch-run1.txt`, `shoot-output.txt`
and the operator's notes. I also read five tiles myself to look for a plain contradiction.

- [MINOR] The rubric is the single home of the live-vs-retired anchor set -> its header
  states the live set as T2, T4, T5 and T8. Each retired anchor carries its retirement and
  binding in place: T1 -> LLR-115/TC-120, T3 -> LLR-100/TC-103, T6 -> LLR-117/TC-122,
  T7 -> LLR-116/TC-121. Each live anchor names its test-held residue and the one clause the
  critic still judges. All ten bound TCs (the four above plus TC-102, TC-124, TC-108,
  TC-296, TC-125 and TC-305) are `Approved` in the registry, and each lists its LLR in
  `verifies`. So the clauses tests hold are verified through the registry's LLR/TC chain,
  not by this verdict. Met.
- [MINOR] The session was fresh and family-heterogeneous -> `launch.sh` starts one
  `codex exec -m gpt-6-luna -c model_reasoning_effort=high -s read-only` session per
  width x theme cell. Each log header reports `model: gpt-6-luna`, `sandbox: read-only` and
  `reasoning effort: high`. That is a different family from the Claude-authored code. All
  six sessions launched at 09:17:24Z and exited 0 between 09:17:53Z and 09:18:07Z.
  Departure, as the record states: every shell command a judge attempted failed with
  `helper_unknown_error: setup refresh had errors`. Those reads were `CLAUDE.md`, the rubric,
  `.agents/skills/antidote/SKILL.md` and `Get-Location`. None was a forbidden path, and none
  succeeded. So no judge cross-read `PROJECT_STATE.html`. The brief offered that read as
  optional, and the Method requires no source read. It is still thinner than the WI-831
  sitting, whose judges did read the page. Met, with that noted.
- [MINOR] Each judge got the rubric, the SN/SR intent and the test-bound scope lines with
  their TC ids, and never the implementer's self-assessment -> `briefs.py` reads every
  quotation from the lane at HEAD. These are the rubric file, SN-023 and SN-024, SR-054,
  LLR-055, TC-055 and the scope lines of LLR-099/TC-102, LLR-119/TC-124, LLR-105/TC-108,
  LLR-285/TC-296, LLR-120/TC-125 and LLR-292/TC-305. LLR-292 has no `SCOPE`, so its whole
  `detail` is quoted. I diffed the rubric section of `judge-1680-light.md` against
  `docs/rubrics/dashboard-usability.md` at HEAD, and the two are byte-identical. No brief
  carries an implementer's assessment or an earlier verdict. Met.
- [MINOR] No judgment on a failed run or an incomplete matrix -> `shoot.mjs` declares 390,
  1280 and 1680 px x light and dark x the tabs present in the page, at device scale 2.
  `shoot-output.txt` shows 36 shots, no `NOT shot` line, and Knowledge `SKIPPED` because
  its dial is off. The brief's stop rule requires a zero exit, and the operator notes record
  exit 0. The first attempt failed on a missing Playwright install. It produced no tiles,
  briefs or verdicts and is kept apart in `attempt1/`. I checked the tiling with my own
  script: each of the six manifests names exactly its cell's six shots. All 328 tiles are at
  most 1500 px on a side. For every shot, the tile areas sum exactly to the shot's area. Each
  brief lists every tile in its manifest (44, 48 or 72), and `launch.sh` attaches each one
  with `-i` in manifest order. Token use scales with tile count: about 74k at 390 px, about
  115k at 1280 px and about 150k at 1680 px. That fits images actually being received, even
  though the sessions were short. Met.
- [MINOR] APPROVE cites numbered anchors, and only live ones -> all six verdicts end
  `VERDICT: APPROVE findings=0 ANCHORS: T2=pass T4=pass T5=pass T8=pass`. No verdict cites
  T1, T3, T6 or T7. Every tile a verdict cites exists in that judge's own manifest. No judge
  raised a finding or a test gap. T5 was judged in each judge's own theme, three cells per
  theme, so both themes are covered. Two departures are mechanical. The verdict files are
  the CLI's `-o` capture of each final message, because the read-only sandbox could not
  write. The `ANCHORS:` suffix follows the WI-831 precedent. Each judge cites only one to
  five tiles per anchor, so its pass is a sample of its cell. Met.
- [MINOR] The rendered evidence does not contradict the APPROVE (my own spot check of five
  tiles, not a verdict) -> `1680px-dark-dag-full-r02of03-c2of3`: the inactive tab labels are
  readable on the dark page, and the active "Roadmap DAG" tab has a violet label and
  underline. `-r03of03-c1of3`/`-c2of3`: the When view opens as a few phase blocks. The wires
  leaving their port fans run in parallel lanes in open space, not under a label. They are
  faint, which no live residue clause covers. `1280px-light-sw-full-r08of09-c1of2`: the How
  view opens on a four-component top level. `390px-dark-arch-full-r05of05`: the clipped SN
  summaries end in an ellipsis, and a panel directly below says "click a block to read its
  full text". So that truncation has a reveal path. I saw nothing that contradicts T2, T4,
  T5 or T8.
- [MINOR] Standing limit -> I recorded the result with `record_observation.py`. The record
  is `docs/test/observations/TC-055.2026-10-25T092405Z.toml`: pass, expiring
  2027-01-23T09:24:05Z, one 90-day lifetime later. Its inputs digest
  `sha256:5bdf43da…` was taken at HEAD and matches the digest in the WI-920 spec. This
  row's assurance is only as recent as that record.

OUTCOME: RECORDED result=pass
