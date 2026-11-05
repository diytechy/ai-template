#!/bin/bash
# usage: t.sh <logfile> <cmd...>  -- runs cmd, tees to logfile, prints exit + wall seconds
log="$1"; shift
start=$(date +%s.%N)
"$@" > "$log" 2>&1
rc=$?
end=$(date +%s.%N)
printf 'exit=%s wall=%.2fs lines=%s log=%s\n' "$rc" "$(echo "$end - $start" | bc)" "$(wc -l < "$log")" "$log"
exit $rc
