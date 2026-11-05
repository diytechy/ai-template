import sys
sys.path.insert(0, "/home/user/ai-template/project-trajectory/scripts")
import integrate, intake
print("tables equal today:", integrate._RETIRED_BARS == intake._RETIRED_WI_BARS)
print("integrate keys:", sorted(integrate._RETIRED_BARS)); print("intake keys   :", sorted(intake._RETIRED_WI_BARS))
for v in ("G1", "DevBar-Reqs", "devstg-impl", ""):
    print(repr(v), "integrate ->", repr(integrate._normalize_bar(v)), "| intake ->", repr(intake.normalize_bar(v)))
