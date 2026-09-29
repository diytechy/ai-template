<!-- Claude Sonnet (read-only) confirmation of WI-545's fix round 3, build/wi-545 7de50658..ac3b534b, after the coordinator's full unfiltered suite found one red. -->

ac3b534b SOUND

BLOCKER: none

MAJOR: none

MINOR: none

**The rebind is load-bearing,** verified two ways:
- **Empirically:** the test's child body, rebinding the OLD `bootstrap.MAPPING`, run in a scratch copy against the real repo, exits 0 with `missing_file — 0 finding(s)`. The gate does not fire, so the old rebind is dead.
- **From the code:**
  - `bootstrap.py:390-391` binds `MAPPING` and `mapping_entries` to the manifest's objects;
  - `mapping_entries` (`kitlib/bootstrap_manifest.py:703`) resolves `MAPPING` through its own module globals;
  - so only `bootstrap_manifest.MAPPING` reaches the lookup. It remains the only literal (`:19`).

**The independent sweep for the class:**
- It took the `__all__` of `agent_brief` (40 names), `agent_policy` (58) and `trajectory_arch` (66), plus the manifest's exports.
- It grepped assignment, `setattr`, `patch` and `patch.object` rebinds through `agent_loop`, `agent_common`, `check_trajectory` and `bootstrap` and their aliases.
- Every hit is an unmoved name, a read or a subprocess result, except `test_decision_record.py:322` (`setattr(al, "worker_prompt")`). That one is valid: `session_body` (`agent_loop.py:349`) calls the bare `worker_prompt`, which resolves through `agent_loop`'s globals, and `agent_loop.py:294` aliases it.
- No other instance was found.

**The docs:** `gen_arch_map`'s docstrings and help now name the canonical home accurately. Nothing was compacted.

**Run:** `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt python -m pytest -q -n 2 tests/test_mapping_purpose_cli.py tests/test_gen_arch_map.py tests/test_decision_record.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py tests/test_bootstrap.py -p no:cacheprovider` → **218 passed in 196.49s**.
