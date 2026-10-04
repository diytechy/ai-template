2eaa8ebd SOUND

BLOCKER: none  
MAJOR: none  
MINOR: none

Verified:

- `../v.md` is refused; ledger and snapshot files remain byte-identical.
- `docs/reviews/../reviews/v.md` records `docs/reviews/v.md`, readable through `git show`.
- All four DA/SUR line omissions and the prior paired mutation fail the actual test. Renderer restored; test passes.
- No registry or `docs/archive/last_approved/` changes. Regenerated views only update provenance.
- Prescribed suite: **226 passed in 281.70s**. Worktree unchanged and clean.

Commands:

```powershell
$env:GIT_CEILING_DIRECTORIES = "C:/Projects/ai-template.wt"
$env:PYTHONDONTWRITEBYTECODE = "1"
C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 0 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-791-recheck tests/test_baseline_snapshot.py tests/test_adjudicate_brief.py tests/test_snapshot_readers.py
```

Also ran scratch-only Python reproductions, Git tree comparisons, `git show`, `git diff --check`, and final status/diff checks.