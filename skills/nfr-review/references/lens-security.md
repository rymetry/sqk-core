# レンズ: セキュリティ

対象特性: セキュリティ（[iso25010 §6](../../../docs/quality-models/iso25010-product-quality-model.md#6-セキュリティsecurity)。
機密性・完全性・否認防止・責任追跡性・真正性等のサブ特性）。

主参照: [secure-development-and-supply-chain.md](../../../docs/secure-development/secure-development-and-supply-chain.md)

## チェック観点

1. **脅威モデリングが実施（または計画）されているか**: 設計段階で
   「何が失敗しうるか」を列挙しているか（[同 doc §4](../../../docs/secure-development/secure-development-and-supply-chain.md#4-脅威モデリング-何が失敗しうるかを設計段階で列挙する)）。
   未実施なら最重要指摘とする。
2. **要件ベースの検証基準があるか**: OWASP ASVS 等のレベル指定・
   検証項目の選定（[同 doc §2](../../../docs/secure-development/secure-development-and-supply-chain.md#2-owasp-top-10webと-asvs-50-リスク認知から要件ベース検証へ)。
   Top 10 はリスク認知、検証は ASVS ベースで）。
3. **認証・認可・権限設計が最小権限になっているか**: 監査ログ・職務分離
   を含む（[同 doc §8](../../../docs/secure-development/secure-development-and-supply-chain.md#8-権限設計-最小権限監査ログ職務分離)）。
   重要操作の責任追跡性（誰が実行したか特定可能か）。
4. **Secure by Default か**: 安全でない設定をユーザーに委ねていないか
   （[同 doc §5](../../../docs/secure-development/secure-development-and-supply-chain.md#5-secure-by-design--secure-by-defaultcisa)）。
5. **セキュリティテスト・解析の使い分けが計画されているか**:
   SAST/DAST/SCA 等の適用範囲とゲート配置（[同 doc §6](../../../docs/secure-development/secure-development-and-supply-chain.md#6-セキュリティテスト解析の使い分け)・
   [§10](../../../docs/secure-development/secure-development-and-supply-chain.md#10-品質ゲートと証跡-リリース判定にセキュリティを組み込む)）。
6. **サプライチェーン（依存・ビルド）の管理があるか**: 依存の既知脆弱性
   監視・来歴（[同 doc §7](../../../docs/secure-development/secure-development-and-supply-chain.md#7-ソフトウェアサプライチェーン-自分が書いていないコードの品質管理)）。
7. **LLM/AI 機能を含む場合は固有リスクを見ているか**: プロンプト
   インジェクション・過剰な代理権限等（[同 doc §3](../../../docs/secure-development/secure-development-and-supply-chain.md#3-owasp-top-10-for-llm-applications2025)・
   [§9](../../../docs/secure-development/secure-development-and-supply-chain.md#9-llmai-エージェント固有のセキュリティ品質)）。
   AI 品質評価の設計自体は ai-system-quality-eval の担当領域。

## 代表トレードオフ（マトリクス検討時の起点）

[iso25010 §典型的なトレードオフ](../../../docs/quality-models/iso25010-product-quality-model.md#典型的なトレードオフ)より:

- セキュリティ vs インタラクション容易性(認証強度と操作の手間 →
  リスクベースで強度を可変に)
- セキュリティ vs 性能効率性(暗号化・監査ログの遅延 → 非同期化等で緩和)
- 互換性(相互運用性) vs セキュリティ(外部連携の開放が攻撃面を拡大 →
  互換性要求に必ずセキュリティ要求を対にする)
