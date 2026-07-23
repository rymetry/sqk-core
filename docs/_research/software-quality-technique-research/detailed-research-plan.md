# Detailed Research Plan

この計画は、`veriserve-hqw-article-essence-index-v3.md` を正典化せず、一次情報確認と既存docsへの分配を行うための作業計画である。

## 原則

- v3は研究入力であり、canonical docs、`knowledge/`、skills の根拠として直接使わない。
- 一次情報確認前の主張は `not-yet-triaged` または `needs-official-check` とする。
- `knowledge/` は `docs/` の派生物であるため、研究カードから直接更新しない。
- veridia向け実装候補は本repoのKB登録対象外である。研究カードでは実装仕様として扱わない。
- HQW由来とHQW外補完候補を混ぜない。HQW外は `origin_layer: external-gap` として隔離する。
- v3が言及する `work/veriserve_articles.jsonl` は現repoに存在しないため、取得済み本文の統計値は再現性メモとして扱う。

## 研究カードモデル

研究内IDは canonical ID と分ける。

- HQW由来: `RC-HQW-R<theme>-<number>`
- HQW外補完: `RC-EXT-R15-<number>`

カードは次の状態を持つ。

| フィールド | 値 |
| --- | --- |
| `origin_layer` | `hqw-article` / `external-gap` |
| `source_layers[]` | `primary-standard` / `paper` / `official-tool-doc` / `official-guidance` / `existing-doc` |
| `verification_state` | `not-yet-triaged` / `needs-official-check` / `partially-checked` / `confirmed-for-scope` / `licensed-text-needed` / `rejected` |
| `confirmed_scope` | 確認済みの主張範囲。未確認なら `unknown` |
| `KB登録判断` | `adopt` / `merge` / `defer` / `reject` / `external-gap` / `existing-additional-candidate` |

`confirmed-for-scope` はカード全体の無条件な正しさを意味しない。`confirmed_scope` に書かれた範囲だけが確認済みである。

`source_layers[]` は出典カテゴリだけを表す。URL・版・ライセンス・claim scope・確認結果は `source-verification-backlog.md` の `source_records` で管理する。旧フィールド名 `source_refs` は研究カードのフィールドとしては使わない。

## 調査レーン

| レーン | v3範囲 | 主な既存参照先 | 初期判断 |
| --- | --- | --- | --- |
| テスト技法・オラクル問題 | R1/R4/R5/R9 | `test-techniques/`, `test-techniques-skill-catalog.md`, `test-technique-status-assessment.csv` | 既存IDへ `merge` が中心。delta debugging は研究候補。 |
| テスト設計・テストプロセス | R6/R9 | `testing-standards-and-assurance-concepts.md`, `test-process-research-summary-test-design.md` | 既存docsへ薄く補強。 |
| 品質モデル・品質マネジメント | R14/R6 | `quality-models/`, `quality-management/` | ISO 25010等は版確認を前提に `merge`。 |
| 概念モデリング・状態モデル | R2/R3 | `quality-models/`, `test-techniques/` | 出典確認不足のため `defer`。 |
| AI/ML/LLM品質 | R7/R8/R16 | `ai-system-quality-model.md`, `ai-governance-regulation-audit.md` | Phase 2は薄い `merge`、専用文書はPhase 3候補。 |
| セキュリティ・サプライチェーン | R10/R11 | `secure-development-and-supply-chain.md` | 既存docsへ `merge`。VEX/reachability等は確認待ち。 |
| ドメイン別品質・安全規格 | R13 | `domain-specific-quality-and-safety-standards.md` | 既存docsへ `merge` または `defer`。 |
| 運用品質・探索的テスト・実機検証 | R12 | `operations-quality/`, `exploratory-testing/`, `human-centered-quality/` | 既存docsへ薄く分配。 |
| HQW外補完 | R15 | `_research` 内のみ | `external-gap`。正典カテゴリへ直置きしない。 |

## PR分割

| PR | 内容 | Phase 2への影響 |
| --- | --- | --- |
| PR1 | v3移動、研究README追加、v3注意書き、`docs/README.md` 更新、参照確認ログ | なし |
| PR2 | 全件skeleton、重要候補詳細カード、分配表、一次情報確認backlog | なし |
| PR3 | test-techniques既存IDへの薄い補強 | #7-#14 skill作成のクリティカルパスに入れない |
| PR4 | AI/LLM、セキュリティ、SBOMの既存docsへの薄い補強 | #7-#14 skill作成のクリティカルパスに入れない |
| PR5以降 | `knowledge/` 派生物の同期 | canonical docs更新後のみ |

Phase 2の正規スコープは、残り8スキル、3不足ナレッジ文書、ゲート委譲、テスト空間マトリクス描画で固定する。この研究作業はスコープ追加ではない。

## 受入確認

- `_research` README が非正典・一時調査・skills非参照・`knowledge/`非同期を明記している。
- v3に Research Index Only の注意書きがある。
- `knowledge-candidate-register.md` の全skeletonに `origin_layer`, `verification_state`, `KB登録判断`, `推奨処理先`, `次アクション` がある。
- `source-verification-backlog.md` に `checked_at`, `official_url`, `version_or_edition`, `license_note`, `claim_scope`, `verification_result` がある。
- `docs/_external-gaps/` の出現は、v3原文または廃止された配置案の説明だけである。
- `_research` は skills の `knowledge_refs` から直接参照されない。
