# WI-966 dispute sitting at f45abd0

DISPUTE: findings=RB-F1;RA-F1

Both findings reach one defect from two inputs. Bootstrap's in-place policy writer (`set_process_key`, with its scan half `_locate_process_key`) still finds a dial by line shape: a `[section]` header line, then a line whose text left of `=` is the key. Its docstring still states the line-shape convention "this file owes the git hooks". This lane retires that convention and invites valid TOML in its place. I reproduced each scenario in a scratch directory with the lane's own functions and its `check_privacy.py --hook-policy` CLI, at this tip.

## RB-F1: an inline or dotted `policies` table defeats the writer

**Observed:**
- *The scaffold flag.* With `policies = { privacy_check = false }` as the file, `set_process_key(..., "policies", "privacy_check", True)` answers `missing`. `apply_privacy_check` drops that answer, and `main` then prints `privacy-check: true` unconditionally (`bootstrap.py:2715`). The file is unchanged, and the hook answers `privacy=off`. A requested privacy gate is reported on while it stays off.
- *Migration.* With `policies = { push = "human" }` and a legacy `docs/privacy-check` holding `true`, `migrate_legacy_config` appends a second `[policies]` header, reports `docs/privacy-check` as moved, and deletes it. The file no longer parses ("Cannot declare ('policies',) twice"). The hooks then refuse as unreadable, which fails closed at the hook, but the legacy declaration is gone and the policy file is broken under a green `migrated:` line.

**It is in scope.** The input is the form this lane's own RESYNC entry invites ("may now hold any valid TOML", with `policies = { privacy_check = true }` as its example). The routes are the kit's own: the documented scaffold flag, and the migration bootstrap runs on every scaffold pass. PROCESS.md §6's bound excludes neither.

**It is convergence-class, so it cannot be SUCCESSOR.** The flag case is a fail-open: a requested gate silently stays off. The migration case loses data: a declared policy is deleted and the file is left unreadable. And it is a gap in the Done-when:
- item 1 says "No kit reader refuses or reads a policy file by its line shape";
- item 2 says a dotted key or inline table "is read as the TOML parser reads it, by every reader";
- the writer's locator is a kit reader of the policy file, and it reads by line shape.

Decision D-008 recorded the round-1 MINOR as outside the spec's named surface, because the Context list does not name the writer. But the Done-when governs, and its "every reader" has no exception. The finding is therefore FIX.

**What the fix must do.** The reviewer's remedy is the smallest one that fits the stdlib rule. There is no TOML writer to make the state unrepresentable, and re-narrowing the file's shape is the rule this lane retires. So the writer must check its target against the one parse:
- a rewrite proceeds only where the parse confirms the located line is that key's declaration;
- otherwise `set_process_key` refuses, naming the form, rather than answering `missing` or appending a duplicate header;
- `apply_privacy_check`, `apply_push_policy` and the gate-policy writer must surface that refusal instead of printing success;
- migration must leave the legacy file in place when the write is refused;
- the docstring's line-shape sentence goes, and the RESYNC entry qualifies "any valid TOML" for the in-place flags and migration.

## RA-F1: a multi-line string decoy redirects the migration's write

**Observed.** The file holds `[policies]`, then `note = """`, a line `privacy_check = false`, a closing `"""`, and the real `privacy_check = false`. A legacy `docs/privacy-check` holds `true`. `migrate_legacy_config` rewrites the line inside the string to `privacy_check = true`, reports the legacy file moved, and deletes it. The parse then holds `note = 'privacy_check = true\n'` and `privacy_check = False`, and the hook answers `privacy=off`. The adopter's declared `true` is lost, and the gate reads off.

**It is in scope and the same defect.** The decoy content is unusual on its own. But the spec names multi-line strings inside its promise (Done-when item 2: "A dotted key, an inline table or a multi-line string ... is read as the TOML parser reads it, by every reader"). §6 counts an input class inside a spec's promise when the spec names it, and a note quoting a dial's own line is exactly what a policy file's explanatory text tends to hold. The outcome is a fail-open with data loss, so the finding is convergence-class.

The fix is RB-F1's: a writer that confirms its target through the parse cannot mistake a line inside a string for the key. This finding adds only the case its test must drive.

RULING: RB-F1 FIX bootstrap's in-place policy writer and its migration caller locate a dial by line shape, so an inline or dotted policies table makes the privacy-check flag report success while writing nothing and makes migration duplicate the table and delete the legacy file; this is a fail-open with data loss against Done-when items 1 and 2's "every reader"
RULING: RA-F1 FIX the same line-shape writer rewrites a key-like line inside a multi-line string, which the spec names inside its promise, and deletes the legacy declaration, leaving the gate off; the RB-F1 fix (the writer confirms its target through the one parse, refuses a target it cannot confirm, and migration keeps the legacy file on a refusal) discharges it, with this decoy among its test cases
