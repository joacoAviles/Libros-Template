#!/usr/bin/env bash
# Compiles staged cases; expected failures are evaluated later by qa.py.
set -euo pipefail
cd "$(dirname "$0")/.."
for tool in latexmk lualatex biber; do
  command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 2; }
done
{
  lualatex --version
  latexmk -v
  biber --version
  printf '\nSOURCE_DATE_EPOCH=%s\n' "${SOURCE_DATE_EPOCH:-unset}"
  uname -a
} > .build/environment.txt
compile_one() {
  local name="$1" directory="$2" result
  set +e
  (
    cd "$directory" || exit 2
    # Luaotfload writes font caches. Never share writable caches between jobs:
    # concurrent changes can keep latexmk dependencies from converging.
    # Relative, non-hidden paths also respect TeX openout_any=p.
    export TEXMFVAR="texmf-var"
    export TEXMFCONFIG="texmf-config"
    export TEXMFCACHE="texmf-cache"
    mkdir -p "$TEXMFVAR" "$TEXMFCONFIG" "$TEXMFCACHE"
    latexmk -lualatex -interaction=nonstopmode -halt-on-error -file-line-error -no-shell-escape main.tex
  ) > "$directory/compile.txt" 2>&1
  result=$?
  set -e
  printf '%s\n' "$result" > "$directory/exit-code.txt"
  printf '%s ... %s\n' "$name" "$result"
  if ((result!=0)) && [[ "$name" != reject-* ]]; then
    printf '\n--- Unexpected compiler failure: %s ---\n' "$name"
    tail -n 60 "$directory/compile.txt"
    printf '\n--- End diagnostics: %s ---\n' "$name"
  fi
}
jobs="${AVIA_JOBS:-4}"
[[ "$jobs" =~ ^[1-8]$ ]] || { echo 'AVIA_JOBS must be 1..8' >&2; exit 2; }
active=0
while IFS=$'\t' read -r name directory; do
  compile_one "$name" "$directory" &
  active=$((active+1))
  if ((active>=jobs)); then wait; active=0; fi
done < .build/plan.tsv
wait
