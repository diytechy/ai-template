"""Per-module stats: tests, lines, run_py/subprocess counts, load_script, scaffold fixture use, bootstrap calls, git init, string-literal asserts."""
import ast, re, pathlib, csv, sys
root = pathlib.Path('/home/user/ai-template/tests')
rows = []
for p in sorted(root.glob('test_*.py')):
    src = p.read_text(encoding='utf-8', errors='replace')
    lines = src.splitlines()
    tree = ast.parse(src)
    tests = []
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'):
            tests.append(n)
    ntests = len(tests)
    # parametrize expansion estimate
    nparam = 0
    for t in tests:
        for d in t.decorator_list:
            if isinstance(d, ast.Call) and getattr(getattr(d.func, 'attr', None), '__str__', None) and getattr(d.func, 'attr', '') == 'parametrize':
                nparam += 1
    run_py = len(re.findall(r'\brun_py\(', src))
    subp = len(re.findall(r'subprocess\.(run|Popen|check_output|check_call|call)\(', src))
    load_script = len(re.findall(r'\bload_script\(', src))
    scaffold_fixture = sum(1 for t in tests if any(a.arg == 'scaffold' for a in t.args.args))
    bootstrap_calls = len(re.findall(r'bootstrap\.py|bootstrap\(|make_minimal_project\(', src))
    git_init = len(re.findall(r'git_init|"init"|\'init\'|trunk_repo\(|claimed_lane\(|fixture_git\(', src))
    # asserts comparing to a string literal >= 40 chars
    long_str_assert = 0
    any_str_assert = 0
    nassert = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert):
            nassert += 1
            found_long = False; found_any = False
            for c in ast.walk(n.test):
                if isinstance(c, ast.Constant) and isinstance(c.value, str):
                    if len(c.value) >= 40: found_long = True
                    if len(c.value) >= 12 and ' ' in c.value: found_any = True
            long_str_assert += found_long
            any_str_assert += found_any
    # tmp_path usage per test
    tmp_path_tests = sum(1 for t in tests if any(a.arg in ('tmp_path',) for a in t.args.args))
    module_fixtures = len(re.findall(r'@pytest\.fixture\(scope=["\'](module|session)["\']', src))
    func_fixtures = len(re.findall(r'@pytest\.fixture\b(?!\(scope)', src))
    rows.append(dict(module=p.stem, lines=len(lines), tests=ntests, parametrized=nparam, run_py=run_py, subprocess=subp,
                     load_script=load_script, scaffold_fixture_tests=scaffold_fixture, bootstrap_refs=bootstrap_calls,
                     git_fixture_refs=git_init, asserts=nassert, long_str_asserts=long_str_assert, phrase_asserts=any_str_assert,
                     tmp_path_tests=tmp_path_tests, module_scope_fixtures=module_fixtures, func_fixtures=func_fixtures))
w = csv.DictWriter(open(sys.argv[1], 'w', newline=''), fieldnames=list(rows[0].keys()))
w.writeheader(); w.writerows(rows)
tot = {k: sum(r[k] for r in rows) for k in rows[0] if k != 'module'}
print(tot)
