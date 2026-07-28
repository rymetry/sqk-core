# ルーティング表（シード）

## 位置づけ

本ファイルは quality-orchestrator の2段階ルーティング（[skill-ecosystem-design-plan.md §4](../../../docs/agent-ecosystem/skill-ecosystem-design-plan.md) 参照）のうち、第2段階「（ノード×意図動詞×ライフサイクルフェーズ）→スキル」対応表のシードである。第1段階の10ノードチェーン分類は同 §4 を参照。

## 変更凍結の注記

[phase1-implementation-guide.md T4](../../../docs/agent-ecosystem/phase1-implementation-guide.md) の規定どおり、判断に迷った場合の追加・変更は Phase 1 中は禁止する。統合試行（T12）の結果を根拠に PR で改訂すること。

**根拠**: ルーティング表は全スキルの `description` と整合しなければならず、場当たりで書き換えるとトリガー精度の検証（未解決論点5）が不能になる。シードを固定し、変更は証拠ベースで行う。

## ルーティング表

| チェーンノード | 意図（代表的な動詞・依頼文） | ルーティング先 | Phase |
|---|---|---|---|
| REQ, AC | テスト条件を出す／仕様を分析する／観点を洗い出す | test-requirement-analysis | MVP |
| RISK | リスクを洗い出す／優先度・厚みを決めたい | risk-analysis | MVP |
| TEST | テストを構造化する／どの粒度・順序・環境でやるか設計する | test-architecture-design | MVP |
| TEST | テストケースを作る／技法を選ぶ | test-design-implementation | MVP |
| TEST | テストを実行した結果をまとめる／flaky を切り分ける | test-execution-support | P2（実装済み） |
| TEST | 探索的にテストしたい／チャーターを選びたい | exploratory-testing-support | P2（実装済み） |
| （全ノード） | 紐づきを確認する／カバレッジを可視化する | traceability-management | MVP |
| EV, REL | リリース判定する／品質ゲートを通してよいか | quality-gate-release-judgment | MVP |
| QC | 非機能をレビューする／特性間のバランスを見る | nfr-review | P2（実装済み） |
| MON, MET | SLO/SLI を設計する／DORA 指標を解釈する | sre-quality-ops | P2（実装済み） |
| TEST（コード差分） | PR・コードをレビューする／静的解析結果を優先度付けする | code-review | P2（実装済み） |
| RISK, MON | 障害・欠陥を分析する／RCA・ポストモーテム | defect-analysis-rca | P2（実装済み） |
| QC, TEST（AI/LLM） | LLM/AI 機能の評価を設計する | ai-system-quality-eval | P2（実装済み） |
| EV | 成果物一式が整合しているかメタレビューする | quality-artifact-review | P2（実装済み） |
| MET | 事業指標（NPS/チャーン等）と品質の相関を見る | business-quality-metrics | P3（実装済み） |

## フォールバック規則

[skill-ecosystem-design-plan.md §4](../../../docs/agent-ecosystem/skill-ecosystem-design-plan.md) のとおり: 曖昧な場合は明確化質問1回まで → それでも定まらない場合は入力が揃っている最上流フェーズへ。**本表の全スキルは実装済み**であり、Phase 列（P2/P3）は導入時期の記録であって未実装の印ではない（#14 は [D-011 フェーズB追記](../../../DECISIONS.md#d-011-phase-2-backlog-の再評価vertical-slice-根拠)で defer→keep へ格上げ、#7/#11/#12/#13 は [D-012](../../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ) ウェーブ1、#9/#10 は同ウェーブ2、#8/#15 は同ウェーブ3で作成。#15 の P3 据え置き解除は D-012）。MVP スキルと同様に全行を通常どおりルーティングする。未実装スキルの行が将来追加された場合のみ、「該当スキルは未実装。手動で `docs/` の該当文書（ルーティング表の Phase 列参照）を参照すること」と案内する。

## 関連ドキュメント

- [phase1-implementation-guide.md](../../../docs/agent-ecosystem/phase1-implementation-guide.md) — 本シードの出典（T4）
- [skill-ecosystem-design-plan.md §4](../../../docs/agent-ecosystem/skill-ecosystem-design-plan.md) — オーケストレーション設計の正典
