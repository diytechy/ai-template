Reviewed: f7809e313a17bf145b639922b1d84192760f7a66

Full-lane review of WI-978 (lane wi-978, range 2f4ebb2a5..f7809e313), convergence stance. I read no docs/reviews, docs/decisions, critique records or lane commit messages. I took pre-fix code only from `git log --format=%h` patches and `git archive` snapshots.

**Verified.** I first named the failure classes to hunt, worst first:
- an unreserved id that the landing admits (fail-open);
- two reservations that overlap (silent wrong content);
- a writer or fold that drops records or lowers a mark (data loss).

What I checked and found right:

- **Disjoint ranges.** `plan_reservation` starts each range one above the larger of the carrier's mark and trunk's committed mark. The carrier moves only by `update-ref <ref> <new> <old>`, with `""` meaning "the ref must not exist" on first use. A lost swap raises `LOST_RACE` before the working file is touched. The sequential, stale-base, after-correction and lost-race cases all pass.
- **Writers keep every record.** `bump_watermark`, `correct_watermark`, the fold and `bootstrap.raise_watermark` all keep records. `bootstrap.raise_watermark` keeps every line it does not raise.
- **Trunk mints.** The trunk mints (intake, plan_artifacts) go through `bump_watermark`.
- **Committed records.** These are read as a union over every baseline, so dropping a record is refused.
- **Carrier-space sweep.** Every carrier space's registry lives under `LANDING_DIRS` (`docs/requirements`, `docs/test`). So the extracted-tree sweep cannot miss a carrier-space id.
- **Landing check, both routes.** The slot reads the lane's delta over its merge base. The hand squash also reads the staged tree over HEAD. Both read retirement records at every tree they judge.
- **This lane against the real carrier.** I ran the shipped check in-process (`trace.landing_id_refusal(root, "wi-978", <merge base>, ["WI-978"])`): it returns None and the fold lag is []. The carrier (`refs/heads/id-carrier`, 58c902c22) holds `LLR 362-363 (WI-978)` and `TC 401-402 (WI-978)`. The same call keyed on WI-963 refuses all four ids.
- **Earlier fixes, confirmed against pre-fix code.** I ran the final tests against `git archive` snapshots of the code before each fix, and every one fails there:
  - At 76b8189ff, 3 of 3 fail: the slot and hand-squash retired-id-inside-reservation cases ("the slot admitted wi-401"; step exit 0), and the hand squash of another lane's number after that lane landed (step exit 0).
  - At cecb461f2, 6 of 6 fail:
    - export-ignore hiding a registry, on both the judgement and the slot;
    - a registry conflict beside the watermark (SystemExit on unparsable TOML);
    - a reservation in a lane behind trunk (TC/WI hand-raise integrity findings);
    - the carrier contributing only record-justified marks (no `carried`);
    - the slot after trunk deletes an id at the lane's base (false refusal of SR-003).
- **Spec amendment.** The in-lane amendment of the spec's fold paragraph matches `id_carrier.carried`.
- **Spine sweep.** SR-174, LLR-362/363, TC-158 and TC-401/402 contradict no existing row I checked: LLR-153/154, TC-147/148/158 and SN-027 (Approved). No SN/SR cell names a carrier (K2).
- **Text items.** PROCESS.md §4 carries keep-or-mint beside CLARITY and MEANING (line 681). spine-questions §0 cites it in one line. The terra prompt drafts only from the reserved ranges. Recipes §4 has "reserve before drafting" and the rebase row's fold. SKILL §4 drops the watermark clause, and both skill copies match.
- **Untouched code.** The act ledger and `_record_act` are untouched.

**Done-when coverage:**

| Done-when item | Covered by |
|---|---|
| Spine | the registry diff |
| Reserve table | test_id_carrier counts, work-item and refusal-writes-nothing cases |
| CAS and first use | test_id_carrier_git first-use and lost-race cases |
| Disjoint ranges and the correction floor | test_id_carrier_git sequential, stale-base and after-correction cases |
| Fold, clean and conflicted | test_id_carrier fold cases; test_fold_ids_on_a_conflicted_watermark |
| Hand-raise, record history, writers | test_id_watermark (TC-158 evidence list) |
| Landing table, both callers | test_id_landing REFUSED parametrized on the slot and the hand squash, plus the claim, own-record, code-only and stale-base cases |
| Landing and refresh fold | test_id_landing fold and refresh-conflict cases |
| Acts unchanged | no act file in the diff |
| Text | the diffs above |
| RESYNC | RESYNC_PACK entry |

Two items are landing-time, not lane, items: regenerating the [generated] cli and interface references, and naming the other open lanes. I could not see the spine sitting's verdict within the convergence reading scope. The integrity floor (approval-immutable, registry-integrity) is clean on the tip.

**Coverage-extension notes (no severity):**
- The counts parser also admits surrounding whitespace and leading zeros (` SR=05`).
- A hand `git merge --no-ff` of a lane on trunk is judged by neither caller. That is the spec's declared residual: only the slot and a squash are callers.
- 19 posix-shell-gated tests were skipped on this box. The hook wiring is pinned by `test_the_pre_commit_hook_runs_the_reserved_ids_step`, and the squash step is driven through `check.py --run-steps reserved-ids`.

**Commands**
- `git rev-parse HEAD` (in C:/Projects/ai-template.wt/wi-978) -> `f7809e313a17bf145b639922b1d84192760f7a66`
- the brief's scoped pytest command (17 files, `-n 2`, the literal `--basetemp`) -> `758 passed, 20 skipped in 1829.28s (0:30:29)`, exit 0. It ran past the shell tool's 1800 s cap, so the harness moved it to the background before it finished. I read its own output file after it completed.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (986 work item(s), 872 done (88%), 34 cancelled, graph acyclic).`, exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=329 TC=356 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 drafts=4 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. Report -> docs\test\report.md`, exit 0. `git status --short` in the worktree printed nothing afterwards.
- pytest of the final retired-id and after-landing tests on a `git archive 76b8189ff` snapshot -> `3 failed, 30 deselected`
- pytest of six final regression tests on a `git archive cecb461f2` snapshot -> `6 failed in 36.07s`
- in-process probe of `trace.landing_id_refusal` / `landing_fold_lag` on this lane -> `refusal: None`, `lag: []`; the WI-963 key refuses LLR-362, LLR-363, TC-401 and TC-402
- in-process probe of `id_carrier.landing_lines(set(), [], ["WI-401"], [("SR",500,510,"WI-401")], [], True, "x")` -> `[]`; the same forged record with SR-006 added -> refused, naming the line
- a scratch AST script cross-checking each changed function's `Implements:` LLR against that row's `module` and `code_symbol` -> the five misses in finding 2

**Findings**

- [MINOR] project-trajectory/scripts/id_carrier.py:486 -> landing-table row 6 ("the landing's watermark carries a record that neither the carrier nor the parent holds -> refused") is judged only when the landing adds a carrier-space id. `landing_lines` returns [] before the record check whenever `added` is empty. A code-only landing whose watermark carries a hand- or agent-written `# reservation: SR 500-510 (WI-NNN)` therefore lands; I confirmed this by running `landing_lines`. On trunk the line is then a committed record, which the hand-raise rule (`_mark_history_findings`) accepts as justifying a mark raised to 510, and the append-only rule keeps forever. That wastes numbers but cannot collide, since landing authority reads the carrier only. The spec's own table makes rows 1 and 6 overlap for this state, and LLR-363's first two sentences say both "no added identity passes" and "a landing-only record refuses" (K1). -> run the landing-only-record comparison before the `if not added` return. A quarantined lane's records are the carrier's, so that stays green. Then state the precedence once, in the spec table and the LLR-363 detail. Unrepresentable is unavailable: a record is a comment line in a hand-editable shared text file, and the landing is already the single owning boundary that validates it. This widens that boundary's existing check rather than adding a guard. -> @owner
- [MINOR] project-trajectory/scripts/retire.py:221 -> K3 back-links. Five new functions name an LLR whose `module` holds the file but whose `code_symbol` lacks the function:
  - `retire.recorded_at` -> LLR-286
  - `id_carrier._count` (id_carrier.py:152) -> LLR-362
  - `id_carrier._ref_value` (:284) -> LLR-362
  - `id_carrier._plumb` (:308) -> LLR-362
  - `id_carrier._id_name` (:418) -> LLR-363

  -> add each symbol to its LLR's `code_symbol`. For `recorded_at` the alternative is to re-tag it LLR-363, the landing reader it serves, with retire.py added to LLR-363's `module`. -> @owner
- [MINOR] project-trajectory/scripts/kitlib/git.py:375 -> §3 "Consolidate, don't duplicate". `claimed_specs` adds a third claim-folder reader beside two that already exist:
  - `kitlib/plan_pass.py:308` `gate_rows`, which lists `docs/work/active/<branch>/` at a revision with its own grammar, `^(WI-\d+)-[^/]*\.md$`;
  - `integrate.py:1015` `_claimed_specs`, which globs the same folder on disk.

  The module docstring now claims "a route that keys on a lane's claim at a revision … never parses the folder itself", which `gate_rows` still does. -> route `gate_rows`' listing through `claimed_specs(root, claim_rev, branch)`, so the claim grammar has one reader at a revision. Or file the move as its own refactor row, and narrow the docstring's claim until it lands. -> @owner

VERDICT: APPROVE findings=3
