---
description: 計画文書の1タスク/ステージを、Codex実装者+Claude多角レビューのループで完遂する(実装=Codex CLI、管理・レビュー=Claude)
argument-hint: <plan-file> <task-or-stage-id>
---

# /execute-task — 計画タスク実行オーケストレーター

<!-- version: 5 (sqk-core適合版) — 対をなすCodex単体版(.codex/prompts/execute-task.md)と同時更新すること。正典はこのrepo収載版(ユーザーグローバル側には置かない) -->

あなた(Claude)は**管理者兼レビュー統括**である。実装はCodex CLI(実装者)へ委譲し、レビューはリスク応分の独立レビューで行う。「タスク/ステージごとの見出し+検証可能なexit criteria」を持つ任意の計画文書で動作する汎用コマンドだが、**信頼できる自作の計画文書にのみ使用する**こと(計画本文がそのまま実装指示になるため)。

引数: $ARGUMENTS(1つ目=計画ファイルパス、2つ目=タスク/ステージID。例: `docs/plan.md PR-02a-1`)。不足・曖昧な場合は実行せず使い方を示して停止する。

**owner(人間)判断の対象**: scope変更・重大/不可逆リスク・予算/timebox超過・最終判定(merge)。これら以外はこのコマンドの範囲で自律的に進める。

作業ディレクトリ: `.agent-work/execute-task/<タスクID>/`(repo-local・gitignored。セッションを跨いで保持される)。実装指示書(`brief.md`)・findings・進行状態(`progress.md`)をここに置き、**各Phase完了時に完了Phaseと要点をprogress.mdへ1行追記する**。同ディレクトリと作業branchが既に存在する場合は**再開モード**とし、brief.mdとprogress.mdと最新findingsを読んで記録済みのPhaseから続行する(その場合Phase 1のclean tree検証は「未commit差分が想定内か」の確認に読み替える)。

## Phase 0 — タスク抽出

1. 計画を読み、タスクIDに該当するセクションを特定する。**計画がnormative節とsuperseded/appendix等の非規範節を区別している場合はnormative節だけを対象とする**。見出しが複数一致する場合、または複合見出し(例:「PR-04 / PR-05」)から単一タスクを切り出す場合は、採用したセクションをユーザーに提示して確認を得る。
2. scope / entry条件 / 作業項目 / exit criteria を抽出する。**exit criteriaが別節(受入基準一覧・工数表・stage共通前文)に分散している場合はタスクIDで計画全体を横断検索し、統合したcriteria一覧を提示してから進む**。
3. 依存関係・mutex・branch base規則・**timebox・abort trigger・stop condition**・実績記録先・evidence保存先も抽出する。**計画のabort/エスカレーション条件が本コマンドの既定より厳しい場合は計画側を優先する**。
4. 人間(owner)専用のentry/exit項目(手動readback・承認等)は分離して列挙する。
5. 抽出できない場合、またはexit criteriaが客観的に検証可能な形で書かれていない場合は、**実行せず理由を報告して停止**する。

## Phase 1 — entry検証

以下を検証し、未達なら**停止して報告**する。**検証手段がない項目は「未達」ではなく「検証不能」として停止**し、確認方法をユーザーに求める:

- working treeがclean(再開モードは上記の読み替え)
- 依存タスクのmerge済み: merge commitの実在(`git log` / `gh pr view <PR> --json mergeCommit`)と、計画の実績記録先の記載で確認する
- mutex: open branch(mainに未mergeのremote branchおよびopen PR)ごとに `git diff main...<branch> --name-only` でtouched filesを取り、mutex対象ファイルと交差しないこと。mutex対象が計画から特定できない場合は報告して停止
- 人間専用のentry項目: ユーザーへ確認を依頼し、evidence受領後に続行する(PR本文向けevidenceはPhase 7でPR本文へ転記する)
- 計画がentry gateとして定義するその他の条件

**Phase 1.5 — 作業branch作成**: 計画のbranch base規則に従うbase commit(例: 依存stageのmerge commit)を特定して作業branchを作成する。規則がなければ現在のmain HEADから。

## Phase 2 — goal条件の提示

exit criteriaを要約したgoal条件文を1〜2行で生成し、コピー可能な形でユーザーに提示する:

> 強制力を付与したい場合は `/goal <条件文>` を実行してください(任意)。

返答は待たず、そのまま次のPhaseへ進む。

## Phase 3 — 実装指示書の生成

会話コンテキストに依存しない**自己完結の実装指示書**を作業ディレクトリに書く。含めるもの:

- タスクのscope・作業項目・統合済みexit criteria全文(計画から転記。要約しない)
- 対象ファイルと、リポジトリ規約(CLAUDE.md/AGENTS.mdの関連ルール、コミット規約)
- 「変更は論理単位でcommitし、**commitを完遂すること(未commitのまま終了しない)**。pushとPR作成はしないこと」
- 「指示書にないファイル(特に `.claude/` `.codex/` `.github/` `CLAUDE.md` `AGENTS.md`)を変更しないこと」
- exit criteriaをローカル検証する具体的なコマンド・手順(存在する場合)

## Phase 4 — Codex実装(バックグラウンド)

推論レベルの規則(計画に定義がない場合のデフォルト):

| 場面 | レベル |
| --- | --- |
| 初回実装 | `xhigh` |
| 修正イテレーション(Phase 6からの再入) | `medium`で開始 |
| 同一指摘が2巡連続で残った場合 | 次巡から`xhigh`へ昇格 |

実行方法:

```
codex exec -m gpt-5.6-sol --sandbox workspace-write -c model_reasoning_effort=<level> \
  "<指示書の絶対パス> を読み、記載どおりに実装してください。指示書にない変更は行わないでください。"
```

- Bashツールの `run_in_background: true` で起動し、完了を待つ。完了後 `git status` / `git diff` で成果を確認する。
- **`.claude/` `.codex/` `.github/` `CLAUDE.md` `AGENTS.md` への差分が指示書に明記なく含まれる場合は、即停止してユーザーへ報告する**。
- uncommitted changesが残っている場合は「commitの完遂」を指示して再実行する。diffが空の場合は失敗として扱う。
- Codexが失敗・無応答(目安: 30分進捗なし)の場合は1回だけ再試行し、それでも失敗ならユーザーへ報告して停止する。
- 並列実装・best-of-Nは**既定では行わない**。ユーザーが明示的に指示した場合のみ、`git worktree`で分離した上で実施し、採用案だけを作業branchへ取り込む。

## Phase 5 — リスク応分レビュー(独立サブエージェント)

実装完了ごとに、Claudeサブエージェントで独立レビューを行う。レビュワーには実装過程のコンテキストを渡さず、リポジトリの実ファイルと計画セクションだけを読ませる(context-free)。

レビュー指示には次を必ず含め、指示文自体を自己完結にする: 対象commit範囲(`git diff <base>..HEAD`)、計画ファイルパスとタスクID、判定形式(深刻度Blocker/High/Medium/Low+該当箇所+推奨対応)、および**既決事項リスト**(却下済み指摘の根拠・残置済みMediumの理由**のみ**。実装経緯は含めない)。

- **通常変更(既定)**: 独立レビュワー**1名**が、①仕様準拠(実装が計画の作業項目とexit criteriaを満たすか。項目ごとにFIXED/PARTIAL/NOT_FIXED判定)と②機械検証(リンク・schema・パース・整合性など機械的に検証可能な項目を実際に実行)を統合して実施する。
- **高影響変更(schema/後方互換、公開契約・Release、大規模な移動・削除、移行・復元・削除ゲート)**: 上記に加えて**追加の独立レビュワー1名**が、③回帰検査(この変更が新たに壊したものをfreshな視点でdiffから探す)と④整合検査(リポジトリ内の他の正典文書・規約との矛盾)を実施する。
- **修正後の再確認は「追加観点」ではなく同一レビューの継続**として扱う(前回のfindingsに対するFIXED/NOT_FIXED判定が主目的。新しい観点を追加しない)。
- レビュワーが失敗した場合は1回再試行し、なお失敗なら当該観点を「未実施」として最終報告に明記する(握り潰さない)。
- レビュワー間で矛盾する判定は厳しい側を採用して妥当性判定に回す。

## Phase 6 — 修正ループ

1. **まず各指摘の妥当性を計画・既決事項と突合して判定する。誤検知はREJECTEDとして根拠を記録し、修正対象から除外する**(却下の記録は「握り潰し」に当たらない)。
2. 有効な指摘をBlocker/High/Medium/Lowに統合し、作業ディレクトリに `findings-round<N>.md` として保存する(巡回間の「同一指摘」は同一ファイル・同一箇所・同一趣旨で対応付け、IDを引き継ぐ)。**自己完結の修正指示書**を生成し、Phase 4(修正イテレーション)へ戻る。
3. 終了条件: **有効なBlocker/High = 0**、かつMediumは修正済みまたは残置理由を記録済み。Lowは任意(まとめて報告)。
4. 上限: **計画が定義するabort trigger/timeboxを最優先**する。計画に定義がない場合のデフォルト: **同一指摘が2巡残った時点で自動続行せず停止**し、残指摘一覧付きでownerへエスカレーションして `simplify / defer / abandon` の判断を仰ぐ。総ラウンド上限は3。

## Phase 7 — 証跡とdraft PR

1. Phase 1のentry条件のうち計画が「entry/実行時のread back」を要求する項目は、PR作成前に**再検証**する。
2. レビュー結果の要約(観点・判定・ラウンド数・却下/残置事項)を作業ディレクトリに保存する。**raw review evidence(レビュワー出力全文・findings)は `.agent-work/` に置き、コミットしない。PR本文へは要旨のみ転記する**。
3. 実績(ラウンド数・概算工数)を最終報告に含める。計画が実績記録先を定義していれば更新する。
4. **作業branchを `git push -u origin <branch>` でpushしてから**(mainへのpushではない)、`gh pr create --draft` を実行する。リポジトリにPR templateが存在する場合はそのchecklistを本文に含めて記入し、変更ファイル一覧・exit criteria検証結果・レビュー要約を追記する。
5. ユーザーへ「draft PR作成済み、merge判断待ち」と報告して**終了する。mergeは絶対に行わない**。

## 禁止事項

- PRのmerge、mainへの直接push、entry検証未達での強行(pushはfeature branchのみ)
- レビューの省略、指摘の握り潰し(却下・残置は必ず根拠を記録)、妥当性検証を省略した盲目的な修正
- raw review evidenceのコミット(`.agent-work/` に置く。PRへは要旨のみ)
- Codexへの指示・レビュー指摘を会話コンテキスト経由で渡すこと(必ずファイル経由)
- 計画に書かれていないscopeの追加実装、user-globalパス(`~/`配下)への状態保存
