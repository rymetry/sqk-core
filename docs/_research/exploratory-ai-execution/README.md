# 探索的テストの AI 実行境界 調査レーン

作成日: 2026-07-28

このレーンは、D-012 ウェーブ3の #8 exploratory-testing-support 着手に先立ち、[DECISIONS.md D-012](../../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ) が決定した役割境界の変更——探索の実行主体を「人間」から「AI エージェント（veridia 等の実行系）」へ改める——を正典へ反映するための出典調査 intake である。改訂対象は、exploratory 知識文書の AI 支援境界（「提案と後処理まで、探索は人間」）、[ハブ §3 #8](../../agent-ecosystem/skill-ecosystem-design-plan.md#3-スキル定義一覧) の役割境界、[phase2 実装ガイド](../../agent-ecosystem/phase2-implementation-guide.md) の #8 受入観点の3箇所である。

`docs/_research/` の共通ルール（research ID と canonical ID の分離、研究カードから直接本文化しない、`source_records` での出典検証、license-safe paraphrase での昇格）は [\_research/README.md](../README.md) に従う。フィールド定義は [software-quality-technique-research のレジスタ](../software-quality-technique-research/knowledge-candidate-register.md)と同じものを使う。

## 研究カード

| research_id | 対象領域 | origin_layer | source_layers[] | verification_state | confirmed_scope | KB登録判断 | 推奨処理先 | 次アクション |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RC-ETAI-001 | LLM エージェントによる GUI テストの自律実行の実証（機能理解に基づく探索・メモリ・意図駆動） | external-gap | paper | confirmed-for-scope | 下記 source_records の GPTDroid・DroidAgent 行に記載の範囲（自律実行の成立、カバレッジ・欠陥検出の実測値、メモリ・意図駆動などの機構） | adopt | `docs/exploratory-testing/exploratory-testing-concepts-and-practice.md` の AI 活用節の改訂 | 昇格済み（本レーンと同一 PR の正典改訂を参照） |
| RC-ETAI-002 | 探索的欠陥発見への拡張とその限界（ベンチマーク実測） | external-gap | paper | confirmed-for-scope | 下記 source_records の GUITester・GUI Testing Arena 行に記載の範囲（探索的欠陥発見タスクの定式化と実測値、最先端モデルでも全サブタスクは苦手という限界の報告） | adopt | 同上（実行主体の変更と同時に、限界・人間監督の必要性の根拠として使う） | 昇格済み |
| RC-ETAI-003 | 汎用 computer-use エージェント基盤（スクリーンショット・マウス・キーボード操作の実行系） | external-gap | official-tool-doc | confirmed-for-scope | 下記 source_records の Anthropic 行に記載の範囲（デスクトップ環境の自律操作機能の提供、beta である旨、セキュリティ上の注意） | adopt | 同上（実行系が汎用エージェント基盤として実装可能である根拠） | 昇格済み |

## source_records

| item | source_type | checked_at | official_url | version_or_edition | license_note | claim_scope | verification_result | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Liu et al., "Make LLM a Testing Expert: Bringing Human-like Interaction to Mobile GUI Testing via Functionality-aware Decisions" | paper | 2026-07-28 | https://doi.org/10.1145/3597503.3639180 （著者版: https://arxiv.org/abs/2310.15780 ） | ICSE 2024 | ACM/IEEE 著作権。本文の再配布はしない。要旨と公表数値の paraphrase のみ | GUI テストを LLM との Q&A として定式化し、機能認識メモリで探索を誘導する GPTDroid の提案。Google Play 93 アプリでベースライン比 +32% のアクティビティカバレッジ、+31% の欠陥検出、新規欠陥 53 件（うち 35 件が confirmed/fixed） | confirmed-for-scope（2026-07-28 に arXiv abstract と ICSE 2024 採録情報を確認） | 正典改訂へ昇格済み |
| Yoon, Feldt, Yoo, "Autonomous Large Language Model Agents Enabling Intent-Driven Mobile GUI Testing" | paper | 2026-07-28 | https://arxiv.org/abs/2311.08649 | arXiv v1（2023-11-15） | arXiv 著者版。要旨と公表数値の paraphrase のみ | 長期・短期メモリを持つ自律 GUI テストエージェント DroidAgent の提案。人手介入なしに意図（タスク）を自ら設定して探索し、Themis ベンチマーク 15 アプリで 61%（従来最良 51%）のアクティビティカバレッジ。生成 374 タスク中 317 件がアプリ機能に照らして現実的と評価 | confirmed-for-scope（2026-07-28 に arXiv abstract を確認） | 正典改訂へ昇格済み |
| Gao et al., "GUITester: Enabling GUI Agents for Exploratory Defect Discovery" | paper | 2026-07-28 | https://arxiv.org/abs/2601.04500 | arXiv v1（2026-01-08） | arXiv 著者版。要旨と公表数値の paraphrase のみ | GUI エージェントによる探索的欠陥発見の定式化。タスク完遂優先で異常を報告しない・システム欠陥をエージェント自身の誤操作と誤帰属するという2課題に対し、計画-実行と階層リフレクションで対処。GUITestBench（26 アプリ・26 欠陥・143 タスク）で F1 48.90%（Pass@3、ベースライン 33.35%） | confirmed-for-scope（2026-07-28 に arXiv abstract を確認） | 正典改訂へ昇格済み（実行主体の成立根拠と限界の両方に使用） |
| Zhao et al., "GUI Testing Arena: A Unified Benchmark for Advancing Autonomous GUI Testing Agent" | paper | 2026-07-28 | https://arxiv.org/abs/2412.18426 | arXiv v1（2024-12-24） | arXiv 著者版。要旨の paraphrase のみ | 自律 GUI テストを意図生成・タスク実行・欠陥検出の3サブタスクに分けたベンチマーク。最先端モデルでも全サブタスクを高水準にはこなせず、実運用適用との間にギャップがあるという報告 | confirmed-for-scope（2026-07-28 に arXiv abstract を確認） | 正典改訂へ昇格済み（人間監督・限界の根拠） |
| Anthropic, "Computer use tool"（Claude Platform Docs） | official-tool-doc | 2026-07-28 | https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool | 2026-07 時点の公開版（beta） | 公式ドキュメント。機能・制約の要旨のみ | スクリーンショット取得・マウス・キーボード操作によるデスクトップ環境の自律操作を LLM に与えるツールの提供。beta であり、セキュリティ上の考慮を明記 | confirmed-for-scope（2026-07-28 にドキュメント本文を確認） | 正典改訂へ昇格済み（汎用実行基盤の存在根拠。特定ベンダーの採用指定はしない） |

## 既存 docs との重複確認（昇格フロー手順4）

- 探索的テストの AI 支援は [exploratory-testing-concepts-and-practice.md の AI 活用節](../../exploratory-testing/exploratory-testing-concepts-and-practice.md#ai活用による探索的テスト支援)が唯一の canonical 記述であり、他3文書（ツアー検証・観点ライブラリ・チャーターカタログ）に境界記述の重複はない（2026-07-28 に `grep -rn "探索は人間\|探索実行は人間" docs/` で確認。ヒットは concepts 文書の要約行を引くハブ §1 目録・ハブ §3 #8・phase2 ガイド #8 のみ）。
- LLM/AI 機能そのものの品質評価（pass@k・LLM-as-judge 等）は [ai-system-quality-model.md](../../quality-models/ai-system-quality-model.md) が担い、本レーンのスコープ（AI が探索テストを実行する側）とは向きが逆であるため重複しない。
- 既存 AI 支援節の Xray・mabl・TestRail・Applitools・NIST AI RMF の記述は「補助者としての AI」の出典として今後も有効であり、削除せず「実行主体としての AI エージェント」の記述を追加する形で改訂する。

## 関連ドキュメント

- [\_research/README.md](../README.md) — intake の共通ルールと昇格フロー
- [exploratory-testing-concepts-and-practice.md](../../exploratory-testing/exploratory-testing-concepts-and-practice.md) — 本レーンから改訂した canonical doc
- [DECISIONS.md D-012](../../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ) — 役割境界変更の決定
