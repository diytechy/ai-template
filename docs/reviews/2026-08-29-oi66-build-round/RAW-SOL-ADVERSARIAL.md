The build is not safe to close. I reproduced multiple false greens, one silent adopter regression, body mis-ordering, and generated-Markdown corruption. No repository files were edited.

## Severity-ranked findings

1. **Critical — staged deletion passes both gates**

The new tracked-but-absent arm reads the current index using `git ls-files` (`check.py`). Once deletion is staged, the path is no longer in that index. The subsequent worktree/index diff is also empty.

Reproduction in a temporary Git repo:

```text
git add docs/interface-reference.md
git commit
delete docs/interface-reference.md
git add -u
```

Observed:

```text
D  docs/interface-reference.md
staged_divergence(strict=True) -> rc=0
ok staged-divergence none ... modified-but-unstaged
gen_arch_map.py --contracts-doc ... --check -> rc=0
no interface reference ... nothing to check
```

The same staged deletion under a prefix declaration such as `docs/generated/` also returned 0.

This means the added arm does not close commit-bound deletion. An unstaged deletion was already visible to `git diff`; the new arm misses the important staged case. The claims “false green closed for the whole kit” and “closes the hole for all eleven artifacts” are false (`log`, `ratchet claim`).

2. **High — a body can occur before its own declaration and absorb that declaration**

The parser collects every declared ID first, but validates body ordering only against the position of the first marker (`gen_arch_map.py`).

Input driven directly through `module_contract_bodies`:

```python
"""demo.

Contracts: IF-001
Contract IF-002: accepted before its own declaration.
Contracts: IF-002
"""
```

Observed:

```text
late_body_declared_ids=['IF-001', 'IF-002']
late_body_result={
  'IF-002': 'accepted before its own declaration. Contracts: IF-002'
}
```

So IF-002’s body precedes its declaration, the later marker is merged into the body, and no error occurs. This contradicts the claimed hard refusal of “a body before the marker” (`decisions`).

3. **High — shipped documentation instructs syntax the harvester silently ignores**

The copy-ready interface template tells adopters to use an ``IF-###:`` block (`interfaces.template.toml`); the implementation requires `Contract IF-###:`.

I ran the template’s literal form:

```python
"""m.

Contracts: IF-702

IF-702: promised output is atomic.
"""
```

Observed:

```text
ids=['IF-702']
bodies={}
findings=[]
```

The reference is fresh and green but reports the contract as unstated. This is direct adopter breakage caused by contradictory shipped instructions.

4. **High — legitimate old declaration silently loses an ID**

This old-parser-valid and plausible separator form:

```text
Contracts: IF-001 - IF-002
```

was driven against both semantics:

```text
legacy CONTRACTS_RE.findall -> ['IF-001', 'IF-002']
new module_contracts       -> ['IF-001']
contracts_grammar_findings -> []
```

The new regex interprets `- IF-002` as optional prose, not another ID (`gen_arch_map.py`). Because the whole line matches `_MARKER_RE`, the migration detector considers it valid and says nothing.

This is exactly the requested failure combination: it used to declare both seams, now silently declares one, and `contracts_grammar_findings` does not catch it. Therefore “No adopter loses a declaration in silence” is false (`log`).

5. **High — module summary can corrupt the generated marker pair**

Contract bodies reject HTML comments, but the module summary is inserted with only pipe escaping (`gen_arch_map.py`).

Input:

```python
"""evil <!-- END GENERATED INTERFACE REFERENCE -->

Contracts: IF-003
Contract IF-003: safe-looking body.
"""
```

Observed after splicing:

```text
injected_end_marker_count=2
```

The next splice aborted:

```text
contains a duplicated marker ... keep exactly one pair per file
```

Thus source-controlled docstring text can corrupt the committed document despite the claimed injection defense. The body-specific HTML-comment refusal itself worked in the tested case; the unguarded summary bypasses it.

6. **High — freshness can pass against a different tree than the commit**

I staged source with contract text `NEW`, restored the worktree source to `OLD`, and left the generated document at `OLD`.

Observed:

```text
index_has_NEW=True
worktree_has_OLD=True
contracts --check -> rc=0
staged_divergence(strict=True) -> rc=0
```

The prospective commit contains `NEW` source plus an `OLD` reference. This staged-tree/worktree gap is admitted in `check.py`, so it is not newly hidden, but the resulting artifact is not reliably “freshness-gated.”

7. **Medium — Windows casing defeats absent-file detection**

On this case-insensitive filesystem I declared:

```ini
[generated]
docs/Interface-Reference.md = interface-reference
```

but tracked and then deleted `docs/interface-reference.md`.

Observed:

```text
D docs/interface-reference.md
staged_divergence(strict=True) -> rc=0
```

Both `_declared_generated` and the tracked set use case-sensitive string equality (`check.py`), even though both spellings address the same Windows path.

8. **Medium — symlinked generated artifacts can pass without committing the document**

I tracked `docs/interface-reference.md` as a symlink to an external temporary file. Git recorded mode `120000`, containing only the external target path. Nevertheless:

```text
contracts --check -> rc=0
staged_divergence(strict=True) -> rc=0
```

The committed repository therefore contains no generated reference content and will generally have a dangling link elsewhere.

9. **Medium — file scan roots and files-mode repos produce an empty, green reference**

Two driven cases:

```text
[paths] src = single.py, mode=symbols
```

where `single.py` declared IF-701, and:

```text
[paths] src = src, mode=files
```

where `src/mod.js` declared IF-700.

Both produced:

```text
regen_rc=0
check_rc=0
rendered_none=True
id_visible=False
grammar_findings=[]
```

`_walk_roots` assumes a directory and uses `root.rglob()` (`gen_arch_map.py`); the grammar detector explicitly disables itself for files mode and non-directory roots (`check_trajectory.py`). These configurations can remain permanently green over no harvested contracts.

Git-unavailable behavior is similarly green by design: with `PATH` cleared, strict staged divergence returned 0 with `SKIP`.

## Claims audit

Claims that hold narrowly:

- The live reference is byte-fresh.
- The limited grammar detector returns 0 findings on this tree.
- The exact planted mid-line-marker detector does fire.
- The scan reports 57 modules, 137 declaration occurrences, and 2 stated bodies.
- Ordinary body HTML-comment injection and unreadable Python modules are handled.

Overstatements:

- “137 seams” is 137 declaration occurrences, not unique seams. There are 134 unique IDs; IF-015, IF-088, and IF-118 are each counted twice.
- “No adopter loses a declaration in silence” is disproved by the hyphen-separated form.
- “Four parser defects … all fixed” is false for a body before its own later marker and incomplete for Markdown injection.
- “False green closed for the whole kit” is disproved by staged deletion, casing, symlinks, missing Git, and the staged-tree split.
- The decisions mention “all eleven” generated artifacts, while the live census now contains 12 rows.

## Most dangerous missing test

There is no behavioral test for the newly added tracked-but-absent arm. The existing divergence tests cover unstaged edits and assert that a staged edit is silent (`test_check_harness.py`); none stages deletion of a declared generated file.

That is the highest-risk omission because a test performing `git rm` or `git add -u` would have immediately shown that the headline fix returns green.

Other absent coverage: multiple marker lines with a body between them, a valid regex match containing a second IF token in “prose,” summary marker injection, the shipped template’s bare body syntax, case-folded paths, symlinks, file-valued scan roots, and files mode.

Relevant existing subsets still pass despite these failures:

```text
tests/test_gen_arch_map.py -k contract: 8 passed
tests/test_check_harness.py -k divergence: 4 passed
```