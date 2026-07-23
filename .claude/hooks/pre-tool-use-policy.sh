#!/usr/bin/env bash
set -uo pipefail
set -f  # トークン分割時の glob 展開を無効化

# Agent-side push policy: agent の通常操作に対する防御層(完全なセキュリティ境界ではない)。
# ブロック: force push 全般 / main 宛の通常 push / --all / --mirror / 宛先不明の bare push。
# 許可: main 以外への非 force の明示 refspec push(feature branch・tag 等)。
# 既知の残余制約(D-008 の範囲内として許容):
# - eval・command substitution 等の間接実行は検出しない
# - 引用文字列の内容は解釈しない。commit メッセージ本文が push コマンド全文を含む場合は
#   過剰ブロック(fail-closed)になりうる
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

# "git push" 以降の引数列(トークン)を検査する
check_push_args() {
  local remote="" refspecs="" tok dest

  for tok in "$@"; do
    case "$tok" in
      --force|--force-with-lease|--force-with-lease=*|-f)
        block "force push is not allowed."
        ;;
      --all)
        block "push --all is not allowed."
        ;;
      --mirror)
        block "push --mirror is not allowed."
        ;;
      +*)
        block "forced refspec is not allowed."
        ;;
      -*)
        continue
        ;;
      *)
        if [[ -z "$remote" ]]; then
          remote="$tok"
        else
          refspecs="$refspecs $tok"
        fi
        ;;
    esac
  done

  if [[ -z "$refspecs" ]]; then
    block "bare 'git push' without an explicit refspec is not allowed (destination unknown)."
  fi

  # 2つ目以降の refspec も含め、宛先が main のものを全て検査する
  for tok in $refspecs; do
    dest="${tok##*:}"
    if [[ "$dest" == "main" || "$dest" == "refs/heads/main" ]]; then
      block "push to main is not allowed (use a feature branch + PR)."
    fi
  done
}

# サブコマンド1つ分を検査する。"git [global options] push" を認識する。
analyze_fragment() {
  local -a toks
  # shellcheck disable=SC2206
  toks=($1)
  local n=${#toks[@]} i=0 j t

  while (( i < n )); do
    if [[ "${toks[i]}" == "git" ]]; then
      j=$((i + 1))
      # push サブコマンドの前に置ける git の global option を読み飛ばす
      while (( j < n )); do
        t="${toks[j]}"
        case "$t" in
          -C|-c|--git-dir|--work-tree|--namespace|--exec-path)
            j=$((j + 2))  # 値を別トークンで取るオプション
            ;;
          -*)
            j=$((j + 1))
            ;;
          *)
            break
            ;;
        esac
      done
      if (( j < n )) && [[ "${toks[j]}" == "push" ]]; then
        check_push_args "${toks[@]:j+1}"
      fi
      i=$((j + 1))
    else
      i=$((i + 1))
    fi
  done
}

if [[ "$cmd" == *git* ]]; then
  # 行継続(バックスラッシュ+改行)を結合してから、改行・; ・| ・& でサブコマンドに
  # 分割し、git を含むサブコマンドだけを検査する。commit メッセージ等の本文行が
  # push 引数の解析に混入しないようにするため。
  normalized="${cmd//\\$'\n'/ }"
  while IFS= read -r sub; do
    [[ "$sub" == *git* ]] || continue
    analyze_fragment "$sub"
  done < <(printf '%s\n' "$normalized" | tr ';|&' '\n')
fi

exit 0
