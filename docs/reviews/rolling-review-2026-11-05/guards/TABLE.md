| # | anchor | fires when | invariant | harmed if violated | honest false-fire | WARN serves? | class |
|---|---|---|---|---|---|---|---|
| 1 | hooks/kit-python.sh:85-100 | no Python 3.11+ on PATH/.venv | floor never skipped/never on old py | nobody when privacy off (slot+CI re-run floor) | non-Python stack contributor; CI image | yes when privacy_check off | DOWNGRADE |
| 2 | hooks/kit-python.sh:139-144 | scripts/ dir not found | floor runs | same | relocated kit w/o KIT_SCRIPTS_DIR; sparse checkout | yes when privacy off | DOWNGRADE |
| 3 | hooks/kit-python.sh:146-149 | --hook-policy exited nonzero | policy known | privacy gate | checker crashed (version skew) | no | KEEP |
| 4 | hooks/kit-python.sh:158-163 + check_privacy.py:363-364 | process.toml AND legacy privacy-check both present | one home per dial | nobody: checker already resolves (reads ON) | re-sync kept legacy file | yes (take checker's answer) | DELETE |
| 5 | hooks/kit-python.sh:164-168 + check_privacy.py:359-361 | process.toml unparseable | policy known | privacy gate | typo in unrelated dial blocks every commit | yes + fail-closed reading (checker does) | DOWNGRADE |
| 6 | hooks/kit-python.sh:169-173 | near-token answer | hook/checker protocol | privacy gate | partial resync | no | KEEP |
| 7 | hooks/pre-commit:287 | path-triggered product step FAILs | declared sensor | adopter opted in | - | n/a | KEEP |
| 8 | hooks/pre-commit:288 + check.py:2830 | a named step unknown to check.py | hook/check.py in step | nobody | hook/check.py version skew refuses EVERY commit | yes (skip+warn unknown names) | DOWNGRADE |
| 9 | hooks/pre-commit:312 + check_privacy.py:589-615 | author email off allowlist / identity unresolvable (privacy on) | identity privacy | publication | - | no | KEEP |
| 10 | hooks/pre-commit:313 + check_privacy.py:572-586 | secret/PII shape in staged diff | trust boundary | publication | documented example line (ALLOW_MARKER exists) | no | KEEP |
| 11 | hooks/commit-msg:54 + check.py:2209-2225 + provenance.py:185-209 | loop marker set, no/foreign trailer | provenance | audit | human shell inheriting a loop env var | no, but name the escape | KEEP |
| 12 | hooks/commit-msg:57 + check_privacy.py:618-628 | secret in commit message | trust boundary | publication | - | no | KEEP |
| 13 | hooks/pre-push:95-102,139-145 | secrets/PII in outgoing range | trust boundary | publication | - | no | KEEP |
| 14 | hooks/pre-push:149-170 | privacy on, no REVIEW_CMD | review happens | publication | documented opt-down exists | documented | KEEP |
| 15 | hooks/pre-push:193-198 | reviewer output contains BLOCK anywhere / lacks APPROVE | verdict binding | publication | narrating LLM reviewer "no reason to BLOCK" | narrow matcher to a verdict line | KEEP (narrow) |
| 16 | kitlib/commit_hooks.py:119-139 (9 call sites) | core.hooksPath not .githooks / hook missing / non-exec | floor on | none: slot re-judges (README 6.2) | fresh clone; FS without exec bits | yes | DOWNGRADE (found 6.2) |
| 17 | kitlib/guard_hooks.py:209-218 | no TTY to consent | consent to write user settings | user | headless coordinator | no | KEEP |
| 18 | kitlib/guard_hooks.py:288-305 | settings slot occupied | never merge beside another hook | user config | - | no | KEEP |
| 19 | check.py:329, run_menu.py:118 | stack.ini malformed | config read | all steps | duplicate key | no | KEEP |
| 20 | check.py:431-446 | [step:] empty/shadow/no command/bad layer | config read | plan | wanting to REPLACE a kit step | no | KEEP |
| 21 | check.py:484 | lane= names no step | no silent re-race | --jobs>1 | typo | no | KEEP |
| 22 | check.py:573 | arch-map mode not symbols/files | config | nothing consumes it now | - | yes | DELETE |
| 23 | check.py:1513 + kitlib/stage.py:654-671 | derive_stage.py missing/fails | plan selection | plan | partial resync | no | KEEP |
| 24 | check.py:1531 + kitlib/stage.py:395-402,560-622 | docs/stage carries a rung not on the ladder | ladder vocabulary | plan | kit upgrade renaming a rung: parse refuses BEFORE fingerprint miss re-derives (repro) | yes: treat as miss, warn | DOWNGRADE |
| 25 | check.py:2252 | bare --strict | usage | - | - | yes | KEEP |
| 26 | check.py:2557 | stale coverage.json undeletable | no false green | gate | locked file (Windows) | no | KEEP |
| 27 | check.py:2761 | no docs/ at CWD | CWD anchor | plan | - | no | KEEP |
| 28 | check.py:2788 | coverage threshold non-int | config | gate | - | no | KEEP |
| 29 | check.py:2335-2365 | declared tool not importable/found (non-lenient) | declared bar runs | gate | bare venv (README 9.12) | --lenient exists | KEEP |
| 30 | check.py:1811-1823 | declared [generated] artifact tracked but absent | freshness not vacuous | gate | removal commit when following README 8.2 (remedy named) | remedy named | KEEP |
| 31 | check.py:1843-1867 + steps() 1177-1183 | generated artifact modified-but-unstaged under --strict | committed tree == checked tree | stale artifact lands | any partial commit (git add -p) while a dashboard is regenerated (repro exit 1) | yes at commit; CI/slot read committed tree | DOWNGRADE |
| 32 | check.py:1891-1972 | dated docs/ratify brief staged with status != A | record immutability | attestation record | archive/move/delete old briefs; typo fix; git history already holds bytes | yes (exempt D, warn on M) | DOWNGRADE |
| 33 | check.py:1975-2011 + held_status.py:633-666 | loop marker outside lane moves a held status | approval authority | owner | - (0.21 s/commit vacuous on lane-less repo) | no | KEEP |
| 34 | check.py:2014-2031 | squash landing with held move | approval authority | owner | - | no | KEEP |
| 35 | check.py:2070-2097 + trace.py:1083-1110 | squash adds unreserved id / watermark lags; unreadable merge base | id uniqueness | irreversible id reuse | shallow clone during hand squash | base-unreadable arm -> warn | KEEP |
| 36 | check.py:2114-2129 + acceptance_record.py:2147-2160 | ruling leaves citing row stale | OI/WI sync | queue | - | no | KEEP |
| 37 | check.py:2146-2162 + text_then_act.py:130-159 | act commit edits non-Status cells | approval record integrity | attestation | - | no | KEEP |
| 38 | check.py:2179-2190 + acceptance_record.py:2240-2290 | approved row under unapproved parent | spine order | attestation | - | no | KEEP |
| 39 | integrate.py:3322-3347 + kitlib/done_when.py:446 | claim copy Done-when changed unblessed; trunk undeclared | Done-when binding | verdict | repo w/o [policies] trunk | trunk-undeclared arm -> warn | KEEP |
| 40 | plan_gate.py:546-565 | squash of a deleted branch | plan gate key | plan binding | stale SQUASH_MSG | yes | DELETE |
| 41 | adoption_record.py:149-170,434-451 | record changed outside close | record integrity | lineage | - | no | KEEP |
| 42 | trace.py:6472-6495 + trace_text.py:588,811 | --strict: provenance (WI id/process cite in a cell) or form (>1 shall) | prose rules | readability | a cell citing a WI id FAILS the Impl gate while kit code/skills cite freely | yes (advisory like EARS) | DOWNGRADE |
| 43 | trace.py:1118-1138 | docs/id-watermark absent/malformed | id record | id reuse | deleted file; pre-watermark scaffold (README 9.2) | no at gate | KEEP (found 9.2) |
| 44 | trace.py:1159-1170 | correction line with no OI registry | ruling authority | id guard | hand-written correction only | yes | DELETE |
| 45 | trace.py:3613 | --approve scope matches no SR | no empty brief | sitting | - | no | KEEP |
| 46 | trace.py:4245-4250 | brief STALE | human reads current brief | attestation | unrelated commit (README 6.4) | yes at commit | DOWNGRADE (found 6.4) |
| 47 | trace.py placeholder_sweep (README 9.9) | SN-000 comment on raw file | no placeholders | gate | shipped comment | fix the scan | found |
| 48 | spine_carrier.py:729-737 + kitlib/stage.py:185-200 | registry under BOTH carriers | one home | readers disagree | mid-migration; two copies of the refusal text (41w, 56w) | yes post-window | DELETE (post-window) |
| 49 | check_trajectory.py:942-960,3405-3420 | pending OI no queued WI cites (before vacuity) | decision reaches queue | owner | OI layer used without WI layer (repro exit 1) | yes at floor, ERROR --strict | DOWNGRADE |
| 50 | check_trajectory.py:1484-1545 | R-A Deliverable vs Status (hard every run) | coherent handoff | next session | hand-edited WI spec in a human-run repo | yes at floor, ERROR --strict | DOWNGRADE |
| 51 | check_docs.py:960-1005 | broken intra-repo link; root README rule | navigability | readers | not-yet-written target | standard linkcheck | KEEP |
| 52 | check_flows.py:174-217 | flows doc absent/no heading/-000 cited (Tests+) | authored flows | reviewers | shipped example flow (README 9.3) | found | KEEP |
| 53 | check_privacy.py:738,748 | git diff/log fails | scan ran | - | not a repo | no | KEEP |
| 54 | integrate.py:1766-1780 | no stack.ini / no [product] test / empty | bar declared | merge | docs-only or spec-only repo on the station | yes (run process bar, warn) | DOWNGRADE |
| 55 | integrate.py:1782-1795 + agent_common.py:449-489 | requirements-dev.txt present and no ./.venv | pinned tools present | false green | poetry/conda/uv-elsewhere; clone with every tool importable refused (repro) | module guard already covers | DELETE |
| 56 | integrate.py:1407-1420 + acceptance_record.py:2304-2327 | range/parent unreadable (shallow) | judged, not guessed | merge | shallow clone at graft | already says shallow + remedy | KEEP |
| 57 | integrate.py:3589-3596 | dirty trunk | clean compose | merge | owner scratch (excepted) | no | KEEP |
| 58 | integrate.py:3624-3650 | merged but not unloaded -> exit 1 | honest remainder | operator | - | no | KEEP |
| 59 | integrate.py:1155 | lane adds a WI id | ids minted on trunk | id collision | - (78-word message) | no | KEEP |
| 60 | integrate.py:369 | WI id named in status.md prose | pre-empts a WARN-level R-D | - | lane mentions its own id | yes | DOWNGRADE |
| 61 | intake.py:1548-1614,1739-1820,1845-1909 | disposition section malformed/thin/empty | all-or-nothing mint | queue | LLM typo refuses the whole mint | no (mint is atomic) | KEEP |
| 62 | intake.py:3403 | act moves FROM retired `Modified` | migration residue | - | - | yes | DELETE (post-window) |
| 63 | agent_route.py:450,568-580 | Model cell has `@` etc. | shell-safe argv on .cmd shims | injection | Vertex id claude-3-5-sonnet@20240620 (repro) | allow @ or quote | DOWNGRADE |
| 64 | agent_route.py:940-960 | agents-enabled unreadable | consent surface | routing | - | no | KEEP |
| 65 | agent_loop.py:4079-4086 | hooks off / scripts fingerprint None | preflight | run | unreadable file | no | KEEP (hooks: found 6.2) |
| 66 | session_service.py:1279,1383 | account not signed in | nothing signs in silently | run | - | no | KEEP |
| 67 | coordinator_guard.py:566-610 | blackout window / no lease / drain | owner dial | owner | - | no | KEEP |
| 68 | dispatch.py:666 | worker preflight failed | lane stays claimed | run | - | no | KEEP |
| 69 | prompts.py:264-270 | provided value names no slot | template edit noticed | nobody (value unused) | operator template that drops a value (repro) | yes | DOWNGRADE |
| 70 | prompts.py:271-276 | declared slot unfilled | no hole in brief | session | - | no | KEEP |
| 71 | prompts.py:220-243 | template empty/unreadable | brief exists | session | - | no | KEEP |
| 72 | bootstrap.py:955-1002,3028-3032 | process.toml form a line edit cannot reach | never write what a parse can't confirm | config | dotted key / inline table | no (names hand edit) | KEEP |
| 73 | bootstrap.py:3023 | kit template missing | scaffold complete | adopter | - | no | KEEP |
| 74 | kitlib/authority.py:176-220 vs agent_policy.py:1239-1290 vs docs/process.toml:62-63 | wrong-typed human_approval_through | one dial meaning | owner | loop preflight REFUSES, hook/slot silently read most-held, doc states only refusal | one posture + doc | DOWNGRADE (found 6.5, new fact) |
| 75 | derive_stage.py:666-672 | docs/stage absent | derived stage recorded | plan | deleted file (scaffold ships placeholder) | yes | DOWNGRADE |
| 76 | derive_stage.py:720-726; gen_arch_map.py:1439,1479; gen_okf --check | generated artifact stale | freshness | readers | README 8.2/10.6 family | found | found |
| 77 | baseline_snapshot.py:1119,1269,1469 | text reached snapshot w/o act; --reattests on seed; snapshot dir absent | approval record | attestation | - (125-word message) | no | KEEP |
