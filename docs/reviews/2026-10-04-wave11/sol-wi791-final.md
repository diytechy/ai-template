38709c82 NOT YET SOUND

## BLOCKER

none

## MAJOR

none

## MINOR

1. project-trajectory/scripts/baseline_snapshot.py:1228 and :1250 — Relative verdict paths are neither resolved nor confined to the repository. I reproduced `../v.md` being accepted and advancing the ledger, contradicting docs/test/test-cases.toml:2489’s outside-repository refusal claim. A valid CLARITY verdict at `docs/reviews/../reviews/v.md` is also recorded unchanged, then refused at merge because `git show` cannot resolve it. Canonicalize relative paths against the root and refuse paths resolving outside it.

2. tests/test_adjudicate_brief.py:866 — The DA/SUR test checks only the assumption’s after text and the surrogate’s before text. I ran the actual test with the renderer omitting the other two sides; it still passed. TC-161 claims before/after coverage for both tiers. Assert each row’s labelled before and after values.

## Verified

The five prior reproduction scenarios are fixed in code and cells. All nine prescribed cell replacements and their test blocks landed exactly. The act changes only SR-228’s Status; seq 29 approves SR-228 and names exactly verdict 005’s fourteen re-attestations. SR-224 remains Drafted. All seven snapshot copies were checked: the act’s three copies and external match live bytes; unchanged components, interfaces and needs retain pre-existing drift. The recorded act is the adjudicator’s judgment, and OI-45’s scripted flip still writes nothing. The worktree remains clean.

## Commands

With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt` and bytecode writes disabled:

```powershell
C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 0 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-791-final tests/test_snapshot_readers.py tests/test_baseline_snapshot.py tests/test_adjudicate_brief.py tests/test_gen_open_items_render.py tests/test_intake.py
```

347 passed in 357.36s.

```powershell
C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict
```

Exit 0, with advisories.

Git log/diff/show, bounded source reads, and scratch-only Python comparisons/probes verified the cells, ledger, snapshot bytes and both findings. `git diff --check 523d576a 38709c82` passed; final `git status --short` was empty.