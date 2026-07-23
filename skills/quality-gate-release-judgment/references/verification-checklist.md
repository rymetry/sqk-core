# 単体実行の検証観点・参照ポインタ表

## 位置づけ

本ファイルは `quality-gate-release-judgment` の単体実行を検証する際の観点と、
判定手順が参照する正典へのポインタ表である。解説は書かず、詳細はすべて
リンク先を正典とする。

## 単体実行の4検証観点

[portability-design.md §3「単体実行の検証観点」](../../../docs/agent-ecosystem/portability-design.md#3-claude-code--cowork-向け実装例フル掲載)
に定義された次の4観点を、Phase 1 の実装完了直後に手動で一度実施し、以後は
回帰確認として使う。

| 観点 | 合格基準（要約） |
| --- | --- |
| 証跡ゼロでの起動 | 質問3件以内で、`gate_status: blocked` を含め必ず判定が返る |
| 証跡過多での起動 | 優先度 A 項目の証跡が揃えば `passed` が根拠付きで返る |
| カウンターメトリクス欠落の検出 | 主指標単独の証跡に対し判定コメントで指摘される |
| エンベロープの再取込可能性 | 出力 JSON が handoff-envelope スキーマに適合する |

## 判定手順が参照する正典

| トピック | 参照先 |
| --- | --- |
| 証跡チェックリスト（優先度 A 項目） | [software-quality-gap-analysis-report.md「収集すべきアーティファクトチェックリスト」](../../../docs/quality-management/software-quality-gap-analysis-report.md#収集すべきアーティファクトチェックリスト) |
| カウンターメトリクスの原則 | [quality-metrics-pitfalls.md 原則3](../../../docs/quality-management/quality-metrics-pitfalls.md#原則-3-カウンターメトリクス対になる指標) |
| 品質特性間のトレードオフ（残存リスク記述の観点） | [iso25010-product-quality-model.md「品質特性間のトレードオフと調停」](../../../docs/quality-models/iso25010-product-quality-model.md#品質特性間のトレードオフと調停) |
| 出力エンベロープのデータ契約 | [schemas/handoff-envelope.schema.json](../../../schemas/handoff-envelope.schema.json)・[schemas/release-decision.schema.json](../../../schemas/release-decision.schema.json) |

## 関連ドキュメント

- [../SKILL.md](../SKILL.md) — 本スキルの手順本体
