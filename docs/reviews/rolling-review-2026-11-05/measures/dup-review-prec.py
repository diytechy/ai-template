import sys
sys.path.insert(0, "/home/user/ai-template/project-trajectory/scripts")
import agent_policy
from kitlib import done_when as dw
branch = "wi-397-x"
# the folder order spec_at() builds (copied from kitlib/done_when.py:455-463)
folders = ["{}/{}".format(dw._ACTIVE, branch)] + ["{}/{}".format(h, s) for s in dw._CLOSED for h in dw._HOMES]
print("done_when.spec_at folder order (highest index wins via max(hits)):")
for i, f in enumerate(folders): print("  ", i, f)
cands = ["docs/archive/work/complete/WI-397-x.md", "docs/work/complete/WI-397-x.md"]
hits = [(folders.index(p.rpartition("/")[0]), p) for p in cands]
print("done_when picks :", max(hits)[1])
print("agent_policy.authoritative_spec picks:", agent_policy.authoritative_spec(cands))
cands2 = ["docs/work/active/%s/WI-397-x.md" % branch, "docs/work/complete/WI-397-x.md"]
hits2 = [(folders.index(p.rpartition("/")[0]), p) for p in cands2]
print("active+complete -> done_when:", max(hits2)[1], "| authoritative_spec:", agent_policy.authoritative_spec(cands2))
