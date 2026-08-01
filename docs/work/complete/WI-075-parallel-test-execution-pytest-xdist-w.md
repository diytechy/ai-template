+++
id = "WI-075"
title = "Parallel test execution - pytest-xdist wiring + verification"
workstream = "scripts"
needs = ["WI-020"]
order = 74
+++

## Deliverable

P2 (2026-07-11): pytest-xdist -n auto wired for the meta-repo. docs/stack.ini [product] test gains -n auto (the smoke tier line + the coverage args untouched); scripts/dev-setup.{sh,ps1} gain a pytest-xdist check row + the --install set (dev-setup.command delegates, unchanged); the shipped stack.ini.template keeps the plain command with -n auto COMMENTED (a knowing opt-in - a downstream suite may not be xdist-safe). Verified, not assumed, on 24 workers: (a) subprocess coverage HOLDS per-worker - combined total 90.8% (serial ~91%, unchanged), coverage step 726s->157s; (b) the meta-tree readers (check_privacy --repo, gen_skills_index --check, dev-setup --check, gen_trajectory graph reads) are read-only, no os.chdir, env/cwd are per-worker - concurrency-safe; (c) Windows spawn overhead fine - plain suite 377s->71s/61s across two clean runs, zero flakes (both 629 passed/3 skipped). CI: the gate job inherits -n auto via stack.ini so it needs pytest-xdist (added to its install); the matrix test job is also parallelized (-n auto + the dep) so all three OSes exercise the parallel path. No SR change (dev tooling + the declared stack command; SR-034/SR-035 stdlib-only claims are about kit SCRIPTS, not the test tooling - uncontradicted). Docs: the PROCESS_OPTIONS parallel-execution paragraph (opt-in template posture, the FB1 test-impact rejection stands, the session-scoped shared-scaffold fixture = the recorded fallback lever, filed not built). Tests: test_stack_profile (meta parallelizes, template opts out, -n auto composes as two argv tokens) + test_onboard_devsetup (dev-setup reports pytest-xdist).
