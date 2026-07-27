# ODC 欠陥タクソノミー調査レーン

作成日: 2026-07-27

このレーンは、D-012 ウェーブ2の #10 defect-analysis-rca の前提ナレッジ文書 `docs/quality-management/defect-taxonomy-odc.md`（ODC・欠陥トリガー/impact 属性・欠陥密度分析）を作成するための出典調査 intake である。[ハブ §1 不足領域リスト](../../agent-ecosystem/skill-ecosystem-design-plan.md#不足領域リスト)が「欠陥分類タクソノミー（ODC）: 未収録。Phase 2 で新規文書化」と指定する領域に対応する。

`docs/_research/` の共通ルール（research ID と canonical ID の分離、研究カードから直接本文化しない、`source_records` での出典検証、license-safe paraphrase での昇格）は [\_research/README.md](../README.md) に従う。フィールド定義は [software-quality-technique-research のレジスタ](../software-quality-technique-research/knowledge-candidate-register.md)と同じものを使う。

## 研究カード

| research_id | 対象領域 | origin_layer | source_layers[] | verification_state | confirmed_scope | KB登録判断 | 推奨処理先 | 次アクション |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RC-ODC-001 | ODC の概念・8属性・値定義・分析パターン | external-gap | paper, official-guidance | confirmed-for-scope | 下記 source_records の verified 行に記載の範囲（ODC v5.2 の8属性と全値・activity→trigger 対応・field defect 適応、1992年原論文の書誌と概念枠組み、RCA との補完関係、テスト改善事例の書誌） | adopt | `docs/quality-management/defect-taxonomy-odc.md` | 昇格済み（本レーンと同一 PR の canonical doc を参照） |
| RC-ODC-002 | 欠陥分類の標準系譜（IEEE 1044） | external-gap | primary-standard | confirmed-for-scope | 公開ページで確認できる範囲（標準の目的・status = inactive-reserved・1993年版の置き換え）。本文定義は要ライセンスのため採用しない | merge | `docs/quality-management/defect-taxonomy-odc.md`（系譜の言及のみ） | 昇格済み。本文詳細が必要になった場合は licensed-text-needed として再起票する |

## source_records

| item | source_type | checked_at | official_url | version_or_edition | license_note | claim_scope | verification_result | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Orthogonal Defect Classification v 5.2 for Software Design and Code | official-guidance | 2026-07-27 | https://s3.us.cloud-object-storage.appdomain.cloud/res-files/70-ODC-5-2.pdf （[chillarege.com/odc.html](https://www.chillarege.com/odc.html) からリンク） | v5.2（2013-09-12） | © IBM。「general interest and informational purposes only」で公開。長文引用はせず、属性・値の列挙と license-safe paraphrase に留める | opener 3属性（Activity/Trigger/Impact）と closer 5属性（Target/Defect Type/Qualifier/Source/Age）の定義と全値、activity→trigger 対応（activity は組織定義・trigger は再定義禁止）、field defect 分類の適応手順、Blocked Test の顧客報告欠陥への不適用 | confirmed-for-scope（2026-07-27 に PDF 全文を確認） | canonical doc へ昇格済み |
| Chillarege et al., "Orthogonal Defect Classification - A Concept for In-Process Measurements" | paper | 2026-07-27 | https://doi.org/10.1109/32.177364 | IEEE TSE 18(11) 943-956, 1992 | IEEE 著作権。本文の再配布はしない。概念の paraphrase のみ | 書誌事項（v5.2 参考文献[1]と DOI ページで確認）、ODC の概念枠組み（欠陥タイプ分布から工程シグネチャを読む in-process 測定、opener/closer の2時点、直交性の要件）は v5.2 文書・chillarege.com の公式解説の記載範囲で確認 | confirmed-for-scope | canonical doc へ昇格済み |
| Chillarege, "ODC - a 10x for Root Cause Analysis" | official-guidance | 2026-07-27 | http://chillarege.com/articles/odc-10x-root-cause-analysis.html | 2006 | 著者公開記事。要旨の paraphrase に留める | 抽象度を上げ分析を体系化することで、古典的 RCA に対し時間と欠陥ストリームのカバレッジの両面で一桁の生産性向上を狙うという位置づけ（タイトルと公開アブストラクトの範囲） | confirmed-for-scope | canonical doc へ昇格済み（RCA との補完関係の節） |
| Butcher, Munro, Kratschmer, "Improving software testing via ODC: Three case studies" | paper | 2026-07-27 | https://doi.org/10.1147/sj.411.0031 | IBM Systems Journal 41(1) 31-44, 2002 | IBM/IEEE 著作権。事例の詳細は再記述せず、trigger 分布によるテスト戦略診断という主旨の言及に留める | 書誌事項と、trigger 分布の分析からテスト戦略の弱点を特定・是正した3事例という主旨（公開アブストラクトと v5.2 参考文献[3]の範囲） | confirmed-for-scope | canonical doc へ昇格済み（分析パターンの節） |
| IEEE 1044-2009, Standard Classification for Software Anomalies | primary-standard | 2026-07-27 | https://standards.ieee.org/ieee/1044/4607/ | 2009（inactive-reserved。2020-03-05 に inactivate、1044-1993 を置き換え） | IEEE 標準本文は要ライセンス。公開ページで status・目的のみ確認 | ソフトウェア異常分類の統一アプローチという目的、および現行 status | confirmed-for-scope（公開ページの範囲） | canonical doc へ昇格済み（標準系譜の言及のみ。本文定義は不採用） |

## 既存 docs との重複確認（昇格フロー手順4）

- ODC 本体は既存 docs に未収録。2026-07-27 に `grep -ri "orthogonal defect|ODC" docs/` で確認した結果、本レーン以外のヒットは agent-ecosystem 2文書（不足領域リスト・phase2 ガイドの計画記述）と部分文字列の誤ヒット1件のみで、domain canon 側に定義記述は無い（[ハブ §1 不足領域リスト](../../agent-ecosystem/skill-ecosystem-design-plan.md#不足領域リスト)の記載どおり）。
- 欠陥密度の定義・実務式は [software-quality-management-practical-reference.md](../../quality-management/software-quality-management-practical-reference.md)、件数・密度メトリクスの誤用は [quality-metrics-pitfalls.md](../../quality-management/quality-metrics-pitfalls.md) が既にカバーする。canonical doc はこれらを参照し再定義しない。
- FTA・STPA 等の hazard analysis 手法は [domain-specific-quality-and-safety-standards.md](../../governance-compliance/domain-specific-quality-and-safety-standards.md)、ブレームレスポストモーテムは [production-quality-sre-observability.md](../../operations-quality/production-quality-sre-observability.md) が既にカバーする。RCA 手法の再記述はしない。
- 欠陥候補の抽出（テスト実行結果からの入力側）は skills/test-execution-support の `DefectCandidateList` が既に定義しており、canonical doc は分類・分析側のみを扱う。

## 関連ドキュメント

- [\_research/README.md](../README.md) — intake の共通ルールと昇格フロー
- [defect-taxonomy-odc.md](../../quality-management/defect-taxonomy-odc.md) — 本レーンから昇格した canonical doc
