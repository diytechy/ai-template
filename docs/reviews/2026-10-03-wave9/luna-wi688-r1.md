7733e2bf NOT YET SOUND

**BLOCKER**

none

**MAJOR**

- `project-trajectory/scripts/hats.py:1092` — On a first write without `--by`, `write_record` omits both `recorded_by` and `recorded_on`, and `record_findings` does not report their absence. For example, `hats.py record record.perspectives.toml --row SR-001` can produce a record with no authorship or date, although LLR-297 says the record holds who recorded the judgements and when (`docs/requirements/low-level-requirements.toml:3138`). TC-312 does not check these fields (`docs/test/test-cases.toml:3158`).

**MINOR**

- `docs/work/active/wi-688/WI-688-re-judge-tc-211-no-result-rec.md:6` — The WI still points to `docs/test/test-cases.toml`, which this range changes by adding TC-312. `check_trajectory.py --strict` warns that WI-688’s SpecRef changed after the WI was last touched and asks for revalidation or reaffirmation.

**Verified**

The changed SR and LLR text matches the implemented applicability, production, missing, stale, and conflict rules; the SR does not name an implementation carrier. LLR-183’s detail amendment leaves its Approved status unchanged, and LLR-297/TC-312 remain Drafted. Implements tags match LLR-297’s module and symbols. The RESYNC_PACK entry is anchored at 9702ca46, which is contained by `origin/refactor_again`. The sample perspective record passes `--check --strict`; the expected TC-211 re-judge result is absent from this range.

**Commands**

- `git diff 9702ca46..7733e2bf` and read-only registry/spec inspection — reviewed the range and requirement cells.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-688 tests/test_hats_record.py tests/test_hats.py tests/test_dogfood_sync.py tests/test_resync_pack.py` — **154 passed, 1 skipped**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0, reported `clean`; emitted advisories, including the WI-688 SpecRef warning above.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/hats.py --root . record docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.perspectives.toml --check --strict` — **no findings**.