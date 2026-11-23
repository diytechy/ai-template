# WI-1024: per-interface candidates (measured at bba30552f)

The population's first pass, one line per live interface, produced by the
plan's rule ([plan.md](plan.md) section 3) over the registries, the code's
back-links and the harvested contract bodies at `bba30552f`. A candidate is
a proposal: each is judged row by row in the build, and the judged table
replaces this one slice by slice.

Evidence tiers:

- **1**: a case naming it verifies the row, and the row's back-link sits in the file stating the contract.
- **2**: the function the interface names carries the row's back-link.
- **3**: a case naming it verifies the row (no back-link in the contract's file).
- **4**: the contract body cites the row.
- **5**: the one row back-linked in the contract's file.
- **6**: several rows back-linked in the contract's file: judged.
- **7**: no evidence: judged, or a new Drafted row.

| Interface | Owner | Channel | Cases naming it | Tier | Candidate rows |
|---|---|---|---|---|---|
| IF-001 | CMP-006 | stdout | 0 | 6 | judged among LLR-001, LLR-002, LLR-003, LLR-041, LLR-215, LLR-229 +12 |
| IF-002 | CMP-007 | exit-code | 0 | 4 | LLR-012 |
| IF-003 | CMP-007 | exit-code | 0 | 5 | LLR-013 |
| IF-004 | CMP-007 | stdout | 0 | 5 | LLR-014 |
| IF-005 | CMP-007 | stdout | 0 | 6 | judged among LLR-017, LLR-018, LLR-031 |
| IF-006 | CMP-007 | exit-code | 0 | 4 | LLR-016 |
| IF-008 | CMP-007 | stdout | 0 | 4 | LLR-038 |
| IF-009 | CMP-006 | exit-code | 0 | 6 | judged among LLR-034, LLR-075, LLR-077, LLR-084, LLR-097, LLR-160 +2 |
| IF-010 | CMP-006 | cli | 0 | 6 | judged among LLR-276, LLR-365, LLR-374, LLR-396, LLR-397, LLR-398 |
| IF-011 | CMP-009 | exit-code | 0 | 6 | judged among LLR-111, LLR-112, LLR-117, LLR-285, LLR-287 |
| IF-012 | CMP-009 | exit-code | 0 | 7 | judged |
| IF-013 | CMP-007 | exit-code | 0 | 6 | judged among LLR-006, LLR-007, LLR-008, LLR-141, LLR-242, LLR-246 +6 |
| IF-014 | CMP-009 | bytes | 0 | 6 | judged among LLR-010, LLR-011, LLR-121, LLR-156, LLR-275, LLR-279 +1 |
| IF-015 | CMP-008 | git | 0 | 6 | judged among LLR-028, LLR-045, LLR-061, LLR-132, LLR-174, LLR-175 +7 |
| IF-016 | CMP-007 | stdout | 0 | 5 | LLR-022 |
| IF-017 | CMP-009 | stdout | 0 | 4 | LLR-024 |
| IF-018 | CMP-009 | file | 1 | 1 | LLR-296 |
| IF-019 | CMP-009 | file | 0 | 6 | judged among LLR-025, LLR-043, LLR-281 |
| IF-020 | CMP-007 | exit-code | 0 | 5 | LLR-040 |
| IF-021 | CMP-006 | file | 0 | 7 | judged |
| IF-022 | CMP-007 | file | 1 | 3 | LLR-368 |
| IF-023 | CMP-006 | file | 0 | 7 | judged |
| IF-024 | CMP-006 | file | 0 | 7 | judged |
| IF-025 | CMP-006 | file | 0 | 7 | judged |
| IF-026 | CMP-006 | file | 0 | 7 | judged |
| IF-028 | CMP-006 | call | 0 | 6 | judged among LLR-276, LLR-365, LLR-374, LLR-396, LLR-397, LLR-398 |
| IF-029 | CMP-009 | file | 0 | 7 | judged; text names its file: LLR-013 |
| IF-030 | CMP-009 | file | 0 | 7 | judged |
| IF-031 | CMP-006 | file | 0 | 7 | judged |
| IF-032 | external:git | git | 0 | 6 | judged among LLR-017, LLR-018, LLR-031 |
| IF-033 | CMP-006 | file | 0 | 7 | judged |
| IF-034 | CMP-006 | file | 0 | 7 | judged |
| IF-035 | CMP-009 | file | 1 | 3 | LLR-279 |
| IF-036 | external:upstream docs | bytes | 0 | 5 | LLR-022 |
| IF-037 | CMP-008 | file | 1 | 3 | LLR-031 |
| IF-038 | CMP-008 | file | 0 | 7 | judged; text names its file: LLR-018, LLR-034, LLR-039, LLR-040 |
| IF-039 | CMP-009 | bytes | 0 | 7 | judged |
| IF-040 | CMP-007 | exit-code | 0 | 6 | judged among LLR-006, LLR-007, LLR-008, LLR-141, LLR-242, LLR-246 +6 |
| IF-041 | external:agent CLI | cli | 0 | 6 | judged among LLR-026, LLR-163 |
| IF-042 | CMP-006 | exit-code | 0 | 6 | judged among LLR-001, LLR-002, LLR-003, LLR-041, LLR-215, LLR-229 +12 |
| IF-043 | CMP-007 | exit-code | 0 | 6 | judged among LLR-017, LLR-018, LLR-031 |
| IF-045 | CMP-008 | file | 0 | 7 | judged; text names its file: LLR-044, LLR-176 |
| IF-046 | CMP-008 | call | 1 | 3 | LLR-313 |
| IF-047 | CMP-008 | file | 1 | 3 | LLR-313 |
| IF-048 | CMP-009 | stdout | 0 | 5 | LLR-047 |
| IF-049 | CMP-007 | file | 1 | 3 | LLR-370 |
| IF-050 | CMP-006 | file | 0 | 6 | judged among LLR-148, LLR-230 |
| IF-051 | CMP-006 | file | 0 | 7 | judged |
| IF-054 | CMP-006 | file | 2 | 3 | LLR-288, LLR-299 |
| IF-056 | CMP-006 | call | 0 | 2 | LLR-034 |
| IF-057 | CMP-006 | file | 0 | 7 | judged; text names its file: LLR-199 |
| IF-059 | CMP-006 | file | 0 | 7 | judged |
| IF-060 | CMP-006 | exit-code | 0 | 5 | LLR-069 |
| IF-068 | CMP-007 | file | 0 | 7 | judged; text names its file: LLR-007, LLR-014, LLR-038, LLR-047 |
| IF-069 | CMP-007 | exit-code | 0 | 4 | LLR-098 |
| IF-070 | CMP-007 | file | 0 | 7 | judged; text names its file: LLR-098 |
| IF-071 | CMP-008 | call | 0 | 2 | LLR-058, LLR-123, LLR-288 |
| IF-072 | CMP-007 | file | 0 | 7 | judged; text names its file: LLR-038, LLR-203, LLR-387 |
| IF-073 | CMP-006 | file | 4 | 3 | LLR-288, LLR-299, LLR-370 |
| IF-074 | CMP-009 | file | 0 | 6 | judged among LLR-118, LLR-271, LLR-283 |
| IF-075 | CMP-006 | call | 1 | 2 | LLR-240, LLR-271 |
| IF-077 | CMP-007 | call | 0 | 5 | LLR-012 |
| IF-078 | CMP-006 | call | 0 | 7 | judged |
| IF-079 | CMP-006 | file | 0 | 7 | judged |
| IF-080 | CMP-008 | exit-code | 1 | 1 | LLR-368 |
| IF-081 | CMP-008 | exit-code | 0 | 6 | judged among LLR-060, LLR-124, LLR-137, LLR-142 |
| IF-082 | CMP-006 | call | 0 | 6 | judged among LLR-034, LLR-075, LLR-077, LLR-084, LLR-097, LLR-160 +2 |
| IF-083 | CMP-006 | call | 0 | 6 | judged among LLR-034, LLR-075, LLR-077, LLR-084, LLR-097, LLR-160 +2 |
| IF-084 | CMP-006 | call | 0 | 6 | judged among LLR-034, LLR-075, LLR-077, LLR-084, LLR-097, LLR-160 +2 |
| IF-085 | CMP-008 | call | 0 | 6 | judged among LLR-058, LLR-059, LLR-089, LLR-123, LLR-131, LLR-152 +1 |
| IF-086 | CMP-007 | exit-code | 0 | 5 | LLR-146 |
| IF-088 | CMP-009 | call | 0 | 6 | judged among LLR-139, LLR-198, LLR-283, LLR-370 |
| IF-089 | CMP-006 | call | 0 | 6 | judged among LLR-001, LLR-002, LLR-003, LLR-041, LLR-215, LLR-229 +12 |
| IF-091 | CMP-006 | call | 5 | 1 | LLR-153, LLR-158, LLR-278, LLR-364 |
| IF-092 | CMP-006 | call | 1 | 3 | LLR-360 |
| IF-093 | CMP-008 | call | 1 | 3 | LLR-056 |
| IF-094 | CMP-008 | call | 1 | 3 | LLR-056 |
| IF-098 | CMP-008 | call | 0 | 2 | LLR-162 |
| IF-101 | CMP-006 | call | 3 | 1 | LLR-362, LLR-363 |
| IF-102 | CMP-006 | call | 0 | 2 | LLR-277 |
| IF-103 | CMP-006 | bytes | 0 | 6 | judged among LLR-222, LLR-407 |
| IF-104 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-105 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-106 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-107 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-108 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-109 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-110 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-111 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-112 | CMP-006 | call | 1 | 1 | LLR-277 |
| IF-114 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-115 | CMP-008 | call | 3 | 1 | LLR-295, LLR-308, LLR-310 |
| IF-118 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-119 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-120 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-121 | CMP-007 | exit-code | 0 | 5 | LLR-170 |
| IF-122 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-123 | CMP-006 | call | 1 | 2 | LLR-245, LLR-271 |
| IF-124 | CMP-006 | call | 1 | 3 | LLR-167 |
| IF-125 | CMP-006 | call | 0 | 2 | LLR-271 |
| IF-126 | CMP-006 | call | 1 | 1 | LLR-273 |
| IF-129 | CMP-006 | call | 2 | 1 | LLR-359 |
| IF-131 | CMP-006 | call | 1 | 1 | LLR-365 |
| IF-132 | CMP-006 | call | 0 | 6 | judged among LLR-276, LLR-365, LLR-374, LLR-396, LLR-397, LLR-398 |
| IF-133 | CMP-006 | call | 0 | 6 | judged among LLR-215, LLR-218, LLR-222, LLR-232, LLR-277, LLR-404 |
| IF-134 | CMP-007 | exit-code | 0 | 7 | judged; text names its file: LLR-021, LLR-043, LLR-122, LLR-158 |
| IF-135 | CMP-007 | exit-code | 0 | 7 | judged; text names its file: LLR-021 |
| IF-139 | CMP-009 | exit-code | 1 | 1 | LLR-199 |
| IF-140 | CMP-009 | file | 2 | 1 | LLR-199 |
| IF-141 | CMP-006 | call | 1 | 3 | LLR-199 |
| IF-142 | CMP-006 | call | 1 | 3 | LLR-199 |
| IF-144 | CMP-007 | exit-code | 0 | 6 | judged among LLR-006, LLR-007, LLR-008, LLR-141, LLR-242, LLR-246 +6 |
| IF-145 | CMP-006 | exit-code | 0 | 6 | judged among LLR-001, LLR-002, LLR-003, LLR-041, LLR-215, LLR-229 +12 |
| IF-146 | CMP-006 | file | 0 | 6 | judged among LLR-001, LLR-002, LLR-003, LLR-041, LLR-215, LLR-229 +12 |
| IF-147 | CMP-007 | exit-code | 0 | 5 | LLR-014 |
| IF-148 | CMP-007 | exit-code | 0 | 6 | judged among LLR-017, LLR-018, LLR-031 |
| IF-149 | CMP-009 | file | 0 | 7 | judged |
| IF-150 | CMP-006 | exit-code | 0 | 6 | judged among LLR-276, LLR-365, LLR-374, LLR-396, LLR-397, LLR-398 |
| IF-151 | CMP-007 | cli | 0 | 5 | LLR-040 |
| IF-152 | CMP-006 | cli | 0 | 5 | LLR-069 |
| IF-153 | CMP-006 | file | 0 | 5 | LLR-069 |
| IF-154 | CMP-008 | cli | 2 | 1 | LLR-207, LLR-368 |
| IF-155 | CMP-008 | cli | 0 | 6 | judged among LLR-060, LLR-124, LLR-137, LLR-142 |
| IF-156 | CMP-008 | file | 0 | 7 | judged |
| IF-157 | CMP-009 | cli | 1 | 1 | LLR-047 |
| IF-158 | CMP-009 | exit-code | 1 | 1 | LLR-047 |
| IF-159 | CMP-006 | file | 0 | 7 | judged |
| IF-160 | CMP-008 | file | 0 | 5 | LLR-046 |
| IF-161 | CMP-006 | file | 0 | 7 | judged |
| IF-162 | CMP-008 | file | 0 | 7 | judged; text names its file: LLR-044 |
| IF-163 | CMP-008 | file | 0 | 7 | judged; text names its file: LLR-026, LLR-056, LLR-061, LLR-075 |
| IF-164 | CMP-009 | file | 1 | 3 | LLR-288 |
| IF-165 | CMP-006 | exit-code | 0 | 6 | judged among LLR-148, LLR-230 |
| IF-166 | CMP-006 | file | 0 | 6 | judged among LLR-001, LLR-002, LLR-003, LLR-041, LLR-215, LLR-229 +12 |
| IF-167 | CMP-007 | file | 0 | 5 | LLR-014 |
| IF-168 | CMP-008 | file | 0 | 7 | judged |
| IF-169 | CMP-007 | stdout | 0 | 5 | LLR-040 |
| IF-170 | CMP-007 | file | 0 | 5 | LLR-040 |
| IF-171 | CMP-008 | cli | 0 | 6 | judged among LLR-058, LLR-059, LLR-089, LLR-123, LLR-131, LLR-152 +1 |
| IF-172 | CMP-008 | stdout | 0 | 6 | judged among LLR-058, LLR-059, LLR-089, LLR-123, LLR-131, LLR-152 +1 |
| IF-175 | CMP-008 | call | 1 | 1 | LLR-207, LLR-262 |
| IF-176 | CMP-006 | call | 1 | 3 | LLR-058 |
| IF-177 | CMP-006 | call | 1 | 2 | LLR-160 |
| IF-178 | CMP-006 | call | 1 | 3 | LLR-210 |
| IF-179 | CMP-008 | call | 1 | 3 | LLR-339 |
| IF-180 | CMP-006 | call | 1 | 1 | LLR-213 |
| IF-186 | CMP-008 | call | 1 | 1 | LLR-151 |
| IF-187 | CMP-007 | exit-code | 1 | 1 | LLR-256 |
| IF-188 | CMP-007 | call | 1 | 3 | LLR-256 |
| IF-189 | CMP-008 | call | 2 | 1 | LLR-339 |
| IF-190 | CMP-006 | call | 1 | 1 | LLR-219 |
| IF-194 | CMP-008 | call | 1 | 1 | LLR-247, LLR-248 |
| IF-195 | CMP-006 | call | 1 | 1 | LLR-249 |
| IF-196 | CMP-006 | call | 2 | 1 | LLR-246, LLR-249 |
| IF-197 | CMP-007 | exit-code | 1 | 3 | LLR-247, LLR-248 |
| IF-198 | CMP-007 | exit-code | 1 | 1 | LLR-257 |
| IF-199 | CMP-006 | call | 1 | 3 | LLR-257 |
| IF-200 | CMP-006 | call | 1 | 1 | LLR-233 |
| IF-201 | CMP-006 | call | 2 | 2 | LLR-223 |
| IF-208 | CMP-006 | call | 2 | 1 | LLR-250, LLR-252 |
| IF-214 | CMP-006 | file | 1 | 1 | LLR-234 |
| IF-215 | CMP-006 | cli | 1 | 1 | LLR-235 |
| IF-216 | CMP-006 | call | 1 | 1 | LLR-243 |
| IF-217 | CMP-006 | call | 1 | 1 | LLR-239 |
| IF-220 | CMP-006 | file | 2 | 1 | LLR-239, LLR-361 |
| IF-224 | CMP-008 | call | 2 | 2 | LLR-061, LLR-339 |
| IF-226 | CMP-006 | call | 1 | 1 | LLR-240 |
| IF-227 | CMP-009 | call | 1 | 1 | LLR-258 |
| IF-228 | CMP-008 | call | 1 | 1 | LLR-254 |
| IF-229 | CMP-008 | cli | 1 | 1 | LLR-255 |
| IF-230 | CMP-007 | exit-code | 1 | 1 | LLR-242 |
| IF-231 | CMP-006 | call | 1 | 1 | LLR-244 |
| IF-233 | CMP-006 | cli | 1 | 1 | LLR-263 |
| IF-239 | CMP-007 | call | 1 | 1 | LLR-261 |
| IF-240 | CMP-007 | cli | 1 | 1 | LLR-261 |
| IF-242 | CMP-008 | call | 2 | 1 | LLR-262 |
| IF-243 | CMP-008 | cli | 1 | 1 | LLR-264 |
| IF-244 | CMP-008 | cli | 1 | 1 | LLR-265 |
| IF-245 | CMP-008 | call | 4 | 1 | LLR-266, LLR-347, LLR-348, LLR-352, LLR-353 |
| IF-246 | CMP-008 | call | 7 | 1 | LLR-269, LLR-346 |
| IF-247 | CMP-008 | file | 4 | 1 | LLR-270, LLR-290 |
| IF-248 | CMP-008 | call | 5 | 1 | LLR-270, LLR-290 |
| IF-252 | CMP-006 | call | 1 | 1 | LLR-274 |
| IF-253 | CMP-008 | file | 1 | 3 | LLR-280 |
| IF-254 | CMP-009 | exit-code | 1 | 1 | LLR-281 |
| IF-255 | CMP-008 | file | 2 | 1 | LLR-303 |
| IF-256 | CMP-008 | call | 1 | 1 | LLR-283 |
| IF-257 | CMP-006 | file | 2 | 1 | LLR-286 |
| IF-258 | CMP-006 | cli | 1 | 1 | LLR-286 |
| IF-264 | CMP-008 | call | 1 | 1 | LLR-288 |
| IF-265 | CMP-006 | call | 1 | 3 | LLR-288 |
| IF-266 | CMP-008 | call | 1 | 1 | LLR-290 |
| IF-267 | CMP-007 | cli | 1 | 1 | LLR-291 |
| IF-269 | CMP-008 | call | 3 | 1 | LLR-293, LLR-294 |
| IF-270 | CMP-006 | call | 1 | 3 | LLR-024 |
| IF-271 | CMP-008 | call | 2 | 1 | LLR-300 |
| IF-272 | CMP-008 | call | 1 | 2 | LLR-270 |
| IF-273 | CMP-008 | call | 2 | 1 | LLR-270 |
| IF-274 | CMP-008 | cli | 3 | 1 | LLR-300 |
| IF-275 | CMP-008 | stdout | 3 | 1 | LLR-300 |
| IF-277 | external:agent CLI | env | 1 | 1 | LLR-300 |
| IF-278 | CMP-008 | env | 1 | 1 | LLR-301 |
| IF-279 | CMP-008 | cli | 1 | 1 | LLR-301 |
| IF-280 | CMP-008 | cli | 2 | 1 | LLR-301 |
| IF-281 | CMP-008 | exit-code | 2 | 1 | LLR-301 |
| IF-282 | CMP-008 | call | 4 | 1 | LLR-270, LLR-305 |
| IF-283 | CMP-008 | cli | 2 | 1 | LLR-306 |
| IF-284 | CMP-008 | exit-code | 1 | 1 | LLR-306 |
| IF-285 | CMP-008 | stdout | 2 | 1 | LLR-306 |
| IF-286 | CMP-008 | call | 3 | 1 | LLR-262, LLR-307 |
| IF-287 | CMP-008 | call | 3 | 1 | LLR-310, LLR-359 |
| IF-288 | CMP-008 | cli | 3 | 1 | LLR-313, LLR-341 |
| IF-289 | CMP-008 | exit-code | 2 | 1 | LLR-313, LLR-341 |
| IF-290 | CMP-008 | call | 1 | 1 | LLR-314 |
| IF-291 | CMP-008 | call | 1 | 1 | LLR-316 |
| IF-292 | CMP-009 | cli | 1 | 3 | LLR-047 |
| IF-293 | CMP-009 | exit-code | 1 | 3 | LLR-047 |
| IF-294 | CMP-008 | call | 1 | 1 | LLR-335 |
| IF-295 | CMP-008 | exit-code | 1 | 1 | LLR-337 |
| IF-296 | CMP-008 | call | 2 | 1 | LLR-338, LLR-359 |
| IF-297 | CMP-008 | call | 1 | 1 | LLR-340 |
| IF-298 | CMP-007 | stdout | 1 | 3 | LLR-021 |
| IF-303 | CMP-008 | call | 1 | 1 | LLR-345 |
| IF-304 | CMP-008 | exit-code | 1 | 1 | LLR-345 |
| IF-305 | CMP-008 | cli | 2 | 1 | LLR-353, LLR-355 |
| IF-306 | CMP-008 | stdout | 1 | 1 | LLR-353, LLR-355 |
| IF-307 | CMP-008 | exit-code | 1 | 1 | LLR-353, LLR-355 |
| IF-308 | CMP-006 | call | 1 | 1 | LLR-358 |
| IF-309 | CMP-008 | call | 1 | 1 | LLR-367 |
| IF-310 | CMP-006 | call | 1 | 2 | LLR-365 |
| IF-311 | CMP-006 | call | 1 | 3 | LLR-367 |
| IF-312 | CMP-006 | call | 1 | 1 | LLR-369 |
| IF-314 | CMP-006 | call | 1 | 3 | LLR-205 |
| IF-315 | CMP-006 | call | 1 | 1 | LLR-234 |
| IF-316 | CMP-006 | call | 2 | 1 | LLR-397 |
| IF-321 | CMP-008 | file | 1 | 1 | LLR-306 |
| IF-322 | CMP-008 | file | 1 | 1 | LLR-314 |
| IF-325 | CMP-006 | call | 1 | 3 | LLR-394 |
| IF-326 | CMP-008 | call | 1 | 2 | LLR-307 |
