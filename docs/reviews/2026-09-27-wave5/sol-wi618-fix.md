<!-- Codex Sol confirmation of WI-618's fix round, d72a5c0a; ruling 50. Links re-rooted from the removed worktree. -->

d72a5c0a NOT YET SOUND

- **[major] IF-257 still accepts a non-empty whitespace-only body.** The contract requires “nothing after the closing fence” ([retire.py:47](../../../project-trajectory/scripts/retire.py)), but `_shape_problem` tests `body.strip()` ([retire.py:183](../../../project-trajectory/scripts/retire.py)), so blank lines, spaces, and tabs after the fence are accepted. The regression covers only a textual body ([test_retire.py:515](../../../tests/test_retire.py)), not whitespace-only bodies.

- **[minor] The advertised `..N` exclusion form is untested.** Its parser expands ranges correctly ([retire.py:441](../../../project-trajectory/scripts/retire.py)), but the exclusion and replacement regressions use only single IDs ([test_retire.py:426](../../../tests/test_retire.py), [test_retire.py:446](../../../tests/test_retire.py)).

No further finding in census replacement ([retire.py:459](../../../project-trajectory/scripts/retire.py)), shallow-clone advisory ([retire.py:575](../../../project-trajectory/scripts/retire.py)), selective `fresh_view` handling ([gen_trajectory.py:299](../../../project-trajectory/scripts/gen_trajectory.py)), or the IF-257/IF-258 split and TC-299 citation ([interfaces.toml:2254](../../../docs/requirements/interfaces.toml), [test-cases.toml:2912](../../../docs/test/test-cases.toml)). The requested pytest command could not start because the read-only environment provided no writable temporary directory.