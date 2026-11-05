import xml.etree.ElementTree as ET, collections, csv, sys
cls = {r["module"]: r["class"] for r in csv.DictReader(open("classes.csv"))}
for name in sys.argv[1:]:
    t = ET.parse(name)
    per = collections.Counter(); cnt = collections.Counter()
    for tc in t.iter('testcase'):
        mod = tc.get('classname').split('.')[-1] if '.' in tc.get('classname') else tc.get('classname')
        # classname is like tests.test_x (module) or tests.test_x.TestCls
        parts = tc.get('classname').split('.')
        mod = [p for p in parts if p.startswith('test_')][0]
        per[mod] += float(tc.get('time')); cnt[mod] += 1
    tot = sum(per.values())
    print(f"== {name}: {sum(cnt.values())} tests in {len(per)} modules, per-test time sum {tot:.1f}s")
    bycls = collections.Counter(); ncls = collections.Counter()
    for m in per:
        bycls[cls.get(m, '?')] += per[m]; ncls[cls.get(m, '?')] += cnt[m]
    for k, v in bycls.most_common():
        print(f"   {k:9s} {v:7.1f}s ({100*v/tot:4.1f}%) {ncls[k]} tests")
    print("top 30 modules by summed test time:")
    for m, s in per.most_common(30):
        print(f"{s:7.1f}s {cnt[m]:4d} tests {s/cnt[m]*1000:6.0f} ms/test {cls.get(m,'?'):8s} {m}")
    print("modules under 1.0s total:", sum(1 for m in per if per[m] < 1.0), "of", len(per))
    with open(name.replace('.junit.xml', '.permodule.csv'), 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(["module", "tests", "seconds", "class"])
        for m, s in per.most_common(): w.writerow([m, cnt[m], f"{s:.2f}", cls.get(m, '?')])
