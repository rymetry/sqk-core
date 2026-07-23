# Distribution Matrix

この表は、v3研究候補を既存docsへ分配するための作業表である。ここでの分配先は候補であり、一次情報確認と既存docs確認後に確定する。

## Research Lane Distribution

| レーン | v3範囲 | 初期判断 | 既存docs候補 | Phase扱い |
| --- | --- | --- | --- | --- |
| テスト技法・オラクル | R1/R4/R5/R9 | 既存IDへ `merge` | `docs/test-techniques/test-techniques-skill-catalog.md`, `docs/test-techniques/testing-standards-and-assurance-concepts.md`, `docs/test-techniques/test-technique-status-assessment.csv` | PR3。Phase 2クリティカルパス外。 |
| テスト設計・プロセス | R6/R9 | 既存docsへ薄い補強 | `docs/test-techniques/test-process-research-summary-test-design.md`, `docs/quality-management/software-quality-gap-analysis-report.md` | PR3。 |
| 品質モデル・品質管理 | R14/R6 | 既存docs/mappingへ `merge` | `docs/quality-models/iso25010-product-quality-model.md`, `docs/quality-management/` | docs確定後にknowledge同期。 |
| 概念・状態モデル | R2/R3 | `defer` | `docs/quality-models/`, `docs/test-techniques/` | Phase 3以降候補。 |
| AI/ML/LLM品質 | R7/R8/R16 | 既存AI docsへ薄い `merge` | `docs/quality-models/ai-system-quality-model.md`, `docs/governance-compliance/ai-governance-regulation-audit.md` | PR4。専用文書はPhase 3候補。 |
| セキュリティ/SBOM | R10/R11 | 既存secure-developmentへ `merge` | `docs/secure-development/secure-development-and-supply-chain.md` | PR4。 |
| ドメイン安全規格 | R13 | 既存domain docsへ `merge` | `docs/governance-compliance/domain-specific-quality-and-safety-standards.md` | PR4以降。 |
| 運用品質・探索・実機 | R12 | 複数既存docsへ分配 | `docs/operations-quality/`, `docs/exploratory-testing/`, `docs/human-centered-quality/` | PR4以降。 |
| HQW外補完 | R15 | `external-gap` | `_research` only | Phase未割当。 |

## Phase 2 Boundary

Phase 2の正規スコープは次のまま固定する。

- 残り8スキル #7-#14
- 不足ナレッジ文書3件
- quality-artifact-reviewへのゲート委譲
- テスト空間マトリクス描画

この研究作業は、Phase 2のスコープを増やさない。PR3/PR4は、既存docsの薄い補強だけを行い、#7-#14 skill作成のクリティカルパスには入れない。

## `knowledge/` Synchronization

`knowledge/` は `docs/` から抽出した派生物である。次の順序を守る。

1. `_research` で候補を整理する。
2. 一次情報確認済みの内容だけをcanonical docsへ入れる。
3. canonical docs側の見出し・用語・マッピングが確定した後、`knowledge/index.md`, `knowledge/terminology/term-map.yaml`, `knowledge/mappings/` の影響を確認する。
4. `knowledge/` は研究カードから直接更新しない。

## Explicit Non-Targets

| 対象 | 判断 | 理由 |
| --- | --- | --- |
| v3本文のveridia実装候補 | reject | 本repoのKB登録対象外。 |
| `docs/_external-gaps/` トップレベル作成 | reject | 既存docs体系にない。HQW外候補は `_research` 内に隔離。 |
| `_research` をskills `knowledge_refs` に入れる | reject | 未検証候補をskillsに参照させない。 |
| Phase 2スキル計画の変更 | reject | Phase 2スコープは既に固定済み。 |
| v3から `knowledge/` へ直接同期 | reject | `knowledge/` は正典docsの派生物。 |
