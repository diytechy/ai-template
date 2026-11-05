# guards-vs-warnings inventory (scratch, partial saves)
## Read so far
- check.py steps() 501-1403, refusal fns 1736-2330
- hooks/pre-commit, commit-msg, kit-python.sh, pre-push
- kitlib/commit_hooks.py, kitlib/guard_hooks.py
## Candidate rows (path:line -> class)
- check.py main(): sys.exit on: malformed stack.ini (329), [step:] empty name/shadow/no command/bad layer (431-446), lane typo (484), arch-map mode (573), derive stage err (1513), hand-edited stage (1531), no docs/ dir at cwd (2761), coverage threshold not int (2788), unknown step name (2807/2830), --strict without --staged-divergence (2252), stale coverage.json undeletable (2557)
- _step_guard: missing module/command => FAIL unless lenient (hook path lenient). Product-only banner.
- hooks: kit_python refuses (no 3.11), kit_policy refuses (no scripts dir; policy read fail; mixed; unreadable; near-token). pre-push: unwired reviewer fails closed unless warn-unwired; reviewer no APPROVE => fail.
- commit_hooks.hooks_refusal: 8 call sites (agent_loop main, agent_route?, integrate 831/2785/3155/3589, coordinator_guard 473, bookkeeping?)
- guard_hooks: occupied settings => refusal; no terminal => refusal (NO_TERMINAL)
- prompts.fill: strict both directions (unknown slot AND unfilled) raise PromptError
- authority.read_dial: malformed dial => MOST_HELD silently (not refusal) -- contrast with process.toml comment "wrong type refused at preflight"
## Candidate NEW findings (to verify)
a) kit-python.sh:85-100 Python 3.11 required to COMMIT for all stacks (non-Python adopters) -> DOWNGRADE when privacy off
b) check_privacy.hook_policy_answer refuse=mixed/unreadable while _process_gate RESOLVES same state (reads ON) -> two policies, one module; hook could take checker's answer
c) prompts.fill strict_check unknown-slot direction refuses templates that drop a value -> DOWNGRADE unknown->warn, keep unfilled
d) kitlib.stage.require_rung raises on unknown rung in docs/stage -> check.py sys.exit cliff at ladder rename; should re-derive
e) staged_divergence --strict refuses partial staging (git add -p) — patches worktree-read gap; CI closes it -> WARN at commit
f) approval_immutability refuses D/move of dated briefs; git history holds bytes -> exempt D or WARN
g) 8 station steps spawn interpreters per commit for lane-less repo -> MEASURE
h) check_trajectory uncited-pending OI ERROR before vacuity -> verify
i) R-A hard error at floor for hand-edited WI -> WARN at floor
j) trace --strict gates on form/provenance/interface_backlink -> forces IF banner (verify)
k) agent_route MODEL_SLUG_RE refuses '@' (Vertex ids) verify
l) read_stack_ini interpolation % verify
r) process.toml comment "wrong type refused at preflight" vs read_dial silent MOST_HELD; agent_loop warn_on_inert_or_malformed_policies WARNS -> doc false
## VERIFIED (repro in clone)
- (d) docs/stage unknown rung: `check.py --list` -> sys.exit "kitlib.stage: docs/stage `stage =` carries 'DevStg-Renamed'..." ; read_stage parses (stage.py:706) and parse->_refuse_non_rungs raises BEFORE fingerprint compare could re-derive
- (e) staged-divergence --strict FAIL on partial commit: touch PROJECT_STATE.html unstaged + stage docs/log.md -> exit 1
- (c) prompts.fill unknown slot -> PromptError (prompts.py:264-270)
- (b) hook_policy_answer -> refuse=mixed while read_privacy_enabled -> off (same module) ; test_process_config pins both
- harness floor: clone w/o ./.venv but pytest+ruff importable -> refused at slot (agent_common.py:475-488)
- timing: 8 station floor steps = 1.82 s/commit on lane-less clone (held 0.21 reserved 0.14 ruling 0.33 tta 0.27 parent 0.20 done-when 0.29 plan 0.21 adoption 0.17); 20 cheap steps 8.97 s total
- 240 nonzero-exit/REFUSED sites in scripts+kitlib; 424 refusal/warning messages >=80 chars, median 22 words, 45 >=40 words, 9 >=60 words; RESYNC_PACK 408 lines mention refus
- 9 hooks_refusal call sites
