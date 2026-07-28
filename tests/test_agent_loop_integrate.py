"""The atomic serialized integrator — scripts/agent_loop.py (WI-184,
SR-063/LLR-064/TC-064; docs/specs/parallel-wi-dispatch.md §9).

The load-bearing guarantees:

  - overlapping trains compose serially against the CURRENT integration HEAD
    and the combined bar always runs (a red declared bar blocks integration
    and leaves the integration ref untouched);
  - a clean 3-way apply integrates WITHOUT re-review, while ANY textual
    conflict parks the train for a focused re-review — never a silent pick;
  - the integration ref advances only by CAS (a stale expected-old fails
    harmlessly), and reservation refs release only AFTER the durable
    disposition advanced;
  - a blocked disposition changes ONLY its WI (Status=blocked + BlockRef +
    trailers) through the same CAS discipline;
  - review verdicts are verified against the EXACT reviewed head — a train
    whose verdict names an older commit does not integrate;
  - publication to the development branch: proceeds when the worktree dirt is
    disjoint from the publish diff (the edits ride the sync forward unchanged),
    deferred (untouched, reported) only when dirt intersects it (WI-230);
    guarded by the durable publish-intent ref so a crash between the dev-ref
    CAS and the worktree sync finishes idempotently instead of reading as user
    dirt;
  - an absent integration ref with dispatcher-owned evidence fails closed
    (never silently re-seeded from the development branch).
"""

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import env_gate_skipif, SCRIPTS, load_script, run_py, seed_venv

agent_loop = load_script("agent_loop")
agent_dispatch = load_script("agent_dispatch")

pytestmark = env_gate_skipif("git")

HEADER = [
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "BuildTier",
    "SafetyClass",
    "BlockRef",
]


def _git(repo, *args):
    p = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout.strip()


def _wi_row(wid, preds="", safety="ordinary", status="queued"):
    return [
        wid,
        "Work " + wid,
        "ws",
        "SR-063",
        preds,
        status,
        "shipped" if status == "done" else "",
        "docs/specs/thing.md",
        "medium",
        safety,
        "",
    ]


def _make_repo(tmp_path, rows, stack_test=None, header=None, product_test=None):
    repo = tmp_path / "repo"
    (repo / "docs" / "requirements").mkdir(parents=True)
    with open(
        str(repo / "docs" / "requirements" / "work-items.csv"),
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:
        w = csv.writer(fh)
        w.writerow(header or HEADER)
        w.writerows(rows)
    (repo / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    (repo / ".gitignore").write_text("out/\n.venv/\n", encoding="utf-8")
    seed_venv(repo)  # WI-286: the dispatcher preflight requires a ≥3.11 root .venv
    (repo / "docs" / "gate-policy").write_text("autonomous\n", encoding="utf-8")
    # The combined bar reads the declared test command: legacy `[stack] test`
    # (raw) OR the kit schema `[product] test` (with {py}/{src}/{tests}
    # substitution — WI-285). A fixture declares at most one.
    if stack_test:
        (repo / "docs" / "stack.ini").write_text(
            "[stack]\ntest = {}\n".format(stack_test), encoding="utf-8"
        )
    elif product_test:
        (repo / "docs" / "stack.ini").write_text(
            "[product]\ntest = {}\n".format(product_test), encoding="utf-8"
        )
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


# Fake worker: commits the trailer protocol. `shared` mode also writes a
# SHARED path with train-specific content (the overlap/conflict fixture).
FAKE = r"""
import argparse, csv, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
wi = re.search(r"- WI: (WI-\d+)", args.prompt).group(1)
train = re.search(r"- Train: (\S+) \(branch", args.prompt).group(1)
base = re.search(r"integration base ([0-9a-f]+)\)", args.prompt).group(1)
mode = (ctl / "mode").read_text().strip() if (ctl / "mode").exists() else ""


def _edit_row(target):
    p = pathlib.Path("docs/requirements/work-items.csv")
    with p.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    for r in rows:
        if r and r[0] == target:
            r[1] = "edited by " + wi
    with p.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)


pathlib.Path("work-" + wi + ".txt").write_text("work", encoding="utf-8")
if mode == "shared":
    pathlib.Path("shared.txt").write_text("content from " + wi, encoding="utf-8")
if mode in ("dashboard", "mixed"):
    # A train-specific dashboard: the generated artifact each WI regenerates,
    # so two trains off one base conflict on it (WI-231 Slice A).
    pathlib.Path("PROJECT_STATE.html").write_text(
        "<html>dashboard from " + wi + "</html>\n", encoding="utf-8"
    )
if mode == "mixed":
    pathlib.Path("shared.txt").write_text("content from " + wi, encoding="utf-8")
if mode == "regrow":  # each train edits its OWN registry row (disjoint union)
    _edit_row(wi)
if mode == "clash":  # every train edits the SAME row (a genuine collision)
    _edit_row("WI-201")
subprocess.run(["git", "add", "-A"], check=True)
msg = "build " + wi + "\n\nWI: " + wi + "\nTrain: " + train + "\nBase: " + base + "\n"
subprocess.run(["git", "commit", "-q", "-m", msg], check=True)
sys.exit(0)
"""


def _setup(tmp_path, rows, stack_test=None, header=None, product_test=None):
    repo = _make_repo(
        tmp_path, rows, stack_test=stack_test, header=header, product_test=product_test
    )
    ctl = tmp_path / "ctl"
    ctl.mkdir()
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    return repo, ctl, template


def _dispatch(repo, template, *extra, jobs="2"):
    return run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template,
            "--pause",
            "0",
            "--poll-seconds",
            "0.2",
            "--model",
            "test",
            "--jobs",
            jobs,
            *extra,
        ],
        cwd=repo,
    )


def _events(repo):
    p = repo / "out" / "dispatch" / "events.jsonl"
    if not p.exists():
        return []
    return [
        json.loads(ln)
        for ln in p.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]


def _reservations(repo):
    out = _git(repo, "for-each-ref", "--format=%(refname)", "refs/llm/reservations")
    return {ln.rsplit("/", 1)[1] for ln in out.splitlines() if ln.strip()}


# --- composition, bar, trailers ---------------------------------------------------


def test_serial_composition_with_trailers_and_bar(tmp_path):
    # Two disjoint trains integrate serially; each integration commit carries
    # Integrated-WI/Train-Head trailers, the declared bar runs on the composed
    # tree, and the dev branch receives BOTH via publication.
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201"), _wi_row("WI-202")],
        stack_test='"{}" -c "import sys; sys.exit(0)"'.format(sys.executable),
    )
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    log = _git(repo, "log", "--format=%s%n%(trailers)", "HEAD")
    assert log.count("integrate: train") == 2
    assert "Integrated-WI: WI-201" in log and "Integrated-WI: WI-202" in log
    assert "Train-Head:" in log
    bars = [e for e in _events(repo) if e["event"] == "integration-bar"]
    assert len(bars) == 2 and all(b["result"] == "pass" for b in bars)
    # Durable evidence landed: log entries + regenerated artifacts on dev.
    assert "integrated train" in (repo / "docs" / "log.md").read_text("utf-8")
    assert (repo / "docs" / "iteration_index.md").exists()
    assert _reservations(repo) == set()


def test_product_schema_bar_runs_on_real_integration(tmp_path):
    # WI-285 done-when: a real integration whose repo declares its harness under
    # the kit schema `[product] test` journals a RUN result ("pass"), not the old
    # fail-open "skipped (no declared test command)". {py} expands to the
    # integrator's interpreter (check._expand), the same substitution check.py
    # makes for the per-commit floor.
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201")],
        product_test='{py} -c "import sys; sys.exit(0)"',
    )
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    bars = [e for e in _events(repo) if e["event"] == "integration-bar"]
    assert bars, "the integrator must journal a combined-bar result"
    assert all(b["result"] == "pass" for b in bars), bars
    assert all("skipped" not in b["result"] for b in bars), bars


def test_red_combined_bar_blocks_integration_and_cas(tmp_path):
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201")],
        stack_test='"{}" -c "import sys; sys.exit(1)"'.format(sys.executable),
    )
    before = _git(repo, "rev-parse", "HEAD")
    proc = _dispatch(repo, template)
    # The train parks for rework; nothing integrates, the integration ref and
    # the dev branch stay exactly where they were, the reservation is HELD.
    assert proc.returncode == agent_loop.EXIT_STALL, proc.stdout + proc.stderr
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == before
    assert _git(repo, "rev-parse", "HEAD") == before
    assert _reservations(repo) == {"WI-201"}
    events = _events(repo)
    assert any(
        e["event"] == "integration-parked" and e["state"] == "rework" for e in events
    )
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert ",done," not in reg, "a red bar must never produce a done row"


def test_missing_binary_combined_bar_parks_not_crashes(tmp_path):
    # SR-008 end-to-end: a declared [product] test whose executable does not
    # exist must PARK the train for rework — the same outcome as a red bar — and
    # never crash the dispatcher. Before the OSError guard, subprocess.run raised
    # FileNotFoundError out of integrate_train and the whole walk-away loop
    # exited 1 AFTER the worker was ready, so nothing parked and the operator got
    # a stack trace instead of a rework.
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201")],
        product_test="llm-nonexistent-binary-xyzzy --run",
    )
    before = _git(repo, "rev-parse", "HEAD")
    proc = _dispatch(repo, template)
    # Parks for rework, exactly like a red bar: nothing integrates, refs frozen,
    # reservation held — and the dispatcher exits its normal stall code, never a
    # crash traceback.
    assert proc.returncode == agent_loop.EXIT_STALL, proc.stdout + proc.stderr
    assert "Traceback" not in (proc.stdout + proc.stderr)
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == before
    assert _git(repo, "rev-parse", "HEAD") == before
    assert _reservations(repo) == {"WI-201"}
    events = _events(repo)
    assert any(
        e["event"] == "integration-parked" and e["state"] == "rework" for e in events
    )
    bars = [e for e in events if e["event"] == "integration-bar"]
    assert bars and all("not runnable" in b["result"] for b in bars), bars
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert ",done," not in reg, "a missing-binary bar must never produce a done row"


# --- WI-285: the combined bar reads the schema the repo actually declares --------
# The integrator used to read docs/stack.ini `[stack] test`, a key the kit's own
# profile (and every check.py-shaped one) does not have — it declares the harness
# under `[product] test`. So the composed-tree bar journalled "skipped (no
# declared test command)" and fail-OPENed on every integration.


def _bar_worktree(tmp_path, ini_text):
    """A minimal composed-tree stand-in: a docs/ dir under a worktree, with a
    docs/stack.ini of `ini_text` (None writes none), for exercising
    _run_combined_bar directly."""
    wt = tmp_path / "wt"
    (wt / "docs").mkdir(parents=True)
    if ini_text is not None:
        (wt / "docs" / "stack.ini").write_text(ini_text, encoding="utf-8")
    return wt


def test_combined_bar_runs_product_schema_not_skips(tmp_path):
    # The kit declares its harness under [product] test = {py} -m pytest, NOT
    # [stack] test. The bar must READ that key (with {py} substitution) and RUN
    # it — the schema mismatch that silently skipped every integration.
    wt = _bar_worktree(
        tmp_path, '[product]\ntest = {py} -c "import sys; sys.exit(0)"\n'
    )
    ok, detail = agent_dispatch._run_combined_bar(str(wt), str(wt))
    assert ok and detail == "pass", detail


def test_combined_bar_product_red_parks(tmp_path):
    # A composed tree that fails its declared [product] bar reports not-ok, so
    # the integrator parks the train instead of integrating.
    wt = _bar_worktree(
        tmp_path, '[product]\ntest = {py} -c "import sys; sys.exit(3)"\n'
    )
    ok, _detail = agent_dispatch._run_combined_bar(str(wt), str(wt))
    assert not ok


def test_combined_bar_red_detail_keeps_the_diagnostic_not_just_the_fail_header(
    tmp_path,
):
    # WI-304 rework, from adversarial review. This bar runs the DOWNSTREAM repo's
    # declared command, so its output grammar is unknown. `_failure_tail` returns
    # the block ENDING at the last `FAIL` line — correct for check.py, where FAIL
    # is a trailing summary; wrong for jest/go, where FAIL is a HEADER and the
    # diagnostic follows it. Routing this site through it truncated a jest failure
    # to the filename alone, and returned a PASSING test's block for `go test`.
    #
    # The operator reading a parked unattended train gets only this string, so the
    # reason must survive. Jest-shaped: a FAIL header, the assertion AFTER it.
    script = (
        "import sys;"
        "print(' FAIL  src/sum.test.js');"
        "print('  * adds 1 + 2');"
        "print('    Expected: 3');"
        "print('    Received: 4');"
        "print('Test Suites: 1 failed, 1 total');"
        "sys.exit(1)"
    )
    wt = _bar_worktree(tmp_path, '[product]\ntest = {py} -c "' + script + '"\n')
    ok, detail = agent_dispatch._run_combined_bar(str(wt), str(wt))
    assert not ok
    assert "Expected: 3" in detail, (
        "the failure reason was truncated to the FAIL header: " + repr(detail)
    )
    assert "Received: 4" in detail, repr(detail)


def test_combined_bar_legacy_stack_key_still_runs(tmp_path):
    # The legacy [stack] test key stays honored as a fallback, so a profile that
    # used it does not silently stop running.
    wt = _bar_worktree(
        tmp_path,
        '[stack]\ntest = "{}" -c "import sys; sys.exit(0)"\n'.format(sys.executable),
    )
    ok, detail = agent_dispatch._run_combined_bar(str(wt), str(wt))
    assert ok and detail == "pass", detail


def test_combined_bar_skips_only_when_no_command_declared(tmp_path):
    # The honest skip: no stack.ini, or a stack.ini declaring NEITHER test key,
    # is a genuinely stackless fixture (skip=pass).
    wt = _bar_worktree(tmp_path, None)
    ok, detail = agent_dispatch._run_combined_bar(str(wt), str(wt))
    assert ok and detail.startswith("skipped")
    wt2 = _bar_worktree(tmp_path / "b", "[paths]\nsrc = src\ntests = tests\n")
    ok2, detail2 = agent_dispatch._run_combined_bar(str(wt2), str(wt2))
    assert ok2 and detail2 == "skipped (no declared test command)"


def test_combined_bar_declared_but_empty_fails_closed(tmp_path):
    # A declared-but-EMPTY command is a misconfiguration, not a stackless skip —
    # fail closed rather than silently pass (the WI-285 fail-open lesson).
    wt = _bar_worktree(tmp_path, "[product]\ntest =\n")
    ok, _detail = agent_dispatch._run_combined_bar(str(wt), str(wt))
    assert not ok


def test_combined_bar_unreadable_profile_parks(tmp_path):
    # A malformed stack.ini raises ValueError from the resolver; the bar PARKS
    # (fail closed), never skips — a stackless fixture has no stack.ini at all.
    wt = _bar_worktree(tmp_path, "not a section header\n")
    ok, detail = agent_dispatch._run_combined_bar(str(wt), str(wt))
    assert not ok and "unreadable" in detail


def test_combined_bar_missing_binary_fails_closed(tmp_path):
    # SR-008: a declared [product] test whose executable is absent raises
    # FileNotFoundError (an OSError) out of subprocess.run. The bar must catch
    # it and return not-ok — a RED bar the integrator reworks, NOT an uncaught
    # crash that exits the whole walk-away dispatcher after the worker is ready.
    wt = _bar_worktree(
        tmp_path, "[product]\ntest = llm-nonexistent-binary-xyzzy --run\n"
    )
    ok, detail = agent_dispatch._run_combined_bar(str(wt), str(wt))
    assert not ok and "not runnable" in detail


def test_declared_test_command_resolution(tmp_path):
    # The shared resolver directly: [product] expands {py}/{src}/{tests} exactly
    # as check.py fills them; [stack] is tokenized RAW (quotes group as one
    # token); NEITHER key -> None (stackless) while a present-but-EMPTY command
    # -> [] (declared) so the caller fail-closes rather than skipping.
    ini = tmp_path / "stack.ini"
    ini.write_text(
        "[paths]\nsrc = lib\ntests = t\n[product]\ntest = {py} -m pytest {src} {tests}\n",
        encoding="utf-8",
    )
    assert agent_dispatch._declared_test_command(ini) == [
        sys.executable,
        "-m",
        "pytest",
        "lib",
        "t",
    ]
    ini.write_text('[stack]\ntest = mytool --run "a b"\n', encoding="utf-8")
    assert agent_dispatch._declared_test_command(ini) == ["mytool", "--run", "a b"]
    ini.write_text("[paths]\nsrc = s\n", encoding="utf-8")
    assert agent_dispatch._declared_test_command(ini) is None
    ini.write_text("[product]\ntest =\n", encoding="utf-8")
    assert agent_dispatch._declared_test_command(ini) == []


def test_combined_bar_runs_under_the_root_venv_interpreter(tmp_path, monkeypatch):
    # WI-286: {py} for the composed-tree bar is the repo's OWN .venv (an absolute
    # path resolved by harness_python), not this process's interpreter — so the
    # bar runs the pinned ≥3.11 toolchain even when the dispatcher was itself
    # launched on ambient Python (the ambient-3.8 risk WI-285's {py}=sys.executable
    # would otherwise re-import).
    root = tmp_path / "root"
    if __import__("os").name == "nt":
        vpy = root / ".venv" / "Scripts" / "python.exe"
    else:
        vpy = root / ".venv" / "bin" / "python"
    vpy.parent.mkdir(parents=True)
    vpy.write_text("stub interpreter\n", encoding="utf-8")  # only resolved, never run
    wt = _bar_worktree(tmp_path, "[product]\ntest = {py} -c pass\n")

    captured = {}

    def spy(ini, py=None):
        captured["py"] = py
        return [sys.executable, "-c", ""]  # a harmless real command so the bar passes

    monkeypatch.setattr(agent_dispatch, "_declared_test_command", spy)
    ok, detail = agent_dispatch._run_combined_bar(str(wt), str(root))
    assert ok and detail == "pass", detail
    assert captured["py"] == str(vpy)  # the root .venv, via harness_python(root)


def test_conflict_forces_focused_re_review_clean_apply_does_not(tmp_path):
    # Two trains write DIFFERENT content to the SAME source path: the first
    # composes cleanly (no re-review), the second hits a textual conflict and
    # parks needs-re-review — its WIs never done, its reservations held. WI-232:
    # a real source conflict now PAGES NEEDS-HUMAN with an ask naming the train
    # and the conflicted path (the WI-127 contract), not a silent RUNNING/STALL.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    (ctl / "mode").write_text("shared", encoding="utf-8")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr

    events = _events(repo)
    integrated = [e for e in events if e["event"] == "integrated"]
    conflicts = [e for e in events if e["event"] == "integration-conflict"]
    assert len(integrated) == 1, "the first train takes the clean fast path"
    assert len(conflicts) >= 1, "the second must hit the conflict, not a pick"
    parked = [
        e
        for e in events
        if e["event"] == "integration-parked" and e["state"] == "needs-re-review"
    ]
    assert parked, "a conflict demands a focused re-review"
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert reg.count(",done,") == 1, "only the cleanly-applied WI is done"
    assert len(_reservations(repo)) == 1, "the conflicted train keeps its claim"
    # The run-state pages the human with a one-line ask naming the train + path.
    run_state = (repo / "docs" / "run-state").read_text(encoding="utf-8")
    assert run_state.startswith("NEEDS-HUMAN")
    ask = [ln for ln in run_state.splitlines() if ln.startswith("ask:")]
    assert ask, "a source-conflict park owes a WI-127 ask line"
    assert "shared.txt" in ask[0], "the ask must name the conflicted path"
    train_tid = next(iter(_reservations_by_train(repo)))
    assert train_tid in ask[0], "the ask must name the parked train"


def _reservations_by_train(repo):
    # {train-id: [WI-ID,...]} from the reservation commits' metadata.
    trains = {}
    out = _git(
        repo,
        "for-each-ref",
        "--format=%(refname) %(objectname)",
        "refs/llm/reservations",
    )
    for ln in out.splitlines():
        if not ln.strip():
            continue
        ref, sha = ln.split()
        wid = ref.rsplit("/", 1)[1]
        meta = json.loads(_git(repo, "log", "-1", "--format=%B", sha))
        trains.setdefault(meta["train"], []).append(wid)
    return trains


def _conflict_count(repo):
    return sum(1 for e in _events(repo) if e["event"] == "integration-conflict")


def test_needs_re_review_relaunch_is_idempotent_until_inputs_change(tmp_path):
    # WI-232 regressions 2 + 3. A parked source conflict must not re-run the
    # identical merge every launch (the silent re-park that burned resumable
    # lanes) — the merge inputs (train tip + integration head) are recorded
    # durably and a relaunch with UNCHANGED inputs skips the merge, still paging
    # NEEDS-HUMAN with the same ask. Only when an input changes does it retry.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    (ctl / "mode").write_text("shared", encoding="utf-8")

    # Launch 1: train A integrates, train B parks needs-re-review (1 conflict).
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr
    assert _conflict_count(repo) == 1
    ask1 = [
        ln
        for ln in (repo / "docs" / "run-state").read_text("utf-8").splitlines()
        if ln.startswith("ask:")
    ][0]
    conflict_refs = _git(
        repo, "for-each-ref", "--format=%(refname)", "refs/llm/conflict"
    ).splitlines()
    assert conflict_refs, "the conflict's merge inputs are recorded durably in git"

    # Launch 2: UNCHANGED inputs. The guard skips the merge — no SECOND
    # integration-conflict event — yet still pages NEEDS-HUMAN with the same ask.
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr
    assert _conflict_count(repo) == 1, "an unchanged relaunch must NOT re-merge"
    assert any(e["event"] == "integration-conflict-held" for e in _events(repo)), (
        "the idempotence guard fires on the unchanged relaunch"
    )
    ask2 = [
        ln
        for ln in (repo / "docs" / "run-state").read_text("utf-8").splitlines()
        if ln.startswith("ask:")
    ][0]
    assert ask2 == ask1, "the paged ask is stable across an unchanged relaunch"

    # Move the integration head (another train integrating, in effect): an empty
    # commit on top of it changes train B's merge inputs, so the next relaunch
    # RETRIES the merge exactly once — a second integration-conflict appears.
    ihead = _git(repo, "rev-parse", "refs/heads/llm/integration")
    tree = _git(repo, "rev-parse", ihead + "^{tree}")
    moved = _git(repo, "commit-tree", tree, "-p", ihead, "-m", "another train")
    _git(repo, "update-ref", "refs/heads/llm/integration", moved)

    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr
    assert _conflict_count(repo) == 2, "a changed-input relaunch retries the merge once"


# --- CAS + fail-closed unit surfaces ----------------------------------------------


def test_cas_ref_stale_old_fails_harmlessly(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    a = _git(repo, "rev-parse", "HEAD")
    (repo / "x.txt").write_text("x", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "second")
    b = _git(repo, "rev-parse", "HEAD")
    assert agent_loop.cas_ref(repo, "refs/heads/llm/integration", a, None)
    # Stale expected-old: the ref already moved to a — a CAS from b must fail
    # without touching it.
    assert not agent_loop.cas_ref(repo, "refs/heads/llm/integration", b, b)
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == a
    # And the honest CAS succeeds.
    assert agent_loop.cas_ref(repo, "refs/heads/llm/integration", b, a)


def test_absent_integration_ref_with_evidence_fails_closed(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    head = _git(repo, "rev-parse", "HEAD")
    err = agent_loop.reserve_traincar(repo, "t-orphan", ["WI-201"], head)
    assert err is None
    # Reservation evidence exists but no integration ref: the dispatcher must
    # fail closed, never silently re-seed from the development branch.
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_PREFLIGHT
    assert "fails closed" in (proc.stdout + proc.stderr)


def test_stale_review_verdict_does_not_integrate(tmp_path):
    # A verdict naming an OLDER head than the reviewed train tip must not
    # count (spec §8: a verdict belongs to the exact reviewed commit).
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, "t-stale", ["WI-201"], head) is None
    # Build the WI on the train branch with a verdict naming a BOGUS sha.
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t-stale")
    (wt / "work.txt").write_text("w", encoding="utf-8")
    vdir = wt / "docs" / "reviews" / "t-stale"
    vdir.mkdir(parents=True)
    (vdir / "001-REVIEW-A-0000000.md").write_text(
        "VERDICT: APPROVE findings=0\n", encoding="utf-8"
    )
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "-q",
        "-m",
        "build WI-201\n\nWI: WI-201\nTrain: t-stale\nBase: {}\n".format(head),
    )
    state, detail = agent_loop.integrate_train(
        repo,
        repo / "docs",
        agent_loop._Journal(repo),
        "t-stale",
        ["WI-201"],
        head,
        review_ctx=(True, 1),
    )
    # WI-260: the only verdict names a BOGUS (older) head, so REVIEW-A filed NO
    # verdict at the reviewed head — a wedged reviewer pages rather than a silent
    # stall, and the integration ref never moves.
    assert state == "needs-human" and "filed no verdict" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == head


# --- WI-260: the per-phase latest-APPROVE unanimity gate (M-29) --------------------

_SR_CRITIQUE_HDR = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
)
_SR_CRITIQUE_ROW = (
    'SR-050,Render,SN-001,"looks real","subj","rubric",,S,Critique,Verified\n'
)


def _wi_row_srrefs(wid, srrefs):
    row = _wi_row(wid)
    row[3] = srrefs  # the SR-Refs column
    return row


def _setup_gate(tmp_path, srrefs="SR-063", render=False):
    """A one-WI train built on its branch with the integration ref seeded — the
    stage right before the verdict gate. Returns (repo, worktree, base_head).
    render=True adds a Critique-verified SR-050 the WI delivers, so the train
    classifies render-surface (CRITIQUE required)."""
    repo = _make_repo(tmp_path, [_wi_row_srrefs("WI-201", srrefs)])
    if render:
        (repo / "docs" / "requirements" / "system-requirements.csv").write_text(
            _SR_CRITIQUE_HDR + _SR_CRITIQUE_ROW, encoding="utf-8"
        )
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "add critique SR")
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, "t1", ["WI-201"], head) is None
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t1")
    (wt / "work.txt").write_text("w", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "-q",
        "-m",
        "build WI-201\n\nWI: WI-201\nTrain: t1\nBase: {}\n".format(head),
    )
    return repo, wt, head


def _plant_verdicts(wt, reviewed, files):
    """Plant reviews/t1/NNN-PHASE-<reviewed7>.md for each (ordinal, phase,
    verdict) and commit them WITHOUT a WI trailer, so the reviewed head stays the
    build commit while the verdict files sit at the train tip. A verdict outside
    {APPROVE, CHANGES-REQUESTED} plants an UNPARSEABLE file (no machine line)."""
    vdir = wt / "docs" / "reviews" / "t1"
    vdir.mkdir(parents=True, exist_ok=True)
    for ordinal, phase, verdict in files:
        name = "{:03d}-{}-{}.md".format(ordinal, phase, reviewed[:7])
        if verdict in ("APPROVE", "CHANGES-REQUESTED"):
            body = "VERDICT: {} findings=0\n".format(verdict)
        else:
            body = "- a finding here but the machine line got mangled\n"
        (vdir / name).write_text(body, encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-q", "-m", "review verdicts")


def _integrate(repo, base, review_ctx):
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    return reviewed, agent_dispatch.integrate_train(
        repo,
        repo / "docs",
        agent_loop._Journal(repo),
        "t1",
        ["WI-201"],
        base,
        review_ctx,
    )


def test_gate_extra_critique_approve_never_covers_a_missing_reviewer(tmp_path):
    # dial-2, NON-render train. REVIEW-A + a stray CRITIQUE approve, REVIEW-B
    # never filed. The pre-change count gate saw 2 approvals (critique counted
    # toward the dial) >= 2 and INTEGRATED; the unanimity gate requires REVIEW-B
    # by NAME, so an extra approval never substitutes -> pages, ref frozen.
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _plant_verdicts(
        wt, reviewed, [(1, "REVIEW-A", "APPROVE"), (1, "CRITIQUE", "APPROVE")]
    )
    _, (state, detail) = _integrate(repo, base, (True, 2))
    assert state == "needs-human" and "REVIEW-B" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == base


def test_gate_same_head_reviewer_dissent_blocks_rework(tmp_path):
    # dial-2. REVIEW-A approve, REVIEW-B CHANGES-REQUESTED at the exact head. The
    # count gate ignored the same-head dissent (it tallied only approvals); the
    # unanimity gate honors the last word -> rework, ref frozen.
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _plant_verdicts(
        wt, reviewed, [(1, "REVIEW-A", "APPROVE"), (1, "REVIEW-B", "CHANGES-REQUESTED")]
    )
    _, (state, detail) = _integrate(repo, base, (True, 2))
    assert state == "rework" and "REVIEW-B" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == base


def test_gate_scripts_train_integrates_without_a_critique(tmp_path):
    # A NON-render dial-2 train: REVIEW-A + REVIEW-B approve and NO critique is
    # scheduled or present. It must integrate — never deadlock waiting for an
    # unscheduled CRITIQUE (design 1, the scripts-train direction).
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _plant_verdicts(
        wt, reviewed, [(1, "REVIEW-A", "APPROVE"), (1, "REVIEW-B", "APPROVE")]
    )
    _, (state, detail) = _integrate(repo, base, (True, 2))
    assert state == "integrated", detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") != base


def test_gate_render_train_cannot_integrate_critique_less(tmp_path):
    # A render-surface dial-2 train with BOTH reviewers approving but NO CRITIQUE
    # filed. The count gate (required_verdicts=2) integrated on the two reviewer
    # approvals; the unanimity gate adds the orthogonal CRITIQUE requirement
    # (WI-243) -> pages, ref frozen (the render-train direction of design 1).
    repo, wt, base = _setup_gate(tmp_path, srrefs="SR-050", render=True)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _plant_verdicts(
        wt, reviewed, [(1, "REVIEW-A", "APPROVE"), (1, "REVIEW-B", "APPROVE")]
    )
    _, (state, detail) = _integrate(repo, base, (True, 2))
    assert state == "needs-human" and "CRITIQUE" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == base


def test_gate_dial0_render_train_gates_on_critique_alone(tmp_path):
    # design 3: a dial-0 RENDER train schedules no reviewer but DOES schedule
    # CRITIQUE. With no critique filed the count gate (required_verdicts=0)
    # skipped the check entirely and integrated critique-less; the unanimity gate
    # requires CRITIQUE -> pages.
    repo, wt, base = _setup_gate(tmp_path, srrefs="SR-050", render=True)
    _, (state, detail) = _integrate(repo, base, (True, 0))
    assert state == "needs-human" and "CRITIQUE" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == base
    # ...and a CRITIQUE APPROVE alone clears it.
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _plant_verdicts(wt, reviewed, [(1, "CRITIQUE", "APPROVE")])
    _, (state2, detail2) = _integrate(repo, base, (True, 0))
    assert state2 == "integrated", detail2
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") != base


def test_gate_dial0_non_render_train_integrates_on_the_bar_alone(tmp_path):
    # design 3: a dial-0 NON-render train schedules no verdict phase at all, so
    # the gate requires nothing and integrates on the combined bar alone
    # (unchanged from the old required_verdicts=0 path).
    repo, wt, base = _setup_gate(tmp_path)
    _, (state, detail) = _integrate(repo, base, (True, 0))
    assert state == "integrated", detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") != base


def test_gate_same_head_flip_escalates_not_silently_wins(tmp_path):
    # design 2: REVIEW-A files CHANGES-REQUESTED at ord 1 then APPROVE at ord 2 —
    # SAME head (code unchanged). A reroll-until-green must NOT clear the gate: it
    # escalates needs-human and journals loudly. The count gate saw the APPROVE
    # file and integrated.
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _plant_verdicts(
        wt, reviewed, [(1, "REVIEW-A", "CHANGES-REQUESTED"), (2, "REVIEW-A", "APPROVE")]
    )
    _, (state, detail) = _integrate(repo, base, (True, 1))
    assert state == "needs-human" and "flip" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == base
    events = [e for e in _events(repo) if e.get("event") == "verdict-escalation"]
    assert events, "the escalation must be journaled loudly"


def test_gate_reverse_flip_is_honored_dissent(tmp_path):
    # design 2 (reverse): APPROVE at ord 1 then CHANGES-REQUESTED at ord 2 — the
    # later dissent IS the last word and blocks -> rework (never a flip). The
    # count gate would have counted the ord-1 APPROVE file and integrated.
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _plant_verdicts(
        wt, reviewed, [(1, "REVIEW-A", "APPROVE"), (2, "REVIEW-A", "CHANGES-REQUESTED")]
    )
    _, (state, detail) = _integrate(repo, base, (True, 1))
    assert state == "rework" and "REVIEW-A" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == base


def test_gate_ambiguous_latest_verdict_pages_not_clears(tmp_path):
    # review fix 2: REVIEW-A APPROVE@ord1 then an UNPARSEABLE re-review@ord2 at
    # the same reviewed head. The mangled later file is the last word: the gate
    # must NOT fall back to the older APPROVE and clear — it reads the phase as
    # having no latest verdict and pages needs-human. BITES the drop-and-keep-
    # APPROVE behavior (which integrated on the ord-1 APPROVE).
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _plant_verdicts(
        wt, reviewed, [(1, "REVIEW-A", "APPROVE"), (2, "REVIEW-A", "MANGLED")]
    )
    _, (state, detail) = _integrate(repo, base, (True, 1))
    assert state == "needs-human" and "REVIEW-A" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == base


@pytest.mark.parametrize(
    "srrefs,render_expected", [("SR-050", True), ("SR-063", False)]
)
def test_scheduler_and_gate_agree_on_critique_phase(tmp_path, srrefs, render_expected):
    # WI-260 review fix 1 (design 1, CRITIQUE half): the gate's render-surface
    # decision must equal the scheduler's CRITIQUE trigger over the SAME
    # commit-subject WI scope — driven, both directions. A Critique SR is present
    # in BOTH cases; only whether the train's scope WI DELIVERS it differs.
    repo, wt, base = _setup_gate(tmp_path, srrefs=srrefs, render=True)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    docs = repo / "docs"
    rng = base + ".." + reviewed
    # Gate side: the classifier over commit-subject scope WIs.
    scope_wis = agent_dispatch._train_scope_wis(repo, "t1", base, reviewed)
    gate_render = agent_dispatch._train_is_render_surface(docs, scope_wis)
    # Scheduler side: the exact functions agent_loop fires CRITIQUE from.
    sched_render = bool(
        agent_loop.build_scope_srs(repo, docs, rng) & agent_loop.load_critique_srs(docs)
    )
    assert gate_render == sched_render == render_expected
    # And the required set reflects it (CRITIQUE present iff render).
    required = agent_dispatch._required_phases(docs, scope_wis, (True, 1))
    assert ("CRITIQUE" in required) is render_expected


# --- WI-282: the reviewed-head trailer-slip diagnostic ----------------------------


def _commit_no_trailer(wt, subject, filename="more.txt"):
    (wt / filename).write_text(subject, encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-q", "-m", subject)
    return _git(wt, "rev-parse", "HEAD")


def test_reviewed_head_trailer_slip_is_journaled(tmp_path):
    # WI-282 secondary: a newer build commit that SLIPPED its WI trailer leaves
    # the substantive tip AHEAD of the reviewed head (newest-WITH-a-WI-trailer),
    # so reviewed_train_head would grade an OLDER commit's verdict while an
    # unnamed commit rides the train. The integrator journals the mismatch by
    # name so it reads as a slipped trailer, not honest dissent.
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(
        repo, "t1", base
    )  # the WI-trailer build
    tip = _commit_no_trailer(wt, "WI-201: more work (trailer slipped)")
    assert tip != reviewed, "the slipped commit is a newer, distinct head"
    assert agent_dispatch._substantive_tip(repo, "t1", base) == tip
    journal = agent_loop._Journal(repo)
    agent_dispatch.warn_reviewed_head_slip(repo, journal, "t1", base, reviewed)
    slips = [e for e in _events(repo) if e.get("event") == "reviewed-head-trailer-slip"]
    assert slips, "the slipped trailer must be journaled loudly"
    assert slips[0]["reviewed"] == reviewed[:12]
    assert slips[0]["build_tip"] == tip[:12]


def test_no_slip_when_only_sanctioned_commits_ride_the_tip(tmp_path):
    # The negative: telemetry:/blocked: commits on top of the WI-trailer build are
    # NOT substantive (subject prefix / Blocked-WI trailer), so the build tip is
    # still the reviewed head — no diagnostic, so the common honest case is quiet.
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    _commit_no_trailer(wt, "telemetry: session 001 review scoreboard", "sb.txt")
    # A blocked disposition rides via its Blocked-WI trailer, free-form subject.
    (wt / "blk.txt").write_text("evidence", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-q", "-m", "partial\n\nBlocked-WI: WI-201\nBlockRef: OI-4\n")
    assert agent_dispatch._substantive_tip(repo, "t1", base) == reviewed
    journal = agent_loop._Journal(repo)
    agent_dispatch.warn_reviewed_head_slip(repo, journal, "t1", base, reviewed)
    slips = [e for e in _events(repo) if e.get("event") == "reviewed-head-trailer-slip"]
    assert not slips, "sanctioned coordinator commits on top are not a slip"


def test_invalid_blocked_wi_evidence_cannot_hide_a_newer_build_commit(tmp_path):
    # Regression for WI-282 REVIEW-A: malformed `Blocked-WI` evidence from a
    # pre-floor or --no-verify commit is not a sanctioned blocked disposition.
    # The integration diagnostic must identify it as the substantive build tip.
    repo, wt, base = _setup_gate(tmp_path)
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", base)
    (wt / "invalid-block.txt").write_text("evidence", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-q", "-m", "partial\n\nBlocked-WI: not-a-wi\nBlockRef: OI-4\n")
    tip = _git(wt, "rev-parse", "HEAD")
    assert agent_dispatch._substantive_tip(repo, "t1", base) == tip
    journal = agent_loop._Journal(repo)
    agent_dispatch.warn_reviewed_head_slip(repo, journal, "t1", base, reviewed)
    slips = [e for e in _events(repo) if e.get("event") == "reviewed-head-trailer-slip"]
    assert slips and slips[0]["build_tip"] == tip[:12]
    assert slips[0]["reviewed"] == reviewed[:12]


def test_slip_fires_when_no_build_commit_carries_a_wi_trailer(tmp_path):
    # WI-282 fail-open regression: a train whose FIRST/ONLY build commit slipped
    # its WI trailer (a pre-floor or `--no-verify` commit) leaves
    # reviewed_train_head() with no WI-trailered head to resolve — it returns
    # None. The substantive tip still exists, so the diagnostic MUST fire with an
    # explicit missing-reviewed value; the old `reviewed and ...` truthiness guard
    # stayed silent here (the exact pre-floor path the diagnostic claims to catch).
    repo = _make_repo(tmp_path, [_wi_row_srrefs("WI-201", "SR-063")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, "t1", ["WI-201"], head) is None
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t1")
    tip = _commit_no_trailer(wt, "WI-201: build (trailer slipped, no WI: trailer)")
    reviewed = agent_dispatch.reviewed_train_head(repo, "t1", head)
    assert reviewed is None, "no commit carries a WI trailer, so none resolves"
    assert agent_dispatch._substantive_tip(repo, "t1", head) == tip
    journal = agent_loop._Journal(repo)
    agent_dispatch.warn_reviewed_head_slip(repo, journal, "t1", head, reviewed)
    slips = [e for e in _events(repo) if e.get("event") == "reviewed-head-trailer-slip"]
    assert slips, "a train with NO WI-trailered head must still journal the slip"
    assert slips[0]["reviewed"] == "(none)"
    assert slips[0]["build_tip"] == tip[:12]


# --- publication + the intent protocol --------------------------------------------


def test_disjoint_dirty_worktree_publishes_and_preserves_the_edit(tmp_path):
    # WI-230: a tracked edit the publish diff never touches (an owner-scratchpad
    # analogue) no longer strands publication — it rides the sync forward
    # byte-for-byte while the development ref lands on the integration target.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    dirty = "# agents (edited, uncommitted)\n"
    (repo / "AGENTS.md").write_text(dirty, "utf-8")  # disjoint from the diff
    dev_before = _git(repo, "rev-parse", "HEAD")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    # Integration advanced AND publication landed; the disjoint edit survives.
    integ = _git(repo, "rev-parse", "refs/heads/llm/integration")
    assert integ != dev_before
    assert _git(repo, "rev-parse", "HEAD") == integ, "publication is no longer stranded"
    assert (repo / "AGENTS.md").read_text("utf-8") == dirty, (
        "a disjoint dirty checkout is carried forward unchanged, never reset"
    )
    code = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "--verify",
            "--quiet",
            "refs/llm/publish-intent",
        ],
        capture_output=True,
    ).returncode
    assert code != 0, "a completed publication deletes its intent"
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert "WI-201,Work WI-201,ws,SR-063,,done," in reg


def test_crash_between_dev_cas_and_sync_recovers_idempotently(tmp_path):
    # Simulate the §11 row: the dev ref already equals the intent's target but
    # the worktree/index still sit at the expected OLD hash. Recovery must
    # finish the sync (reset to target + delete the intent) — never classify
    # the mechanically stale checkout as user dirt.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    old = _git(repo, "rev-parse", "HEAD")
    # Build a target commit on the integration ref.
    (repo / "landed.txt").write_text("landed", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integrated content")
    target = _git(repo, "rev-parse", "HEAD")
    _git(repo, "reset", "--hard", old)  # dev checkout back at the old hash
    _git(repo, "update-ref", "refs/heads/llm/integration", target)
    # The crash left: intent ref written, dev ref CAS'd to target, sync unrun.
    tree = _git(repo, "rev-parse", target + "^{tree}")
    meta = json.dumps(
        {
            "train": "publish",
            "wis": ["publish"],
            "base": target,
            "target": target,
            "old": old,
            "ref": "refs/heads/" + _git(repo, "branch", "--show-current"),
        },
        sort_keys=True,
    )
    intent = _git(repo, "commit-tree", tree, "-p", target, "-m", meta)
    _git(repo, "update-ref", "refs/llm/publish-intent", intent)
    branch = _git(repo, "branch", "--show-current")
    _git(repo, "update-ref", "refs/heads/" + branch, target)

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state in ("noop", "published"), detail
    assert _git(repo, "rev-parse", "HEAD") == target
    assert (repo / "landed.txt").exists(), "the sync completed"
    code = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "--verify",
            "--quiet",
            "refs/llm/publish-intent",
        ],
        capture_output=True,
    ).returncode
    assert code != 0, "the finished intent is deleted"


# --- WI-230: publish under disjoint dirt -----------------------------------------


def _intent_absent(repo):
    return (
        subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "rev-parse",
                "--verify",
                "--quiet",
                "refs/llm/publish-intent",
            ],
            capture_output=True,
        ).returncode
        != 0
    )


def _publish_fixture(tmp_path):
    """A repo whose integration ref sits one commit ahead of the development
    branch. The publish diff touches ONLY `published.txt`; `docs/notes.md` and
    `docs/run-state` are tracked bystanders the diff never touches. The dev
    checkout is reset back to `old`. Returns (repo, branch, old, target)."""
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    (repo / "published.txt").write_text("base\n", encoding="utf-8")
    (repo / "docs" / "notes.md").write_text("notes base\n", encoding="utf-8")
    (repo / "docs" / "run-state").write_text("RUNNING base\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "tracked baseline")
    branch = _git(repo, "branch", "--show-current")
    old = _git(repo, "rev-parse", "HEAD")
    (repo / "published.txt").write_text("base\nadvanced\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integration content")
    target = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", target)
    _git(repo, "reset", "--hard", old)
    return repo, branch, old, target


def test_publish_carries_disjoint_dirt_forward(tmp_path):
    # Regression 1: a dirty tracked file disjoint from the publish diff no
    # longer defers — publication lands and the edit survives byte-for-byte.
    repo, branch, old, target = _publish_fixture(tmp_path)
    (repo / "docs" / "notes.md").write_text("notes base\nWIP edit\n", "utf-8")

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state == "published", detail
    assert _git(repo, "rev-parse", "refs/heads/" + branch) == target
    assert (repo / "published.txt").read_text("utf-8") == "base\nadvanced\n"
    assert (repo / "docs" / "notes.md").read_text("utf-8") == "notes base\nWIP edit\n"
    assert _intent_absent(repo), "a completed publication deletes its intent"


def test_publish_defers_when_dirt_intersects_the_diff(tmp_path):
    # Regression 2: dirt on a path the publication would advance still defers,
    # leaving the checkout and the development ref untouched (never reset/stash).
    repo, branch, old, target = _publish_fixture(tmp_path)
    (repo / "published.txt").write_text("base\nLOCAL conflict\n", "utf-8")

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state == "deferred", detail
    assert _git(repo, "rev-parse", "refs/heads/" + branch) == old, "dev ref untouched"
    assert (repo / "published.txt").read_text("utf-8") == "base\nLOCAL conflict\n"
    assert _intent_absent(repo), "an intersecting defer writes no intent"
    assert any(
        e["event"] == "publish-deferred" and e.get("reason") == "dirty-worktree"
        for e in _events(repo)
    )


def test_run_state_rewrite_alone_no_longer_strands_publication(tmp_path):
    # Regression 4: the dispatcher's own end-of-run run-state rewrite (dirt on
    # docs/run-state, disjoint from the diff) can no longer strand publication.
    repo, branch, old, target = _publish_fixture(tmp_path)
    (repo / "docs" / "run-state").write_text("DONE new\n", "utf-8")

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state == "published", detail
    assert _git(repo, "rev-parse", "refs/heads/" + branch) == target
    assert (repo / "docs" / "run-state").read_text("utf-8") == "DONE new\n"


def test_crash_replay_carries_disjoint_dirt_forward(tmp_path):
    # Regression 3: the §11 replay (intent present, crash between the dev-ref
    # CAS and the sync) with a disjoint uncommitted edit present must finish the
    # sync AND preserve the edit — never read the mechanically stale checkout,
    # nor the disjoint dirt, as a blocking divergence.
    repo, branch, old, target = _publish_fixture(tmp_path)
    # Reconstruct the crash-window state: dev ref already CAS'd to target while
    # the worktree/index still sit at old, the intent written, plus disjoint dirt.
    _git(repo, "update-ref", "refs/heads/" + branch, target)
    (repo / "docs" / "notes.md").write_text("notes base\nWIP survives\n", "utf-8")
    tree = _git(repo, "rev-parse", target + "^{tree}")
    meta = json.dumps(
        {
            "train": "publish",
            "wis": ["publish"],
            "base": target,
            "target": target,
            "old": old,
            "ref": "refs/heads/" + branch,
        },
        sort_keys=True,
    )
    intent = _git(repo, "commit-tree", tree, "-p", target, "-m", meta)
    _git(repo, "update-ref", "refs/llm/publish-intent", intent)

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state in ("noop", "published"), detail
    assert _git(repo, "rev-parse", "HEAD") == target
    assert (repo / "published.txt").read_text("utf-8") == "base\nadvanced\n", (
        "the interrupted sync completed"
    )
    assert (repo / "docs" / "notes.md").read_text(
        "utf-8"
    ) == "notes base\nWIP survives\n"
    assert _intent_absent(repo), "the finished intent is deleted"

    # Idempotent replay: a second pass with the edit still dirty is a clean noop
    # (no pending intent), never a spurious divergence defer.
    state2, _ = agent_loop.publish_integration(repo, journal, branch)
    assert state2 == "noop"
    assert (repo / "docs" / "notes.md").read_text(
        "utf-8"
    ) == "notes base\nWIP survives\n"


def test_publish_defers_on_untracked_collision_with_an_added_path(tmp_path):
    # WI-230 review (MAJOR, top data-loss class): the publish diff ADDS a path
    # where the owner holds an UNTRACKED file of distinct content. Publication
    # must defer — the collision is caught at the gate so the dev ref never
    # moves, and git's read-tree refuses to clobber it at the sync — so the file
    # survives byte-for-byte. Locks the behavior against a future swap of
    # read-tree for a forced (clobbering) sync variant.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    branch = _git(repo, "branch", "--show-current")
    old = _git(repo, "rev-parse", "HEAD")
    (repo / "added.txt").write_text("PUBLISHED content of the added file\n", "utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integration adds a file")
    target = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", target)
    _git(repo, "reset", "--hard", old)  # dev back at old; added.txt leaves the tree
    owner = "OWNER untracked content — must not be lost\n"
    (repo / "added.txt").write_text(owner, "utf-8")  # untracked, distinct content

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state == "deferred", detail
    assert _git(repo, "rev-parse", "refs/heads/" + branch) == old, (
        "dev ref must not move"
    )
    assert (repo / "added.txt").read_text("utf-8") == owner, (
        "the untracked file survives byte-for-byte"
    )
    assert _intent_absent(repo), "a gate deferral writes no intent"


def test_publish_refuses_a_non_descendant_integration_target(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    base = _git(repo, "rev-parse", "HEAD")
    branch = _git(repo, "branch", "--show-current")

    (repo / "integration-only.txt").write_text("integration", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integration side")
    integration_head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "reset", "--hard", base)

    (repo / "development-only.txt").write_text("development", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "development side")
    development_head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", integration_head)

    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.publish_integration(repo, journal, branch)
    assert state == "deferred"
    assert integration_head in detail and development_head in detail
    assert _git(repo, "rev-parse", "refs/heads/" + branch) == development_head
    event = [e for e in _events(repo) if e["event"] == "publish-deferred"][-1]
    assert event["reason"] == "non-descendant-target"
    assert event["integration_head"] == integration_head
    assert event["development_head"] == development_head


def test_relaunch_pages_before_work_when_integration_and_dev_diverge(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    base = _git(repo, "rev-parse", "HEAD")

    (repo / "integration-only.txt").write_text("integration", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "integration side")
    integration_head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "reset", "--hard", base)

    dev_commits = []
    for number in (1, 2):
        (repo / "dev-{}.txt".format(number)).write_text(
            "development {}".format(number), encoding="utf-8"
        )
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "development {}".format(number))
        dev_commits.append(_git(repo, "rev-parse", "HEAD"))
    development_head = dev_commits[-1]
    _git(repo, "update-ref", "refs/heads/llm/integration", integration_head)

    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr
    assert _git(repo, "rev-parse", "HEAD") == development_head
    for commit in dev_commits:
        assert _git(repo, "merge-base", "--is-ancestor", commit, "HEAD") == ""
    assert not list((repo / "out" / "dispatch" / "trains").glob("*.json"))

    run_state = (repo / "docs" / "run-state").read_text(encoding="utf-8")
    assert run_state.startswith("NEEDS-HUMAN") and "ask:" in run_state
    assert integration_head in run_state and development_head in run_state
    event = [e for e in _events(repo) if e["event"] == "integration-diverged"][-1]
    assert event["integration_head"] == integration_head
    assert event["development_head"] == development_head


def test_disposition_regeneration_is_artifact_gated_and_ordered(tmp_path, monkeypatch):
    worktree = tmp_path / "wt"
    (worktree / "docs" / "okf").mkdir(parents=True)
    (worktree / "PROJECT_STATE.html").write_text("dashboard", encoding="utf-8")
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((__import__("pathlib").Path(argv[1]).name, kwargs["cwd"]))
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(agent_loop.agent_dispatch.subprocess, "run", fake_run)
    ok, detail = agent_loop.agent_dispatch._regenerate_disposition_artifacts(worktree)
    assert ok and detail == ""
    assert [name for name, cwd in calls] == ["gen_okf.py", "gen_trajectory.py"]
    assert all(cwd == str(worktree) for name, cwd in calls)

    calls[:] = []
    (worktree / "docs" / "okf").rename(worktree / "docs" / "okf-disabled")
    (worktree / "PROJECT_STATE.html").unlink()
    ok, detail = agent_loop.agent_dispatch._regenerate_disposition_artifacts(worktree)
    assert ok and detail == "" and calls == []


def test_disposition_regen_status_map_opts_in_on_open_items_alone(
    tmp_path, monkeypatch
):
    # WI-283: the status-map floor step splices status.md AND open-items.md from one
    # `--status` run and is vacuous only when BOTH are absent — so the regen must
    # opt in on EITHER. A repo carrying open-items.md but no status.md must still
    # trigger `--status`; keying the opt-in on status.md alone (the pre-fix rule)
    # would skip it and strand the pending projection against its own floor. (The
    # blocked/dual-plan/integrate paths call generate_status first, which synthesizes
    # status.md and would MASK this end-to-end — so it is pinned here, at the unit.)
    # WI-322 moved the second marker from docs/open-items.md to the registry the
    # generated owner surface reads.
    worktree = tmp_path / "wt"
    (worktree / "docs" / "requirements").mkdir(parents=True)
    (worktree / "docs" / "requirements" / "open-items.csv").write_text(
        "OI-ID,Title,Status\nOI-1,pending thing,pending\n", encoding="utf-8"
    )
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(
            (Path(argv[1]).name, list(argv[4:]))
        )  # name + flags after --root <wt>
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(agent_loop.agent_dispatch.subprocess, "run", fake_run)
    ok, detail = agent_loop.agent_dispatch._regenerate_disposition_artifacts(worktree)
    assert ok and detail == ""
    # The registry opts in BOTH generators that read it: the status snapshot's
    # one-liner projection and the owner surface itself.
    assert calls == [
        ("gen_trajectory.py", ["--status"]),
        ("gen_open_items.py", []),
    ]


def test_dual_plan_regen_failure_salvages_round_evidence(tmp_path, monkeypatch):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)

    def fake_round(worktree, wid, row, template, model, timeout, prompt_map):
        round_dir = worktree / "docs" / "plans" / "DP-001-wi-201"
        round_dir.mkdir(parents=True)
        (round_dir / "verdict.md").write_text("SELECT A", encoding="utf-8")
        return "SELECTED", "plan A"

    monkeypatch.setattr(agent_loop.agent_dispatch, "run_dual_plan_round", fake_round)
    monkeypatch.setattr(
        agent_loop.agent_dispatch,
        "_regenerate_disposition_artifacts",
        lambda worktree: (
            False,
            "disposition regen failed (gen_okf.py): injected failure",
        ),
    )
    state, detail = agent_loop.dual_plan_disposition(
        repo,
        agent_loop._Journal(repo),
        "t-dual",
        "WI-201",
        {},
        "unused",
        "unused",
        1,
        {},
    )
    assert state == "error"
    assert "disposition regen failed (gen_okf.py): injected failure" in detail
    assert "round evidence salvaged to" in detail
    salvaged = (
        repo
        / "out"
        / "dispatch"
        / "salvage"
        / "t-dual"
        / "DP-001-wi-201"
        / "verdict.md"
    )
    assert salvaged.read_text(encoding="utf-8") == "SELECT A"


def test_dual_plan_validator_failure_is_fail_closed_with_salvage(tmp_path, monkeypatch):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    (repo / "docs" / "requirements" / "system-requirements.csv").write_text(
        "SR-ID\nSR-063\n", encoding="utf-8"
    )
    (repo / "PROJECT_STATE.html").write_text("existing view", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "enable trajectory view")
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)

    def invalid_round(worktree, wid, row, template, model, timeout, prompt_map):
        round_dir = worktree / "docs" / "plans" / "DP-003-wi-201"
        round_dir.mkdir(parents=True)
        (round_dir / "verdict.md").write_text("SELECT invalid", encoding="utf-8")
        with (worktree / "docs" / "requirements" / "work-items.csv").open(
            "a", encoding="utf-8", newline=""
        ) as fh:
            csv.writer(fh).writerow(_wi_row("WI-202", preds="WI-999"))
        return "SELECTED", "invalid child predecessor"

    monkeypatch.setattr(agent_loop.agent_dispatch, "run_dual_plan_round", invalid_round)
    state, detail = agent_loop.dual_plan_disposition(
        repo,
        agent_loop._Journal(repo),
        "t-invalid",
        "WI-201",
        {},
        "unused",
        "unused",
        1,
        {},
    )
    assert state == "error"
    assert "disposition regen failed (gen_trajectory.py):" in detail
    assert "predecessor 'WI-999' is not a work item" in detail
    assert "round evidence salvaged to" in detail
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == head
    salvaged = (
        repo
        / "out"
        / "dispatch"
        / "salvage"
        / "t-invalid"
        / "DP-003-wi-201"
        / "verdict.md"
    )
    assert salvaged.read_text(encoding="utf-8") == "SELECT invalid"


def test_cas_stale_dual_plan_salvages_committed_round_evidence(tmp_path, monkeypatch):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)

    def fake_round(worktree, wid, row, template, model, timeout, prompt_map):
        round_dir = worktree / "docs" / "plans" / "DP-002-wi-201"
        round_dir.mkdir(parents=True)
        (round_dir / "verdict.md").write_text("SELECT B", encoding="utf-8")
        # An EXTERNAL actor moves the integration ref mid-round: a dangling
        # sibling commit stales the disposition's CAS after its commit lands,
        # so the evidence is committed and porcelain is clean at reset time.
        tree = _git(repo, "rev-parse", "HEAD^{tree}")
        moved = _git(repo, "commit-tree", tree, "-p", "HEAD", "-m", "external")
        _git(repo, "update-ref", "refs/heads/llm/integration", moved)
        return "SELECTED", "plan B"

    monkeypatch.setattr(agent_loop.agent_dispatch, "run_dual_plan_round", fake_round)
    monkeypatch.setattr(
        agent_loop.agent_dispatch,
        "_regenerate_disposition_artifacts",
        lambda worktree: (True, ""),
    )
    state, detail = agent_loop.dual_plan_disposition(
        repo,
        agent_loop._Journal(repo),
        "t-cas",
        "WI-201",
        {},
        "unused",
        "unused",
        1,
        {},
    )
    assert state == "error"
    assert "integration ref moved externally" in detail
    assert "round evidence salvaged to" in detail
    salvaged = (
        repo / "out" / "dispatch" / "salvage" / "t-cas" / "DP-002-wi-201" / "verdict.md"
    )
    assert salvaged.read_text(encoding="utf-8") == "SELECT B"


@pytest.mark.parametrize("committed", [False, True], ids=["porcelain", "diff"])
def test_salvage_handles_git_quoted_non_ascii_round_path(tmp_path, committed):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    old_head = _git(repo, "rev-parse", "HEAD")
    round_name = "DP-004-caf\u00e9"
    try:
        round_dir = repo / "docs" / "plans" / round_name
        round_dir.mkdir(parents=True)
        (round_dir / "verdict.md").write_text("SELECT unicode", encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        pytest.skip("filesystem cannot represent non-ASCII round paths: {}".format(exc))
    _git(repo, "config", "core.quotepath", "true")
    if committed:
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "unicode round")

    salvage = agent_loop.agent_dispatch._salvage_round_evidence(
        repo, repo, "t-unicode", old_head if committed else None
    )
    expected = (
        repo / "out" / "dispatch" / "salvage" / "t-unicode" / round_name / "verdict.md"
    )
    assert salvage.endswith("t-unicode")
    assert expected.read_text(encoding="utf-8") == "SELECT unicode"


def test_select_disposition_passes_the_kit_freshness_hook(tmp_path, monkeypatch):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201")])
    req = repo / "docs" / "requirements"
    (req / "stakeholder-needs.md").write_text(
        "# Stakeholder Needs\n\n"
        "| SN-ID | Need | Why | Priority | Acceptance intent |\n"
        "|---|---|---|---|---|\n"
        "| SN-063 | Safe disposition commits. | Preserve work. | Must | "
        "Fresh generated views. |\n",
        encoding="utf-8",
    )
    (req / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
        "SR-063,Safe disposition,SN-063,The system shall preserve disposition "
        "work.,Safety.,Generated views are fresh.,,M,Test,Verified\n",
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(
        "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
        "LLR-063,SR-063,Disposition,src,disposition,Regenerates views.,"
        "(see TC-063),Verified\n",
        encoding="utf-8",
    )
    (repo / "docs" / "test").mkdir()
    (repo / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,"
        "Evidence,Status\n"
        "TC-063,SR-063;LLR-063,Integration,commit,Full,,Fresh views,Yes,"
        "tests/test_agent_loop_integrate.py,Verified\n",
        encoding="utf-8",
    )
    for generator in ("gen_okf.py", "gen_trajectory.py"):
        proc = run_py([SCRIPTS / generator, "--root", repo], cwd=repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed generated artifacts")
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)

    # Enable the shipped hook itself. KIT_SCRIPTS_DIR is its documented
    # downstream override and points it at this checkout's kit scripts.
    _git(repo, "config", "core.hooksPath", str(SCRIPTS.parent / "hooks"))
    monkeypatch.setenv("KIT_SCRIPTS_DIR", str(SCRIPTS))

    def fake_round(worktree, wid, row, template, model, timeout, prompt_map):
        round_dir = worktree / "docs" / "plans" / "DP-001-wi-201"
        round_dir.mkdir(parents=True)
        (round_dir / "verdict.md").write_text("SELECT A", encoding="utf-8")
        with (worktree / "docs" / "requirements" / "work-items.csv").open(
            "a", encoding="utf-8", newline=""
        ) as fh:
            csv.writer(fh).writerow(_wi_row("WI-202", preds="WI-201"))
        return "SELECTED", "plan A"

    monkeypatch.setattr(agent_loop.agent_dispatch, "run_dual_plan_round", fake_round)
    state, detail = agent_loop.dual_plan_disposition(
        repo,
        agent_loop._Journal(repo),
        "t-hook",
        "WI-201",
        {},
        "unused",
        "unused",
        1,
        {},
    )
    assert state == "SELECTED", detail
    staging = repo / "out" / "dispatch" / "worktrees" / "integrate-t-hook"
    for generator in ("gen_okf.py", "gen_trajectory.py"):
        proc = run_py([SCRIPTS / generator, "--root", staging, "--check"], cwd=repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr


def test_blocked_disposition_changes_only_its_wi(tmp_path):
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, "t-blk", ["WI-201"], head) is None
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t-blk")
    (wt / "evidence.txt").write_text("why it is stuck", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "-q",
        "-m",
        "blocked WI-201\n\nBlocked-WI: WI-201\nBlockRef: OI-42\n",
    )
    journal = agent_loop._Journal(repo)
    state, new_head = agent_loop.blocked_disposition(
        repo, repo / "docs", journal, "t-blk", ["WI-201"], head
    )
    assert state == "integrated", new_head
    # ONLY WI-201 changed, with its BlockRef; the trailers are on the commit.
    show = _git(
        repo, "show", "refs/heads/llm/integration:docs/requirements/work-items.csv"
    )
    assert "WI-201,Work WI-201,ws,SR-063,,blocked" in show and "OI-42" in show
    assert "WI-202,Work WI-202,ws,SR-063,,queued" in show
    log = _git(repo, "log", "-1", "--format=%(trailers)", "refs/heads/llm/integration")
    assert "Blocked-WI: WI-201" in log and "BlockRef: OI-42" in log
    assert _reservations(repo) == set(), "released only after the CAS"


# --- WI-283: a blocked disposition regenerates every floor-checked projection ---

_STATUS_BEGIN = "<!-- BEGIN GENERATED STATUS -->"

# WI-322: briefs are registry ROWS and the projection renders into the generated
# docs/open-items.html, so the disposition's regeneration target is that view
# rather than a marker block spliced into markdown.
_OPEN_ITEMS_CSV = (
    "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
    "Recommendation,WI-Refs,RuledDate,RulingRef\n"
    "OI-42,a real pending decision,pending,,rule the thing.,,,,,,,\n"
)

_STATUS_MD = (
    "# Status\n\nHand-authored forward intent.\n\n"
    + _STATUS_BEGIN
    + "\nplaceholder\n<!-- END GENERATED STATUS -->\n"
)


@pytest.mark.parametrize("with_status_md", [True, False])
def test_blocked_disposition_regenerates_pending_projection(tmp_path, with_status_md):
    # The live 2026-07-23 shape (train 3-g3-WI-273-b45e): flipping a WI to blocked
    # feeds the pending-owner-actions projection, which WI-322 renders into the
    # generated docs/open-items.html. The disposition must regenerate it so its
    # own commit passes the SAME floor the pre-commit hook runs. Covered both with and without a
    # shipped docs/status.md (generate_status synthesizes one either way) — the
    # opt-in's INDEPENDENCE from that side-effect is pinned by the unit test
    # test_disposition_regen_status_map_opts_in_on_open_items_alone below.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    (repo / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "requirements" / "open-items.csv").write_text(
        _OPEN_ITEMS_CSV, encoding="utf-8"
    )
    if with_status_md:
        (repo / "docs" / "status.md").write_text(_STATUS_MD, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "add generated projections")
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)

    assert agent_loop.reserve_traincar(repo, "t-blk", ["WI-201"], head) is None
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t-blk")
    (wt / "evidence.txt").write_text("why it is stuck", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "-q",
        "-m",
        "blocked WI-201\n\nBlocked-WI: WI-201\nBlockRef: OI-42\n",
    )

    journal = agent_loop._Journal(repo)
    state, new_head = agent_loop.blocked_disposition(
        repo, repo / "docs", journal, "t-blk", ["WI-201"], head
    )
    assert state == "integrated", new_head

    # The committed view now lists the blocked WI — regeneration fired.
    projected = _git(repo, "show", "refs/heads/llm/integration:docs/open-items.html")
    assert "WI-201" in projected and "blocked" in projected
    assert "OI-42" in projected

    # ... and the composed tree passes BOTH floors the commit faced — the
    # status snapshot and the owner surface are separate steps since WI-322.
    view = tmp_path / "view"
    _git(repo, "worktree", "add", "--detach", str(view), new_head)
    for script, flags in (
        ("gen_trajectory.py", ["--status", "--check"]),
        ("gen_open_items.py", ["--check"]),
    ):
        proc = run_py([SCRIPTS / script, "--root", view, *flags], cwd=view)
        assert proc.returncode == 0, script + ": " + proc.stdout + proc.stderr


# --- WI-238: a blocked disposition survives a registry without a BlockRef column --

LEGACY_HEADER = HEADER[:-1]  # a registry that predates the BlockRef column


def _legacy_row(wid, status="queued", deliverable=""):
    # A 10-field row (no BlockRef cell) — the shape adopted repos carried before
    # the column existed (the WI-229 field event).
    return [
        wid,
        "Work " + wid,
        "ws",
        "SR-063",
        "",
        status,
        deliverable,
        "docs/specs/thing.md",
        "medium",
        "ordinary",
    ]


def test_rewrite_wi_rows_adopts_absent_blockref_column(tmp_path):
    # An update naming a column the registry LACKS extends the header + writes the
    # value rather than silently dropping the field (the root defect).
    reg = tmp_path / "work-items.csv"
    with reg.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(LEGACY_HEADER)
        w.writerow(_legacy_row("WI-201"))
        w.writerow(_legacy_row("WI-202"))
    updated = agent_dispatch._rewrite_wi_rows(
        reg, {"WI-201": {"Status": "blocked", "BlockRef": "OI-42"}}
    )
    assert updated == ["WI-201"]
    text = reg.read_text(encoding="utf-8")
    dr = csv.DictReader(text.splitlines())
    assert "BlockRef" in dr.fieldnames  # the header adopted the column
    rows = list(dr)
    r201 = next(r for r in rows if r["WI-ID"] == "WI-201")
    assert r201["Status"] == "blocked" and r201["BlockRef"] == "OI-42"
    # An untouched legacy row reads the new column as "" (DictReader -> None).
    r202 = next(r for r in rows if r["WI-ID"] == "WI-202")
    assert (r202.get("BlockRef") or "") == ""
    assert text.splitlines()[0].count("BlockRef") == 1  # no duplicate column


def test_rewrite_wi_rows_column_present_writes_without_doubling(tmp_path):
    # With the column already present, behaviour is unchanged: the value is
    # written and no second column appears.
    reg = tmp_path / "work-items.csv"
    with reg.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(HEADER)  # already carries BlockRef
        w.writerow(_wi_row("WI-201"))
    agent_dispatch._rewrite_wi_rows(
        reg, {"WI-201": {"Status": "blocked", "BlockRef": "OI-3"}}
    )
    text = reg.read_text(encoding="utf-8")
    assert text.splitlines()[0].count("BlockRef") == 1
    r = next(iter(csv.DictReader(text.splitlines())))
    assert r["Status"] == "blocked" and r["BlockRef"] == "OI-3"


def test_rewrite_wi_rows_leaves_untouched_rows_byte_for_byte(tmp_path):
    # Untouched rows — including a CRLF registry's quoted, multi-line Deliverable
    # cell (the WI-231 lesson) — survive the extension verbatim, and the file's
    # dominant line ending is preserved.
    reg = tmp_path / "work-items.csv"
    quoted = (
        "WI-202,Work WI-202,ws,SR-063,,done,"
        '"shipped:\r\n- line one\r\n- line two, with comma",'
        "docs/specs/thing.md,medium,ordinary\r\n"
    )
    plain = (
        "WI-203,Work WI-203,ws,SR-063,,queued,,docs/specs/thing.md,medium,ordinary\r\n"
    )
    body = (
        ",".join(LEGACY_HEADER) + "\r\n"
        "WI-201,Work WI-201,ws,SR-063,,queued,,docs/specs/thing.md,medium,ordinary\r\n"
        + quoted
        + plain
    )
    reg.write_bytes(body.encode("utf-8"))
    agent_dispatch._rewrite_wi_rows(
        reg, {"WI-201": {"Status": "blocked", "BlockRef": "OI-9"}}
    )
    after = reg.read_bytes().decode("utf-8")
    assert quoted in after, "the quoted multi-line Deliverable row is byte-identical"
    assert plain in after, "an untouched plain row is byte-identical"
    assert after.count("\r\n") >= 4, "the dominant CRLF line ending is preserved"
    assert after.splitlines()[0].endswith(",BlockRef")
    assert (
        "WI-201,Work WI-201,ws,SR-063,,blocked,,docs/specs/thing.md,"
        "medium,ordinary,OI-9\r\n"
    ) in after


def test_rewrite_wi_rows_fails_loud_naming_column_when_headerless(tmp_path):
    # A malformed (headerless) registry cannot adopt the column: fail loudly
    # naming it rather than commit a row validation will reject.
    reg = tmp_path / "work-items.csv"
    reg.write_text("", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        agent_dispatch._rewrite_wi_rows(
            reg, {"WI-201": {"Status": "blocked", "BlockRef": "OI-1"}}
        )
    assert "BlockRef" in str(exc.value)


def test_rewrite_wi_rows_fails_loud_when_unreadable(tmp_path):
    # An unreadable registry (a directory at the path) fails loudly naming the
    # column, never a bare OSError traceback.
    reg = tmp_path / "work-items.csv"
    reg.mkdir()
    with pytest.raises(ValueError) as exc:
        agent_dispatch._rewrite_wi_rows(reg, {"WI-201": {"BlockRef": "OI-1"}})
    assert "BlockRef" in str(exc.value)


def _blocked_field_setup(tmp_path, header, rows):
    """The WI-229 field shape: a reserved train carrying a Blocked-WI/BlockRef
    trailer over an integration ref whose registry uses `header`."""
    repo, ctl, template = _setup(tmp_path, rows, header=header)
    head = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", head)
    assert agent_loop.reserve_traincar(repo, "t-blk", ["WI-201"], head) is None
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", str(wt), "llm/train/t-blk")
    (wt / "evidence.txt").write_text("why it is stuck", encoding="utf-8")
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "-q",
        "-m",
        "blocked WI-201\n\nBlocked-WI: WI-201\nBlockRef: OI-42\n",
    )
    return repo, head


def test_blocked_disposition_extends_columnless_registry_end_to_end(tmp_path):
    # The end-to-end field shape: a Blocked-WI trailer + a registry that predates
    # the BlockRef column. The disposition adopts the column, commits, releases
    # the reservation, and the committed result passes the SAME validator that
    # used to reject it forever (the unbreakable parked-error loop).
    repo, head = _blocked_field_setup(
        tmp_path, LEGACY_HEADER, [_legacy_row("WI-201"), _legacy_row("WI-202")]
    )
    journal = agent_loop._Journal(repo)
    state, new_head = agent_loop.blocked_disposition(
        repo, repo / "docs", journal, "t-blk", ["WI-201"], head
    )
    assert state == "integrated", new_head
    show = _git(
        repo, "show", "refs/heads/llm/integration:docs/requirements/work-items.csv"
    )
    assert show.splitlines()[0].endswith("BlockRef"), "the column was adopted"
    assert "WI-201,Work WI-201,ws,SR-063,,blocked" in show and "OI-42" in show
    assert "WI-202,Work WI-202,ws,SR-063,,queued" in show
    verify = tmp_path / "verify"
    _git(repo, "worktree", "add", "-q", "--detach", str(verify), new_head)
    ct = run_py([SCRIPTS / "check_trajectory.py"], cwd=verify)
    assert ct.returncode == 0, ct.stdout + ct.stderr
    assert _reservations(repo) == set(), "released only after the CAS"


def test_blocked_disposition_fails_loud_on_headerless_registry(tmp_path):
    # When the column cannot be adopted (a malformed, headerless registry at the
    # integration HEAD), the transaction errors naming the column, commits
    # nothing, and holds the reservation — never the silent parked loop.
    repo, head = _blocked_field_setup(tmp_path, LEGACY_HEADER, [_legacy_row("WI-201")])
    reg = repo / "docs" / "requirements" / "work-items.csv"
    reg.write_text("", encoding="utf-8")  # malformed: no header row
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "corrupt registry")
    bad = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/heads/llm/integration", bad)
    journal = agent_loop._Journal(repo)
    state, detail = agent_loop.blocked_disposition(
        repo, repo / "docs", journal, "t-blk", ["WI-201"], bad
    )
    assert state == "error"
    assert "BlockRef" in detail, "the error names the un-adoptable column"
    assert _git(repo, "rev-parse", "refs/heads/llm/integration") == bad, "no commit"
    assert _reservations(repo) == {"WI-201"}, "the reservation is held"


# --- WI-231: regenerate generated artifacts / union WI rows on composition -------


def _seed_dashboard(repo):
    """Commit a real generated PROJECT_STATE.html so racing trains conflict on it
    (the field scenario) rather than add/add it."""
    subprocess.run(
        [sys.executable, str(SCRIPTS / "gen_trajectory.py"), "--root", str(repo)],
        check=True,
        stdin=subprocess.DEVNULL,
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed dashboard")


def _trajectory_fresh(repo):
    return (
        subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "gen_trajectory.py"),
                "--root",
                str(repo),
                "--check",
            ],
            capture_output=True,
        ).returncode
        == 0
    )


def _no_park(events):
    return not [
        e
        for e in events
        if e["event"] == "integration-parked" and e["state"] == "needs-re-review"
    ]


def test_two_trains_regenerating_the_dashboard_integrate_without_parking(tmp_path):
    # Slice A: two trains reserved off one base each regenerate PROJECT_STATE.html;
    # the second's composition conflict is a GENERATED artifact, so the integrator
    # regenerates from the merged sources and continues — no re-review park — and
    # the published dashboard matches its merged sources (`--check` green).
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201"), _wi_row("WI-202")],
        stack_test='"{}" -c "import sys; sys.exit(0)"'.format(sys.executable),
    )
    # A README H1 pins the dashboard's project name independent of the worktree
    # basename, so a regen in the integrate worktree matches one at the repo root.
    (repo / "README.md").write_text("# Fixture Project\n", encoding="utf-8")
    _seed_dashboard(repo)
    (ctl / "mode").write_text("dashboard", encoding="utf-8")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    events = _events(repo)
    assert len([e for e in events if e["event"] == "integrated"]) == 2
    assert _no_park(events), "a generated-only conflict never parks"
    regenerated = [e for e in events if e["event"] == "integration-regenerated"]
    assert regenerated, "the dashboard conflict is auto-resolved by regeneration"
    assert any("PROJECT_STATE.html" in e.get("paths", "") for e in regenerated)
    assert _trajectory_fresh(repo), "the integrated dashboard matches merged sources"
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert reg.count(",done,") == 2


def test_disjoint_registry_row_edits_union_without_parking(tmp_path):
    # Slice B: two trains edit DIFFERENT WI rows. A line-level merge misreads the
    # adjacent-row edits as a collision; the WI-ID-keyed union takes each side's
    # row and composition continues — both edits survive, both rows land done.
    repo, ctl, template = _setup(
        tmp_path,
        [_wi_row("WI-201"), _wi_row("WI-202")],
        stack_test='"{}" -c "import sys; sys.exit(0)"'.format(sys.executable),
    )
    (ctl / "mode").write_text("regrow", encoding="utf-8")
    proc = _dispatch(repo, template)
    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr

    events = _events(repo)
    assert len([e for e in events if e["event"] == "integrated"]) == 2
    assert _no_park(events), "disjoint rows union rather than park"
    assert [e for e in events if e["event"] == "integration-regenerated"], (
        "the union path fired (a line-merge would have parked)"
    )
    reg = (repo / "docs" / "requirements" / "work-items.csv").read_text("utf-8")
    assert "edited by WI-201" in reg and "edited by WI-202" in reg
    assert reg.count(",done,") == 2


def test_same_row_both_sides_edit_still_parks(tmp_path):
    # Slice B guard: both trains edit the SAME row (WI-201). That is a genuine
    # both-sides collision the union must NOT auto-resolve — it parks like today.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    (ctl / "mode").write_text("clash", encoding="utf-8")
    proc = _dispatch(repo, template)
    # A source conflict (a both-sides registry-row collision) is human work, so
    # the drained run pages NEEDS-HUMAN (WI-232), not the old silent STALL.
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr

    events = _events(repo)
    assert len([e for e in events if e["event"] == "integrated"]) == 1
    parked = [
        e
        for e in events
        if e["event"] == "integration-parked" and e["state"] == "needs-re-review"
    ]
    assert parked, "a both-sides row collision demands a focused re-review"
    assert len(_reservations(repo)) == 1, "the parked train keeps its claim"
    assert (repo / "docs" / "run-state").read_text("utf-8").startswith("NEEDS-HUMAN")


def test_mixed_generated_and_source_conflict_parks(tmp_path):
    # A conflict spanning a generated artifact AND a hand-written source file:
    # the presence of the non-generated path forces a park — never a silent pick
    # of the generated side while the source conflict is ignored.
    repo, ctl, template = _setup(tmp_path, [_wi_row("WI-201"), _wi_row("WI-202")])
    _seed_dashboard(repo)
    (ctl / "mode").write_text("mixed", encoding="utf-8")
    proc = _dispatch(repo, template)
    # The non-generated side makes this a source conflict: it pages NEEDS-HUMAN
    # (WI-232) rather than the old silent STALL.
    assert proc.returncode == agent_loop.EXIT_NEEDS_HUMAN, proc.stdout + proc.stderr

    events = _events(repo)
    assert len([e for e in events if e["event"] == "integrated"]) == 1
    parked = [
        e
        for e in events
        if e["event"] == "integration-parked" and e["state"] == "needs-re-review"
    ]
    assert parked, "a source-file conflict alongside a generated one still parks"
    assert not [e for e in events if e["event"] == "integration-regenerated"], (
        "a mixed conflict must not silently regenerate"
    )
    assert len(_reservations(repo)) == 1, "the parked train keeps its claim"


# --- WI-231: pure-helper units ---------------------------------------------------

_STATUS_BLOCK = ("<!-- BEGIN GENERATED STATUS -->", "<!-- END GENERATED STATUS -->")


def test_merge_wi_rows_unions_disjoint_and_parks_collisions():
    base = [["WI-1", "queued"], ["WI-2", "queued"]]
    ours = [["WI-1", "done"], ["WI-2", "queued"]]
    theirs = [["WI-1", "queued"], ["WI-2", "done"]]
    # Disjoint edits union, preserving base order.
    assert agent_dispatch._merge_wi_rows(base, ours, theirs) == [
        ["WI-1", "done"],
        ["WI-2", "done"],
    ]
    # A one-sided addition rides through; base order then the new tail.
    added = agent_dispatch._merge_wi_rows(base, ours, theirs + [["WI-3", "queued"]])
    assert added[-1] == ["WI-3", "queued"]
    # The SAME row changed on both sides is a genuine collision -> park.
    assert (
        agent_dispatch._merge_wi_rows(
            [["WI-1", "queued"]], [["WI-1", "a"]], [["WI-1", "b"]]
        )
        is None
    )


def test_block_conflict_resolves_in_block_but_parks_in_prose():
    inside = "prose\n{0}\n<<<<<<< HEAD\nx\n=======\ny\n>>>>>>> B\n{1}\ntail\n".format(
        *_STATUS_BLOCK
    )
    # A conflict confined to the generated block resolves (regeneration then
    # overwrites the block); the hand-authored prose is preserved verbatim.
    resolved = agent_dispatch._resolve_block_conflict(inside, _STATUS_BLOCK)
    assert resolved is not None and "prose" in resolved and "tail" in resolved
    assert "<<<<<<<" not in resolved
    # A conflict touching the hand-authored region must still park.
    outside = "<<<<<<< HEAD\np\n=======\nq\n>>>>>>> B\n"
    assert agent_dispatch._resolve_block_conflict(outside, _STATUS_BLOCK) is None


def test_block_conflict_resolves_under_crlf():
    # WI-231 rework defect 3: on an autocrlf checkout the markers arrive with a
    # trailing \r; the block must still latch and an in-block conflict resolve —
    # not false-park, which would defeat Slice A for status.md/architecture.md.
    begin, end = _STATUS_BLOCK
    crlf = (
        "prose\r\n{0}\r\n<<<<<<< HEAD\r\nx\r\n=======\r\ny\r\n>>>>>>> B\r\n"
        "{1}\r\ntail\r\n".format(begin, end)
    )
    resolved = agent_dispatch._resolve_block_conflict(crlf, _STATUS_BLOCK)
    assert resolved is not None, "a CRLF in-block conflict must resolve like LF"
    assert "prose" in resolved and "tail" in resolved and "<<<<<<<" not in resolved


def _plain_repo(tmp_path, name):
    repo = tmp_path / name
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    return repo


def _conflict_merge(repo):
    subprocess.run(
        ["git", "-C", str(repo), "merge", "--no-ff", "--no-commit", "theirs"],
        capture_output=True,
        stdin=subprocess.DEVNULL,
    )


def test_marker_straddling_hunk_parks(tmp_path):
    # WI-231 rework defect 1: a REAL git-produced hunk that starts in-block but
    # swallows the END marker + adjacent prose on both sides (each side edits the
    # last generated line AND the following prose line) must PARK — taking OURS
    # would silently drop the other side's hand-authored prose.
    repo = _plain_repo(tmp_path, "straddle")
    begin, end = _STATUS_BLOCK

    def status(genb, prose):
        return "\n".join([begin, "genA", genb, end, prose, "tail", ""])

    (repo / "status.md").write_text(status("genB", "prose"), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    home = _git(repo, "branch", "--show-current")
    _git(repo, "branch", "theirs")
    (repo / "status.md").write_text(status("genB-OURS", "prose-OURS"), encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "ours")
    _git(repo, "checkout", "-q", "theirs")
    (repo / "status.md").write_text(
        status("genB-THEIRS", "prose-THEIRS"), encoding="utf-8"
    )
    _git(repo, "commit", "-q", "-am", "theirs")
    _git(repo, "checkout", "-q", home)
    _conflict_merge(repo)

    conflicted = (repo / "status.md").read_text(encoding="utf-8")
    assert "<<<<<<<" in conflicted, "the fixture must produce a real conflict"
    assert agent_dispatch._resolve_block_conflict(conflicted, _STATUS_BLOCK) is None, (
        "a marker-straddling hunk parks rather than dropping the other side's prose"
    )


def test_union_preserves_untouched_multiline_cell(tmp_path):
    # WI-231 rework defect 2: a base row with a quoted, embedded-newline Title
    # that NEITHER side touches must survive the row union byte-for-byte — the
    # strip/splitlines round-trip previously collapsed it and silently rewrote the
    # untouched neighbor on the integration ref.
    repo = _plain_repo(tmp_path, "multiline")
    rel = "docs/requirements/work-items.csv"
    (repo / "docs" / "requirements").mkdir(parents=True)

    def reg(s2, s3):
        return (
            'WI-ID,Title,Status\nWI-1,"multi\nline title",queued\n'
            "WI-2,plain,{}\nWI-3,other,{}\n".format(s2, s3)
        )

    def write_reg(s2, s3):  # newline="" keeps the embedded \n verbatim (floor-safe)
        with open(str(repo / rel), "w", encoding="utf-8", newline="") as fh:
            fh.write(reg(s2, s3))

    write_reg("queued", "queued")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    home = _git(repo, "branch", "--show-current")
    _git(repo, "branch", "theirs")
    write_reg("done", "queued")
    _git(repo, "commit", "-q", "-am", "ours edits WI-2")
    _git(repo, "checkout", "-q", "theirs")
    write_reg("queued", "done")
    _git(repo, "commit", "-q", "-am", "theirs edits WI-3")
    _git(repo, "checkout", "-q", home)
    _conflict_merge(repo)

    assert agent_dispatch._union_registry(str(repo), rel), "disjoint rows union"
    result = (repo / rel).read_text(encoding="utf-8")
    assert '"multi\nline title"' in result, "the untouched multi-line cell survives"
    assert "WI-2,plain,done" in result and "WI-3,other,done" in result


# --- WI-235: the generated-artifact set is DECLARED in docs/stack.ini ------------

_DEFAULT_GENERATED_INI = (
    "[generated]\n"
    "PROJECT_STATE.html = trajectory\n"
    "docs/okf/ = okf\n"
    "docs/architecture.md = archmap | <!-- BEGIN GENERATED MODULE MAP --> "
    "| <!-- END GENERATED MODULE MAP -->\n"
    "docs/status.md = status | <!-- BEGIN GENERATED STATUS --> "
    "| <!-- END GENERATED STATUS -->\n"
)


def test_generated_artifacts_declaration_governs_the_set(tmp_path):
    # The declaration reader: absent => the built-in defaults byte-for-byte
    # (regression 4), a present section is authoritative (extra joins, omitted
    # drops), a malformed row fails closed with a non-blank reason.
    wt = tmp_path / "wt"
    (wt / "docs").mkdir(parents=True)
    ini = wt / "docs" / "stack.ini"

    ini.write_text("[stack]\ntest = x\n", encoding="utf-8")  # section absent
    arts, err = agent_dispatch._generated_artifacts(str(wt))
    assert err is None and arts == agent_dispatch.DEFAULT_GENERATED_ARTIFACTS

    ini.unlink()  # no stack.ini at all is likewise the defaults
    arts, err = agent_dispatch._generated_artifacts(str(wt))
    assert err is None and arts == agent_dispatch.DEFAULT_GENERATED_ARTIFACTS

    # A declared EXTRA artifact joins; a partially-generated file keeps its markers.
    ini.write_text(
        _DEFAULT_GENERATED_INI + "docs/extra.html = trajectory\n", encoding="utf-8"
    )
    arts, err = agent_dispatch._generated_artifacts(str(wt))
    assert err is None
    assert ("docs/extra.html", None, "trajectory") in arts
    assert (
        "docs/status.md",
        ("<!-- BEGIN GENERATED STATUS -->", "<!-- END GENERATED STATUS -->"),
        "status",
    ) in arts

    # A present section is the WHOLE set: omitting a default drops it.
    ini.write_text("[generated]\ndocs/okf/ = okf\n", encoding="utf-8")
    arts, err = agent_dispatch._generated_artifacts(str(wt))
    assert err is None and arts == (("docs/okf/", None, "okf"),)

    # A BARE section is a legitimate declaration of "no generated artifacts" — an
    # empty set (every generated conflict parks), NOT an error (rework MINOR).
    ini.write_text("[generated]\n", encoding="utf-8")
    arts, err = agent_dispatch._generated_artifacts(str(wt))
    assert arts == () and err is None

    # A malformed row fails closed: an empty set + a non-blank reason. Covers a
    # bad kind, a marker count that is neither 0 nor 2, and a DEGENERATE pair whose
    # BEGIN == END (rework MAJOR 1: equal markers would make the block latch open).
    for bad in (
        "PROJECT_STATE.html = nosuchkind\n",
        "docs/x.md = status | oneonly\n",
        "docs/x.md = status | SAME | SAME\n",
    ):
        ini.write_text("[generated]\n" + bad, encoding="utf-8")
        arts, err = agent_dispatch._generated_artifacts(str(wt))
        assert arts == () and err and err.strip()

    # A stack.ini that EXISTS but is unreadable (a directory in its place, or a
    # permission-denied file) must PARK, not fall open to the defaults (rework
    # MAJOR 2b: configparser.read silently skips unreadable files).
    ini.unlink()
    ini.mkdir()  # docs/stack.ini is now a directory
    arts, err = agent_dispatch._generated_artifacts(str(wt))
    assert arts == () and err and err.strip(), (
        "unreadable stack.ini parks, not defaults"
    )


def _generated_conflict_repo(tmp_path, name, rel_path, stack_ini, stack_bytes=None):
    """A REAL conflict on `rel_path`: base commits it (plus an optional stack.ini,
    written as UTF-8 text OR raw `stack_bytes`), two branches write different
    content, HEAD is left on `home` so a merge of `theirs` conflicts. Returns the
    repo path."""
    repo = _plain_repo(tmp_path, name)
    (repo / rel_path).parent.mkdir(parents=True, exist_ok=True)
    (repo / rel_path).write_text("base\n", encoding="utf-8")
    if stack_bytes is not None:
        (repo / "docs").mkdir(exist_ok=True)
        (repo / "docs" / "stack.ini").write_bytes(stack_bytes)
    elif stack_ini is not None:
        (repo / "docs").mkdir(exist_ok=True)
        (repo / "docs" / "stack.ini").write_text(stack_ini, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    home = _git(repo, "branch", "--show-current")
    _git(repo, "branch", "theirs")
    (repo / rel_path).write_text("ours\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "ours")
    _git(repo, "checkout", "-q", "theirs")
    (repo / rel_path).write_text("theirs\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "theirs")
    _git(repo, "checkout", "-q", home)
    return repo


def _compose_theirs(repo, tid="t-235"):
    journal = agent_loop._Journal(repo)
    theirs = _git(repo, "rev-parse", "theirs")
    return agent_dispatch._compose_train(str(repo), str(repo), journal, tid, theirs)


def test_declared_extra_artifact_composes_where_an_absent_section_parks(
    tmp_path, monkeypatch
):
    # Regression 1: a repo-declared EXTRA generated artifact auto-resolves the
    # composition conflict it would otherwise park on. Regeneration is stubbed so
    # the test isolates the declaration wiring from the real generators.
    captured = {}

    def fake_regen(wt, paths, artifacts):
        captured["paths"] = list(paths)
        captured["artifacts"] = artifacts
        return True, ""

    monkeypatch.setattr(agent_dispatch, "_regenerate_generated", fake_regen)

    ini = _DEFAULT_GENERATED_INI + "docs/extra.html = trajectory\n"
    repo = _generated_conflict_repo(tmp_path, "extra-declared", "docs/extra.html", ini)
    assert _compose_theirs(repo) is None, "a declared extra artifact auto-resolves"
    assert ("docs/extra.html", None, "trajectory") in captured["artifacts"]
    assert "docs/extra.html" in captured["paths"]

    # The SAME conflict with NO [generated] declaration parks like today.
    absent = _generated_conflict_repo(tmp_path, "extra-absent", "docs/extra.html", None)
    detail = _compose_theirs(absent)
    assert detail and "docs/extra.html" in detail


def test_removed_default_generated_artifact_parks_again(tmp_path, monkeypatch):
    # Regression 2: a present [generated] section is authoritative, so OMITTING a
    # default (PROJECT_STATE.html) removes it from the auto-resolvable set and a
    # conflict on it parks.
    monkeypatch.setattr(
        agent_dispatch, "_regenerate_generated", lambda w, p, a: (True, "")
    )
    ini = "[generated]\ndocs/okf/ = okf\n"  # PROJECT_STATE.html deliberately dropped
    repo = _generated_conflict_repo(tmp_path, "removed", "PROJECT_STATE.html", ini)
    detail = _compose_theirs(repo)
    assert detail and "PROJECT_STATE.html" in detail


def _restamp_repo(tmp_path, name, src_lines, baseline_text):
    """A worktree declaring `[paths] src = scripts`, one script of `src_lines`
    lines, and a ratchet-shaped baseline file."""
    wt = tmp_path / name
    (wt / "scripts").mkdir(parents=True)
    (wt / "docs").mkdir(parents=True)
    (wt / "docs" / "stack.ini").write_text("[paths]\nsrc = scripts\n", encoding="utf-8")
    (wt / "scripts" / "big.py").write_text(
        "".join("x = {}\n".format(i) for i in range(src_lines)), encoding="utf-8"
    )
    (wt / "ratchet.py").write_text(baseline_text, encoding="utf-8")
    return wt


def test_wi289_linecounts_restamp_uses_the_merged_actuals_not_either_side(tmp_path):
    """WI-289: the module-size ratchet is re-stamped by every train against its own
    base, so on a merge BOTH sides are stale — the composed tree is longer than
    either. Taking a side is therefore always wrong; only a measurement from the
    merged tree is right, which is why this regenerates rather than parks.

    Every rationale comment must survive: those comments are the ratchet's audit
    trail, and only the NUMBER may be rewritten.
    """
    baseline = (
        "BASELINE = {\n"
        "    # +76 (4511 -> 4587), WI-284: reviewed bump, reason in the log.\n"
        '    "big.py": 4587,\n'
        '    "gone.py": 999,\n'
        "}\n"
    )
    wt = _restamp_repo(tmp_path, "restamp", 250, baseline)
    ok, detail = agent_dispatch._restamp_linecount_baselines(wt, ["ratchet.py"])
    assert ok, detail
    out = (wt / "ratchet.py").read_text(encoding="utf-8")
    # measured from the merged tree — not 4587 (ours) and not any theirs value
    assert '"big.py": 250,' in out
    # the audit trail survives verbatim
    assert "# +76 (4511 -> 4587), WI-284: reviewed bump, reason in the log." in out
    # a baseline naming a module that does not exist is left alone, not guessed
    assert '"gone.py": 999,' in out


def test_wi289_linecounts_restamp_preserves_crlf(tmp_path):
    """The re-stamp must not relay a CRLF checkout to LF (WI-234 splice
    discipline) — it edits numbers in place, it does not rewrite the file's form."""
    wt = _restamp_repo(tmp_path, "crlf", 12, "placeholder\n")
    with (wt / "ratchet.py").open("w", encoding="utf-8", newline="") as fh:
        fh.write('BASELINE = {\r\n    "big.py": 1,\r\n}\r\n')
    ok, _ = agent_dispatch._restamp_linecount_baselines(wt, ["ratchet.py"])
    assert ok
    raw = (wt / "ratchet.py").read_bytes()
    assert b'"big.py": 12,' in raw
    assert b"\r\n" in raw and b"\n" not in raw.replace(b"\r\n", b"")


def test_wi289_dupes_census_replaces_a_stale_body_and_keeps_the_header(tmp_path):
    """The census body is regenerated from the MERGED tree; the hand-authored
    comment header (which documents the fingerprint format) is preserved. A stale
    fingerprint line from either side must not survive."""
    wt = _restamp_repo(tmp_path, "dupes", 5, "unused\n")
    census = wt / "docs" / "dupes-allow"
    census.write_text(
        "# census header — documents the format, must survive\n"
        "# second header line\n"
        "\n"
        "deadbeefcafe  stale.py == alsostale.py\n",
        encoding="utf-8",
    )
    ok, detail = agent_dispatch._regen_dupes_census(wt, ["docs/dupes-allow"])
    assert ok, detail
    out = census.read_text(encoding="utf-8")
    assert "# census header — documents the format, must survive" in out
    assert "# second header line" in out
    assert "deadbeefcafe" not in out  # the stale body is gone


def test_wi289_declared_restamp_kinds_parse_and_resolve_instead_of_parking(tmp_path):
    """End to end: the two WI-289 kinds are accepted by the declaration reader and a
    conflict confined to a declared re-stamp path RESOLVES rather than parking —
    the behaviour whose absence forced the hand-integration of WI-274/276/282."""
    ini = (
        _DEFAULT_GENERATED_INI
        + "docs/dupes-allow = dupes\ntests/ratchet.py = linecounts\n"
    )
    wt = tmp_path / "decl"
    wt.mkdir()
    (wt / "docs").mkdir()
    (wt / "docs" / "stack.ini").write_text(ini, encoding="utf-8")
    arts, err = agent_dispatch._generated_artifacts(str(wt))
    assert err is None, err
    kinds = {matcher: kind for matcher, _block, kind in arts}
    assert kinds["docs/dupes-allow"] == "dupes"
    assert kinds["tests/ratchet.py"] == "linecounts"
    # and a conflict on the declared path auto-resolves (does not park)
    repo = _generated_conflict_repo(tmp_path, "restamp-e2e", "tests/ratchet.py", ini)
    detail = _compose_theirs(repo)
    assert detail is None, detail


def test_malformed_generated_section_fails_closed_to_park(tmp_path):
    # Regression 3: an unparseable [generated] row must NEVER widen resolution —
    # the integrator fails closed and parks with a non-blank reason naming it.
    ini = _DEFAULT_GENERATED_INI + "docs/extra.html = status | onlyonemarker\n"
    repo = _generated_conflict_repo(tmp_path, "malformed", "PROJECT_STATE.html", ini)
    detail = _compose_theirs(repo)
    assert detail and "malformed [generated] row" in detail


def test_degenerate_marker_pair_fails_closed_to_park(tmp_path):
    # Rework MAJOR 1: a row whose BEGIN == END would make _resolve_block_conflict's
    # `inside` latch open (the `elif stripped == end` is dead), so a conflict in
    # prose below the block would resolve take-ours and silently drop prose. The
    # declaration must be rejected as malformed so _compose_train parks.
    ini = _DEFAULT_GENERATED_INI + "docs/extra.md = status | SAME | SAME\n"
    repo = _generated_conflict_repo(tmp_path, "degenerate", "PROJECT_STATE.html", ini)
    detail = _compose_theirs(repo)
    assert detail and "malformed [generated] row" in detail


def test_non_utf8_stack_ini_parks_without_stranding_the_merge(tmp_path):
    # Rework MAJOR 2a: a non-UTF-8 stack.ini (a Windows-1252 smart-quote byte)
    # must fail closed to park, and _compose_train's `git merge --abort` must still
    # run — an escaping UnicodeDecodeError would leave the worktree UU-conflicted
    # and crash the unattended loop.
    bad = b"[generated]\nPROJECT_STATE.html = trajectory \x93smart\x94\n"
    repo = _generated_conflict_repo(
        tmp_path, "cp1252", "PROJECT_STATE.html", None, stack_bytes=bad
    )
    detail = _compose_theirs(repo)
    assert detail and "unreadable" in detail, "a non-UTF-8 stack.ini parks (no crash)"
    unmerged = _git(repo, "diff", "--name-only", "--diff-filter=U")
    assert unmerged == "", "the merge --abort ran: the worktree is conflict-free"


# --- WI-287: the integrator's spec close-ritual at done-flip --------------------
def test_wi287_archive_closed_specs_moves_live_spec_and_skips_the_rest(tmp_path):
    """A `docs/specs/<file>.md` SpecRef is git-mv'd to docs/archive/specs/
    <stem>.<date>.md; an empty SpecRef, a non-docs/specs anchor, and an
    already-absent file are all skipped (the ritual only archives a real live
    spec). Mirrors the WI-275 (spec file) vs WI-279 (repo-review anchor) live case."""
    repo = tmp_path / "repo"
    (repo / "docs" / "specs").mkdir(parents=True)
    (repo / "docs" / "requirements").mkdir(parents=True)
    (repo / "docs" / "specs" / "WI-900.md").write_text("# spec\n", encoding="utf-8")
    with open(
        str(repo / "docs" / "requirements" / "work-items.csv"),
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerow(_wi_row("WI-900", status="done"))  # SpecRef docs/specs/thing.md
        w.writerow(_wi_row("WI-901", status="done"))
        w.writerow(_wi_row("WI-902", status="done"))
    # Point each SpecRef deliberately: a real spec file, a review anchor, empty.
    reg = repo / "docs" / "requirements" / "work-items.csv"
    rows = list(csv.reader(reg.open(newline="", encoding="utf-8")))
    si = HEADER.index("SpecRef")
    for r in rows[1:]:
        if r[0] == "WI-900":
            r[si] = "docs/specs/WI-900.md"
        elif r[0] == "WI-901":
            r[si] = "docs/repo-review-2026-07-22.md#m-4-some-anchor"
        elif r[0] == "WI-902":
            r[si] = ""
    with reg.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")

    specrefs = agent_dispatch._wi_specrefs(reg, {"WI-900", "WI-901", "WI-902"})
    assert specrefs["WI-900"] == "docs/specs/WI-900.md"
    assert specrefs["WI-901"].startswith("docs/repo-review")
    assert specrefs["WI-902"] == ""

    moved = agent_dispatch._archive_closed_specs(repo, specrefs, "2026-07-23")
    # Only the real live spec moved; the anchor + the empty ref are no-ops.
    assert moved == [
        ("docs/specs/WI-900.md", "docs/archive/specs/WI-900.2026-07-23.md")
    ]
    assert not (repo / "docs" / "specs" / "WI-900.md").exists()
    assert (repo / "docs" / "archive" / "specs" / "WI-900.2026-07-23.md").is_file()


def test_wi288_archival_relinks_inbound_links_from_every_depth(tmp_path):
    """WI-288: archival must redirect inbound markdown links, or it strands a
    dangling link — the live 2026-07-24 failure, where a train's own docs/log.md
    entry linked the spec it was closing and the break only showed up on the
    composed tree as a red check_docs.

    Resolution is by resolved PATH, so all three depths are covered by one rule,
    and each replacement is re-relativised to its own file's directory.
    """
    repo = tmp_path / "repo"
    (repo / "docs" / "specs").mkdir(parents=True)
    (repo / "docs" / "reviews").mkdir(parents=True)
    (repo / "docs" / "specs" / "WI-900.md").write_text("# spec\n", encoding="utf-8")
    # the live case: the train's own log entry links its still-live spec
    (repo / "docs" / "log.md").write_text(
        "WI-900 landed, spec [WI-900](specs/WI-900.md) refers.\n"
        "With a fragment too: [anchor](specs/WI-900.md#done-when).\n",
        encoding="utf-8",
    )
    (repo / "docs" / "reviews" / "001-REVIEW-A.md").write_text(
        "Judged against [the spec](../specs/WI-900.md).\n", encoding="utf-8"
    )
    (repo / "README.md").write_text(
        "Root link: [spec](docs/specs/WI-900.md)\n"
        "Untouched: [ext](https://example.com/specs/WI-900.md) [frag](#specs)\n",
        encoding="utf-8",
    )
    moved = agent_dispatch._archive_closed_specs(
        repo, {"WI-900": "docs/specs/WI-900.md"}, "2026-07-23"
    )
    assert moved == [
        ("docs/specs/WI-900.md", "docs/archive/specs/WI-900.2026-07-23.md")
    ]

    log = (repo / "docs" / "log.md").read_text(encoding="utf-8")
    # link TEXT preserved, only the TARGET redirected (the repo convention)
    assert "[WI-900](archive/specs/WI-900.2026-07-23.md)" in log
    assert "[anchor](archive/specs/WI-900.2026-07-23.md#done-when)" in log
    # one level deeper: re-relativised, not copied verbatim
    review = (repo / "docs" / "reviews" / "001-REVIEW-A.md").read_text(encoding="utf-8")
    assert "[the spec](../archive/specs/WI-900.2026-07-23.md)" in review
    # from the repo root the target keeps its docs/ prefix
    readme = (repo / "README.md").read_text(encoding="utf-8")
    assert "[spec](docs/archive/specs/WI-900.2026-07-23.md)" in readme
    # an external URL that merely *contains* the path, and a bare fragment, are
    # left exactly alone
    assert "[ext](https://example.com/specs/WI-900.md)" in readme
    assert "[frag](#specs)" in readme


def test_wi288_relink_preserves_crlf_and_skips_unrelated_files(tmp_path):
    """The rewrite must not convert a CRLF checkout to LF (WI-234 splice
    discipline), and a file with no matching link must not be rewritten at all."""
    repo = tmp_path / "repo"
    (repo / "docs" / "specs").mkdir(parents=True)
    (repo / "docs" / "specs" / "WI-900.md").write_text("# spec\n", encoding="utf-8")
    crlf = repo / "docs" / "crlf.md"
    with crlf.open("w", encoding="utf-8", newline="") as fh:
        fh.write("line one\r\nsee [s](specs/WI-900.md)\r\n")
    other = repo / "docs" / "other.md"
    with other.open("w", encoding="utf-8", newline="") as fh:
        fh.write("nothing here\r\nlinks [x](other.md)\r\n")
    before = other.read_bytes()

    touched = agent_dispatch._relink_archived_specs(
        repo, [("docs/specs/WI-900.md", "docs/archive/specs/WI-900.2026-07-23.md")]
    )
    assert touched == ["docs/crlf.md"]  # only the file that actually linked it
    raw = crlf.read_bytes()
    assert b"[s](archive/specs/WI-900.2026-07-23.md)" in raw
    # every newline is still CRLF: strip the CRLFs and no bare LF may remain
    assert b"\r\n" in raw and b"\n" not in raw.replace(b"\r\n", b"")
    assert other.read_bytes() == before  # byte-identical, not rewritten


def test_wi287_done_flip_update_clears_specref(tmp_path):
    """The done-flip update dict carries SpecRef='' so a terminal WI clears its
    SpecRef in the same surgical rewrite (the cell half of the ritual)."""
    reg = tmp_path / "work-items.csv"
    with reg.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerow(_wi_row("WI-900", status="queued"))  # SpecRef docs/specs/thing.md
    agent_dispatch._rewrite_wi_rows(
        reg, {"WI-900": {"Status": "done", "Deliverable": "d", "SpecRef": ""}}
    )
    row = next(r for r in csv.DictReader(reg.open(newline="", encoding="utf-8")))
    assert row["Status"] == "done"
    assert row["SpecRef"] == ""
