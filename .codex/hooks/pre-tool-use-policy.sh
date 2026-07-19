#!/usr/bin/env bash
set -uo pipefail

# Agent-side push policy: agent の通常操作に対する防御層(完全なセキュリティ境界ではない)。
# ブロック: force push 全般 / main 宛の通常 push / --all / --mirror / 宛先不明の bare push。
# 許可: feature branch への明示 push。
# .claude/hooks と .codex/hooks の両コピーは同一内容を維持する(tests/test_hooks.py が検証)。

input="$(cat)"

cmd=""
if command -v jq >/dev/null 2>&1; then
  cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // .command // empty' 2>/dev/null || true)"
fi
if [[ -z "$cmd" ]]; then
  cmd="$input"
fi

block() {
  echo "Blocked: $1" >&2
  exit 2
}

if [[ "$cmd" =~ git[[:space:]]+push ]]; then
  # 最初の "git push" 以降をコマンド区切りまで切り出して解析する
  seg="$(printf '%s' "$cmd" | sed -E 's/.*git[[:space:]]+push//' | sed -E 's/[;|&].*$//')"

  if [[ "$seg" =~ (^|[[:space:]])--force(-with-lease)?(=[^[:space:]]*)?($|[[:space:]]) ]] ||
     [[ "$seg" =~ (^|[[:space:]])-f($|[[:space:]]) ]]; then
    block "force push is not allowed."
  fi
  if [[ "$seg" =~ (^|[[:space:]])--all($|[[:space:]]) ]]; then
    block "push --all is not allowed."
  fi
  if [[ "$seg" =~ (^|[[:space:]])--mirror($|[[:space:]]) ]]; then
    block "push --mirror is not allowed."
  fi

  remote=""
  refspec=""
  for tok in $seg; do
    case "$tok" in
      +*)
        block "forced refspec is not allowed."
        ;;
      -*)
        continue
        ;;
      *)
        if [[ -z "$remote" ]]; then
          remote="$tok"
        elif [[ -z "$refspec" ]]; then
          refspec="$tok"
        fi
        ;;
    esac
  done

  if [[ -z "$refspec" ]]; then
    block "bare 'git push' without an explicit refspec is not allowed (destination unknown)."
  fi

  dest="${refspec##*:}"
  if [[ "$dest" == "main" || "$dest" == "refs/heads/main" ]]; then
    block "push to main is not allowed (use a feature branch + PR)."
  fi
fi

exit 0
