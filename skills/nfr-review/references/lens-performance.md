# レンズ: 性能

対象特性: 性能効率性（[iso25010 §2](../../../docs/quality-models/iso25010-product-quality-model.md#2-性能効率性performance-efficiency)。
時間効率性・資源効率性・容量満足性）、および負荷変動に関わる範囲で
柔軟性（拡張性）。

主参照: [iso25010-product-quality-model.md](../../../docs/quality-models/iso25010-product-quality-model.md)、
[production-quality-sre-observability.md](../../../docs/operations-quality/production-quality-sre-observability.md)

## チェック観点

1. **応答時間・スループットの水準が測定可能な形で定義されているか**:
   「十分高速」は測定不能。対象・負荷条件・パーセンタイル水準・証跡の
   基本形に変換できるか（[iso25010 §受入基準の基本形](../../../docs/quality-models/iso25010-product-quality-model.md#受入基準品質ゲートへの落とし込みパターン)）。
2. **負荷条件（同時利用者数・データ量・ピーク特性）が明示されているか**:
   手がかり語「○秒以内」「同時○人」「大量データ」に水準が伴うか
   （[iso25010 §手がかり語対応表](../../../docs/quality-models/iso25010-product-quality-model.md#要求の手がかり語--品質特性-対応表)）。
3. **容量満足性・資源効率性の上限が定義されているか**: ストレージ・
   メモリ・接続数の上限と、上限接近時の挙動。
4. **スケール戦略が負荷増減の実態に対応しているか**: 拡張性（柔軟性の
   サブ特性）との接続。クラウド移行・負荷増減の手がかり語がある場合は
   柔軟性も併せて確認する。
5. **本番での測定・監視手段が設計されているか**: SLI/SLO・
   オブザーバビリティの計画（[production-quality §SLI/SLO/SLA](../../../docs/operations-quality/production-quality-sre-observability.md#sli--slo--sla-とエラーバジェット)・
   [§オブザーバビリティ](../../../docs/operations-quality/production-quality-sre-observability.md#オブザーバビリティ3-本柱と-opentelemetry)）。
   SLO の詳細設計は sre-quality-ops の担当領域であり、本レンズでは
   「測定手段の有無・水準の定義可能性」までを見る。
6. **性能テストの実施条件・証跡が計画されているか**: 負荷テストの環境・
   データ規模が本番相当か、証跡（レポート）の残し方。

## 代表トレードオフ（マトリクス検討時の起点）

[iso25010 §典型的なトレードオフ](../../../docs/quality-models/iso25010-product-quality-model.md#典型的なトレードオフ)より:

- 性能効率性 vs 保守性(高度な最適化が可読性・変更容易性を下げる →
  ボトルネックに限定して最適化し ADR に残す)
- 柔軟性 vs 性能効率性(抽象化層のオーバーヘッド → 性能予算を先に定義)
- セキュリティ vs 性能効率性(暗号化・検査・監査ログの遅延 → データ
  分類で処理を差別化)
