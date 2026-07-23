#!/usr/bin/env bash
set -uo pipefail

# Agent-side push policy: agent の通常操作に対する防御層(完全なセキュリティ境界ではない)。
# ブロック: force push 全般 / main 宛の通常 push / --all / --mirror / 宛先不明の bare push。
# 許可: main 以外への非 force の明示 refspec push(feature branch・tag 等)。
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

check_push_segment() {
  # "git push" 直後から次のコマンド区切りまでの引数列を検査する
  local seg="$1"
  local remote="" refspec="" tok dest

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
}

if [[ "$cmd" =~ git[[:space:]]+push ]]; then
  # コマンドは複数行になりうる(commit メッセージの本文など)。改行・; ・| ・& で
  # サブコマンドに分割し、"git push" を含むサブコマンドだけを検査することで、
  # メッセージ本文の記号(+ など)を refspec と誤検知したり、push 行の解析が
  # メッセージ行のトークンでずれて main 宛 push を見逃したりしないようにする。
  while IFS= read -r sub; do
    [[ "$sub" =~ git[[:space:]]+push ]] || continue
    seg="$(printf '%s' "$sub" | sed -E 's/.*git[[:space:]]+push//')"
    check_push_segment "$seg"
  done < <(printf '%s\n' "$cmd" | tr ';|&' '\n')
fi

exit 0
