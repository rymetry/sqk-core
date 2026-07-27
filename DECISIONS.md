# v2 意思決定記録

この文書は、`sqk-core`（v2）の主要な意思決定を軽量に記録する。v1 の ADR 群に代わる記録であり、各決定の背景と理由を、実装や運用に必要な範囲で維持する。

## D-001: sqk-core への再構築

**決定内容**: v1（`software-quality-knowledge-base`）から、価値の核である domain canon、skills、schemas、knowledge、platforms を repo-template 起点の `sqk-core` へ選択移植し、最小ガバナンスで再出発する。移行完了後に v1 を削除し、その履歴は Release `archive-sqkb-v1` の bundle で保全する。

**理由**: v1 ではガバナンス機構が約57,000行に達し、約14,000行の知識本体のおよそ4倍になった結果、1変更あたりの修正コストが過大になった。知識の価値を維持しながら通常の変更コストを下げるには、増築ではなく選択移植による再構築が必要だった。

## D-002: provenance 能力の軽量な維持

**決定内容**: v1 の provenance registry 機構（約13,000行）は移植しない。出典、`derived_from`、`knowledge_refs`、authority 区分を追跡する能力は、文書内出典、git 履歴、本 `DECISIONS.md`、`MIGRATION-SOURCES.sha256` で維持する。対応は [MIGRATION.md](./MIGRATION.md) の「Authority の対応」に記録する。

**理由**: provenance の能力は必要だが、専用 registry とその検証機構はガバナンス膨張の大きな要因だった。既存の文書・git・移植ハッシュで必要な追跡可能性を保てるため、専用機構は不要と判断した。

## D-003: レビュー証跡の保管

**決定内容**: v1 の cycle レポートのような review evidence 文書はコミットしない。raw なレビュー証跡は gitignore された `.agent-work/` に置き、PR 本文には要旨だけを転記する。通常変更は独立1名、高影響変更は追加1名を目安とするリスク応分のレビューを行う。

**理由**: raw evidence を恒久文書として蓄積すると、知識本体と無関係なメタ文書が増え続ける。PR に判断要旨を残せば日常変更に必要な説明責任を保ちつつ、レビュー負荷を変更リスクに合わせられる。

## D-004: 生成物と curated derived artifact

**決定内容**: 自動生成物をコミットする場合は、generator と drift 検査を必須とする。`knowledge/` など手作業で保守する curated derived artifact には、canonical source refs と更新ルールを必須とする。

**理由**: 自動生成物は再生成可能性と差分検出がなければ陳腐化し、手作業の派生物は出典と更新順序がなければ canonical source と乖離する。生成方法に応じた最小の整合手段を持たせる必要がある。

## D-005: v1 ADR 要旨の保存（superseded）

**決定内容**: v1 の ADR 4件は移植せず、以下の要旨だけを保存する。いずれも v2 では規範ではなく、superseded とする。

- ADR-0001: 品質スキル・エコシステム設計プランの実行記録（2026-07-07）。`docs/` 全23ファイルの実査から、設計3文書（skill-ecosystem-design-plan / knowledge-management-design / portability-design）を確立した。正典は設計3文書側にある。
- ADR-0002: Phase 2 実装ガイド起草の実行記録（2026-07-07）。Phase 1 / 1b の実測を受入基準へ反映し、RoutingDecision の形状や新スキーマ範囲などを確定した。
- ADR-0003: Repository Architecture Evolution Plan v0.19.1 の G0 acceptance（2026-07-11、solo self-acceptance）。consumer audit で外部 consumer の兆候がないことを確認し、solo-baseline profile を適用した。
- ADR-0004: 同計画 v0.20.0 の G0 re-acceptance（2026-07-15）。exact-revision 照合（commit / blob / SHA-256）による受理を記録した。

**理由**: この Evolution Plan の多段ゲート路線（G0 / G1、provenance registry、review evidence 機構）は v1 膨張の主因であり、D-001 により v2 では採用しない。一方、過去判断の所在を見失わないため要旨を残し、原文は Release `archive-sqkb-v1` の bundle で保全する。

## D-006: v1 Execution freeze の失効

**決定内容**: v1 の `phase2-implementation-guide` にあった Execution freeze は v1 の宣言であり、v2 では失効している。v2 における Phase 2 の扱いは D-007 と [ROADMAP.md](./ROADMAP.md) に従う。移植済み文書には superseded 注記を付す。

**理由**: freeze は v1 の architecture 作業完了まで Phase 2 着手を凍結するための制約であり、選択移植後の v2 にその前提を持ち込む理由がない。v2 の実装順序は、現在の成果物と欠陥を基準に再設定する必要がある。

## D-007: Phase 2 の再ベースライン

**決定内容**: v1 の Phase 2 スコープ（残り8スキル、ナレッジ文書3件など）はそのまま引き継がない。vertical slice 完了後に keep / merge / defer / drop を再評価してから実装する。`docs/agent-ecosystem/phase2-implementation-guide.md` は backlog material として保持する。

**理由**: v1 の計画を実需の確認前に全量実装すると、consumer のいない仕組みを再び増やすおそれがある。まず実タスクで既存スキルチェーンの価値と不足を確認し、その結果に基づいて Phase 2 の投資対象を選ぶ。

## D-008: auto-merge の無効化と hook の位置づけ

**決定内容**: リポジトリの auto-merge は有効化しない（`.allow_auto_merge == false`）。Dependabot auto-merge workflow は削除済みとし、すべてのコンテンツ変更を PR 経由にして、merge 判断は人間が行う。

`.claude/hooks/` と `.codex/hooks/` の push ブロックは、agent の通常操作に対する防御層であり、完全なセキュリティ境界ではない。admin の人間操作は運用規律で扱う（branch protection は承認0、`enforce_admins: false`）。

**理由**: 自動 merge を避けて人間の判断点を保つ一方、hook が admin 操作まで強制的に封じると誤認しないためである。通常の agent 操作への予防策と、権限者が守る運用規律を明確に分ける。

## D-009: metadata archive の非公開保管

**決定内容**: v1 の PR / Issue / review metadata export（`v1-github-metadata.tar.gz`、SHA-256 `3bb0bc3ec51031644216e02da683ff4ebfa292dbf80c271f228d88a855424937`、84,168 bytes）は公開リポジトリに含めず、非公開のローカルバックアップとして保管する。公開履歴は Release `archive-sqkb-v1` の public bundle で提供する。

**理由**: metadata export には公開 repository の再構築に不要な運用情報が含まれうる。履歴の公開保全と metadata の保管範囲を分離し、公開範囲を必要最小限にする。

## D-010: SKILL.md `version` の authority

**決定内容**: `SKILL.md` frontmatter の `version` は、SKILL.md 自身を authority とする。スキルの実質的な変更（inputs / outputs、手順、判定基準の変更）を含む PR では、同一 PR 内で semver に従って `version` を更新する。変更履歴の追跡は git 履歴で行う。

**理由**: v1 では provenance registry（`artifacts.yaml`）が `version` の writable authority であり、frontmatter は readonly projection だった。D-002 で registry を移植しないと決定した結果、version 更新の規律が未宣言になっていた。authority の所在と更新タイミングを明文化し、更新判断の属人化を防ぐ。

## D-011: Phase 2 backlog の再評価（vertical slice 根拠）

**決定内容**: D-007 が求める Phase 2 backlog の再評価を、vertical slice（m0 Viewer Analytics のテスト設計を既存7スキルチェーンで一気通し）の実測を根拠に実施した。結果は次のとおり分類する。

- **keep（次の実装対象）**: 実証済みチェーンの「深さ」を埋める4件のみ。(1) `StakeholderList` の schema 追加と risk-analysis の生成手当て（RISK→STK の接続が存在しない構造的欠落）、(2) `schemas/README.md` の content/items 使い分け明文化と HTC/各マトリクスの専用 schema 追加（機械検証範囲の拡張）、(3) traceability-management の「各段後随時起動」→「複合フロー末尾で一括」への文言修正、(4) テスト空間3軸マトリクス描画の稼働確認（slice で既に稼働）。
- **defer（判断保留・ドメイン別再評価待ち）**: 8新スキル（#7〜#14）とナレッジ文書3件（code-review-techniques / defect-taxonomy-odc / japanese-test-design-methods）。slice はテスト設計1本であり、別ドメイン（コードレビュー・RCA・SRE・AI評価・テスト実行・探索）向けスキルの価値を判定する根拠を持たない。各項目は該当ドメインの実タスクが現れた時点で再評価する（D-007 の哲学を再帰適用）。#14 quality-artifact-review はメタレビュー+ゲート委譲先で「幅」ではなく「深さ」寄りのため、keep 4件（フェーズA）の完了後の再評価キュー先頭に置く。
- **drop（積極的破棄）**: 現時点でなし。「テスト設計 slice で不要だった」は「恒久的に不要」を意味しないため、drop ではなく defer とする。

**理由**: slice の最も強い実測は「1本の実タスクで8スキルは1つも使われず、既存7スキルには構造的な穴（StakeholderList・REQ ノード・マトリクス系 schema の不在）があった」ことである。幅（8スキル）を足す前に深さ（既存チェーンの完全性・機械検証）を埋めるのが、consumer のいない仕組みを増やさないという D-005 / D-007 の原則に整合し、実証済みユースケースについて core を実際に end-to-end で完成させる。raw な slice 証跡（RISK/HTC/DTC/TAE/COV/TC/保証/トレーサビリティ/再評価分析）は `.agent-work/vertical-slice/viewer-analytics/` に保持し、コミットしない。

**フェーズB追記（2026-07-27）**: keep 4件（フェーズA）の完了後、再評価キュー先頭の #14 quality-artifact-review を、slice 成果物一式（エンベロープ 01〜07）に対する #14 相当のメタレビューの手動実行（dry-run）で再評価し、**defer → keep（実装）へ格上げ**した。判定根拠は2点。(1) **増分価値**: 既存チェーンが構造的に見ない「エンベロープ横断の整合」（owner 裁定が後工程の rationale に散在し元エンベロープの open_questions が未解決のまま残る状態矛盾、決定・約束のライフサイクル追跡の不在、trace_ids 列挙規約の不整合）で、既報告と重複しない新規所見を検出した。traceability-management は ID リンク、release-judgment は証跡の存在のみを見るため、この領域の担い手は #14 以外にいない。(2) **slice 弱点 N5 への解**: 所見 severity 4値（blocker/major/minor/info）→3値 gate_status の導出規則（blocker→blocked／major→passed-with-risks／minor・info のみ→passed。文書化済み仮定＋緩和策つきは minor とする）を slice 7段に遡及適用したところ、全段 passed-with-risks だった実績が3段（risk／traceability／release-judgment）で passed に分化し、「健全な進行」と「要注意」を gate_status で区別できることを実測した。実装は skills/quality-artifact-review（v0.1.0）＋ `schemas/artifact-review-finding.schema.json`。ルーティング表の #14 行昇格（T3a 相当）と orchestrator ゲート判定の委譲（T12）はスコープ外とし、別 PR の follow-up とする（owner 確認済み）。残る #7〜#13 とナレッジ文書3件は defer 継続（ドメイン別再評価待ち、変更なし）。dry-run 証跡は `.agent-work/d011-phase-b/` に保持し、コミットしない。
