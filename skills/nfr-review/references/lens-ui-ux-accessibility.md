# レンズ: UI/UX + アクセシビリティ

対象特性: インタラクション容易性（[iso25010 §4](../../../docs/quality-models/iso25010-product-quality-model.md#4-インタラクション容易性interaction-capability旧-使用性usability)。
2023年版で使用性から改称。運用操作性・ユーザエラー防止・セルフ記述性・
アクセシビリティ等のサブ特性を含む）。

主参照: [accessibility-ux-human-centered-quality.md](../../../docs/human-centered-quality/accessibility-ux-human-centered-quality.md)

## チェック観点

1. **WCAG 適合の目標が明示されているか**: 適合レベル（A/AA/AAA）と対象
   達成基準の指定。実務の目安は WCAG 2.2 AA（[同 doc §1](../../../docs/human-centered-quality/accessibility-ux-human-centered-quality.md#1-wcag-22-原則適合レベル新規達成基準)
   の POUR 4原則・達成基準を参照）。
2. **法規制の適用判定がされているか**: 対象市場に応じた要求
   （日本: JIS X 8341-3・障害者差別解消法／EU: EAA／米国: ADA・Section 508。
   [同 doc §2](../../../docs/human-centered-quality/accessibility-ux-human-centered-quality.md#2-法規制規格の対応)）。
3. **自動チェックの限界を織り込んでいるか**: 自動ツールで検出できる
   達成基準は一部に留まる（同 doc の自動チェック限界の実測）。手動検証・
   支援技術での確認計画の有無。
4. **ユーザエラー防止の設計があるか**: 破壊的操作の確認・取り消し・
   入力制約の設計（インタラクション容易性のサブ特性）。
5. **使いやすさの水準が測定可能か**: 「使いやすいこと」ではなく、
   タスク完了率・SUS/NPS/CSAT 等の測定指標と水準
   （[iso25010 §受入基準の例](../../../docs/quality-models/iso25010-product-quality-model.md#受入基準品質ゲートへの落とし込みパターン)）。
6. **AI/LLM を含む UI では信頼較正が設計されているか**: AI 出力の確信度
   提示・誤り時の回復手段（同 doc の AI UI 信頼較正）。

## 非該当の典型

エンドユーザー向け UI を持たない対象（バッチ・内部 API 等）。ただし
運用者向け画面・CLI・エラーメッセージがあれば運用操作性の観点で該当
しうるため、非該当と断定する前に利用者の範囲を確認する。

## 代表トレードオフ（マトリクス検討時の起点）

- セキュリティ vs インタラクション容易性（多要素認証・入力制約が操作の
  手間を増やす → リスクベースで強度を可変に。[iso25010 §典型的なトレードオフ](../../../docs/quality-models/iso25010-product-quality-model.md#典型的なトレードオフ)）
- 性能効率性 vs リッチな UI 表現
