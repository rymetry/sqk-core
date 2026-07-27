# レンズ: アーキテクチャ

対象特性: 保守性（[iso25010 §7](../../../docs/quality-models/iso25010-product-quality-model.md#7-保守性maintainability)）・
柔軟性（[§8](../../../docs/quality-models/iso25010-product-quality-model.md#8-柔軟性flexibility旧-移植性portability)。
2023年版で移植性から改称、拡張性を含む）・互換性（[§3](../../../docs/quality-models/iso25010-product-quality-model.md#3-互換性compatibility)）・
信頼性（[§5](../../../docs/quality-models/iso25010-product-quality-model.md#5-信頼性reliability)。
構造起因の障害分離・回復性）。

主参照: [iso25010-product-quality-model.md](../../../docs/quality-models/iso25010-product-quality-model.md)、
[production-quality-sre-observability.md](../../../docs/operations-quality/production-quality-sre-observability.md)

## チェック観点

1. **変更容易性・テスト容易性が構造に織り込まれているか**: モジュール性・
   結合度、テスト容易性（保守性のサブ特性）。「変更しやすい」の手がかり語
   に測定可能な水準（カバレッジ・静的解析基準等）が伴うか。
2. **障害分離と回復性が設計されているか**: 単一障害点の有無、
   フェイルオーバー・RPO/RTO の定義（信頼性の回復性。
   [iso25010 §受入基準の例](../../../docs/quality-models/iso25010-product-quality-model.md#受入基準品質ゲートへの落とし込みパターン)）。
3. **外部連携の互換性要求が定義されているか**: API 契約・バージョニング・
   共存条件（互換性）。連携ごとにセキュリティ要求（真正性・責任追跡性）
   が対になっているか（セキュリティレンズと連携して見る）。
4. **環境変化への適応が実需ベースか**: クラウド移行・負荷増減・マルチ
   環境の要求（柔軟性）に対し、変化が実際に見込まれる軸だけを柔軟化して
   いるか（投機的汎用化の禁止。[iso25010 §典型的なトレードオフ](../../../docs/quality-models/iso25010-product-quality-model.md#典型的なトレードオフ)）。
5. **リリース・デプロイ戦略が品質制御に使われているか**: カナリア・
   ブルーグリーン等の段階的リリースと自動ロールバック条件
   （[production-quality §リリース戦略](../../../docs/operations-quality/production-quality-sre-observability.md#リリース戦略デプロイを品質制御装置にする)）。
6. **アーキテクチャ決定が記録されているか**: トレードオフの採用案・
   却下案・理由・見直し条件が ADR として残る運用か
   （[iso25010 §調停・優先順位付けの手順](../../../docs/quality-models/iso25010-product-quality-model.md#調停優先順位付けの手順)の
   「却下した選択肢も記録する」）。

## 品質シナリオによる具体化

抽象的な特性名ではなく「刺激→環境→応答→応答測定」の品質シナリオ形式で
書き、シナリオ同士の衝突としてトレードオフを可視化する
（[iso25010 §調停・優先順位付けの手順](../../../docs/quality-models/iso25010-product-quality-model.md#調停優先順位付けの手順)の手順2）。

## 代表トレードオフ（マトリクス検討時の起点）

- 性能効率性 vs 保守性(最適化の複雑化 → ボトルネック限定 + ADR)
- 柔軟性 vs 性能効率性(抽象化層のオーバーヘッド → 性能予算で評価)
- 安全性 vs 可用性(フェールセーフによる安全停止 → 「安全側に倒す」を
  品質方針に明文化)
- 機能適合性(完全性) vs 保守性(機能を盛るほど複雑度が上がる →
  機能適切性を評価軸に加える)
