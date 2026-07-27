# 日本発テスト設計技法 調査レーン

作成日: 2026-07-27

このレーンは、D-012 ウェーブ2の `docs/test-techniques/japanese-test-design-methods.md`（phase2 実装ガイド T1 の「日本発テスト設計技法」領域）を作成するための出典調査 intake である。[ハブ §1 不足領域リスト](../../agent-ecosystem/skill-ecosystem-design-plan.md#不足領域リスト)が Phase 2 での新規文書化を指定する領域（3色ボールペン分析・要求のメタモデル分析・ゆもつよメソッド・Tiramis 8要素・ラルフチャート・観点/フレーム/コンテナ階層化）に対応する。

`docs/_research/` の共通ルールとフィールド定義は [\_research/README.md](../README.md) および [software-quality-technique-research のレジスタ](../software-quality-technique-research/knowledge-candidate-register.md)に従う。

## 研究カード

| research_id | 対象領域 | origin_layer | source_layers[] | verification_state | confirmed_scope | KB登録判断 | 推奨処理先 | 次アクション |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RC-JTD-001 | 3色ボールペンによる仕様書分析 | external-gap | official-guidance, existing-doc | confirmed-for-scope | 原典（齋藤孝の読書・情報活用法）の書誌と、テスト分野への応用記事（ソフトウェア・テストPRESS Vol.2）の存在、色の意味づけ（赤=客観的に最重要／青=客観的にまあ重要／緑=主観的に気になる・曖昧・矛盾） | adopt | `docs/test-techniques/japanese-test-design-methods.md` | 昇格済み。応用記事の執筆者名は公開検索で確定できず（誌面確認が必要）、文書では記事書誌までを記載 |
| RC-JTD-002 | テスト要求分析の概念・テスト観点（テスト対象×テスト目的） | external-gap | official-guidance | confirmed-for-scope | JaSST'12 Tokyo 智美塾資料（鈴木三紀夫）の全文で確認: テスト観点=テスト対象とテスト目的、分解・体系化、テスト要求の源泉（Policy/People/Process/Product/Quality/Cost/Delivery）、リスク識別（要求/技術/スキル/政治） | adopt | 同上 | 昇格済み |
| RC-JTD-003 | ゆもつよメソッド | external-gap | official-guidance | confirmed-for-scope | 湯本剛本人の智美塾資料（JaSST'13）でテスト分析プロセス（実現したい品質の具体的把握→テスト箇所の選択→テストの目的設定、機能の整理&再分類→テストタイプ特定→テストカテゴリ作成→テスト条件となる仕様項目特定→テスト対象アイテム特定）、WACATE 2014 資料で論理的機能構造（入力・変換・貯蔵・出力・サポート）とテストカテゴリの作り方 | adopt | 同上 | 昇格済み |
| RC-JTD-004 | HAYST法・ラルフチャート | external-gap | official-guidance, existing-doc | confirmed-for-scope | JaSST'18 Tohoku 基調資料（秋山浩一）の全文で確認: ステップ（6W2H→FV表→ラルフチャート→FL表→直交表）、ラルフチャート=目的機能のモデル（入力・出力・状態変数・ノイズ・アクティブノイズ。品質工学の P-チャート系譜）、因子の性質×テスト技法対応、FL表の規約（水準1=デフォルト・異常値は入れない）。書籍2冊（日科技連 2007/2014）の書誌 | adopt | 同上 | 昇格済み |
| RC-JTD-005 | NGT/VSTeP（テスト観点・コンテナ・フレームの階層化） | external-gap | official-guidance | confirmed-for-scope | 西康晴の公式資料（qualab.jp、2013）の全文で確認: NGT 記法（観点の階層記述、詳細化・組み合わせ・順序依存の関係、ステレオタイプ）、VSTeP プロセス（テスト要求分析=観点図のリファイン→テストアーキテクチャ設計=剪定・ズームイン/アウト・テストコンテナ分割・テストフレーム構築→テスト詳細設計→テスト実装=集約）、問題意識（CPM法・固定3レイヤー法） | adopt | 同上 | 昇格済み |
| RC-JTD-006 | Tiramis 8要素 | external-gap | unknown | needs-official-check | unknown（2026-07-27 の公開 Web 検索で一次出典を特定できず。JaSST 智美塾資料・ASTER テスト要求分析チュートリアル全文にも該当語なし） | defer | canonical 収録見送り | 一次出典（発表資料・記事・書籍）が特定できた時点で再起票する。それまで skills はこの手法を前提としない |
| RC-JTD-007 | 要求のメタモデル分析 | external-gap | unknown | needs-official-check | unknown（同上。「テスト観点の分解・体系化」としての実質は RC-JTD-002 の確認済み範囲が部分的に代替する） | defer | canonical 収録見送り | 同上 |

## source_records

| item | source_type | checked_at | official_url | version_or_edition | license_note | claim_scope | verification_result | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 齋藤孝『三色ボールペン情報活用術』 | existing-doc | 2026-07-27 | https://www.kadokawa.co.jp/product/200301000423/ | 角川oneテーマ21、2003 | 書籍本文は要ライセンス。色の意味づけの要約のみ | 3色（赤・青・緑）による読解・情報整理法の原典 | confirmed-for-scope（公式ページで書誌確認） | 昇格済み |
| ソフトウェア・テストPRESS Vol.2「3色ボールペンで読む仕様書」 | official-guidance | 2026-07-27 | https://www.fujisan.co.jp/product/1254160/ （技術評論社。総集編にも収録） | Vol.2（2005） | 誌面本文は要ライセンス。手法の要旨の paraphrase のみ | 3色ボールペン法の仕様書読解への応用、色の意味づけ（赤=客観・最重要／青=客観・まあ重要／緑=主観・気になる） | confirmed-for-scope（複数の二次情報で一致確認。誌面原本は未確認のため執筆者名は記載しない） | 執筆者名は誌面確認後に追記可 |
| 鈴木三紀夫「智美塾 テスト要求分析の概念」 | official-guidance | 2026-07-27 | https://jasst.jp/symposium/jasst12tokyo/pdf/A2-2.pdf | JaSST'12 Tokyo、2012-01-25 | © Mikio Suzuki。JaSST 公式サイト公開資料。paraphrase のみ | テスト観点=テスト対象×テスト目的、テスト要求の源泉、リスク識別、テスト要求（品質特性・前提条件・制約） | confirmed-for-scope（2026-07-27 に PDF 全文確認） | 昇格済み |
| 湯本剛「ゆもつよメソッドのテスト要求分析とテストアーキテクチャ設計」 | official-guidance | 2026-07-27 | http://jasst.jp/symposium/jasst13tokyo/pdf/A2-3.pdf | JaSST'13 Tokyo 智美塾、2013-01-30 | 本人発表資料（JaSST 公式公開）。paraphrase のみ | ゆもつよ風テスト開発プロセスの工程分解（テスト分析〜テスト実装の各活動名と順序） | confirmed-for-scope（2026-07-27 に PDF 全文確認） | 昇格済み |
| 朱峰錦司「テスト分析入門 -『ゆもつよメソッド』を例に-」 | official-guidance | 2026-07-27 | https://www.slideshare.net/kjstylepp/ss-36095291 | WACATE 2014 Summer、2014-06-21 | 公開スライド。paraphrase のみ | 論理的機能構造（入力・変換・貯蔵・出力・サポート）とテストカテゴリの作り方（各要素にテスト対象から見てふさわしい名前付け） | confirmed-for-scope | 昇格済み。湯本本人の博士論文説明資料（https://www.slideshare.net/yumotsuyo/ss-106842170）が本人一次情報として補強に使える |
| 秋山浩一「HAYST法によるテスト設計の考え方」 | official-guidance | 2026-07-27 | https://jasst.jp/symposium/jasst18tohoku/pdf/S1.pdf | JaSST'18 Tohoku、2018-05-25 | © Fuji Xerox。JaSST 公式公開資料。paraphrase のみ | HAYST法のステップ（6W2H→FV表→ラルフチャート→FL表）、ラルフチャートの構成（入力・出力・状態変数・ノイズ・アクティブノイズ）と品質工学系譜、因子の性質×技法対応表、FL表の規約 | confirmed-for-scope（2026-07-27 に PDF 全文確認） | 昇格済み |
| 『ソフトウェアテストHAYST法入門』（吉澤正孝・秋山浩一・仙石太郎） | existing-doc | 2026-07-27 | https://www.amazon.co.jp/dp/4817192283 | 日科技連出版社、2007 | 書籍本文は要ライセンス。書誌の参照のみ | HAYST法の体系的解説書という位置づけ（続編『事例とツールで学ぶHAYST法』2014 も同様） | confirmed-for-scope（書誌のみ） | 詳細定義が必要になれば licensed-text-needed で再起票 |
| 西康晴「テスト観点に基づくテスト開発方法論 VSTePの概要」 | official-guidance | 2026-07-27 | https://qualab.jp/materials/VSTeP.130510.color.pdf | 2013-05-10 | © NISHI, Yasuharu。本人サイト公開資料。paraphrase のみ | NGT 記法、テスト観点図、テストコンテナ・テストフレーム、VSTeP のテスト開発プロセス、CPM法・固定3レイヤー法の問題意識 | confirmed-for-scope（2026-07-27 に PDF 全文確認） | 昇格済み |

## 既存 docs との重複確認（昇格フロー手順4）

- 本領域は既存 docs に未収録（[ハブ §1 不足領域リスト](../../agent-ecosystem/skill-ecosystem-design-plan.md#不足領域リスト)の記載どおり）。skills/test-requirement-analysis（3色ボールペン分析モード）と skills/test-architecture-design（ゆもつよ・Tiramis への言及）が「プロンプト由来・出典補強待ち」とタグ付けした記述を持ち、本レーンの昇格によって参照先が実在化する。
- テストプロセス（TRA→TAD→TDD/TI→TE）の工程定義は [test-process-research-summary-test-design.md](../../test-techniques/test-process-research-summary-test-design.md) を正とし、canonical doc は技法群を同プロセスへの「プラグイン」として位置づける（工程定義を再記述しない）。
- 技法カタログの個別技法 ID は [test-techniques-skill-catalog.md](../../test-techniques/test-techniques-skill-catalog.md) が正。本 doc は同カタログの補完（分析系・観点系の方法論）であり、技法カードの再記述はしない。

## 関連ドキュメント

- [\_research/README.md](../README.md) — intake の共通ルールと昇格フロー
- [japanese-test-design-methods.md](../../test-techniques/japanese-test-design-methods.md) — 本レーンから昇格した canonical doc
