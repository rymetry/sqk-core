# 事業品質メトリクス（VOC・NPS・チャーン・LTV）調査レーン

作成日: 2026-07-28

このレーンは、D-012 ウェーブ3の #15 business-quality-metrics の前提ナレッジ文書 `docs/quality-management/business-quality-metrics-methods.md`（VOC・NPS・チャーン・LTV と品質シグナルの相関分析手法）を作成するための出典調査 intake である。[ハブ §1 不足領域リスト](../../agent-ecosystem/skill-ecosystem-design-plan.md#不足領域リスト)が「VOC・NPS・チャーン・LTV相関分析手法 — 最薄領域。SUS/NPS/CSAT は human-centered-quality に部分収録のみ」と指定する領域に対応する。P3 据え置きの解除は [DECISIONS.md D-012](../../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ) による。

`docs/_research/` の共通ルール（research ID と canonical ID の分離、研究カードから直接本文化しない、`source_records` での出典検証、license-safe paraphrase での昇格）は [\_research/README.md](../README.md) に従う。フィールド定義は [software-quality-technique-research のレジスタ](../software-quality-technique-research/knowledge-candidate-register.md)と同じものを使う。

## 研究カード

| research_id | 対象領域 | origin_layer | source_layers[] | verification_state | confirmed_scope | KB登録判断 | 推奨処理先 | 次アクション |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RC-BQM-001 | NPS の定義と成長相関の主張 | external-gap | paper | confirmed-for-scope | 下記 source_records の Reichheld 行に記載の範囲（0〜10 推奨質問、promoter/passive/detractor 区分、NPS 算式、成長との相関の原主張） | adopt | `docs/quality-management/business-quality-metrics-methods.md` | 昇格済み（本レーンと同一 PR の canonical doc を参照） |
| RC-BQM-002 | NPS 優位性の再検証（縦断研究） | external-gap | paper | confirmed-for-scope | 下記 source_records の Keiningham 行に記載の範囲（縦断データでの再現失敗の報告と書誌） | adopt | 同上（NPS の限界・単独指標にしない原則の根拠） | 昇格済み |
| RC-BQM-003 | VOC の定義と手法（ニーズの識別・構造化・優先度付け） | external-gap | paper | confirmed-for-scope | 下記 source_records の Griffin & Hauser 行に記載の範囲（VOC の3タスク、インタビュー件数とニーズ抽出の目安） | adopt | 同上 | 昇格済み |
| RC-BQM-004 | 顧客価値の割引現在価値定義とリテンションの企業価値インパクト | external-gap | paper | confirmed-for-scope | 下記 source_records の Gupta et al. 行に記載の範囲（顧客価値の定義、リテンション/マージン/獲得コスト 1% 改善の企業価値影響の実測比較） | adopt | 同上（品質→リテンション投資の説明材料） | 昇格済み |
| RC-BQM-005 | チャーン・LTV の確率モデル（sBG・BG/NBD） | external-gap | paper | confirmed-for-scope | 下記 source_records の Fader & Hardie 2行に記載の範囲（sBG によるリテンション曲線の射影、BG/NBD による非契約型の購買・生存モデル、いずれも表計算で実装可能という実務性） | adopt | 同上 | 昇格済み |
| RC-BQM-006 | GQM（Goal-Question-Metric）による測定の構造化 | external-gap | official-guidance | confirmed-for-scope | 下記 source_records の Basili et al. 行に記載の範囲（GQM の3層構造と書誌） | adopt | 同上（相関分析を Goal から下ろす枠組み。§6） | 昇格済み |

## source_records

| item | source_type | checked_at | official_url | version_or_edition | license_note | claim_scope | verification_result | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Reichheld, "The One Number You Need to Grow" | paper | 2026-07-28 | https://hbr.org/2003/12/the-one-number-you-need-to-grow | Harvard Business Review 81(12), 46-55, 2003-12 | HBR 著作権。本文の再配布はしない。定義・算式・主張の paraphrase のみ | 「友人に薦めるか」の 0〜10 質問1問が成長の最良予測子になりうるという原主張。promoter（9-10）/passive（7-8）/detractor（0-6）の区分と NPS = promoter% − detractor% の算式。購買・紹介行動と成長への接続という調査設計 | confirmed-for-scope（2026-07-28 に HBR 公式ページと複数の書誌記録で確認） | canonical doc へ昇格済み |
| Keiningham, Cooil, Andreassen, Aksoy, "A Longitudinal Examination of Net Promoter and Firm Revenue Growth" | paper | 2026-07-28 | https://doi.org/10.1509/jmkg.71.3.039 | Journal of Marketing 71(3), 39-51, 2007-07 | Sage/AMA 著作権。要旨と公表結論の paraphrase のみ | ノルウェー顧客満足バロメーターの縦断データ（21社・15,500+ インタビュー）で Net Promoter 研究の分析を追試し、他指標に対する「明確な優位性」の主張を再現できなかったという報告。2007 MSI/H. Paul Root Award 受賞 | confirmed-for-scope（2026-07-28 に DOI ページと出版社・著者所属機関の公表資料で確認） | canonical doc へ昇格済み（NPS の限界の節） |
| Griffin, Hauser, "The Voice of the Customer" | paper | 2026-07-28 | https://doi.org/10.1287/mksc.12.1.1 | Marketing Science 12(1), 1-27, 1993 | INFORMS 著作権。要旨と公表数値の paraphrase のみ | VOC を顧客ニーズの識別・構造化・優先度付けの3タスクとして定式化（QFD の VOC 要素）。セグメントが明確なら 20〜30 件のインタビューで足りるという目安、インタビューから 100〜200 のニーズ表現が得られるという目安 | confirmed-for-scope（2026-07-28 に INFORMS 公式ページと複数の書誌記録で確認） | canonical doc へ昇格済み |
| Gupta, Lehmann, Stuart, "Valuing Customers" | paper | 2026-07-28 | https://doi.org/10.1509/jmkr.41.1.7.25084 | Journal of Marketing Research 41(1), 7-18, 2004-02 | Sage/AMA 著作権。要旨と公表数値の paraphrase のみ | 顧客価値＝将来収益の割引現在価値の期待値という定義。公開データ5社での実証で、リテンション 1% 改善は企業価値を約 5% 改善（マージン 1% 改善は約 1%、獲得コスト 1% 改善は約 0.1%）し、割引率 1% の変化に対して約5倍のインパクトという比較 | confirmed-for-scope（2026-07-28 に DOI ページ・著者所属機関公開版で確認） | canonical doc へ昇格済み |
| Fader, Hardie, "How to Project Customer Retention" | paper | 2026-07-28 | https://doi.org/10.1002/dir.20074 | Journal of Interactive Marketing 21(1), 76-90, 2007 | Wiley/Elsevier 著作権。要旨とモデル構造の paraphrase のみ | shifted-beta-geometric（sBG）モデル。各顧客の期末解約確率 θ が Beta 分布に従い異質であるという仮定でリテンション曲線を射影する。表計算で実装可能で、単純外挿より正確な射影を与えるという主張 | confirmed-for-scope（2026-07-28 に出版社ページと著者公開のモデルノートで確認） | canonical doc へ昇格済み |
| Fader, Hardie, Lee, "'Counting Your Customers' the Easy Way: An Alternative to the Pareto/NBD Model" | paper | 2026-07-28 | https://doi.org/10.1287/mksc.1040.0098 | Marketing Science 24(2), 275-284, 2005 | INFORMS 著作権。要旨とモデル構造の paraphrase のみ | 非契約型（離脱が観測できない）顧客基盤向けの BG/NBD モデル。Pareto/NBD（Schmittlein et al. 1987）とほぼ同等の結果を大幅に容易な実装（表計算可能）で得られるという主張 | confirmed-for-scope（2026-07-28 に INFORMS 公式ページで確認） | canonical doc へ昇格済み |
| Basili, Caldiera, Rombach, "The Goal Question Metric Approach" | paper | 2026-07-28 | https://onlinelibrary.wiley.com/doi/10.1002/0471028959.sof142 （初出: Encyclopedia of Software Engineering, Wiley, 1994, 528-532） | 1994（Wiley 参照版あり） | Wiley 著作権。3層構造の paraphrase のみ | 測定を Goal（目的・視点・環境）→ Question → Metric の3層で概念レベルから導出する枠組み | confirmed-for-scope（2026-07-28 に Wiley 参照ページと複数の書誌記録で確認） | canonical doc へ昇格済み（§6 の枠組み） |

## 既存 docs との重複確認（昇格フロー手順4）

- SUS・NPS・CSAT の質問紙としての定義・運用（遅行指標として先行指標とセットで使う原則を含む）は [accessibility-ux-human-centered-quality.md](../../human-centered-quality/accessibility-ux-human-centered-quality.md) が既にカバーする。canonical doc は NPS の算式と限界（縦断研究）・事業指標としての扱いに限定し、質問紙運用は再定義しない。
- メトリクスの誤用・Goodhart/Campbell の法則・カウンターメトリクス強制は [quality-metrics-pitfalls.md](../../quality-management/quality-metrics-pitfalls.md) が既にカバーする。canonical doc は参照のみ行い再記述しない。
- GQM の品質管理文脈での言及・COQ は [software-quality-management-practical-reference.md](../../quality-management/software-quality-management-practical-reference.md) が既にカバーする。canonical doc は GQM を事業指標×品質シグナルの相関分析へ適用する部分のみを扱う。
- SLI/SLO・エラーバジェット等の品質シグナル側の定義は [production-quality-sre-observability.md](../../operations-quality/production-quality-sre-observability.md) が正典であり、再定義しない。
- VOC・チャーン・LTV の手法本体は既存 docs に未収録（2026-07-28 に `grep -ri "VOC\|チャーン\|LTV\|lifetime value" docs/` で確認。ヒットはハブ・phase2 ガイドの計画記述、human-centered-quality の運用シグナル言及、本レーンのみで、手法定義は無い）。

## 関連ドキュメント

- [\_research/README.md](../README.md) — intake の共通ルールと昇格フロー
- [business-quality-metrics-methods.md](../../quality-management/business-quality-metrics-methods.md) — 本レーンから昇格した canonical doc
- [DECISIONS.md D-012](../../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ) — #15 P3 据え置き解除の決定
