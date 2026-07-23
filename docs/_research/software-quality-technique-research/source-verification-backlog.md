# Source Verification Backlog

このbacklogは、研究カードをcanonical docsへ移す前に確認すべき一次情報・規格・論文・公式実装を管理するためのもの。`not-yet-checked` は未確認を意味し、確認済みを装わない。

この表を `source_records` と呼び、各行を source record として扱う。研究カード側の `source_layers[]` が出典カテゴリだけを表すのに対し、source record は `official_url`, `version_or_edition`, `license_note`, `claim_scope`, `verification_result` を持ち、canonical docs へ移す前の確認単位になる。

| item | source_type | checked_at | official_url | version_or_edition | license_note | claim_scope | verification_result | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ISO/IEC 25010 product quality model | primary-standard | not-yet-checked | https://www.iso.org/standard/78176.html | 2023 | ISO本文は要ライセンス。公開ページは版・範囲確認のみ。 | 2023年版の品質モデル、2011年版との差分 | needs-official-check | 公開ページで版を確認し、詳細定義は長文引用しない。 |
| ISO/IEC/IEEE 29119-4 test techniques | primary-standard | not-yet-checked | https://www.iso.org/standard/79430.html | 2021 | ISO本文は要ライセンス。 | テスト設計技法の標準上の範囲 | needs-official-check | 既存test-techniques文書の出典範囲と照合。 |
| IEEE 1012 V&V | primary-standard | not-yet-checked | https://standards.ieee.org/ieee/1012/7324/ | 2024 | 標準本文は要ライセンス。 | V&V/IV&V、レビュー・評価・テストの関係 | needs-official-check | R6候補の根拠範囲を確認。 |
| ISTQB CTFL v4.0 | official-guidance | not-yet-checked | https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/ | v4.0 / v4.0.1 syllabus | 公開シラバス範囲で要約。 | テストレベル、技法、保守、独立性 | needs-official-check | 既存docsとの用語差分を確認。 |
| Barr et al. Oracle Problem survey | paper | not-yet-checked | https://doi.org/10.1109/TSE.2014.2372785 | 2015 | 論文本文はライセンスに従う。 | テストオラクル問題の分類 | needs-official-check | `ORA-01` 補強範囲を確認。 |
| QuickCheck | paper | not-yet-checked | https://doi.org/10.1145/357766.351266 | 2000 | ACM本文はライセンスに従う。 | property-based testingの原典 | needs-official-check | `PROP-01` の出典整理。 |
| Hypothesis | official-tool-doc | not-yet-checked | https://hypothesis.readthedocs.io/en/latest/ | current docs | 公式docsの要約に留める。 | PBT実装例、生成・縮小・再現性 | needs-official-check | `PROP-01` 実装例として確認。 |
| Metamorphic testing surveys | paper | not-yet-checked | unknown | unknown | 論文本文はライセンスに従う。 | metamorphic relationと適用条件 | needs-official-check | DOI/公式ページを確定する。 |
| Mutation testing survey | paper | not-yet-checked | https://doi.org/10.1109/TSE.2010.62 | 2011 | 論文本文はライセンスに従う。 | mutation testingとmutation scoreの限界 | needs-official-check | `FAULT-02` 補強範囲を確認。 |
| Stryker | official-tool-doc | not-yet-checked | https://stryker-mutator.io/docs/ | current docs | 公式docsの要約に留める。 | mutation testing実装例 | needs-official-check | 実装例として確認。 |
| AFL++ | official-tool-doc | not-yet-checked | https://aflplus.plus/docs/ | current docs | 公式docsの要約に留める。 | coverage-guided fuzzing実装例 | needs-official-check | `FUZZ-*` 実装例として確認。 |
| KLEE | official-tool-doc | not-yet-checked | https://klee-se.org/ | current docs | 公式docsの要約に留める。 | symbolic execution実装例 | needs-official-check | `SYM-01` 補強範囲を確認。 |
| Delta debugging | paper | not-yet-checked | unknown | 2002 | 論文本文はライセンスに従う。 | failure-inducing input minimization | needs-official-check | `DELTA-01` 研究候補の妥当性を確認。 |
| Pact | official-tool-doc | not-yet-checked | https://pact.io/ | current docs | 公式docsの要約に留める。 | contract testing実装例 | needs-official-check | API/contract候補との重複確認。 |
| NIST AI RMF | official-guidance | not-yet-checked | https://www.nist.gov/itl/ai-risk-management-framework | 1.0 and updates | 公開資料の要約に留める。 | AIリスク管理、trustworthy AI | needs-official-check | AI/LLM候補の根拠範囲を確認。 |
| NIST SSDF SP 800-218 | official-guidance | not-yet-checked | https://csrc.nist.gov/pubs/sp/800/218/final | v1.1 | Public domain想定だが出典表記する。 | secure software development practices | needs-official-check | secure-development既存文書と照合。 |
| OWASP ASVS | official-guidance | not-yet-checked | https://owasp.org/www-project-application-security-verification-standard/ | current stable | OWASPライセンス確認。 | web application security requirements | needs-official-check | R10の要求化・テスト化範囲を確認。 |
| OWASP LLM Top 10 | official-guidance | not-yet-checked | https://genai.owasp.org/ | current | OWASPライセンス確認。 | LLM/GenAI security categories | needs-official-check | 既存docsの版表記と照合。 |
| NTIA SBOM | official-guidance | not-yet-checked | https://www.ntia.gov/page/software-bill-materials | current page | 公開資料の要約に留める。 | SBOM minimum elements and format context | needs-official-check | R11/SBOM記述の根拠範囲を確認。 |
| CycloneDX | official-tool-doc | not-yet-checked | https://cyclonedx.org/specification/overview/ | current spec | 公式docsの要約に留める。 | SBOM/VEX/AI-BOM等の仕様範囲 | needs-official-check | version_or_editionをPR時点で確認。 |
| SPDX | official-guidance | not-yet-checked | https://spdx.dev/ | current | ライセンス確認。 | SBOM format and ISO/IEC 5962 relation | needs-official-check | SPDXの現行仕様とISO関係を確認。 |
| ISO 26262 | primary-standard | not-yet-checked | https://www.iso.org/standard/68383.html | 2018 | ISO本文は要ライセンス。 | automotive functional safety | needs-official-check | R13の版確認。 |
| ISO/SAE 21434 | primary-standard | not-yet-checked | https://www.iso.org/standard/70918.html | 2021 | ISO本文は要ライセンス。 | automotive cybersecurity engineering | needs-official-check | R13/R10の接続を確認。 |
| ISO 21448 SOTIF | primary-standard | not-yet-checked | https://www.iso.org/standard/77490.html | 2022 | ISO本文は要ライセンス。 | intended functionality safety | needs-official-check | SOTIFとISO 26262の境界を確認。 |
