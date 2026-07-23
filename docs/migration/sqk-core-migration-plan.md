# v1 → sqk-core 移行計画（確定版 / GO）

## Context

`software-quality-knowledge-base`（v1）はガバナンス機構（`docs/agent-ecosystem` 18k行 + `provenance/` 13k行 + `scripts/` 18k行 + `tests/` 8k行 ≒ 57k行）が知識成果物本体（domain canon 10.3k行 + skills/schemas/knowledge 4k行）の約4倍に膨張し、1変更あたりの修正コストが過大になった。価値の核を `repo-template` 起点の新リポジトリ **`sqk-core`**（public）へ移植し、最小ガバナンスで再出発する。移行完了後、ユーザー自身が v1 を削除する。

**Status: completed**（完了記録は文末を参照）。実行は 1タスク=1PR=1セッション、merge 判断は人間。Task 0・1 は preflight/external setup（例外として PR なし、または setup PR のみ）。

**スレッド分割と計画の収載**: Task 0〜1（v1 凍結・リポジトリ/フォルダ作成・実行基盤の導入）は本スレッドで実行し、Task 1 の setup PR で本計画を **`docs/migration/sqk-core-migration-plan.md`** として sqk-core にコミットする。**Task 2 以降は sqk-core 専用スレッドで、repo 収載版の計画を正として実行する**（`/execute-task docs/migration/sqk-core-migration-plan.md <Task-ID>` 形式で参照）。このため、`/execute-task` コマンド・hooks 等の実行基盤は Task 1 の setup PR に含める（Task 3 ではなく。repo-template には `.claude/commands/` も `.codex/prompts/` も存在しないため）。

- v1 HEAD: `ced0ccc495b45a37a446a20319674a6d2468262b`（open PR/Issue 0件、tree clean 確認済み）
- ローカル配置: v2 = `~/Dev/personal-projects/sqk-core`、バックアップ = `~/Dev/personal-projects/backups/sqk`
- 検証済み環境: gh（repo スコープ、SSH push）、uv 0.11.7、codex-cli 0.144.4、`sqk-core` 名は空き

## Global Constraints

- コンテンツ変更は全て PR 経由・merge は人間。auto-merge 無効化、Dependabot auto-merge workflow 削除（D-008）
- branch protection は v1 と同一: PR必須・承認0・`enforce_admins: false`・force push 禁止・branch 削除禁止
- v1 は Task 0 完了後 read-only
- pytest 固定コマンド（CI・Task 5 も同一）: `uv run --with pytest --with jsonschema --with pyyaml pytest tests/ -v`
- リポジトリ内文書に user-global パス（`~/` 配下）を書かない。bundle は Release URL + SHA-256 + bytes + source commit で記録。**例外**: `docs/migration/sqk-core-migration-plan.md` は移行期間限定の実行文書としてローカルパスの記載を許容し、Task 5 完了時に status: completed を付す（durable 文書 = README / MIGRATION / DECISIONS / ROADMAP には適用しない）
- 自動生成物をコミットする場合は generator + drift 検査を必須。手作業保守の curated derived artifact は canonical source refs と更新ルールを必須
- メタ文書量は警告指標（hard gate にしない）。多段ゲートは実需（複数人・外部 consumer・運用事故）が現れるまで導入しない

## 移植対象

**as-is 移植（manifest + SHA-256 検証）:**
- `docs/` domain canon 8ディレクトリ（exploratory-testing / governance-compliance / human-centered-quality / operations-quality / quality-management / quality-models / secure-development / test-techniques）
- `docs/_research/` 一式、`skills/` 一式（README + 7ユニット）、`knowledge/` 一式、`platforms/` 3 README
- `schemas/` の skill I/O 8件: handoff-envelope / detailed-test-condition / test-architecture-element / coverage-item / test-case / assurance-statement / risk-item / release-decision

**transform して移植（Task 1 の setup PR で導入）:**
- `.claude/commands/execute-task.md`・`.codex/prompts/execute-task.md`: v10 はコピーせず `git show 8a32d8d:...`（Claude 108行 / Codex 84行、G0言及ゼロ）を復元ベースに適合（後述の適合仕様）
- `.codex/hooks.json`: as-is 移植（`git rev-parse --show-toplevel` 起動のため repo-local で機能する。これがないと Codex 側で hook が起動しない）
- `.claude/hooks/`・`.codex/hooks/`: v2 で強化（main 宛の通常 push もブロック）+ `tests/test_hooks.py`

**transform して移植（Task 3 で実施）:**
- `docs/agent-ecosystem/` 7件（パス維持、冒頭に v2 status 注記: active×3 / historical×1 / final report×2 / backlog material×1）: skill-ecosystem-design-plan / knowledge-management-design / portability-design / phase1-implementation-guide / phase1-integration-trial-report / phase1b-coldstart-trial-report / phase2-implementation-guide（Execution freeze ブロックを superseded 注記へ差し替え）
- `schemas/README.md`: 8 I/O スキーマのみ掲載、provenance/G0 系記述を削除
- symlink 3本再作成: `.claude/skills -> ../skills`、`.agents/skills -> ../skills`、`CLAUDE.md -> AGENTS.md`

**`.gitignore` への追記（Task 1 の setup PR。negation 込みの正確な形）:**

```
knowledge/dynamic/*
!knowledge/dynamic/README.md
!knowledge/dynamic/_templates/
!knowledge/dynamic/_templates/**
.agent-work/
__pycache__/
*.pyc
.pytest_cache/
```

（`knowledge/dynamic/` 丸ごと指定は不可 — as-is 移植対象の README・_templates までignoreされる。v1 の .gitignore 43〜45行目と同趣旨 + `**` 行で堅牢化）

**drop（v2 へ持ち込まない）:**
- `docs/agent-ecosystem/` の上記7件以外（ADR×4 は要旨を DECISIONS.md へ、policy-0001、evolution-plan、review-evidence cycle18-47、fable-review×3、pr-02a×2、concept-clarification-plan、roadmap-status、risk-analysis.json、trace-links.json）
- `provenance/` 一式（機構を削除、能力=出典/derived_from/knowledge_refs/authority 区分は文書側+git 履歴で維持）
- `schemas/` ガバナンス系5件
- **v1 由来の `scripts/`・`tests/` はコピーしない**（v2 で新規作成する `scripts/check.py`・`tests/test_check.py`・`tests/test_hooks.py`・fixtures は保持する）
- template の `.github/workflows/dependabot-auto-merge.yml`（Task 1 で削除）

---

## Task 0: v1 凍結とバックアップ確定【preflight・PRなし】

1. 開始状態確認: `git fetch && git status` clean、HEAD == `ced0ccc495b45a37a446a20319674a6d2468262b`、open PR/Issue 0件
2. タグ: `git tag -a v1-final -m "v1 final state before migration to sqk-core (archive: sqk-core Release archive-sqkb-v1)"` → `git push origin v1-final` → `git ls-remote --tags origin | grep -F v1-final` で存在確認
3. bundle 2種を `~/Dev/personal-projects/backups/sqk/` に作成:
   - 公開用: `git bundle create ~/Dev/personal-projects/backups/sqk/sqk-v1-public.bundle main v1-final`
   - 保全用（38 local branch 含む・非公開）: `git bundle create ~/Dev/personal-projects/backups/sqk/sqk-v1-all-refs.bundle --all`
   - `shasum -a 256 ~/Dev/personal-projects/backups/sqk/*.bundle | tee ~/Dev/personal-projects/backups/sqk/SHA256SUMS`、`ls -l` で bytes 記録
4. 復元検証（両 bundle・必須）: `mktemp -d` へ clone → `git fsck --full` → `test "$(git rev-parse 'v1-final^{commit}')" = "ced0ccc495b45a37a446a20319674a6d2468262b"` 照合
5. PR/Issue/review/comment export（`M=~/Dev/personal-projects/backups/sqk/v1-github-metadata`、`R=rymetry/software-quality-knowledge-base`）:
   - `gh pr list --repo $R --state all --limit 100 --json number,title,body,author,state,createdAt,mergedAt,mergeCommit,baseRefName,headRefName,url > "$M/prs.json"`
   - `gh issue list --repo $R --state all --limit 100 --json number,title,body,author,state,createdAt,closedAt,url > "$M/issues.json"`
   - PR ごと（reviews / review-comments / issue-comments の3種）: `gh api --paginate --slurp "repos/$R/pulls/$n/reviews?per_page=100" | jq 'add' > "$M/pr-$n-reviews.json"`（他2種も同形式: `pulls/$n/comments`、`issues/$n/comments`）
   - 検証: `find "$M" -type f -name '*.json' -exec jq empty {} +`、`test "$(jq length "$M/prs.json")" -eq 34`
   - `tar -czf v1-github-metadata.tar.gz` で固定し SHA-256 + bytes を SHA256SUMS へ追記、展開して復元確認
6. 以後 v1 read-only を完了記録に明記

## Task 1: sqk-core 作成と監査済みセットアップ【setup PRのみ】

`setup-repo.sh` は無改変では実行しない（auto-merge 有効化・protection 後の直 push・Dependabot auto-merge が制約と矛盾）。

1. `gh repo create rymetry/sqk-core --template rymetry/repo-template --public --clone` → `~/Dev/personal-projects/sqk-core` へ配置
2. `gh repo edit`: projects/discussions/wiki OFF、delete-branch-on-merge ON、**auto-merge は有効化しない** → `.allow_auto_merge == false` readback
3. Actions 権限: `default_workflow_permissions=read`、`can_approve_pull_request_reviews=false`
4. branch protection PUT（v1 と同一 JSON: 承認0 / enforce_admins false / force push・削除禁止）→ readback 確認
5. setup PR（`setup/bootstrap` ブランチ、**Task 2 以降の実行基盤をここで導入**）→ 人間 merge:
   - LICENSE/SECURITY placeholder 置換 + `dependabot-auto-merge.yml` 削除
   - **本計画を `docs/migration/sqk-core-migration-plan.md` としてコミット**（Task 2〜5 は sqk-core 専用スレッドがこの repo 収載版を正として実行）
   - **適合済み execute-task**（Claude 版 `.claude/commands/execute-task.md` + Codex 版 `.codex/prompts/execute-task.md`。`git show 8a32d8d:...` を復元ベースに以下の適合仕様を適用、同一 PR で同期）
     - 状態保存先は repo-local `.agent-work/execute-task/`（ignored）。user-global パス言及ゼロ
     - G0/G1・Policy-0001・activation・provenance への依存をすべて除去
     - 1 task = 1 PR、feature branch のみ push、draft PR 作成、merge は人間
     - レビュー: 通常=独立レビュー1名。高影響変更（schema/後方互換、公開契約・Release、大規模移動・削除、移行・復元・削除ゲート）のみ追加1名。修正後の再確認は同一レビューの継続として扱う
     - 同一指摘が2巡残ったら自動続行せず停止し、owner が `simplify / defer / abandon` を判断
     - owner 判断の対象: scope 変更・重大/不可逆リスク・予算/timebox 超過・最終判定
     - raw review evidence は `.agent-work/` に置き、コミットしない（要旨のみ PR へ）
   - **強化済み hooks**（`.claude/hooks/`・`.codex/hooks/` 両方: force push 系 + main 宛通常 push + `--all`/`--mirror`/宛先不明 bare push をブロック、feature branch 明示 push は許可）
   - **`.codex/hooks.json`** を v1 から as-is 移植し、repo-local パス（`git rev-parse --show-toplevel` 起動）で機能することを確認
   - **`tests/test_hooks.py`**（回帰テスト: `origin main` / `HEAD:main` / `HEAD:refs/heads/main` / force 系 / `--all`・`--mirror`・bare → block、feature branch → allow、Claude/Codex 判定一致）
   - **`.gitignore` 追記**（上記 negation 込みブロック）

## Task 2: 検証入口 check.py【PR-V2-0a・移植より先】

Create: `scripts/check.py`（PEP 723、依存 jsonschema + PyYAML）、`tests/test_check.py` + fixtures、`.github/workflows/check.yml`

検査項目: (1) `.md` 相対リンク・アンカー解決、(2) `schemas/*.schema.json` の draft 2020-12 メタスキーマ検証、(3) `_research` 漏洩 — **対象は SKILL.md frontmatter の `knowledge_refs`・derived artifact の構造化 source refs・operational input 参照のみ**（README 等の境界説明言及は許可。正当言及 pass の fixture を含める）、(4) SKILL.md frontmatter の schema 参照・`knowledge_refs` 実在、(5) symlink target 実在

TDD: 失敗 fixtures → FAIL 確認 → 実装 → PASS → **Task 1 完了後の bootstrap 済み v2 に対し green** → CI（check.py + 固定 pytest コマンド）→ `test:`/`feat:` 分割コミット → PR

## Task 3: コンテンツ移植【PR-V2-0b・merge 条件 = check green】

1. ブランチ `migrate/content-from-v1`
2. keep manifest 作成（`git ls-files` で as-is 対象を列挙）+ SHA-256 採取 → **`MIGRATION-SOURCES.sha256` としてコミット**（path count・source commit は MIGRATION.md に記載）
3. manifest どおりコピー → `shasum -a 256 -c` 全件 OK（失敗1件でも停止）
4. agent-ecosystem 7件移植 + 各冒頭に `> **v2 status**: ...` 注記
5. phase2 ガイドの Execution freeze を superseded 注記へ差し替え（D-006 参照、v1 原文は Release `archive-sqkb-v1` 参照と記載）
6. 実行基盤（Task 1 で導入済み）と移植コンテンツの**整合確認**: execute-task・hooks・`.codex/hooks.json` が移植後のパス構成で機能すること、user-global パス言及ゼロ、`tests/test_hooks.py` green を再確認（導入は Task 1 で完了済み。ここでは移植コンテンツとの不整合があれば同 PR で修正）
7. symlink 3本再作成（`rm CLAUDE.md && ln -s AGENTS.md CLAUDE.md` 含む）、AGENTS.md 最小書き換え
8. `schemas/README.md` transform（8 I/O のみ掲載、provenance/G0 記述削除）
9. MIGRATION.md 作成: 経緯 / keep-transform-drop 一覧 / v1 履歴の所在（Release URL・SHA-256・bytes・source commit。**bundle 内部タグ `v1-final` ≠ Release タグ `archive-sqkb-v1` を明記**）/ authority 対応表 / metadata archive の扱い
10. リンク掃引（evolution-plan / policy-0001 / adr-000 / roadmap-status / provenance / validate-registry / g0-activation を grep）→ `uv run scripts/check.py` green まで修正 → PR（要判断項目は PR 説明に列挙）

## Task 4: 最小ガバナンス文書【PR-V2-1】

1. README.md 書き換え: コンセプト / レイヤーモデル（provenance 行→「文書内出典 + git 履歴 + DECISIONS.md」）/ 担う・担わないこと / 昇格ルール / veridia 関係 / ガードレール / **再発防止原則**（control file 0〜1件・2巡ルール・consumer なき仕組み禁止・governance 追加の根拠明示・メタ文書量は警告指標）
2. DECISIONS.md: D-001 再構築 / D-002 provenance 能力維持 / D-003 レビュー証跡 / D-004 生成物 / D-005 v1 ADR 要旨 superseded / D-006 freeze 失効 / D-007 Phase 2 再ベースライン / **D-008 auto-merge 無効化・hook は「agent の通常操作に対する防御層」（完全なセキュリティ境界ではない。admin の人間操作は運用規律）** / D-009 metadata archive 処置
3. ROADMAP.md: Phase 1 実績要約 + v2 順序（既知欠陥6件 → vertical slice → Phase 2 keep/merge/defer/drop 再評価 → 実装 → Phase 3 素材）。全て repo-local 記述
4. docs/README.md 書き換え（agent-ecosystem の位置づけ限定）
5. check green → PR

## Task 5: 移行完了ゲートと v1 削除【人間の最終操作を含む】

1. 完了チェック: check.py PASS / 固定 pytest PASS / symlink 3本 / `ls -d skills/*/ | wc -l` == 7 / schemas 8 / agent-ecosystem 7 / `.allow_auto_merge == false`
2. Release 作成: **`gh release create archive-sqkb-v1 ~/Dev/personal-projects/backups/sqk/sqk-v1-public.bundle --repo rymetry/sqk-core --latest=false`**（v2 に `v1-final` タグを作らない。notes に source commit / SHA-256 / bytes / 復元手順 / タグ名の違い）
3. **Release からの復旧検証（v1 削除の前提条件）**: `gh release download archive-sqkb-v1` → SHA-256 照合 → clone + `git fsck --full` → bundle 内 `test "$(git rev-parse 'v1-final^{commit}')" = "ced0ccc495b45a37a446a20319674a6d2468262b"` → **v2 remote も `mktemp -d` へ fresh clone して check + pytest green**。全 green を確認したら **`ready-for-v1-deletion` を `.agent-work/` とユーザーへの報告にのみ記録**（この時点で PR は作らない）
4. **ユーザー自身が** GitHub で v1 リポジトリを削除（agent は実行しない）。ローカル v1 working tree の削除もこの後
5. v1 削除後、`docs/migration/sqk-core-migration-plan.md` に **status: completed・削除日・確認結果**を追記する **PR を1本**作成（Task 5 の PR はこれのみ。「1タスク=1PR」と整合。completed 化は v1 削除の後）

## 検証（全体）

- Task 1 setup PR: CI は未導入のため**固定 pytest コマンドのローカル実行** + 人間レビュー
- Task 2 以降の各 PR: CI（check.py + 固定 pytest）green + 人間レビュー
- Task 0: bundle 2種の復元検証、export の jq 検証・件数一致（PR 34件）・tar SHA-256
- Task 1: hook 回帰テスト（`tests/test_hooks.py`）green（ローカル実行）、`.codex/hooks.json` の repo-local 起動確認
- Task 3: MIGRATION-SOURCES.sha256 全件一致、実行基盤との整合確認、check green
- Task 5: Release 再ダウンロード復旧検証 + v2 fresh clone 検証 → `ready-for-v1-deletion` → v1 削除（人間） → `completed` 化 PR

## 確定済み決定

public 維持 / 監査済み bundle のみ public（全 ref bundle・metadata は非公開でローカル保管、`~/Dev/personal-projects/backups/sqk` は通常バックアップ対象に含める）/ `docs/agent-ecosystem/` 名称維持 / auto-merge 無効化 / enforce_admins false / execute-task はリスク応分レビュー（通常1名+高影響+1名）

## 完了記録（status: completed）

- Task 0〜4: 完了（Task 2 = PR #2、Task 3 = PR #3、Task 4 = PR #4。各 merge は人間判断）
- Task 5 ステップ1〜3: 2026-07-23 完了
  - 完了チェック: `check.py` PASS（5項目 issues=0）/ 固定 pytest 52 passed / symlink 3本 / skills 7 / schemas 8 / agent-ecosystem 7 / `.allow_auto_merge == false`
  - Release `archive-sqkb-v1` 作成済み（`sqk-v1-public.bundle`、SHA-256 `6bc2c2e603038fbe1bf90931ba068bbcd002d0e8c9c003d44ceccf014d3b551c`、2,022,458 bytes、`--latest=false`。v2 に `v1-final` タグは作成していない）
  - 復旧検証: Release 再ダウンロード → SHA-256・bytes 一致 → bundle clone + `git fsck --full` OK → bundle 内 `v1-final^{commit}` == `ced0ccc495b45a37a446a20319674a6d2468262b` / v2 remote fresh clone で check + pytest green
- 削除前監査（追加実施）: GitHub 実体（main HEAD == `v1-final` == `ced0ccc4…`、`refs/pull/1-34/head` 全34 commit は all-refs bundle に収録済み）を確認のうえ、4観点の独立監査（as-is 完全性 67/67 byte-perfect / コンセプト・方針整合 / transform 忠実性 / drop 完全性 72件全て計画根拠あり）が全 PASS。Low 所見の追随修正は PR #5 で反映済み
- v1 リポジトリ（`rymetry/software-quality-knowledge-base`）削除: YYYY-MM-DD ユーザーにより実施（GitHub リポジトリ削除。ローカル working tree の削除は任意のタイミング）<!-- 削除実施後に日付を確定してから merge する。それまで本 PR は draft を維持 -->
