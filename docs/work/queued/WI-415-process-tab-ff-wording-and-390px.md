+++
id = "WI-415"
title = "Process-tab polish: the ff-wording one-string fix and the 390px legibility observation (WI-389 REVIEW-A findings 1-2, minted trunk-side at intake per the R3 invariant). FINDING 1, the one-string fix: the Trunk advance card's note reads 'ff trunk to the barred tree', which misstates the shipped act - trunk advances via the --no-ff merge commit itself (integrate.py's slot; a true ff is what the RULING-6 audit reds); the reviewer's replacement 'advance trunk to the barred tree' fits the 34-char note budget. One string in traj_panels' station panel + regen; the drawn picture must not contradict the code it derives from. FINDING 2, per the render-critique discipline (observations filed as their own WIs): at 390px the station's note lines render ~3.3 CSS px - illegible without pinch-zoom; no overflow or truncation, titles marginal, the esc list and svg title tooltips carry the content. JUDGE the fix honestly at the panel's design constraints (bigger notes at narrow widths, a two-line wrap, or dropping notes below a width threshold in favor of the tooltips) - verify by pixels per the skill matrix, and take the smallest change that makes the 390px render honest; recording a measured accept-with-tooltips is a legitimate outcome if every alternative damages the 1280/1680 reads. Scope: traj_panels station panel + its tests + pixel evidence."
workstream = "scripts"
specref = "docs/reviews/WI-389-REVIEW-A.md"
buildtier = "quick"
safety_class = "ordinary"
+++
