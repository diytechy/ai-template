# WI-413 — REVIEW-A (2026-08-02)

**Reviewer:** OPENAI-SOL (`gpt-5.6-sol`) via the `codex` CLI — cross-family,
fresh context, independent of the builder. Charter:
[code-review-adversarial](../rubrics/code-review-adversarial.md). Given the code
diff and the requirement surface (WI-388 REVIEW-A finding 6) and **not** the
builder's Deliverable, fragment or commit messages.

**Verdict: REWORK** — 1 BLOCKING, 2 MAJOR, 1 MINOR. The builder's fix direction
(derive the dedup token from the returned spec's last-touch commit) does not
hold: `git log -1 -- <path>` names the last touch for ANY reason, so ordinary
lifecycle activity — clearing a `blockref` to re-queue, moving a still-marked
spec `queued/` → `deferred/` — moves the token and re-mints. Machine-local
absolute paths in the reviewer's own output were rewritten to repo-relative
form; nothing else in the verdict is edited.

---

## Subject framing

This diff changes disposition identity from the observed merge/sweep HEAD to the most recent commit touching the returned spec’s current pathname. That identity is persisted in the disposition title and drives exact-title deduplication across both merge-slot intake and recovery sweeps.

The required contract is:

1. Repeated sweeps of one return event mint exactly one disposition.
2. A genuine later handback mints another disposition.

I did not read the prohibited implementer assessments or branch commit messages.

## Failure classes hunted

Worst-first:

- Silent suppression of an owed second judgment.
- Duplicate dispositions after normal requeue/defer activity.
- Laundering through the modified previously-green test.
- Missing, shallow, renamed, dirty, or detached Git history.
- Byte-identical returns, reverts, and abbreviated-hash collisions.

## Modified-test judgment

The old fixture was wrong: committing only `seed.txt` while manually claiming another handback outcome does not model `returned_spec` (project-trajectory/scripts/handback.py:177). It produced:

```text
old unrelated-file fixture: merge_shas_differ=True second_minted=0
```

The new fixture is directionally faithful because it commits a changed returned spec, although actual `returned_spec` appends another `## Handback` section rather than replacing the first note. A complete shipped `hand_back → re-claim → hand_back` drive produced:

```text
real hand_back twice: handback_sections=2 dispositions=2
```

Therefore, modifying the old fixture did not launder the old fixture’s real contract.

## What I ran

The literal requested command initially lacked `python` on PATH:

```text
$ python -m pytest -q tests/test_intake.py
zsh:1: command not found: python
```

Using the repo’s declared virtualenv:

```text
$ PATH=.venv/bin:$PATH python -m pytest -q tests/test_intake.py
.....................                                                    [100%]
21 passed, 1 warning in 4.52s
```

The warning was only an unwritable pytest cache; the lane worktree remained clean.

Independent `/tmp` drives:

```text
stable-three counts: [1, 1, 1]
returned_spec second event: handback_sections=2 dispositions=2
same-return requeue-edit: tokens=a84a5cf->a9dbb0e dispositions=2
same-return path-move: token=8fdc79a dispositions=2
untracked-return counts: [1, 2, 2]
detached-head counts: [1, 1]
shallow-clone: is_shallow=true token=e509662 counts=[1, 1]
shallow existing disposition: original_token=a84a5cf shallow_token=b872b6f counts=1->2
```

Mutation back to the previous HEAD-based behavior proved the new regression test is load-bearing:

```text
old-token mutation counts: [1, 2, 3]
```

Byte-identical `returned_spec` mutation:

```text
byte-identical returned_spec mutation: bytes_equal=True dispositions=2
```

Collision drive over 80,000 real Git commits:

```text
7-prefix collision suppression: first=7920e94dd741 second=7920e941063e git_abbrev=7920e941063e helper_token=7920e94 counts=1->1
```

I did not construct a separate amend/history-rewrite scenario and am not relying on one for any finding. A byte-restoring revert was driven and reminted:

```text
post-return edit then byte-restoring revert: dispositions= 3
```

## Findings

1. **BLOCKING — `intake.py:516` (project-trajectory/scripts/intake.py:516) and `intake.py:557` (project-trajectory/scripts/intake.py:557): the “return event” identity changes after ordinary requeue/defer activity.**

   `_return_event7` finds the latest touch of the current pathname, not the commit that performed the return. Clearing `blockref` changed the token and minted a duplicate. Moving the still-marked spec from `queued/` to `deferred/` changed both the token and the pathname embedded in the title, also minting a duplicate.

   These are normal lifecycle operations explicitly mentioned by the new comments. The implementation therefore does not provide “one event one name however many sweeps.”

   Derive or persist an immutable return-event identity and an immutable event pathname/key. Add drives for blockref clearing, queued→deferred, and equivalent requeue moves.

2. **MAJOR — `intake.py:516` (project-trajectory/scripts/intake.py:516): missing or shallow history falls back to a changing observer and remints.**

   An untracked returned spec yielded `[1, 2, 2]`: the first sweep used fallback HEAD, then the bookkeeping commit added the spec, so the second sweep identified that bookkeeping commit as a different event.

   A shallow clone containing an existing disposition similarly changed the apparent last-touch commit to the unrelated shallow-boundary commit and went from one disposition to two.

   History insufficient to establish an event should refuse loudly or use an identity stored with the return; it must not silently substitute current HEAD. Detached HEAD itself behaved correctly.

3. **MAJOR — `intake.py:518` (project-trajectory/scripts/intake.py:518): truncating Git’s unambiguous `%h` can silently suppress a genuinely new handback.**

   Git lengthened two colliding commit abbreviations to 12 characters, but `_return_event7` truncated both back to the same seven characters. With the first disposition present, the second distinct return-touch commit produced `sweep minted 0 row(s)`.

   This is the worse failure class: an owed judgment disappears silently. Preserve Git’s full unambiguous abbreviation or use the full object ID as the deduplication key.

4. **MINOR — `intake.py:512` (project-trajectory/scripts/intake.py:512) and `test_intake.py:304` (tests/test_intake.py:304): the stated byte-identical limitation and test framing are inaccurate.**

   Even when `returned_spec` was mutated to return byte-identical contents, `hand_back` moved the spec from `active/` to `queued/`, so Git recorded a new touch and a second disposition was minted. The test’s opening comment also still says the title carries the merge SHA.

   Correct the rationale and preferably retain an actual two-handback integration test.

## Required-behavior coverage map

| Required behavior | Coverage | Result |
|---|---|---|
| Repeated sweep of one still-marked return mints one disposition | New triple-sweep test and `[1,1,1]` drive | Narrow clean-history case passes; overall behavior fails after requeue, move, dirty recovery, or shallow cloning |
| Genuine second handback mints a second disposition | New test, direct `returned_spec` drive, and full `hand_back → re-claim → hand_back` drive | Covered and passes |

VERDICT: REWORK