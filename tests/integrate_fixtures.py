"""The shared test API for the integrate.py family (WI-521 slice 2).

`tests/test_integrate.py` was a 3,520-line monolith — M-06 of the 2026-08-19
repository review, and one of the four the review named. `WI-483` ruled that a
test split RIDES ALONG with a subsystem decomposition and that a standalone
split was out of scope; that rule was honoured across seven slices, delivered
nothing, and `WI-508` then filed no decomposition at all. `WI-521` is explicitly
unbound from it, so this split is standalone and is taken along the file's OWN
seven behaviour sections rather than by line count:

    test_integrate.py            the CLAIM rung and the refusals in front of it
    test_integrate_admission.py  what the slot ADMITS: outcome, the R1 mint
                                 refusal, the verdict gate, the declared bar,
                                 the branch tree's harness, the window audit
    test_integrate_station.py    the station protocol — refresh, attestation,
                                 the merge slot — and the real-bar end-to-end
    test_integrate_unload.py     the §5.6 unload of the branch and its worktree

WHAT LIVES HERE is exactly what MORE THAN ONE of those modules uses, measured
rather than guessed (the `tests/traj_fixtures.py` rule, WI-277, applied again):
the git plumbing, the spec/watermark/stack.ini repo builders every section
starts from, the pinned commit stamps, and the two builders whose callers
straddle a boundary (`scaffolded_closed_branch`, built by the station's
end-to-end and reused by the unload queue tests; `_worktree_count`, the other
way round). Anything used by a single module moved WITH that module —
`claim_dir` and `spec_move` to the claim tests, `verdict_repo` to admission,
`station_repo` to the station, `residue_lane` to unload.

Never let this file accrete: a helper only one module calls belongs in that
module, and a helper this file grows for a second caller must be justified the
same way. No `test_` prefix, so it is never collected; imported the way
`conftest` is.

TWO PROPERTIES OF THESE FIXTURES ARE LOAD-BEARING, not hygiene, and they are
stated here because they now serve four modules instead of one:

  * **every git fixture is a REAL repository.** The queue derives everything
    from history — finished-ness from `ls-tree`, verdict freshness from commit
    times — so a fake would test the wrong thing.
  * **every ordering-sensitive commit is pinned** with `GIT_AUTHOR_DATE` /
    `GIT_COMMITTER_DATE`. Git records whole seconds, so two back-to-back
    commits in a test TIE, and a tie would hide whether a freshness rule is
    really time-derived (the tests/test_trunk_step.py idiom).
"""

import subprocess

from conftest import (
    SCRIPTS,
    load_script,
    make_minimal_project,
    pin_autocrlf,
    record_ids,
    run_py,
    set_process_key,
    skip_without_env_gates,
)

integ = load_script("integrate")

# Pinned commit stamps (unix seconds). Named rather than inlined so the ORDER a
# freshness test depends on is readable at the assertion.
T_BASE = 1_000_000
T_CODE = 1_000_100
T_VERDICT = 1_000_200
T_LATER = 1_000_300


# --- fixtures: real git repos ------------------------------------------------


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=None):
    """Commit everything staged/untracked, optionally at an EXACT timestamp
    (the tests/test_trunk_step.py `_commit` shape — git records whole seconds,
    so an unpinned pair of commits ties)."""
    import os

    env = dict(os.environ)
    if when is not None:
        stamp = "@{} +0000".format(when)  # git's raw date format
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
    _git(root, "add", "-A", env=env)
    _git(root, "commit", "-qm", message, env=env)


def git_repo(root, branch="main"):
    """A committed git repo on `branch` (the tests/test_check_lane.py `git_repo`
    shape, copied rather than imported — no test module in this suite imports
    another, and conftest is not this module's to extend).

    `git init -b` is 2.28+, so the branch is set with a symbolic-ref instead.
    The identity is repo-local because integrate.py commits through
    `agent_common.git`, which passes no `-c user.*`; signing is off so a
    developer's global `commit.gpgsign` cannot wedge the fixture.

    `conftest.pin_autocrlf` is called for the same class of reason (WI-461/
    WI-465; see its docstring for the general mechanism), and it is
    load-bearing here, not hygiene: the EOL fixtures below forge line endings
    and assert on the BYTES `git cat-file` gives back (WI-403), so on an
    unpinned Windows box the forged CRLF never reaches git at all —
    `_relinked_exactly` would compare two LF blobs, excusing the claim, and
    `test_a_whole_file_crlf_relay_in_a_claim_shape_convicts` would go red
    while `test_a_crashed_claim_that_relinked_a_crlf_doc_is_still_excused`
    passes vacuously (WI-337: a fixture that takes the platform's translation
    cannot test the platform's bytes)."""
    skip_without_env_gates("git")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    pin_autocrlf(root)
    _git(root, "symbolic-ref", "HEAD", "refs/heads/" + branch)
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    # Repo furniture, seeded BEFORE any claim: `trace._read_marks` refuses an
    # absent watermark, and introducing it in the claim commit instead would
    # make that commit touch an undeclared path — which RULING-6's audit reads,
    # correctly, as a non-merge trunk commit touching product paths.
    write_watermark(root, WI=401)
    _commit(root, "seed", when=T_BASE)
    return root


def spec_text(
    wid,
    title="Widget",
    safety="ordinary",
    needs=(),
    order=0,
    deliverable="A widget, shipped.",
    specref=None,
    bar=None,
    brief=None,
    adjudicates=(),
):
    """One work-item spec in the format `scripts/wi_convert.py` emits (the
    tests/test_wi_folder_loaders.py `spec_text` shape).

    The `## Deliverable` body is written by DEFAULT because the CLOSED form is
    the one that has to survive `check_trajectory` on the composed tree: R-A
    errors on a `status=done` WI with an empty Deliverable, and `complete/` is
    where every claimed spec ends up. `specref` is written only when given: the
    WI-370 claim rung wants it on a QUEUED spec, R-F wants it gone from an
    closed one, so each fixture states which shape it is."""
    lines = [
        'id = "{}"'.format(wid),
        'title = "{}"'.format(title),
        'workstream = "ws"',
        'sr_refs = ["SR-001"]',
        "needs = [{}]".format(", ".join('"{}"'.format(n) for n in needs)),
        'safety_class = "{}"'.format(safety),
        "order = {}".format(order),
    ]
    if specref:
        lines.append('specref = "{}"'.format(specref))
    if bar:
        lines.append('bar = "{}"'.format(bar))
    if brief:
        lines.append('brief = "{}"'.format(brief))
    if adjudicates:
        lines.append(
            "adjudicates = [{}]".format(
                ", ".join('"{}"'.format(rid) for rid in adjudicates)
            )
        )
    text = "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def write_spec(root, where, wid, slug="widget", **kw):
    """Write `docs/work/<where>/<wid>-<slug>.md`; return its path.

    `newline="\\n"` explicitly: integrate._spec_frontmatter matches `+++\\n`, so
    a fixture that took the platform default would not parse on Windows — and a
    fixture that takes the platform default cannot test the platform (WI-337)."""
    path = root / "docs" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def _rev(root, ref):
    return _git(root, "rev-parse", ref).strip()


def _branches(root):
    return _git(root, "branch", "--format=%(refname:short)").split()


def write_watermark(root, **marks):
    """Give a fixture repo the `docs/id-watermark` every real repo carries.

    These fixtures are bare git repos rather than bootstrapped scaffolds, so
    they ship no watermark — and `trace._read_marks` REFUSES an absent file
    rather than reading it as "no id is taken", which is the whole point of the
    guard (ADOPTING.md). The mark has to cover the ids the fixture allocates:
    a `WI-401` spec means the WI space stands at 401."""
    body = "".join(
        "{} = {}\n".format(space, marks.get(space, 0))
        for space in ("ASSET CMP DP IF LLR MOD OI PART PB REPO SN SR TC WI".split())
    )
    path = root / "docs" / "id-watermark"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8", newline="\n")
    return path


def claim_repo(tmp_path, branch="main", wi="WI-401", **spec_kw):
    """A trunk repo whose `docs/work/` spec folder IS the work-item registry
    (Phase 2b dual-read: real specs present => the folder is authoritative, so
    no docs/requirements/work-items.csv is needed at all). The queued spec
    resolves its SpecRef to the fixture's own seed file so the WI-370 rung
    passes by default — a rung-specific test overrides it."""
    git_repo(tmp_path, branch=branch)
    spec_kw.setdefault("specref", "seed.txt")
    write_spec(tmp_path, "queued", wi, **spec_kw)
    declare_generated(tmp_path)
    _commit(tmp_path, "file " + wi, when=T_CODE)
    return tmp_path


def declare_generated(root):
    """Declare the §5.2 generated set, the way the shipped stack.ini template
    does. NOT decoration: the claim folds `trunk_step --regen` into its commit,
    and with a `docs/work/` registry present that regen writes
    PROJECT_STATE.html — so a repo that has not declared its generated
    artifacts produces a claim commit touching an UNDECLARED path, which is the
    same thing `integrate audit` (RULING-6) flags and which `_abandoned_claim`
    reads with the same allowed set. Declaring it makes the fixture a repo the
    rest of the harness would also accept, rather than bending a rule to fit."""
    ini = root / "docs" / "stack.ini"
    ini.parent.mkdir(parents=True, exist_ok=True)
    text = ini.read_text(encoding="utf-8") if ini.exists() else ""
    if "[generated]" not in text:
        text += ("\n" if text and not text.endswith("\n") else "") + (
            "[generated]\nPROJECT_STATE.html = trajectory\n"
        )
    ini.write_text(text, encoding="utf-8", newline="\n")


# --- 3. the verdict gate (RULING-7) ------------------------------------------


VERDICT_APPROVE = """# Review A — WI-401

Model: test/reviewer

VERDICT: APPROVE findings=0
"""


# --- 6. end to end, against a REAL green bar ---------------------------------


E2E_DEMO_SRC = '''"""Demo pure core for the kit self-test. Pure — no I/O."""


def add(a, b):
    """Add two numbers. Implements: SR-001, LLR-001"""
    return a + b


def sub(a, b):
    """Subtract two numbers. Implements: SR-001, LLR-001"""
    return a - b
'''


def scaffolded_closed_branch(tmp_path):
    """A bootstrapped scaffold whose WI-401 is claimed, built and CLOSED on
    `wi-401`: exactly the state the queue runs against. Returns (repo, claim_sha).

    The bar this sets up for is REAL. `make_minimal_project` gives the scaffold a
    fully traced SN->SR->LLR->TC chain, so `check.py --trunk-lane` at the derived
    gate (DevStg-Impl) and the smoke tier genuinely passes on the refreshed branch —
    measured 17 PASS steps, zero SKIP. `_run_bar` is deliberately NOT stubbed by
    any caller: a monkeypatched bar would make every downstream assertion true of
    a queue that merges anything.

    Two fixture notes, each a real property of the script under test:

      * NO `.venv` is seeded. `agent_common.harness_python` prefers the repo's
        own `.venv` and falls back to `sys.executable`; a `seed_venv`-style
        `venv.create(with_pip=False)` interpreter carries neither pytest nor
        ruff, so it would red the format/lint/test steps of the very bar these
        tests need to pass honestly. The fallback lands on THIS suite's
        interpreter, which is floor-satisfying and carries the pinned tools.
      * `out/` is gitignored by the fixture wholesale, where the shipped
        `gitignore.template` names its paths one by one (`out/run-logs/`,
        `out/agent-loop.lock`, `out/integrate.lock`, `out/subagent-gate.log`).
        `integrate()` opens its coordinator lock at `out/integrate.lock` BEFORE
        checking the trunk is clean; the lock's own line entered the template
        after this fixture first recorded a stock scaffold refusing itself as
        "dirty" on that file.
    """
    skip_without_env_gates("git")
    repo = tmp_path / "repo"
    repo.mkdir()
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", repo], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    make_minimal_project(repo)

    # SN-028: the scaffold already carries docs/process.toml, so the dial is set
    # THERE — writing the legacy file beside it is the mixed config the reader
    # now refuses outright.
    set_process_key(repo, "policies", "review_rounds", 0)
    with (repo / ".gitignore").open("a", encoding="utf-8", newline="\n") as fh:
        fh.write("out/\n")
    # A queued spec owes a resolving SpecRef (the WI-370 claim rung); the
    # scaffold's own docs/log.md serves. The closing move below CLEARS it,
    # because the closed form is what check_trajectory --strict sees on the
    # composed tree and R-F wants a terminal SpecRef empty.
    write_spec(repo, "queued", "WI-401", specref="docs/log.md")
    record_ids(repo)  # WI-401 is an ALLOCATED id; the mark must cover it

    # The scaffold is committed as one seed on the default branch (bootstrap does
    # not init a repo), so the claim below is the FIRST thing the queue sees.
    _git(repo, "init", "-q")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(
        repo, "symbolic-ref", "HEAD", "refs/heads/master"
    )  # local init.defaultBranch varies
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "commit.gpgsign", "false")
    _commit(repo, "seed: the scaffolded project", when=T_BASE)

    # 1. claim -> the trunk bookkeeping commit + the branch cut.
    proc = run_py(
        [
            SCRIPTS / "integrate.py",
            "--root",
            ".",
            "claim",
            "--wi",
            "WI-401",
            "--branch",
            "wi-401",
        ],
        cwd=repo,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    claim_sha = _rev(repo, "HEAD")

    # 2. the worker's branch: one product commit, then the closing move.
    _git(repo, "checkout", "-q", "wi-401")
    (repo / "src" / "demo.py").write_text(E2E_DEMO_SRC, encoding="utf-8", newline="\n")
    _commit(repo, "feat: subtract, verifying SR-001", when=T_CODE)
    # The closing move edits the spec the way a real close does: the file
    # lands in complete/ with its SpecRef cleared (R-F), not byte-moved. The
    # terminal home is the archive since WI-504 (OI-55 ruled (a)) — one
    # directory deeper than the active workspace `active/` sits in.
    src = repo / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    dst = repo / "docs" / "archive" / "work" / "complete" / "WI-401-widget.md"
    dst.write_text(
        src.read_text(encoding="utf-8").replace('specref = "docs/log.md"\n', ""),
        encoding="utf-8",
        newline="\n",
    )
    _git(repo, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
    _commit(repo, "close: WI-401 -> complete", when=T_VERDICT)
    _git(repo, "checkout", "-q", "master")
    return repo, claim_sha


# --- 7. the §5.6 unload: the branch AND its worker worktree (WI-359) ----------


def _worktree_count(root):
    """Registered worktrees, the trunk included (so a lone trunk counts 1)."""
    return len([ln for ln in _git(root, "worktree", "list").splitlines() if ln.strip()])
