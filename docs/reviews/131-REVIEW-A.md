# 131-REVIEW-A — adversarial review of WI-354

**Reviewer:** `codex` / OpenAI (non-Anthropic, per SR-084 — the builder was
Opus, so provider heterogeneity is what makes this an independent check).
**Subject:** `fc27814` — the single WI-354 commit (13 files, +369/-46): the
anchor half of R-E, IF-077, and the WI-355 filing.

Given the branch's calibration explicitly (its recurring defect is signed CLAIMS
the code does not support, not broken code) and told to MUTATE the guards. It
restored the worktree byte-exact.

**Six findings held; one was corrected in BOTH directions.** MINOR 5 correctly
refuted the stated rationale for `nearest_anchor`'s prefix pass — plain `difflib`
does find WI-326's own truncation — but its recommendation to DELETE the branch
was itself measured and rejected: a severer truncation (`2026-07-26--wi-326`)
returns nothing from `difflib` while the prefix pass returns the exact heading.
The branch stays, the rationale was corrected, and the measured pair is now
pinned by a test. *When a review hands you a fix, measure the fix too.*

One caveat on the evidence: the reviewer could not run the repo `.venv` and used
Python 3.8 for focused tests, below the declared 3.11 floor. Every
code-behaviour finding was therefore re-verified here on 3.11.9 before being
acted on; all four guard mutations were reproduced independently.

Disposition is recorded in `docs/log.md`.

---

CHANGES-REQUESTED — 7 findings (1 BLOCKER, 3 MAJOR, 3 MINOR)

The mandated `.venv` could not run: it reports `No Python at "C:\Users\Peter\AppData\Local\Programs\Python\Python311\python.exe"`. Focused tests therefore used the available `C:\Python38\python.exe`; the exact historical full-suite green could not be rerun.

## 1. BLOCKER — A pathless bogus anchor still passes strict R-E

Claim/code: [check_trajectory.py:1262](C:\Projects\ai-template\project-trajectory\scripts\check_trajectory.py:1262) claims both halves of `path#anchor` resolve, but an empty path returns no findings:

```python
if not pathpart:
    return []
```

Evidence from the real CLI with `SpecRef=#totally-invented`:

```text
returncode 0
stdout check_trajectory: clean (1 work item(s), 0 done (0%), graph acyclic).
stderr
```

Thus the central defect remains reachable: a bad anchor silently passes, and all five changed tests remain green.

Fix: reject a non-empty SpecRef with an empty path. Also require the resolved path to be an in-root regular file, then add strict tests for `#bogus`, a `.md` directory, and an out-of-root absolute path.

## 2. MAJOR — Removing required case normalization survives every new test

Claim/code: [check_trajectory.py:1275](C:\Projects\ai-template\project-trajectory\scripts\check_trajectory.py:1275) correctly lowercases fragments to match `check_docs`, but the guard does not protect it.

Mutation:

```diff
- if anchors is None or frag.lower() in anchors:
+ if anchors is None or frag in anchors:
- near = nearest_anchor(frag.lower(), anchors)
+ near = nearest_anchor(frag, anchors)
```

All five anchor tests stayed green:

```text
..... [100%]
5 passed in 2.31s
```

Under that mutation, an uppercase version of a real `docs/log.md` anchor produced a false error:

```text
WI-X: SpecRef 'docs/log.md#SESSION-2026-07-28-...' names no such heading ...
```

`check_docs` accepts fragments case-insensitively, so this mutation reopens the exact cross-home disagreement the property test claims to prevent.

Fix: exercise the valid slug in mixed/uppercase form in both the markdown link and SpecRef homes. The mutation above must fail.

## 3. MAJOR — “5 anchored rows” is false in the committed live registry

Claim: [log.md:17567](C:\Projects\ai-template\docs\log.md:17567) and WI-354’s Deliverable report “5 rows carry an anchored SpecRef.”

Measured HEAD:

```text
anchored_count 6
WI-061 deferred open=True path_exists=True anchor_resolves=True
WI-063 deferred open=True path_exists=True anchor_resolves=True
WI-158 deferred open=True path_exists=True anchor_resolves=True
WI-277 deferred open=True path_exists=True anchor_resolves=True
WI-280 deferred open=True path_exists=True anchor_resolves=True
WI-355 queued   open=True path_exists=True anchor_resolves=True
```

The likely timing error is visible in the same commit: WI-355 was added after the five-row census. “All open, all resolve” holds, but the signed live count does not.

Fix: rerun the census after the final registry edit and change every signed count to six. Prefer recording the reproducible census command/output.

## 4. MAJOR — The growth history cannot support both “sixth bump” and “~90 lines per slice”

Claim: [test_module_size_ratchet.py:403](C:\Projects\ai-template\tests\test_module_size_ratchet.py:403).

The exact file-size claim holds:

```text
fc27814^ splitlines 2497
fc27814  splitlines 2590
```

But ratchet history shows seven consecutive baseline increases after the initial 1926 entry:

```text
1926 -> 2048  +122
2048 -> 2058   +10
2058 -> 2063    +5
2063 -> 2135   +72
2135 -> 2495  +360
2495 -> 2497    +2
2497 -> 2590   +93
```

Using commits, this is the seventh increase and averages 94.9 lines. Combining the two WI-316 commits to obtain six slices gives an average of 110.7, not roughly 90. Combining the +2 review fix with its preceding slice leaves five slices averaging 132.8.

No consistent unit makes both signed claims true.

Fix: define “slice” mechanically and recalculate. If measuring baseline edits, say seventh and approximately +95 per edit.

## 5. MINOR — The prefix-special-case rationale is false and its test is hollow

Claim/code: [check_trajectory.py:1230](C:\Projects\ai-template\project-trajectory\scripts\check_trajectory.py:1230) says plain `difflib` scores the WI-326 truncation too poorly.

Measured against the actual live anchor set:

```text
short_len 44 full_len 76
SequenceMatcher ratio 0.7333333333333333
anchor_count 453
get_close_matches:
['2026-07-26--wi-326-a-green-that-hid-47-tests-caught-by-not-trusting-a-number']
```

The synthetic test fixture also clears the 0.6 cutoff:

```text
fixture_ratio 0.6222222222222222
fixture_plain ['s1-first-slice-with-a-long-tail']
```

I deleted the prefix branch entirely; all five tests still passed:

```text
..... [100%]
5 passed in 2.70s
```

Fix: remove the prefix branch and false rationale, or retain it only with a demonstrated real candidate set where plain `get_close_matches` chooses no result or the wrong result.

## 6. MINOR — “Regenerate PROJECT_STATE.html LAST” is not a real ordering rule

Claim: [log.md:17607](C:\Projects\ai-template\docs\log.md:17607).

I copied the generator’s inputs to an isolated root, deliberately made the generated status block stale, rendered the dashboard, ran `run_status`, and rendered again:

```text
status_had_stale_marker True
gen_trajectory: status snapshot regenerated -> docs/status.md
status_has_stale_marker_after False
before_sha256 6094e99e530a7616921f6aa2a5ce82497628cca560004977efb35b2297d9864f
after_sha256  6094e99e530a7616921f6aa2a5ce82497628cca560004977efb35b2297d9864f
dashboard_changed_by_status_regen False
```

`build_html` does not consume status contents; it only links to `status.md` if the file exists. Status regeneration therefore cannot stale the dashboard. The observed staleness came from another shared input changing after dashboard generation—likely the late WI-355 registry addition—not from `--status`.

Fix: remove the ordering rule. State the actual invariant: regenerate each derived artifact after its source inputs have reached their final state.

## 7. MINOR — The cross-home property test claims a code-span shape it never exercises

Claim: [test_trajectory.py:451](C:\Projects\ai-template\tests\test_trajectory.py:451) says “em dash, code span and punctuation all normalize,” but its heading is:

```python
heading = "S1 — the strict slice, part 2"
```

There is no inline code span.

The named parser subtlety is real and materially changes the anchor:

```text
raw heading: Alpha `beta` gamma
slugify_raw: alpha-beta-gamma
parse_doc_anchors: ['alpha--gamma', 'doc']
```

Fix: put an actual backtick span in the fixture and assert that `slugify(raw_heading)` differs from the parser-exposed anchor before checking both homes.

## Named suspects that held

- **3 HOLDS:** an equivalent inline implementation measured `ssot_findings` at C901 **11**; the extracted HEAD functions measure `ssot_findings=7`, `specref_findings=6`, both under 10.
- **4 HOLDS:** `check_docs.py` and `check_trajectory.py` are both in bootstrap `MAPPING`; optional `schedule.py` is not.
- **5 HOLDS:** enumerating all 21 resolved commands for gate `all` versus `G3` found only `trajectory` different; G3 adds `--strict`.
- **6 HOLDS:** captured `--gate G3 --run-steps trajectory` used no `--strict`, while `--gate G3 --list` printed it.
- **7 HOLDS:** none of SN/SR/LLR/TC changed; SR-068 remained byte-identical and `Verified`.
- **8 HOLDS to the reproducible extent:** collection produced exactly `1728 tests`; `1722 + 6 = 1728`, and the commit adds four tests while changing one. The changed surface passed targeted testing, but the historical full green was not rerun because the supplied venv is broken.
- **10 HOLDS:** `parse_doc` strips inline code spans over the whole document before heading slugification.
- **11 HOLDS:** both `git show ... | Measure-Object -Line` and `Get-Content ... | Measure-Object -Line` returned **2343**, while `splitlines()` returned **2590** with 247 blank lines.
- **13 HOLDS:** copying only `check_trajectory.py` and omitting `check_docs.py` reached the fallback and passed a bogus anchored SpecRef path-only without raising:

  ```text
  check_trajectory: clean (1 work item(s), 0 done (0%), graph acyclic).
  fallback_exit=0
  ```

- **14 HOLDS:** IF-077 is structurally aligned: `Consumes`, `ThisProject=scripts/check_trajectory` in CMP-001, counterpart `scripts/check_docs` in CMP-003. The actual import runs from `check_trajectory` to `check_docs`; strict trajectory and the architecture-map freshness check both passed.
- The `doc_anchors -> None` and disabled Markdown-suffix mutations each failed three anchor tests. Deleting anchor checking made the cross-home property fail. Adding one module line made the ratchet fail at `2590 -> 2591`.
- **1 partially holds:** all six—not five—anchored rows are open and resolve.
- **2 partially holds:** `2497 -> 2590` is exact.
- **9 and 12 are REFUTED** by findings 5 and 6.

Final `git status --short`:

```text
?? docs/pause
```
