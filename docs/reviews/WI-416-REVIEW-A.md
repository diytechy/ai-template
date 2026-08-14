# WI-416 — REVIEW-A (2026-08-03)

**Reviewer:** OPENAI-SOL (`gpt-5.6-sol`) via the `codex` CLI — cross-family,
fresh context, independent of the adjudicator. Charter:
[code-review-adversarial](../rubrics/code-review-adversarial.md). Given the diff
and the requirement surface (WI-416's brief, WI-413's spec, both prior REVIEW-A
rounds, and the shipped `intake.py`/`handback.py`/`schedule.py`). On an
adjudication row the REASONING IS THE DELIVERABLE, so the `## Deliverable` was
in scope to read (the WI-414 precedent). Run under `--sandbox workspace-write`
rather than the registry's bypass flag; the reviewer's own drives confirm the
sandbox did not constrain it. Machine-local absolute paths in the reviewer's
output were rewritten to repo-relative form (`<scratch>` = the session
scratchpad); nothing else in the verdict is edited.

**Verdict: REWORK** — 1 BLOCKING, 1 MAJOR, 1 MINOR. The *disposition* is
affirmed: re-queue as scoped is correct, and the reviewer's own control probe
independently confirms the fix fits `intake.py` + tests with no `handback.py`
change. What is rejected is the *brief*: B/B+/B+2 add a state pre-filter while
leaving `_rev7`'s seven-character title token and `_mint`'s exact-title filter
authoritative, so the round-1 finding-3 collision class survives and silently
discards an owed second judgement.

---

This diff is a docs-only R3 adjudication record. It changes WI-413 from
scheduler-blocked to ready by deleting its `blockref`, preserves the returned
lane's permanent `## Handback` record, and writes the implementation brief that
a future WI-413 lane will use to change `intake.py`'s handback sweep. Its blast
radius is the ready frontier now and the future persisted disposition registry
if that brief is followed. It changes no shipped Python in this diff and must
satisfy R3 plus WI-413's two named behaviors.

The disposition outcome itself is right: a state-based solution can be
completed inside `intake.py` plus tests, so no identity persisted by
`handback.py`, scope widening, or migration is inherently required. The
submitted proof and build brief are not right yet. B, B+, and B+2 retain the
shipped seven-character title token and `_mint`'s exact-title filter. I
reproduced the prior worst failure class through B+2: a genuine second handback
was silently discarded.

## Failure classes hunted, worst-first

1. Silent suppression of an owed second judgment after the first disposition
   closed.
2. Duplicate dispositions from repeated bare sweeps and each R3 lifecycle.
3. A wrong ruling that widens scope or re-queues an unbuildable row.
4. A non-R3 outcome, recursive handback, branch-side WI mint, altered permanent
   Handback record, or uncleared scheduler block.
5. False driven evidence or stale migration guidance.

All writes were confined to the supplied scratchpad. The prototypes were copies
of the real repo and retained the real `intake.py`; `review_drive.py` imports the
copied real `handback.returned_spec` and `handback._note`, and invokes the real
`intake.py sweep` CLI as a subprocess. No product bar was run because WI-416 is
`adjudication`, whose declared bar is none.

## Exact commands and driven output

### R3 enactment and persisted record

```text
$ git apply --numstat <scratch>/wi416.diff
26	1	docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md
158	0	docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md

$ rg '^diff --git|^new file mode|^deleted file mode' <scratch>/wi416.diff
diff --git a/docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md b/docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md
diff --git a/docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md b/docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md

$ PATH=.venv/bin:$PATH python - <<'PY'
from pathlib import Path
import subprocess
p = Path('docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md')
old = subprocess.run(['git', 'show', 'HEAD:' + p.as_posix()], check=True, text=True, capture_output=True).stdout
new = p.read_text(encoding='utf-8')
def note(text):
    return text.split('## Handback\n', 1)[1].split('\n## ', 1)[0]
print('Handback byte-identical:', note(old).encode() == note(new).encode())
print('HEAD blockref:', 'blockref =' in old.split('+++', 2)[1])
print('diff blockref:', 'blockref =' in new.split('+++', 2)[1])
PY
Handback byte-identical: True
HEAD blockref: True
diff blockref: False

$ .venv/bin/python schedule-old/project-trajectory/scripts/schedule.py --root schedule-old ready --explain | rg '^WI-413\b'; .venv/bin/python project-trajectory/scripts/schedule.py --root . ready --explain | rg '^WI-413\b'
WI-413     blocked   parallel     rank=6 P0   down=0   path=0   excluded:blocked:docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md
WI-413     ready     parallel     rank=6 P0   down=0   path=0   parallel:ordinary;ready
```

The diff modifies only the two existing specs, adds no WI file, preserves the
Handback bytes, and makes the real scheduler read WI-413 as ready.

### Current shipped baseline on the diff state

I cloned HEAD, copied only the two reviewed files into the clone, committed that
scratch state, and ran the real current CLI:

```text
$ .venv/bin/python live-baseline/project-trajectory/scripts/intake.py --root live-baseline sweep
intake: minted WI-419 at docs/work/queued/WI-419-dispose-wi-413-handed-back-at-0f61e33.md
intake: sweep minted 1 row(s).
```

This confirms WI-413's named defect and WI-416's sequencing warning.

### What the B+2 prototype actually retained

```text
$ git -C bplus2 show --stat --oneline --no-renames ed822604; rg -n "def _open_disposition_ids|def _pending_open_item_ids|def _rev7|handed back at|def _mint|state_guarded|drafts = \[d for d in drafts" bplus2/project-trajectory/scripts/intake.py | head -n 30
ed822604 review prototype B+2
 project-trajectory/scripts/intake.py | 56 +++++++++++++++++++++++++++++++++---
 1 file changed, 52 insertions(+), 4 deletions(-)
485:def _open_disposition_ids(root):
499:def _pending_open_item_ids(root):
510:def _rev7(root, rev):
569:                    "dispose: {} handed back at {} ({}) - {} (a disposition "
772:def _mint(root, drafts, subject_verb):
779:    drafts = [d for d in drafts if str(d["title"]).strip() not in titles]
```

So “no hash exists” and “neither prototype reads git” do not describe the
prototype. The new state reads leave `_rev7`, its title token, and terminal-row
exact-title dedup intact.

### The two ordinary required behaviors

```text
$ PATH=.venv/bin:$PATH python review_drive.py bplus core
returned_spec/_note: WI-900 lane=lane-one sections=1 blockref=True
intake: minted WI-901 at docs/work/queued/WI-901-dispose-wi-900-handed-back-at-c67d205.md
intake: sweep minted 1 row(s).
intake: WI-900 carries a handback and an OPEN disposition row already cites it - no second disposition minted (a judgement is already pending)
intake: sweep minted 0 row(s).
intake: WI-900 carries a handback and an OPEN disposition row already cites it - no second disposition minted (a judgement is already pending)
intake: sweep minted 0 row(s).
same_return_counts=1
after_requeue_close_no_new_return=1
returned_spec/_note: WI-900 lane=lane-two sections=2 blockref=True
intake: minted WI-902 at docs/work/queued/WI-902-dispose-wi-900-handed-back-at-3749ddb.md
intake: sweep minted 1 row(s).
after_genuine_second=2
intake: WI-900 carries a handback and an OPEN disposition row already cites it - no second disposition minted (a judgement is already pending)
intake: sweep minted 0 row(s).
after_second_resweep=2 handback_sections=2
```

Those are the relevant exact lines from the full output; B+ passes the ordinary
`1 -> 1 -> 1` and real second-return `1 -> 2 -> 2` drives. B+2 produced the same
counts.

The nastiest open-row case is also genuinely loud and self-evidencing:

```text
$ PATH=.venv/bin:$PATH python review_drive.py bplus loud
returned_spec/_note: WI-920 lane=lane-one sections=1 blockref=True
intake: minted WI-921 at docs/work/queued/WI-921-dispose-wi-920-handed-back-at-f559482.md
intake: sweep minted 1 row(s).
returned_spec/_note: WI-920 lane=lane-two sections=2 blockref=True
intake: WI-920 carries a handback and an OPEN disposition row already cites it - no second disposition minted (a judgement is already pending)
intake: sweep minted 0 row(s).
open_suppression dispositions=1 sections=2 specref_exists=True
```

That path is not defective: a real open row points to the spec carrying both
notes.

### B alone and the surface-open-item lifecycle

```text
$ PATH=.venv/bin:$PATH python review_drive.py b b-only
returned_spec/_note: WI-910 lane=lane-one sections=1 blockref=True
intake: minted WI-911 at docs/work/queued/WI-911-dispose-wi-910-handed-back-at-91b5862.md
intake: sweep minted 1 row(s).
intake: minted WI-912 at docs/work/queued/WI-912-dispose-wi-910-handed-back-at-2d58a42.md
intake: sweep minted 1 row(s).
B_only_no_new_return_dispositions=2

$ .venv/bin/python review_drive.py bplus oi
returned_spec/_note: WI-940 lane=lane-one sections=1 blockref=True
intake: minted WI-942 at docs/work/queued/WI-942-dispose-wi-940-handed-back-at-23aeccc.md
intake: sweep minted 2 row(s).
intake: minted WI-943 at docs/work/queued/WI-943-dispose-wi-940-handed-back-at-2c5ae64.md
intake: sweep minted 1 row(s).
after_surface_oi_close_dispositions=2

$ .venv/bin/python review_drive.py bplus2 oi
returned_spec/_note: WI-940 lane=lane-one sections=1 blockref=True
intake: minted WI-941 at docs/work/queued/WI-941-dispose-wi-940-handed-back-at-763a907.md
intake: sweep minted 1 row(s).
intake: WI-940 carries a handback and a pending open item already cites it - no disposition minted (a judgement is already pending)
intake: sweep minted 0 row(s).
after_surface_oi_close_dispositions=1
```

The B+ run also minted another synthetic target already present in that clone,
which is why its first CLI total is two; the WI-940-specific count is the final
`2`. The drives confirm the Deliverable's B and B+ lifecycle diagnoses, and
that B+2 closes the open-item residual.

### Silent suppression still present in B+2

I generated two valid Git commit objects with distinct full SHA-1s but the same
seven-character prefix, used the first for the first real CLI event, closed the
first disposition and re-queued the target, then used real
`returned_spec`/`_note` for the second event and the second commit for its CLI.

```text
$ .venv/bin/python review_drive.py bplus2 collision
SCENARIO seven-prefix collision WI-930
returned_spec/_note: WI-930 lane=lane-one sections=1 blockref=True
collision_search attempts=6898 nonces=2113,6898 shas=1051541bf800,1051541c7d7e prefix_equal=True
$ PATH=.venv/bin:$PATH python project-trajectory/scripts/intake.py --root . sweep --before 1051541bf800835791b5e1f55fe0e006b57ec362 --after 1051541bf800835791b5e1f55fe0e006b57ec362
intake: minted WI-944 at docs/work/queued/WI-944-dispose-wi-930-handed-back-at-1051541.md
intake: sweep minted 1 row(s).
rc=0
after_first_collision_event=1
returned_spec/_note: WI-930 lane=lane-two sections=2 blockref=True
$ PATH=.venv/bin:$PATH python project-trajectory/scripts/intake.py --root . sweep --before 1051541c7d7e4710ed0361357088239041ad9863 --after 1051541c7d7e4710ed0361357088239041ad9863
intake: sweep minted 0 row(s).
rc=0
after_genuine_second_colliding_event=1 sections=2
titles=['dispose: WI-930 handed back at 1051541 (docs/work/queued/WI-930-returned.md) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)']
```

No WI-930 open-row or pending-OI line appeared on the second sweep. The first
row was terminal. The only remaining suppressor was `_mint`'s silent exact-title
filter, so this is the same owed-judgment loss as the prior rejection.

### Control: the disposition can remain “re-queue as scoped”

I carried the proposed state predicate through `_handback_drafts` (queued plus
blockref), marked handback drafts state-guarded, and let only state-owed drafts
bypass title dedup. Those were `intake.py` changes only. The same collision drive
then passed:

```text
$ .venv/bin/python review_drive.py stateonly collision
returned_spec/_note: WI-930 lane=lane-one sections=1 blockref=True
collision_search attempts=11671 nonces=1536,11671 shas=07e34c3fa4ba,07e34c3ca734 prefix_equal=True
intake: minted WI-931 at docs/work/queued/WI-931-dispose-wi-930-handed-back-at-07e34c3.md
intake: sweep minted 1 row(s).
after_first_collision_event=1
returned_spec/_note: WI-930 lane=lane-two sections=2 blockref=True
intake: minted WI-932 at docs/work/queued/WI-932-dispose-wi-930-handed-back-at-07e34c3.md
intake: sweep minted 1 row(s).
after_genuine_second_colliding_event=2 sections=2

$ .venv/bin/python project-trajectory/scripts/intake.py --root . sweep
intake: WI-930 carries a handback and an OPEN disposition row already cites it - no second disposition minted (a judgement is already pending)
intake: sweep minted 0 row(s).
stateonly_collision_resweep_dispositions=2
```

This is a scope probe, not a proposed production patch. It establishes that the
Handback note's “must persist identity in `handback.py`” conclusion is too broad.
The remaining work still fits WI-413; WI-416's specific B+/B+2 instructions are
what remain incomplete.

### Migration statement and declared close-order red

```text
$ rg -l '^## Handback$' docs/work | sort; rg -l '^## Handback$' docs/work | wc -l; PATH=.venv/bin:$PATH python <frontmatter-probe>
docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md
       1
docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md status=queued blockref=None

$ PATH=.venv/bin:$PATH python project-trajectory/scripts/check_trajectory.py --root . --strict
check_trajectory: ERROR - R-A WI-416: status=queued (open) but the Deliverable is non-empty (an open WI's Deliverable is filled only at close)
check_trajectory: 1 error(s) in docs/work.
```

The strict command also emitted the ten pre-existing connectivity warnings
shown by the tool; the two lines above are its complete error/summary. This is
the expected red disclosed by WI-416 until its spec moves to `complete/`, not a
finding.

## Findings

1. **BLOCKING — `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:72`, `:74-77`, `:112-141`; `docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md:27-40`; `project-trajectory/scripts/intake.py:485-490`, `:525-530`, `:729-738` — B+/B+2 still silently suppress a genuine second return through the old title identity.**

   The Deliverable says no hash exists, neither prototype reads Git, the
   identity failure family is absent, and the only suppression is a loud pending
   judgment. The driven B+2 copy disproves all four claims. `_rev7` still reads
   Git and truncates to seven characters; `_handback_drafts` still puts it in
   the title; `_mint` still silently drops an exact title found in any state.
   Two distinct return commits with that prefix produced two real Handback
   sections but one disposition, with no pending artifact for the second event.

   Keep **re-queue as scoped**, but correct both records. The brief must carry
   unresolved-state authority through the shared draft/mint path rather than
   add a pre-filter while leaving title identity authoritative. Require a
   regression that closes the first disposition, performs a real second
   `returned_spec`/`_note`, forces an equal title token (or removes token
   authority), and proves `1 -> 2 -> 2`.

2. **MAJOR — `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:103-110`, `:134-141`; `docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md:37-40` — B+2 is left optional even though B+ fails one of R3's four outcomes.**

   I reproduced B+ at two dispositions after “surface an open item” closed the
   first, and B+2 at one. WI-416 allows either the open-item join or “a decision
   to leave the residual open”; WI-413 calls it optional. That permits shipping
   a known form of the remint defect. Make B+2, or another driven closure of that
   lifecycle, required. Deliberately accepting the defect would require a new
   owner-facing decision, not a builder option inside WI-413.

3. **MINOR — `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:42-44` — the migration measurement is stale within the same diff.**

   The final diff has one returned spec, but it does not “already carry both the
   section and the blockref”; this diff removed its blockref to enact re-queue.
   The no-migration conclusion remains sound because this return has already
   been adjudicated, not because the final tree still presents it as unresolved.
   State the measurement's pre-disposition timing or the final-tree reason.

## Requirement coverage

| Requirement / duty | Driven observation | Result |
|---|---|---|
| One unresolved return, repeated bare sweeps | B+/B+2 `1 -> 1 -> 1` | PASS |
| Genuine later real handback, then re-sweep | Ordinary SHA `1 -> 2 -> 2`; equal 7-prefix B+2 `1 -> 1` | FAIL |
| No owed judgment silently suppressed | Open-row skip loud; title-collision skip silent and artifact-free | FAIL |
| Re-queue/defer/cancel do not re-mint | B+ re-queue held at one; queued-only predicate bounds defer/cancel | PASS |
| Surface-open-item does not re-mint | B+ two; B+2 one | PASS only with B+2, which scope makes optional |
| R3 enactment and R1 | Existing files only; blockref removed; `blocked -> ready`; no new WI file | PASS |
| Permanent Handback record | Byte-identical to HEAD | PASS |
| Scope stays `intake.py` + tests | State-authoritative control passed collision without `handback.py` change | PASS; ruling outcome correct |
| Migration account matches final artifact | One Handback spec, final `blockref=None` | FAIL wording |

VERDICT: REWORK

---

## Round 2 — REWORK (1 BLOCKING, 1 MAJOR)

Independent fresh-context round 2, given round 1's recorded findings and told to
REGENERATE the collision rather than trust the pasted output. It did: two fresh
colliding commit pairs (31,590 and 23,918 nonce attempts), driven through the
real CLI as pytest cases.

**Round 1's three corrections are confirmed genuine, and the BLOCKING collision
is actually fixed** — baseline `1 -> 1`, the four-item prototype `1 -> 2`, with
the two dispositions now distinguishable (`return 1` / `return 2`). The
ordinal-title change this row went past the verdict to add was judged
**justified, not scope creep**. The amendment, census-gap and no-recursion
tests sharing `_mint` stay green.

What is rejected is the *newly added* pending-judgement machinery: the brief's
suppressors key off `WI-Refs` and `SpecRef`, which are broad relationship
fields, not disposition provenance — so an UNRELATED pre-existing open item or
adjudication row starves a genuine first return (minted 0). And the state
predicate assumes `handback.returned_spec` guarantees a non-empty `blockref`,
which it does not.

This diff is a docs-only R3 adjudication record. It re-queues WI-413 by clearing its `blockref`, preserves the permanent Handback note, and replaces the future `intake.py` implementation brief. Its blast radius is the scheduler frontier plus future disposition identity, suppression, and recovery behavior in the shared mint path.

The R3 enactment and all three round-1 corrections are genuine. The rewritten brief is still unsafe: its new provenance-free suppressors can starve a genuine return, and its state predicate depends on a nonempty `blockref` that the real handback producer does not guarantee.

## Failure classes hunted, worst-first

1. An owed disposition suppressed or indefinitely starved by a false “judgment pending” match.
2. Silent loss when the proposed state predicate disagrees with real handback output.
3. Duplicate dispositions after bypassing exact-title dedup, including same-merge recovery and every R3 lifecycle.
4. Regression in amendment or census-gap callers sharing `_mint`.
5. R3/R1 violation, altered Handback history, false migration evidence, or unjustified title-format scope growth.

All writes were confined to the supplied scratchpad. No product bar was run because `adjudication` declares none.

## Exact commands and driven output

### Diff enactment and permanent record

```text
$ S=<scratch>/review-a-r2-codex.VcfVSP
$ R="$S/repo"
$ D=<scratch>/wi416-r2.diff
$ git -C "$R" apply --numstat "$D"
55	1	docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md
169	0	docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md

$ git -C "$R" diff --name-status
M	docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md
M	docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md

$ git -C "$R" diff --diff-filter=A --name-only
[no output]

$ .venv/bin/python "$R/project-trajectory/scripts/schedule.py" --root "$R" ready --explain | rg '^WI-413\b'
WI-413     ready     parallel     rank=6 P0   down=0   path=0   parallel:ordinary;ready

$ REVIEW_REPO="$R" .venv/bin/python - <<'PY'
import os, subprocess
from pathlib import Path
root = Path(os.environ['REVIEW_REPO'])
rel = Path('docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md')
old = subprocess.run(['git', '-C', str(root), 'show', 'HEAD:' + rel.as_posix()], check=True, capture_output=True).stdout
new = (root / rel).read_bytes()
def note(data):
    return data.split(b'## Handback\n', 1)[1].split(b'\n## ', 1)[0]
print('Handback byte-identical:', note(old) == note(new))
print('HEAD blockref:', b'blockref =' in old.split(b'+++', 2)[1])
print('diff blockref:', b'blockref =' in new.split(b'+++', 2)[1])
PY
Handback byte-identical: True
HEAD blockref: True
diff blockref: False
```

Before applying the diff, the same scheduler command reported:

```text
WI-413     blocked   parallel     rank=6 P0   down=0   path=0   excluded:blocked:docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md
```

There is no added WI file, drafted follow-up, open-item edit, or recursive disposition.

### Original seven-character collision, regenerated

The baseline and four-item prototype both use the real `returned_spec`/`_note` output and real `intake.py sweep` CLI:

```text
$ set -o pipefail
$ S=<scratch>/review-a-r2-codex.VcfVSP
$ B="$S/baseline"; P="$S/prototype"
$ .venv/bin/python -m pytest -q -s \
  "$B/tests/test_wi416_review_r2.py::test_real_cli_reproduces_the_seven_character_collision" \
  --basetemp="$S/pytest-baseline-collision-final" 2>&1 \
  | rg 'real_return|collision_search|sweep minted|after_first|after_second|titles=|passed'
real_return lane=lane-one sections=1 blockref=True
collision_search attempts=31590 nonces=208,31590 shas=327affb959f8,327affb5aa07 prefix_equal=True
intake: sweep minted 1 row(s).
after_first=1
real_return lane=lane-two sections=2 blockref=True
intake: sweep minted 0 row(s).
after_second=1 sections=2
titles=['dispose: WI-005 handed back at 327affb (docs/work/queued/WI-005-returned.md) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)']
1 passed in 0.41s

$ .venv/bin/python -m pytest -q -s \
  "$P/tests/test_wi416_review_r2.py::test_real_cli_reproduces_the_seven_character_collision" \
  --basetemp="$S/pytest-prototype-collision-final" 2>&1 \
  | rg 'real_return|collision_search|sweep minted|after_first|after_second|titles=|passed'
real_return lane=lane-one sections=1 blockref=True
collision_search attempts=23918 nonces=1524,23918 shas=2a2093330f71,2a2093340a2e prefix_equal=True
intake: sweep minted 1 row(s).
after_first=1
real_return lane=lane-two sections=2 blockref=True
intake: sweep minted 1 row(s).
after_second=2 sections=2
titles=['dispose: WI-005 handed back (return 1, docs/work/queued/WI-005-returned.md) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)', 'dispose: WI-005 handed back (return 2, docs/work/queued/WI-005-returned.md) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)']
1 passed in 0.53s
```

Round 1’s BLOCKING collision is therefore actually fixed by items 1–4.

### Duplicate and shared-mint regression drives

```text
$ .venv/bin/python -m pytest -q -s \
  "$P/tests/test_wi416_review_r2.py::test_bare_sweep_and_same_merge_recovery_hold_one_return" \
  "$P/tests/test_wi416_review_r2.py::test_every_r3_outcome_closes_without_a_remint" \
  "$P/tests/test_wi416_review_r2.py::test_state_owed_bypasses_an_identical_title_then_open_state_holds" \
  --basetemp="$S/pytest-prototype-lifecycles-final" 2>&1 \
  | rg 'same_merge_and_bare_counts|r3_lifecycles|forced_equal_title_counts|passed'
same_merge_and_bare_counts=[1, 1, 1, 1]
r3_lifecycles={'requeue': (1, 1), 'defer': (1, 1), 'cancel': (1, 1), 'open-item': (1, 1)}
forced_equal_title_counts=1->2->2 titles_equal=True
3 passed in 2.29s

$ .venv/bin/python -m pytest -q \
  "$P/tests/test_intake.py::test_the_amendment_mint_is_idempotent_across_a_rerun" \
  "$P/tests/test_intake.py::test_the_census_mints_gap_rows_and_dedupes_on_rerun" \
  "$P/tests/test_intake.py::test_a_handed_back_adjudication_row_mints_no_second_disposition" \
  --basetemp="$S/pytest-prototype-shared-mint"
conftest: could not bound CPU use (PermissionError: [Errno 1] Operation not permitted) — this run is NOT capped.
...                                                                      [100%]
3 passed in 0.66s
```

Thus the state-owed bypass does not inherently duplicate same-merge recovery, amendment, census, or recursive-disposition paths. The ordinal-title change is justified rather than scope creep: it removes obsolete Git identity from trigger (b), leaves the other triggers’ exact-title behavior intact, and requires no migration of existing rows.

### New suppressors introduced by the brief

```text
$ .venv/bin/python -m pytest -q -s \
  "$B/tests/test_wi416_review_r2.py::test_current_code_mints_despite_a_preexisting_unrelated_pending_oi" \
  "$B/tests/test_wi416_review_r2.py::test_current_code_mints_a_real_return_that_retains_an_empty_blockref" \
  --basetemp="$S/pytest-baseline-controls-final" 2>&1 \
  | rg 'baseline_unrelated|baseline_empty|passed'
baseline_unrelated_pending_oi dispositions=1 pending_oi=OI-099
baseline_empty_blockref sections=1 parsed_blockref='' dispositions=1
2 passed in 0.61s

$ .venv/bin/python -m pytest -q -s \
  "$P/tests/test_wi416_review_r2.py::test_preexisting_unrelated_pending_oi_suppresses_a_genuine_return" \
  "$P/tests/test_wi416_review_r2.py::test_unrelated_open_adjudication_suppresses_a_genuine_return" \
  "$P/tests/test_wi416_review_r2.py::test_real_return_over_an_empty_blockref_key_is_not_seen_as_owed" \
  --basetemp="$S/pytest-prototype-suppressors-final" 2>&1 \
  | rg 'already cites|unrelated_pending|unrelated_open|empty_blockref|passed'
intake: WI-005 carries a handback and a pending open item already cites it - no disposition minted (a judgement is already pending)
unrelated_pending_oi actual_dispositions=0 pending_oi=OI-099
intake: WI-005 carries a handback and an OPEN disposition row already cites it - no second disposition minted (a judgement is already pending)
unrelated_open_adjudication actual_dispositions=0 open_row=WI-006
empty_blockref sections=1 parsed_blockref='' dispositions=0
3 passed in 0.42s
```

## Coverage map

| Required behavior | Driven result | Result |
|---|---|---|
| Original seven-character collision | Baseline `1→1`; items 1–4 `1→2` | PASS |
| State-authoritative identical-title bypass | Forced equal titles `1→2→2` | PASS |
| One unresolved return across repeated/same-merge recovery | `[1,1,1,1]` | PASS |
| Four R3 closures | requeue/defer/cancel/open-item all `(1,1)` | PASS |
| Amendment and census dedup | Selected real tests green | PASS |
| No recursion | Existing real test green | PASS |
| Suppress only a pending disposition judgment | Unrelated OI and unrelated adjudication each suppress | FAIL |
| State predicate covers real handback output | Empty retained `blockref` produces zero rows | FAIL |
| R3/R1 enactment | Existing files only; blocked→ready; permanent note unchanged | PASS |
| Round-1 record corrections | Old false claims no longer asserted; lifecycle required; migration timing corrected | PASS |

## Findings

1. **BLOCKING — `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:56`, `docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md:48` — the required pending-judgment filters mistake generic references for disposition provenance and suppress genuine returns.**

   `WI-Refs` is a broad relationship field used by `context_block` for premise-risk joins; it does not say an OI was surfaced as this return’s R3 outcome. `SpecRef` likewise identifies an open row’s general spec-of-record, not that the row is the handback disposition. A pre-existing OI about API X and an unrelated adjudication row both cited WI-005. A faithful implementation printed “judgement already pending” and minted zero dispositions for a genuine first return.

   The brief must require positive disposition provenance. At minimum, an open adjudication must be identified as the target’s disposition rather than merely share its `SpecRef`; a surfaced OI must link to the particular disposition/return, not merely mention the target in `WI-Refs`. Add negative controls for pre-existing unrelated OIs and adjudications.

2. **MAJOR — `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:36`, `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:52`, `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:146`, `project-trajectory/scripts/handback.py:192` — the claimed persisted-state invariant is not enforced by the real producer.**

   `returned_spec` adds a blockref only when no `blockref =` key exists. A syntactically valid ready spec carrying `blockref = ""` keeps that empty value when genuinely returned. The actual transform produced one Handback section and parsed `BlockRef=''`. Current intake minted its disposition; the required queued+nonempty-blockref prototype silently minted zero on a bare sweep.

   Treating mere key presence as state would not fix this: `schedule._disposition` treats the empty value as ready. The brief must either normalize/enforce a nonempty blockref in the real handback path or explicitly repair/refuse this state before relying on it, with a regression covering the actual `returned_spec` output. Until then, “no `handback.py` change” and “any future return re-adds both markers” are unsupported.

VERDICT: REWORK

---

## Round 3 — REWORK (2 BLOCKING)

Independent fresh-context round 3, asked FIRST to judge whether the owner-directed
change of shape (drop the implementation prescription; record ruled facts + failure
classes; route the producer defect as a drafted follow-up) was legitimate scoping or
an evasion laundering two rounds of findings into prose.

**Ruled legitimate, and argued** — from §A5.2 (`concurrency-v2.md:638-642`), from R3's
"the row's job is the judgement, never the recovery" (`rulings-context-2026-08-01.md:123-139`),
and from the WI-414 precedent, which ruled scope and left the amendment's construction
to the row with the real bar. The reviewer also verified the rewritten records PRESERVE
rather than dissolve the earlier failures (F1 carries the collision, F2 the four R3
outcomes, F4 both starvation controls, F5 the routed producer defect).

Both BLOCKING findings are record COMPLETENESS/ACCURACY defects, not new mechanism
holes: one previously driven starvation class was dropped, and one historical count is
wrong.

This diff is a docs-only R3 adjudication disposition. It re-queues WI-413 by clearing its `blockref`, replaces the rejected implementation prescription with failure constraints for the future product-bar lane, and drafts—but does not mint—one follow-up for `handback.returned_spec`’s empty-`blockref` defect. Its blast radius is WI-413’s scheduler readiness, the future handback-dedup design, and the follow-up that intake will mint when WI-416 closes.

## Shape judgment

The new shape is legitimate adjudication scope, not inherently an evasion.

- §A5.2 says an adjudication row runs no product bar because its outputs are Status changes and work-registry judgments (`docs/concurrency-v2.md:638-642`).
- R3 says the dispatcher/intake machinery creates the row, while “the row’s job is the judgement, never the recovery” (`docs/archive/history/rulings-context-2026-08-01.md:123-139`). Any follow-up is drafted in the adjudication row and minted later by intake, not assigned an ID in-lane (`docs/log.md:28-40`).
- WI-414 is a direct precedent: it ruled the affected scope and left construction of the exact amendment to the spine row with the real bar (`docs/work/complete/WI-414-adjudicate-tc-056-ratified-routed-cel.md:71-79`).
- The rewritten records preserve the WI-416 review failures rather than claiming a mechanism fixed them: F1 carries the title-collision loss; F2 makes all four R3 outcomes mandatory; F4 carries both false-provenance starvation controls; F5 records and routes the producer defect; the migration timing is corrected.

Therefore, removing the unsafe prescription and returning mechanism ownership to WI-413 is proper. The record is still incomplete because one previously driven starvation class was dropped, and one historical assertion is false.

## Failure classes hunted, worst-first

1. A genuinely owed disposition becoming permanently unclaimable or silently starved.
2. Silent loss through title collisions, false provenance, or empty-`blockref` assumptions.
3. Duplicate dispositions across repeated sweeps, same-merge recovery, and all four R3 outcomes.
4. Regression in amendment, census, or no-recursion paths sharing `_mint`.
5. R1/R3 violation: lane-side ID mint, recursive handback, altered history, or uncleared block.
6. False or overstated adjudication record facts.

## Findings

1. **BLOCKING — `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:72-171`; `docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md:46-72` — F1–F6 omit open-disposition path durability, quietly dropping WI-413 round-2’s dangling-`specref` starvation finding.**

   WI-413’s binding round-2 review found that moving a returned spec can leave its open disposition pointing at the deleted pathname and therefore unclaimable (`docs/reviews/WI-413-REVIEW-A.md:231-235`). Neither F1–F6 nor the required regression shape covers this.

   I reproduced it through the shipped paths: current intake minted WI-419 for WI-413; real `spec_move.move_spec` moved WI-413 from `queued/` to `deferred/`; the disposition retained the queued pathname; actual `integrate.claim` refused it under R-E. This is judgment starvation, not a cosmetic dangling link.

   A future lane can pass every listed regression without ever moving the target while its disposition remains open, yet ship this defect. Add a failure class and real move→claim regression, or explicitly route this separate defect as another drafted follow-up, as was done for empty `blockref`.

2. **BLOCKING — `docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md:19-23` — the record says there were four prior findings; the binding review contains five.**

   Round 1 recorded one BLOCKING, one MAJOR, and one MINOR; round 2 recorded one BLOCKING and one MAJOR. The intended distinction appears to be four implementation-prescription findings plus one stale-migration record defect, but the Deliverable says “all four findings against this row.” Under the supplied rule that false record claims are blocking, this must say five and distinguish the four prescription findings from the corrected record-only MINOR.

## Exact driven commands and output

### Derived identities and F1 collision

```text
$ R3_LAST=<scratch>/r3-last-touch.H99DUu
$ git -C "$R3_LAST" checkout -q b05dca68
$ R3_LAST="$R3_LAST" R3_SCRATCH=<scratch> .venv/bin/python - <<'PY'
import os, runpy, sys, tempfile
from pathlib import Path
repo = Path(os.environ['R3_LAST'])
sys.path.insert(0, str(repo / 'tests'))
sys.path.insert(0, str(repo / 'project-trajectory/scripts'))
ns = runpy.run_path(str(repo / 'tests/test_intake.py'))
root = ns['handback_repo'](Path(tempfile.mkdtemp(dir=os.environ['R3_SCRATCH'])))
ns['_sweep'](root)
target = root / 'docs/work/queued/WI-005-returned.md'
target.write_text('\n'.join(ln for ln in target.read_text(encoding='utf-8').splitlines() if not ln.startswith('blockref =')) + '\n', encoding='utf-8', newline='\n')
ns['_commit'](root, 'ordinary re-queue clears blockref', when=ns['T_CODE'] + 400)
ns['_sweep'](root)
disps = sorted((root / 'docs/work/queued').glob('WI-*-dispose-*.md'))
print('last_touch_after_clear_dispositions=', len(disps), sep='')
PY
intake: minted WI-006 at docs/work/queued/WI-006-dispose-wi-005-handed-back-at-a84a5cf.md
intake: sweep minted 1 row(s).
intake: minted WI-007 at docs/work/queued/WI-007-dispose-wi-005-handed-back-at-748e5d1.md
intake: sweep minted 1 row(s).
last_touch_after_clear_dispositions=2

$ R3_NOTE=<scratch>/r3-note-digest.zkqJdY
$ git -C "$R3_NOTE" checkout -q b2046825
$ R3_NOTE="$R3_NOTE" R3_SCRATCH=<scratch> .venv/bin/python - <<'PY'
import os, runpy, sys, tempfile
from pathlib import Path
repo = Path(os.environ['R3_NOTE'])
sys.path.insert(0, str(repo / 'tests'))
sys.path.insert(0, str(repo / 'project-trajectory/scripts'))
ns = runpy.run_path(str(repo / 'tests/test_intake.py'))
root = ns['handback_repo'](Path(tempfile.mkdtemp(dir=os.environ['R3_SCRATCH'])))
ns['_sweep'](root)
target = root / 'docs/work/queued/WI-005-returned.md'
target.write_text(target.read_text(encoding='utf-8') + '\n## Context\n\nUnrelated annotation.\n', encoding='utf-8', newline='\n')
ns['_commit'](root, 'append unrelated context', when=ns['T_CODE'] + 400)
ns['_sweep'](root)
disps = sorted((root / 'docs/work/queued').glob('WI-*-dispose-*.md'))
print('note_digest_after_context_dispositions=', len(disps), sep='')
PY
intake: minted WI-006 at docs/work/queued/WI-006-dispose-wi-005-handed-back-105f0d3ce0a.md
intake: sweep minted 1 row(s).
intake: minted WI-007 at docs/work/queued/WI-007-dispose-wi-005-handed-back-d14ea3977e6.md
intake: sweep minted 1 row(s).
note_digest_after_context_dispositions=2
```

Fresh collision rerun against the shipped baseline and historical state-authoritative prototype:

```text
$ S=<scratch>/review-a-r2-codex.VcfVSP
$ PYTEST_CPU_CAP=off .venv/bin/python -m pytest -q -s "$S/baseline/tests/test_wi416_review_r2.py::test_real_cli_reproduces_the_seven_character_collision" --basetemp="$S/pytest-r3-baseline-collision" 2>&1 | rg 'real_return|collision_search|sweep minted|after_first|after_second|titles=|passed'
real_return lane=lane-one sections=1 blockref=True
collision_search attempts=11400 nonces=1152,11400 shas=23a5466b0234,23a5466a54e9 prefix_equal=True
intake: sweep minted 1 row(s).
after_first=1
real_return lane=lane-two sections=2 blockref=True
intake: sweep minted 0 row(s).
after_second=1 sections=2
titles=['dispose: WI-005 handed back at 23a5466 (docs/work/queued/WI-005-returned.md) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)']
1 passed in 0.42s

$ PYTEST_CPU_CAP=off .venv/bin/python -m pytest -q -s "$S/prototype/tests/test_wi416_review_r2.py::test_real_cli_reproduces_the_seven_character_collision" --basetemp="$S/pytest-r3-prototype-collision" 2>&1 | rg 'real_return|collision_search|sweep minted|after_first|after_second|titles=|passed'
real_return lane=lane-one sections=1 blockref=True
collision_search attempts=11400 nonces=1152,11400 shas=23a5466b0234,23a5466a54e9 prefix_equal=True
intake: sweep minted 1 row(s).
after_first=1
real_return lane=lane-two sections=2 blockref=True
intake: sweep minted 1 row(s).
after_second=2 sections=2
titles=['dispose: WI-005 handed back (return 1, docs/work/queued/WI-005-returned.md) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)', 'dispose: WI-005 handed back (return 2, docs/work/queued/WI-005-returned.md) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)']
1 passed in 0.52s
```

### F2–F5 spot checks

```text
$ PYTEST_CPU_CAP=off .venv/bin/python -m pytest -q -s \
  "$S/prototype/tests/test_wi416_review_r2.py::test_bare_sweep_and_same_merge_recovery_hold_one_return" \
  "$S/prototype/tests/test_wi416_review_r2.py::test_every_r3_outcome_closes_without_a_remint" \
  "$S/prototype/tests/test_wi416_review_r2.py::test_state_owed_bypasses_an_identical_title_then_open_state_holds" \
  --basetemp="$S/pytest-r3-prototype-lifecycles" 2>&1 | rg 'same_merge_and_bare_counts|r3_lifecycles|forced_equal_title_counts|passed'
same_merge_and_bare_counts=[1, 1, 1, 1]
r3_lifecycles={'requeue': (1, 1), 'defer': (1, 1), 'cancel': (1, 1), 'open-item': (1, 1)}
forced_equal_title_counts=1->2->2 titles_equal=True
3 passed in 2.27s

$ PYTEST_CPU_CAP=off .venv/bin/python -m pytest -q -s \
  "$S/prototype/tests/test_wi416_review_r2.py::test_preexisting_unrelated_pending_oi_suppresses_a_genuine_return" \
  "$S/prototype/tests/test_wi416_review_r2.py::test_unrelated_open_adjudication_suppresses_a_genuine_return" \
  "$S/prototype/tests/test_wi416_review_r2.py::test_real_return_over_an_empty_blockref_key_is_not_seen_as_owed" \
  --basetemp="$S/pytest-r3-prototype-suppressors" 2>&1 | rg 'already cites|unrelated_pending|unrelated_open|empty_blockref|passed'
intake: WI-005 carries a handback and a pending open item already cites it - no disposition minted (a judgement is already pending)
unrelated_pending_oi actual_dispositions=0 pending_oi=OI-099
intake: WI-005 carries a handback and an OPEN disposition row already cites it - no second disposition minted (a judgement is already pending)
unrelated_open_adjudication actual_dispositions=0 open_row=WI-006
empty_blockref sections=1 parsed_blockref='' dispositions=0
3 passed in 0.44s

$ PYTEST_CPU_CAP=off .venv/bin/python -m pytest -q -s \
  "$S/baseline/tests/test_wi416_review_r2.py::test_current_code_mints_despite_a_preexisting_unrelated_pending_oi" \
  "$S/baseline/tests/test_wi416_review_r2.py::test_current_code_mints_a_real_return_that_retains_an_empty_blockref" \
  --basetemp="$S/pytest-r3-baseline-controls" 2>&1 | rg 'baseline_unrelated|baseline_empty|passed'
baseline_unrelated_pending_oi dispositions=1 pending_oi=OI-099
baseline_empty_blockref sections=1 parsed_blockref='' dispositions=1
2 passed in 0.62s

$ PYTEST_CPU_CAP=off .venv/bin/python -m pytest -q \
  "$S/prototype/tests/test_intake.py::test_the_amendment_mint_is_idempotent_across_a_rerun" \
  "$S/prototype/tests/test_intake.py::test_the_census_mints_gap_rows_and_dedupes_on_rerun" \
  "$S/prototype/tests/test_intake.py::test_a_handed_back_adjudication_row_mints_no_second_disposition" \
  --basetemp="$S/pytest-r3-prototype-shared-mint"
...                                                                      [100%]
3 passed in 0.64s
```

Real producer plus real scheduler:

```text
$ PYTHONPATH=project-trajectory/scripts .venv/bin/python - <<'PY'
import handback, schedule
rel = 'docs/work/queued/WI-005-returned.md'
base = '''+++
id = "WI-005"
title = "Returned"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
blockref = ""
+++
'''
note = handback._note('lane-one', 'genuine return', '1111111111..2222222222')
returned = handback.returned_spec(base, rel, note)
row, _ = schedule.parse_spec_row(returned, 'queued/WI-005-returned.md')
wi = schedule.load_wis([row])[0]
empty = schedule._disposition(wi, {'WI-005':'queued'}, set(), schedule.CONCURRENCY_PARALLEL, ['parallel:ordinary'], {})
blocked = schedule._disposition(dict(wi, blockref=rel), {'WI-005':'queued'}, set(), schedule.CONCURRENCY_PARALLEL, ['parallel:ordinary'], {})
print('retained_blockref_lines=', [ln for ln in returned.splitlines() if ln.startswith('blockref =')], sep='')
print('handback_sections=', returned.count('\n## Handback\n'), 'parsed_blockref=', repr(wi['blockref']), sep='')
print('empty_disposition=', empty, sep='')
print('nonempty_disposition=', blocked, sep='')
PY
retained_blockref_lines=['blockref = ""']
handback_sections=1parsed_blockref=''
empty_disposition=('ready', ['parallel:ordinary', 'ready'])
nonempty_disposition=('blocked', ['excluded:blocked:docs/work/queued/WI-005-returned.md'])
```

### Draft parser and real intake mint

```text
$ PYTHONPATH=project-trajectory/scripts .venv/bin/python - <<'PY'
from pathlib import Path
import intake
p = Path('docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md')
drafts, refusal = intake.parse_dispositions(p.read_text(encoding='utf-8'), p.as_posix())
print('draft_count=', len(drafts), 'refusal=', refusal, sep='')
for d in drafts:
    print('draft_keys=', sorted(d), sep='')
    print('workstream=', repr(d.get('workstream')), ' buildtier=', repr(d.get('buildtier')), ' kind=', repr(d.get('kind')), sep='')
    print('specref=', repr(d.get('specref')), ' needs=', repr(d.get('needs')), ' planmode=', repr(d.get('planmode')), sep='')
print('queued_merged_outcome=', intake._disposition_drafts(Path('.'), {'WI-416': 'merged'}), sep='')
PY
draft_count=1refusal=None
draft_keys=['buildtier', 'kind', 'specref', 'title', 'workstream']
workstream='scripts' buildtier='strong' kind='ordinary'
specref='docs/reviews/WI-416-REVIEW-A.md' needs=None planmode=None
queued_merged_outcome=([], None)
```

In a scratch clone with the reviewed files copied and WI-416 moved to `complete/`, I drove `intake_after_merge`:

```text
intake: minted WI-419 at docs/work/queued/WI-419-handback-returned-spec-does-not-guarante.md
first_minted=[('WI-419', 'docs/work/queued/WI-419-handback-returned-spec-does-not-guarante.md')] refusal=None
minted_row={'WI-ID': 'WI-419', 'Status': 'queued', 'SafetyClass': 'ordinary', 'BuildTier': 'strong', 'SpecRef': 'docs/reviews/WI-416-REVIEW-A.md', 'Predecessors': ''}
rerun_minted=[] refusal=None
```

Thus the section parses, mints nothing while WI-416 remains queued, chooses no ID itself, carries no `needs`, mints an ordinary follow-up at the real merge arm, and dedupes its rerun.

### Missing path-starvation class

After minting the live WI-413 disposition in another scratch clone:

```text
$ .venv/bin/python "$R3_PATH/project-trajectory/scripts/intake.py" --root "$R3_PATH" sweep
intake: minted WI-419 at docs/work/queued/WI-419-dispose-wi-413-handed-back-at-8f9b3bb.md
intake: sweep minted 1 row(s).

$ R3_PATH="$R3_PATH" PYTHONPATH="$R3_PATH/project-trajectory/scripts" .venv/bin/python - <<'PY'
import os, subprocess
from pathlib import Path
import agent_common as ac
import integrate, spec_move
root = Path(os.environ['R3_PATH'])
src = 'docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md'
dst = 'docs/work/deferred/WI-413-bare-sweep-re-mints-open-dispositions.md'
touched, refusal = spec_move.move_spec(root, src, dst)
print('move_touched=', touched, ' move_refusal=', refusal, sep='')
subprocess.run(['git','-C',str(root),'add','-A'], check=True)
subprocess.run(['git','-C',str(root),'commit','-q','--no-verify','-m','scratch: defer returned target'], check=True)
row = next(r for r in ac.read_spec_rows(root / 'docs/work') if r['WI-ID'] == 'WI-419')
print('disposition_specref=', repr(row['SpecRef']), ' exists=', (root / row['SpecRef']).is_file(), sep='')
rc = integrate.claim(root, 'WI-419', 'wi-419-review-r3')
print('claim_rc=', rc, sep='')
PY
integrate: REFUSED - WI-419 SpecRef 'docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md' does not resolve to an in-repo FILE (R-E: a directory or missing path reds the bar) - fix the queued spec, then claim (WI-370)
move_touched=[] move_refusal=None
disposition_specref='docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md' exists=False
claim_rc=1
```

### R1/R3 enactment and record count

```text
$ git diff --no-ext-diff HEAD -- docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md | cmp - <scratch>/wi416-r3.diff; printf 'diff_cmp_rc=%s\n' "$?"
diff_cmp_rc=0

$ git apply --numstat <scratch>/wi416-r3.diff
59	1	docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md
206	0	docs/work/queued/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md

$ .venv/bin/python project-trajectory/scripts/schedule.py --root . ready --explain | rg '^WI-413\b'
WI-413     ready     parallel     rank=6 P0   down=0   path=0   parallel:ordinary;ready

$ rg -l '^## Handback$' docs/work | sort
docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md

$ rg -l '^## Handback$' docs/work | wc -l
       1
```

The `## Handback` section compared byte-identical to HEAD, and HEAD had the frontmatter `blockref` while the diff does not:

```text
handback_byte_identical=True
head_blockref=Truediff_blockref=False
```

Prior-finding count:

```text
$ rg -n '^[0-9]+\. \*\*(BLOCKING|MAJOR|MINOR)' docs/reviews/WI-416-REVIEW-A.md
280:1. **BLOCKING — ...
297:2. **MAJOR — ...
306:3. **MINOR — ...
523:1. **BLOCKING — ...
529:2. **MAJOR — ...
```

Declared close-order red:

```text
$ PYTHONPATH=project-trajectory/scripts .venv/bin/python project-trajectory/scripts/check_trajectory.py --root . --strict 2>&1 | rg 'ERROR|error\(s\)'
check_trajectory: ERROR - R-A WI-416: status=queued (open) but the Deliverable is non-empty (an open WI's Deliverable is filled only at close)
check_trajectory: 1 error(s) in docs/work.
```

No product bar was run because `safety_class = "adjudication"` declares no product bar. No tracked file was modified by this review; scratch writes remained under the supplied scratchpad.

VERDICT: REWORK
