# Knowledge Candidate Register

このレジスタは、v3から抽出された知識候補を正典化前に管理するためのものである。ここに載っている候補は採用済みではない。

## Field Definitions

| フィールド | 説明 |
| --- | --- |
| `research_id` | 研究内ID。canonical ID と混同しない。 |
| `origin_layer` | `hqw-article` または `external-gap`。 |
| `source_layers[]` | 確認候補の出典レイヤ。複数可。 |
| `verification_state` | 現在の確認状態。 |
| `confirmed_scope` | 確認済み範囲。未確認なら `unknown`。 |
| `KB登録判断` | `adopt` / `merge` / `defer` / `reject` / `external-gap` / `existing-additional-candidate`。 |
| `推奨処理先` | canonical docs への分配先を第一に書く。`knowledge/` / `schemas/` / `skills/` が出る場合は、canonical docs 昇格後の派生影響候補・schema影響候補・非採用判断としてだけ扱い、research から直接登録しない。 |
| `次アクション` | 次のPRまたは調査作業。 |

## Theme Skeletons

| research_id | v3入口 | origin_layer | source_layers[] | verification_state | confirmed_scope | KB登録判断 | 推奨処理先 | 次アクション |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RC-HQW-R1-001 | R1 Oracle Problem対応技法 | hqw-article | existing-doc, paper, official-tool-doc | partially-checked | 既存カタログに多くの技法IDが存在する範囲 | merge | `docs/test-techniques/` | `ORA-01`, `PROP-01`, `META-01`, `DIFF-01`, `FAULT-02`, `FUZZ-*`, `SYM-01`, `CONC-01` への補強差分を設計する。 |
| RC-HQW-R2-001 | R2 概念モデルとsource grounding | hqw-article | paper, official-tool-doc | not-yet-triaged | unknown | defer | unknown | UML/xtUML/OAL/SHACL/DTDL等の一次情報確認後に分類する。 |
| RC-HQW-R3-001 | R3 状態・イベント・entry action | hqw-article | paper, official-tool-doc, existing-doc | not-yet-triaged | unknown | defer | `docs/test-techniques/` or `docs/quality-models/` | MBT/状態遷移テスト既存記述との重複を確認する。 |
| RC-HQW-R4-001 | R4 カバレッジ拡張 | hqw-article | primary-standard, existing-doc | partially-checked | 既存docsにcoverage限界とWB系IDがある範囲 | merge | `docs/test-techniques/` | coverageを品質保証そのものにしない注意を既存docsへ薄く補強する。 |
| RC-HQW-R5-001 | R5 API・契約・スキーマ駆動テスト | hqw-article | official-tool-doc, existing-doc | partially-checked | Pact等は公式実装例として確認対象にできる範囲 | merge | `docs/test-techniques/` | 既存契約/API技法との重複確認を行う。 |
| RC-HQW-R6-001 | R6 UAT・BDD・V&V・レビュー証跡 | hqw-article | primary-standard, official-guidance, existing-doc | needs-official-check | unknown | merge | `docs/test-techniques/`, `docs/quality-management/` | IEEE 1012/レビュー規格の確認範囲をsource backlogで確定する。 |
| RC-HQW-R7-001 | R7 RAG/LLM groundedness | hqw-article | official-guidance, paper, existing-doc | partially-checked | 既存AI品質モデルにRAG/groundedness項目がある範囲 | merge | `docs/quality-models/ai-system-quality-model.md` | Phase 2では薄い補強に留め、専用文書はPhase 3候補にする。 |
| RC-HQW-R8-001 | R8 教師データ・評価セット・ML品質 | hqw-article | primary-standard, paper, official-tool-doc, existing-doc | needs-official-check | unknown | defer | `docs/quality-models/` | ISO/IEC 25012/25059/5259系と既存AI品質文書の範囲を確認する。 |
| RC-HQW-R9-001 | R9 回帰テスト選択・スイート管理 | hqw-article | paper, existing-doc | partially-checked | `REG-*` が既存カタログに存在する範囲 | merge | `docs/test-techniques/` | suite management全体を既存REG群へ接続する。 |
| RC-HQW-R10-001 | R10 セキュリティ検証 | hqw-article | official-guidance, existing-doc | partially-checked | 既存secure-development docsにSAST/DAST/SCA/ASVS等がある範囲 | merge | `docs/secure-development/secure-development-and-supply-chain.md` | OWASP/NISTの版と範囲を確認して薄く補強する。 |
| RC-HQW-R11-001 | R11 SBOMと継続監視 | hqw-article | official-guidance, existing-doc | partially-checked | 既存secure-development docsにSBOM/SCA/VEX周辺がある範囲 | merge | `docs/secure-development/secure-development-and-supply-chain.md` | VEX/reachability/ML-BOMはsource backlogで確認する。 |
| RC-HQW-R12-001 | R12 性能・実機・探索的・モンキー | hqw-article | official-tool-doc, official-guidance, existing-doc | partially-checked | 既存operations/exploratory/human-centered docsに接続先がある範囲 | merge | `docs/operations-quality/`, `docs/exploratory-testing/`, `docs/human-centered-quality/` | 運用品質・探索的・端末実機の分配粒度を確定する。 |
| RC-HQW-R13-001 | R13 車載・OT・組込み | hqw-article | primary-standard, official-guidance, existing-doc | needs-official-check | unknown | merge | `docs/governance-compliance/domain-specific-quality-and-safety-standards.md` | ISO 26262/21434/SOTIF/IEC 62443の版確認を行う。 |
| RC-HQW-R14-001 | R14 ISO/IEC 25010 2011/2023 | hqw-article | primary-standard, existing-doc | partially-checked | 既存docsとmappingが存在する範囲 | merge | canonical: `docs/quality-models/iso25010-product-quality-model.md`; derived impact: `knowledge/mappings/iso25010-2011-2023.yaml` | docs側の変更がある場合のみknowledge mapping同期を検討する。 |
| RC-EXT-R15-001 | R15 HQW外補完候補 | external-gap | primary-standard, official-tool-doc, existing-doc | not-yet-triaged | unknown | external-gap | `_research` only | HQW由来候補と混ぜず、候補ごとに分割する。 |
| RC-HQW-R16-001 | R16 human-agent delegation | hqw-article | official-guidance, existing-doc | partially-checked | 既存AIガバナンス文書にhuman oversight/agent traceがある範囲 | merge | `docs/governance-compliance/ai-governance-regulation-audit.md` | HumanDecisionBoundary等は実装仕様でなく品質運用概念として扱う。 |

## v3 Section 3 Candidate Skeletons

| research_id | v3登録候補 | origin_layer | source_layers[] | verification_state | confirmed_scope | KB登録判断 | 推奨処理先 | 次アクション |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RC-HQW-K1-001 | `docs/test-techniques/oracle-problem-techniques.md` | hqw-article | existing-doc, paper, official-tool-doc | partially-checked | 既存オラクル/自動生成系IDの存在 | merge | 既存 `test-techniques` | 新規文書化前に既存 `ORA-01` と技法カードへ分配する。 |
| RC-HQW-K2-001 | `docs/test-techniques/state-event-model-based-testing.md` | hqw-article | existing-doc, paper, official-tool-doc | not-yet-triaged | unknown | defer | unknown | MBT/状態遷移既存記述と一次情報確認を行う。 |
| RC-HQW-K3-001 | `docs/test-techniques/coverage-selection-and-limits.md` | hqw-article | existing-doc, primary-standard | partially-checked | 既存coverage限界記述の存在 | merge | 既存 `testing-standards-and-assurance-concepts.md` | coverage限界の薄い補強に留める。 |
| RC-HQW-K4-001 | `docs/test-techniques/api-contract-schema-testing.md` | hqw-article | existing-doc, official-tool-doc | partially-checked | 既存API/契約技法への接続可能性 | merge | 既存 `test-techniques` | OpenAPI/Pact/Schemathesisの公式確認を行う。 |
| RC-HQW-K5-001 | `docs/test-techniques/uat-bdd-vv-evidence.md` | hqw-article | existing-doc, primary-standard, official-guidance | needs-official-check | unknown | merge | 既存 `test-techniques` and `quality-management` | V&V/レビュー規格確認後に分配する。 |
| RC-HQW-K6-001 | `docs/test-techniques/regression-suite-management.md` | hqw-article | existing-doc, paper | partially-checked | 既存 `REG-*` の存在 | merge | 既存 `REG-*` | REG群を束ねる追記で足りるか確認する。 |
| RC-HQW-K7-001 | `docs/test-techniques/test-automation-readiness.md` | hqw-article | existing-doc, official-tool-doc | not-yet-triaged | unknown | defer | unknown | 既存flaky/E2E/automation記述との重複を確認する。 |
| RC-HQW-K8-001 | `docs/test-techniques/performance-load-testing.md` | hqw-article | existing-doc, official-tool-doc, official-guidance | partially-checked | 既存operations-qualityへの分配先 | merge | `docs/operations-quality/` | performance testingは運用品質へ分配する。 |
| RC-HQW-K9-001 | `docs/test-techniques/rag-source-grounding-evaluation.md` | hqw-article | existing-doc, paper, official-guidance | partially-checked | 既存AI品質モデルのRAG項目 | defer | Phase 3 candidate | Phase 2では既存AI品質モデルへの薄い補強のみ。 |
| RC-HQW-K10-001 | `docs/test-techniques/llm-grader-human-calibration.md` | hqw-article | existing-doc, paper, official-guidance | partially-checked | `ADD-LLM-09` と `LLM-04` の存在 | existing-additional-candidate | `ADD-LLM-09`, `LLM-04` | 既存追加候補として扱い、新規IDを作らない。 |
| RC-HQW-K11-001 | `docs/quality-models/iso-25010-2011-2023-quality-taxonomy.md` | hqw-article | existing-doc, primary-standard | partially-checked | 既存ISO 25010 doc and mappingの存在 | merge | 既存ISO 25010 doc and mapping | 新規文書ではなく既存docs/mappingへ同期判断。 |
| RC-HQW-K12-001 | `docs/quality-models/conceptual-information-model-schema.md` | hqw-article | paper, official-tool-doc | not-yet-triaged | unknown | defer | unknown | 概念モデリング一次情報確認後に再分類する。 |
| RC-HQW-K13-001 | `docs/quality-models/ai-data-and-model-quality.md` | hqw-article | existing-doc, primary-standard, paper, official-tool-doc | needs-official-check | unknown | defer | Phase 3 candidate | ISO/AI data品質出典確認後に判断する。 |
| RC-HQW-K14-001 | `docs/secure-development/secure-development-and-supply-chain.md` | hqw-article | existing-doc, official-guidance | partially-checked | 既存secure-development docの存在 | merge | 既存secure-development doc | 既存文書へ薄く補強する。 |
| RC-HQW-K15-001 | `docs/governance-compliance/domain-specific-quality-and-safety-standards.md` | hqw-article | existing-doc, primary-standard, official-guidance | needs-official-check | unknown | merge | 既存domain-specific doc | 車載/OT規格の版確認を行う。 |
| RC-HQW-K16-001 | `docs/governance-compliance/ai-governance-and-risk-management.md` | hqw-article | existing-doc, official-guidance | partially-checked | 既存AI governance docの存在 | merge | 既存AI governance doc | 新規文書化せず既存文書の範囲確認。 |
| RC-HQW-K17-001 | `docs/quality-management/sqa-qc-third-party-verification.md` | hqw-article | existing-doc, primary-standard, official-guidance | needs-official-check | unknown | defer | unknown | QA/QC/SQA/第三者検証の既存doc重複を確認する。 |
| RC-HQW-K18-001 | `docs/operations-quality/continuous-quality-operations.md` | hqw-article | existing-doc, official-guidance | partially-checked | 既存operations-quality docの存在 | merge | 既存operations-quality doc | 新規文書でなく既存SRE/operationsへ薄く補強。 |
| RC-HQW-K19-001 | `docs/human-centered-quality/uat-device-experience-quality.md` | hqw-article | existing-doc, official-guidance | partially-checked | 既存human-centered docの存在 | merge | 既存human-centered doc | UAT/実機を既存利用時品質文脈へ分配。 |
| RC-HQW-K20-001 | `knowledge/terminology/term-map.yaml` | hqw-article | existing-doc | not-yet-triaged | unknown | defer | canonical: TBD; derived impact: `knowledge/terminology/term-map.yaml` | canonical docs更新後にだけ同期する。 |
| RC-HQW-K21-001 | `knowledge/mappings/` | hqw-article | existing-doc | not-yet-triaged | unknown | defer | canonical: TBD; derived impact: `knowledge/mappings/` | docs側で正典化した写像だけ派生物化する。 |
| RC-HQW-K22-001 | `schemas/*.schema.json` | hqw-article | existing-doc | not-yet-triaged | unknown | defer | canonical/design: TBD; schema impact: `schemas/` | Phase 2の既存スキーマ計画と衝突しないよう保留。 |
| RC-HQW-K23-001 | `skills/*` | hqw-article | existing-doc | not-yet-triaged | unknown | reject | none | `_research` をskillsの `knowledge_refs` へ直接入れない。 |
| RC-EXT-K24-001 | `docs/_external-gaps/` | external-gap | primary-standard, official-tool-doc, existing-doc | not-yet-triaged | unknown | external-gap | `_research` only | 旧配置案として扱い、トップレベルカテゴリは作らない。 |

## Detailed Cards

### RC-HQW-R1-001 Oracle Problem対応技法

- v3上の入口:
  - 研究テーマ: R1
  - 記事No: No.12, 25, 31, 45, 50, 57, 62, 64
  - 現在の登録先候補: `docs/test-techniques/oracle-problem-techniques.md`
- 既存docsとの関係:
  - 既存で十分: `ORA-01`, `PROP-01`, `META-01`, `DIFF-01`, `FAULT-02`, `FUZZ-*`, `SYM-01`, `CONC-01` は既存カタログにある。
  - 追記が必要: delta debugging、oracle-aware coverage、各技法の誤用リスク。
  - 新規文書が必要: 現時点では未決定。まず既存IDへ `merge`。
- 一次情報・規格・論文:
  - [要確認] Barr et al. Oracle Problem survey, DOI/著者版PDF範囲
  - [要確認] QuickCheck, Hypothesis docs, Segura/Chen metamorphic testing, Jia & Harman mutation testing
  - [要確認] Zeller delta debugging, AFL++/Fuzzing Book, KLEE/SAGE
- 実装例・ツール:
  - Hypothesis, AFL++, Stryker, KLEE
- KB登録判断:
  - `merge`
- 推奨処理先:
  - docs path: `docs/test-techniques/test-techniques-skill-catalog.md`, `docs/test-techniques/testing-standards-and-assurance-concepts.md`
  - 派生影響候補: 後続PRで `knowledge/terminology/term-map.yaml` 影響確認
  - schema影響候補: なし
- 注意点:
  - coverageやmutation scoreを品質保証そのものにしない。
  - differential testingの差分を即欠陥扱いしない。
  - metamorphic relationやpropertyは妥当性レビューが必要。
- 次アクション:
  - PR3で既存IDに出典確認状態と誤用リスクを薄く追記する。

### RC-HQW-R7-001 RAG/LLM groundedness

- v3上の入口:
  - 研究テーマ: R7
  - 記事No: No.19, 21, 23, 37, 39, 13, 64
  - 現在の登録先候補: `docs/test-techniques/rag-source-grounding-evaluation.md`
- 既存docsとの関係:
  - 既存で十分: `docs/quality-models/ai-system-quality-model.md` にRAG品質、groundedness、LLM-as-a-judgeの核がある。
  - 追記が必要: grounding source granularity、unsupported claim rate、unknown/abstention accuracy、judge校正履歴。
  - 新規文書が必要: Phase 2では不要。Phase 3候補。
- 一次情報・規格・論文:
  - [要確認] NIST AI RMF, NIST GenAI profile, Ragas, MT-Bench/Chatbot Arena
- 実装例・ツール:
  - Ragas, DeepEval等は公式ドキュメント確認後に扱う。
- KB登録判断:
  - `merge`
- 推奨処理先:
  - docs path: `docs/quality-models/ai-system-quality-model.md`, `docs/governance-compliance/ai-governance-regulation-audit.md`
  - 派生影響候補: 後続PRでterm-map影響確認
  - schema影響候補: なし
- 注意点:
  - LLM-as-a-judgeは評価者自体のバイアスと校正を切り離す。
  - RAG groundednessは検索品質と生成忠実性を混同しない。
- 次アクション:
  - PR4で既存AI品質文書への薄い補強に限定する。

### RC-HQW-K10-001 LLM-as-Judge Calibration

- v3上の入口:
  - 研究テーマ: R7/R16
  - 記事No: No.23, 64, 19
  - 現在の登録先候補: `docs/test-techniques/llm-grader-human-calibration.md`
- 既存docsとの関係:
  - 既存で十分: `LLM-04` と `ADD-LLM-09` が既に存在する。
  - 追記が必要: human label、rubric version、judge model version、swap test、評価者間一致。
  - 新規文書が必要: Phase 2では不要。Phase 3候補。
- 一次情報・規格・論文:
  - [要確認] MT-Bench/Chatbot Arena, LLM-as-a-judge bias papers, NIST AI RMF
- 実装例・ツール:
  - 評価ハーネス/校正セットは実装例として扱い、標準と混同しない。
- KB登録判断:
  - `existing-additional-candidate`
- 推奨処理先:
  - docs path: `docs/test-techniques/test-technique-status-assessment.csv`, `docs/quality-models/ai-system-quality-model.md`
  - 派生影響候補: 後続PRでterm-map影響確認
  - schema影響候補: なし
- 注意点:
  - `ADD-LLM-09` を新規研究IDとして再発明しない。
- 次アクション:
  - PR4で既存追加候補として扱う。

### RC-HQW-R10-001 / RC-HQW-R11-001 Security and SBOM

- v3上の入口:
  - 研究テーマ: R10/R11
  - 記事No: No.48, 55, 59, 63, 74, 75, 77, 19
  - 現在の登録先候補: `docs/secure-development/secure-development-and-supply-chain.md`
- 既存docsとの関係:
  - 既存で十分: SSDF、OWASP、SAST/DAST/SCA、SBOM、SLSA、provenanceは既存文書にある。
  - 追記が必要: VEX/reachability、ML-BOM、リリース後継続監視の粒度。
  - 新規文書が必要: 現時点では不要。
- 一次情報・規格・論文:
  - [要確認] NIST SSDF SP 800-218, OWASP ASVS, OWASP LLM Top 10, NTIA SBOM, SPDX, CycloneDX
- 実装例・ツール:
  - SCA/SBOM生成ツールは代表例として扱い、標準と混同しない。
- KB登録判断:
  - `merge`
- 推奨処理先:
  - docs path: `docs/secure-development/secure-development-and-supply-chain.md`
  - 派生影響候補: 後続PRでterm-map/mappings影響確認
  - schema影響候補: なし
- 注意点:
  - 版番号と公開日が変わりやすい。PR時点で確認日を残す。
- 次アクション:
  - PR4で既存文書の薄い補強に留める。

### RC-EXT-R15-001 HQW外補完候補

- v3上の入口:
  - 研究テーマ: R15
  - 記事No: HQW外
  - 現在の登録先候補: v3原文では `docs/_external-gaps/`
- 既存docsとの関係:
  - 既存で十分: 一部は既存docsに含まれる可能性がある。
  - 追記が必要: 候補ごとに個別判断。
  - 新規文書が必要: 現時点では不要。
- 一次情報・規格・論文:
  - [要確認] pairwise/ACTS/PICT, classification tree, chaos engineering, WCAG, test data management等
- 実装例・ツール:
  - 公式ツール・標準団体情報を優先する。
- KB登録判断:
  - `external-gap`
- 推奨処理先:
  - docs path: `_research` only
  - 派生影響候補: なし
  - schema影響候補: なし
- 注意点:
  - HQW由来候補と混ぜない。
  - `docs/_external-gaps/` は未採用の旧配置案として扱う。
- 次アクション:
  - 候補を分割し、既存docsとの重複確認後に個別PR化する。
