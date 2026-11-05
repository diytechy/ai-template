"""Reproduce the numbers cited in this review's README (stdlib only).

Run from the repository root: `python docs/reviews/rolling-review-2026-11-05/measure.py`.
Each block prints one labelled line so the README's figures can be re-derived
after a change rather than trusted.
"""

import ast
import collections
import io
import pathlib
import re
import tokenize
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "project-trajectory" / "scripts"
TESTS = ROOT / "tests"

STATION = (
    "agent_ session_ dispatch integrate intake handback schedule coordinator_ "
    "adjudicat amendment_brief review_brief rejudge consolidate plan_ hats "
    "held_status acceptance_record bookkeeping trunk_step score_reviews lane "
    "claude_transcripts codex_call usage_ingest subagent_gate prompts dual_plan "
    "overnight blackout accounts text_then_act baseline_snapshot spine_carrier "
    "id_carrier migrate_carrier spec_move wi_convert retire record_observation "
    "decision adoption_record gen_verdict_rollup"
).split()
META_TESTS = (
    "smoke_tier conftest_isolation module_size_ratchet dogfood_sync dogfood_widening "
    "rule_sync rule_sync_driven generated_freshness_census generated_freshness_wiring "
    "commit_floor_census hooks_on_census hooks_on_routes kit_path_invariant "
    "import_layers dashboard_size_budget complexity_ratchet dependency_ledger "
    "check_dupes_census shipped_tier ci_tier_declaration smoke_budget smoke_budget_meter "
    "cpu_cap wi_loader_sync status_vocabulary_contract generated_newlines generated_set "
    "csv_header kitlib_spec_listing meta_repo_hook shell_portability launcher_interpreter "
    "env_gates test_evidence"
).split()


def rows(path, table=None):
    """Rows of one registry; `table` names the tier's own TOML table (need,
    requirement, design, test) so a sibling table in the same file (the
    stakeholders beside the needs) is not counted as a row of the tier."""
    data = tomllib.load(open(path, "rb"))
    out = []
    for name, value in data.items():
        if table and name != table:
            continue
        if isinstance(value, dict):
            for rid, row in value.items():
                if isinstance(row, dict) and re.match(r"^[A-Z]+-\d+$", rid):
                    out.append((rid, row))
    return out


def code_and_doc_lines(path):
    src = path.read_text(encoding="utf-8")
    doc, code = set(), set()
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        span = range(tok.start[0], tok.end[0] + 1)
        if tok.type == tokenize.COMMENT or (
            tok.type == tokenize.STRING
            and tok.line.strip().startswith(('"""', "'''", 'r"""'))
        ):
            doc.update(span)
        elif tok.type not in (
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.ENCODING,
            tokenize.ENDMARKER,
        ):
            code.update(span)
    return len(code - doc), len(doc)


def main():
    py = sorted(SCRIPTS.rglob("*.py"))
    code = doc = station = 0
    defs = collections.defaultdict(list)
    for p in py:
        c, d = code_and_doc_lines(p)
        code += c
        doc += d
        if any(p.stem.startswith(s) for s in STATION):
            station += c + d
        for node in ast.parse(p.read_text(encoding="utf-8")).body:
            if isinstance(node, ast.FunctionDef) and node.name != "main":
                defs[node.name].append(p.name)
    print(
        f"scripts: {len(py)} files, {code} code lines, {doc} comment/docstring lines (ratio {doc / code:.2f})"
    )
    print(f"unattended-station share: {station} lines")
    print(
        f"function names defined in >1 module: {sum(1 for v in defs.values() if len(v) > 1)}"
    )
    wi = sum(len(re.findall(r"WI-\d+", p.read_text(encoding="utf-8"))) for p in py)
    print(f"WI-### citations in scripts: {wi}")

    tests = sorted(TESTS.glob("test_*.py"))
    print(
        f"tests: {len(tests)} modules, {sum(len(p.read_text(encoding='utf-8').splitlines()) for p in tests)} lines"
    )
    meta = sum(
        len((TESTS / f"test_{m}.py").read_text(encoding="utf-8").splitlines())
        for m in META_TESTS
        if (TESTS / f"test_{m}.py").exists()
    )
    print(f"meta-level test modules (suite/CI/layout as subject): {meta} lines")
    asserts = longstr = 0
    funcs = {}
    for p in tests:
        tree = ast.parse(p.read_text(encoding="utf-8"))
        funcs["tests/" + p.name] = {
            n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                asserts += 1
                if any(
                    isinstance(s, ast.Constant)
                    and isinstance(s.value, str)
                    and len(s.value) >= 40
                    for s in ast.walk(node.test)
                ):
                    longstr += 1
    print(f"asserts: {asserts}; asserting a >=40-char string literal: {longstr}")

    sn = rows(ROOT / "docs/requirements/stakeholder-needs.toml", "need")
    stk = rows(ROOT / "docs/requirements/stakeholder-needs.toml", "stakeholder")
    sr = rows(ROOT / "docs/requirements/system-requirements.toml", "requirement")
    llr = rows(ROOT / "docs/requirements/low-level-requirements.toml", "design")
    tc = rows(ROOT / "docs/test/test-cases.toml", "test")
    # The first pass's broad regex (counts ALLCAPS English such as TOML/HEAD too);
    # the second pass adds the stricter proxies the §12 verification settled on.
    ident = re.compile(r"\b[a-z]+_[a-z_]+\(?|\b[A-Z][A-Z_]{3,}\b|\.py\b")
    call_or_py = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\(|\.py\b")
    snake_call_py = re.compile(r"\b[a-z]+_[a-z_]+\b|\b[A-Za-z_][A-Za-z0-9_]*\(|\.py\b")

    def repeats_own_symbol(r):
        toks = [t for t in re.split(r"[,;/ ]+", str(r.get("code_symbol", ""))) if len(t) > 2]
        toks.append(pathlib.Path(str(r.get("module", "")).split(";")[0]).stem)
        detail = str(r.get("detail", ""))
        return any(re.search(r"\b" + re.escape(t) + r"\b", detail) for t in toks if t)

    print(f"SN {len(sn)} (+{len(stk)} STK) SR {len(sr)} LLR {len(llr)} TC {len(tc)}")
    details = [str(r.get("detail", "")) for _, r in llr]
    print(
        f"LLR detail with code identifiers (broad regex): {sum(1 for d in details if ident.search(d))}; "
        f"call syntax or .py: {sum(1 for d in details if call_or_py.search(d))}; "
        f"snake_case|call|.py: {sum(1 for d in details if snake_call_py.search(d))}; "
        f"repeating own module/code_symbol token: {sum(1 for _, r in llr if repeats_own_symbol(r))}; "
        f">600 chars: {sum(1 for d in details if len(d) > 600)}; >1500 chars: {sum(1 for d in details if len(d) > 1500)}"
    )
    expected = [str(r.get("expected", "")) for _, r in tc]
    print(
        f"TC expected opening 'Satisfies (SR|the)': {sum(1 for e in expected if re.match(r'Satisfies (SR|the)', e))}; "
        f"opening 'Satisfies': {sum(1 for e in expected if e.startswith('Satisfies'))}; "
        f"pointer with <=3 words beyond it (strictly vacuous): {sum(1 for e in expected if e.startswith('Satisfies') and len(re.sub(r'^Satisfies[^:.]*', '', e).split()) <= 3)}"
    )
    methods = [str(r.get("method", "")) for _, r in tc]
    print(
        f"TC method median chars: {sorted(len(m) for m in methods)[len(methods) // 2]}; max: {max(len(m) for m in methods)}; >300: {sum(1 for m in methods if len(m) > 300)}"
    )
    node_refs = dead = 0
    for rid, r in tc:
        for ref in re.split(r"[;\s]+", str(r.get("evidence", ""))):
            f, _, node = ref.partition("::")
            if node and f in funcs:
                node_refs += 1
                dead += node.split("[")[0] not in funcs[f]
    print(
        f"TC evidence node ids: {node_refs}; pointing at missing test functions: {dead}"
    )
    coord = re.compile(
        r"loop|lane|coordinator|adjudicat|sitting|dispatch|merge slot|trunk|session|verdict|brief|review round|worker|handback|claim",
        re.I,
    )
    print(
        f"SR rows about the station/coordination layer: {sum(1 for _, r in sr if coord.search(str(r.get('title', '')) + str(r.get('requirement', ''))))}"
    )


if __name__ == "__main__":
    main()
