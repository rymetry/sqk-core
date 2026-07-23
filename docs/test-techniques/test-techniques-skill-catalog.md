# テスト技法スキルカタログ

目的: ソフトウェア検証に使うテスト技法を、AIスキル・教育コンテンツ・社内標準プロセスに分解しやすい形で整理する。

想定読者: QAエンジニア、テストアーキテクト、SET/SDET、開発リード、品質保証責任者。

---

## 0. このカタログの使い方

このカタログでは、テスト技法を「知っている用語」ではなく、**実行可能な skill** として扱う。

各技法は、次の観点で skills 化する。

```yaml
skill_id: 技法を一意に識別するID
name: 技法名
purpose: 何を検出・保証するための技法か
when_to_use: どんな仕様・リスク・システムで使うべきか
inputs: 必要な入力情報
procedure: 実行手順
outputs: 成果物
coverage_or_exit: 十分性・完了条件
common_defects: 見つけやすい欠陥
combine_with: 併用すべき技法
pitfalls: 失敗パターン
references: 根拠・参考文献
```

**重要な前提:** テスト技法は万能薬ではない。万能薬を求める姿勢そのものがだいたい品質事故の前兆である。技法は、対象・リスク・制約に合わせて組み合わせる。

---

## 1. 調査から得た要点

### 1.1 標準系から見た中核

ISTQB/JSTQB Foundation Level と ISO/IEC/IEEE 29119-4 の整理では、テスト技法は大きく以下に分けられる。

- 仕様ベース / ブラックボックス技法
- 構造ベース / ホワイトボックス技法
- 経験ベース技法
- 協調ベースのアプローチ
- 静的テスト、レビュー、静的解析
- カバレッジ測定
- リスクベースのテスト設計

IEEE 1012 は、V&V をテストだけでなく、分析、評価、レビュー、インスペクション、アセスメントまで含むライフサイクル活動として扱う。したがって、skills 化でも「テストケース生成」だけに閉じない。

### 1.2 論文・研究系から追加すべき強い技法

標準シラバスに出てくる古典技法に加えて、実務で skills 化する価値が高い技法は次の通り。

| 技法 | なぜ強いか |
| --- | --- |
| 組合せテスト / t-wise | 入力、設定、環境の爆発を抑えながら相互作用欠陥を狙える。 |
| プロパティベーステスト | 例示ベースではなく、性質・不変条件から大量の入力を生成できる。 |
| メタモルフィックテスト | 正解オラクルが作りにくい対象でも、入力変換と出力関係で検査できる。 |
| ミューテーションテスト | テストスイートの欠陥検出力を「人工欠陥を殺せるか」で測れる。 |
| ファジング | パーサ、API、プロトコル、セキュリティ境界に強い。 |
| シンボリック / コンコリック実行 | パス条件を解いて到達しにくい分岐の入力を生成できる。 |
| モデルベーステスト | 状態機械や仕様モデルから体系的にテストを生成できる。 |
| 差分テスト | 複数実装・バージョン・モデルの不一致をオラクルとして使える。 |
| テストオラクル設計 | 自動化のボトルネックである「どう合否判定するか」を明示できる。 |
| 回帰テスト選択・優先順位付け | CI/CDで全部回せない現実を多少まともに扱える。 |
| 契約テスト | マイクロサービス/API間の互換性破壊を早期に検出できる。 |
| カオスエンジニアリング | 分散システムの耐障害性を制御実験として検証できる。 |
| ML/LLM向けメタモルフィック・ロバストネステスト | 非決定的・確率的・オラクル困難なAIシステムを扱いやすい。 |

---

## 2. 優先度の読み方

| 優先度 | 意味 |
| --- | --- |
| S | 多くの案件で標準スキルとして持つべき。 |
| A | 条件が合えば非常に有効。積極的に skills 化すべき。 |
| B | 専門性・コスト・対象制約がある。必要に応じて採用。 |
| R | 研究寄り・高度運用向け。PoCや専門チーム向け。 |

---

## 3. テスト技法一覧

### 3.1 静的検証・レビュー・解析

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| REV-01 | インスペクション / 形式レビュー | S | 要求、設計、コード、テスト仕様の欠陥を実行前に潰す | 指摘一覧、是正結果、レビュー記録 | 重要成果物のレビュー完了、重大指摘のクローズ | R1, R4, R5 |
| REV-02 | ウォークスルー / 技術レビュー | S | 作成者が成果物を説明し、理解齟齬を早期に見つける | 質問、指摘、改善案 | 参加者の合意、未解決論点の管理 | R1, R5 |
| REV-03 | 要求品質レビュー / 曖昧性レビュー | S | 要求が曖昧、矛盾、不完全、検証不能なとき | 要求欠陥リスト、受け入れ基準案 | 検証可能性、完全性、一貫性、追跡可能性 | R1, R4, R5 |
| STA-01 | 静的コード解析 | S | コーディング規約、バグパターン、型、未使用、null、例外を検出 | 解析レポート、警告一覧 | 重大警告ゼロ、例外承認、ルールセット妥当性 | R4, R32 |
| STA-02 | SAST / 静的セキュリティ解析 | A | 認証、認可、入力処理、秘密情報、依存関係にリスクがある | 脆弱性候補、修正指示 | 高リスク脆弱性の是正、誤検知処理 | R21, R22 |
| STA-03 | 複雑度・依存関係・アーキテクチャ解析 | A | 保守性、変更影響、循環依存、巨大関数を評価する | 複雑度、依存グラフ、変更影響範囲 | 閾値超過の是正、リスク箇所のテスト強化 | R3, R5 |
| STA-04 | 抽象解釈 | A | 組込み、安全系、実行時エラーの不在を強く示したい | 証明レポート、未証明箇所 | ランタイムエラー不在の証明、仮定の明示 | R32 |
| STA-05 | 形式仕様レビュー / モデル検査 / 定理証明 | B | 並行性、プロトコル、安全制約、スマートコントラクトなど | 形式仕様、反例、証明 | 性質の充足、反例分析、仮定の管理 | R32 |
| RV-01 | アサーション / Design by Contract | A | 事前条件、事後条件、不変条件を実行時に検査したい | 契約、アサーション、違反ログ | 重要不変条件の明文化、違反ゼロ | R20, R33 |
| RV-02 | ランタイム検証 | B | 実行トレースを形式的仕様・時相条件で監視したい | モニタ、トレース、違反イベント | 監視対象性質の網羅、オーバーヘッド評価 | R33 |

### 3.2 仕様ベース / ブラックボックス技法

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| BB-01 | 同値分割 | S | 入力、状態、条件を有効・無効のクラスに分けられる | 同値クラス表、代表値テスト | 有効/無効クラスの網羅 | R1, R2 |
| BB-02 | 境界値分析 | S | 数値、日付、文字数、件数、閾値、上限下限がある | 境界値テスト | 下限、上限、直前、直後、最小、最大の確認 | R1, R2 |
| BB-03 | デシジョンテーブル | S | 複数条件の組合せで結果が変わる | 条件・アクション表、テストケース | 条件組合せ、矛盾、欠落の確認 | R1, R2 |
| BB-04 | 原因結果グラフ | A | 条件数が多く、論理関係を視覚化したい | 原因結果グラフ、決定表 | 制約、排他、包含、結果の網羅 | R2 |
| BB-05 | 状態遷移テスト | S | ステータス、画面遷移、ワークフロー、ライフサイクルがある | 状態遷移図、遷移テスト | 状態、妥当遷移、不正遷移、全遷移 | R1, R2 |
| BB-06 | ユースケース / シナリオテスト | S | 業務フロー、ユーザー操作、E2E確認が重要 | シナリオ、事前条件、期待結果 | 主要フロー、代替フロー、例外フロー | R1, R2 |
| BB-07 | 分類木法 | A | 入力条件を階層分類し、組合せを設計したい | 分類木、組合せ表 | 各分類の代表値、組合せ網羅 | R2 |
| BB-08 | 構文テスト / 文法テスト | A | DSL、ファイル形式、クエリ、コマンド、プロトコルを扱う | 文法規則、生成入力 | 有効構文、無効構文、境界構文 | R2, R13 |
| BB-09 | ドメイン分析テスト | A | 複数条件による境界・領域分割が重要 | ドメイン表、ON/OFFポイント | 領域境界と隣接領域 | R2 |
| BB-10 | 受け入れ基準 / ATDD / BDD | S | PO、開発、テスト間で期待結果を合意したい | Given-When-Then、受け入れテスト | 受け入れ基準の検証可能性、例示の十分性 | R1 |
| BB-11 | チェックリストベーステスト | S | 過去障害、標準観点、ドメイン知識を再利用したい | チェックリスト、結果記録 | 観点網羅、定期更新 | R1, R5 |
| COM-01 | ペアワイズ / All-pairs | A | パラメータや設定値が多すぎる | 2-wise組合せ表 | 全ペア組合せの網羅 | R10, R11 |
| COM-02 | n-wise / covering array | A | 2要因より高次の相互作用欠陥が懸念される | 3-wise以上の組合せ表 | 指定t値の組合せ網羅 | R10, R11 |
| COM-03 | 直交表 / HAYST | A | 因子水準が多く、実験計画法的に整理したい | 直交表、因子水準表 | 水準割付、交互作用の扱い | R10, R11 |
| COM-04 | 構成組合せテスト | A | OS、DB、ブラウザ、端末、権限、設定値が絡む | 構成マトリクス | リスクの高い構成、t-wise構成 | R3, R10 |

### 3.3 構造ベース / ホワイトボックス技法

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| WB-01 | ステートメント / ブランチテスト | S | 単体、API、重要ロジックを最低限構造的に確認 | カバレッジレポート | 文・分岐カバレッジ、未到達理由 | R1, R2 |
| WB-02 | デシジョン / 条件テスト | A | 複合条件の真偽が重要 | 条件組合せテスト | 各条件の真偽、判定結果への影響 | R2 |
| WB-03 | MC/DC | A | 安全クリティカル、複雑な条件判定 | MC/DCテスト、根拠表 | 各条件が独立に判定へ影響すること | R24 |
| WB-04 | パステスト / Prime Path | B | パス依存、複雑な制御フローを評価したい | パス集合、実行結果 | 実行可能パス、代表パス、未達理由 | R2, R34 |
| WB-05 | データフローテスト | A | 変数の定義・使用、初期化漏れ、更新漏れが重要 | def-useペア、テスト | all-defs、all-uses、du-path | R2, R34 |
| WB-06 | ループテスト | A | 境界回数、0回、1回、多回、最大回数が重要 | ループ境界テスト | 0/1/2/n/max/max+1 | R2 |
| WB-07 | カバレッジ基準設計 | S | テスト十分性を説明する必要がある | カバレッジ目標、測定結果 | 要求、コード、状態、リスクの各網羅 | R1, R2 |

### 3.4 経験ベース・リスクベース・故障ベース

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| EXP-01 | エラー推測 | S | 仕様に書かれにくい失敗パターンを狙う | 欠陥仮説、テストアイデア | 過去障害、実装癖、境界、例外の反映 | R1 |
| EXP-02 | 探索的テスト | S | 仕様が不完全、変化が速い、未知リスクが多い | チャーター、メモ、欠陥 | 学習、設計、実行の同時進行、発見密度 | R1 |
| EXP-03 | セッションベーステスト管理 | A | 探索的テストを管理可能にしたい | セッションシート、時間枠、結果 | チャーター達成、発見事項、阻害要因 | R1 |
| RISK-01 | リスクベーステスト | S | 全部テストできない。つまり普通のプロジェクト | リスク表、優先度、テスト配分 | 影響度、発生確率、検出困難性、残存リスク | R1, R2 |
| RISK-02 | 過去障害ベーステスト | A | 類似障害、再発防止、横展開を狙う | 障害パターン、再発防止テスト | 過去障害分類と再現条件の網羅 | R5 |
| FAULT-01 | フォールトインジェクション | A | 障害時の回復性、耐障害性、例外処理を確認 | 注入条件、観測結果 | 注入障害、検出、隔離、回復の確認 | R30 |
| FAULT-02 | ミューテーションテスト | A | テストスイートの欠陥検出力を評価したい | mutation score、殺せなかったmutant | 生存mutant分析、等価mutant扱い | R9 |
| FAULT-03 | ネガティブ / ロバストネステスト | S | 不正入力、異常順序、破損データ、権限違反 | 異常系ケース | 安全な失敗、エラー処理、ログ、復旧 | R1, R22 |

### 3.5 オラクル・性質・モデル・自動生成系

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| ORA-01 | テストオラクル設計 | S | 自動化・大量生成で合否判定がボトルネックになる | オラクル一覧、判定規則 | false positive/false negative、判定根拠 | R20 |
| ORA-02 | ゴールデンマスター / Approval Testing | A | 既存挙動を保護したい、仕様が弱いレガシーを扱う | 基準出力、差分承認 | 意図した差分と回帰の分離 | R20 |
| PROP-01 | プロパティベーステスト | A | 個別例ではなく不変条件で検査できる | property、generator、shrinker | 性質、生成分布、反例縮小 | R6 |
| META-01 | メタモルフィックテスト | A | 期待値が直接定義しにくい、科学計算、検索、ML、LLM | metamorphic relation、変換テスト | 入力変換後の出力関係、違反検出 | R7, R8 |
| MBT-01 | モデルベーステスト | A | 状態、プロトコル、ワークフロー、仕様モデルがある | モデル、生成テスト、トレース | モデル要素、遷移、要求の網羅 | R16 |
| DIFF-01 | 差分テスト | A | 複数実装、複数バージョン、互換実装、コンパイラがある | 差分入力、出力比較 | 不一致分析、どちらが正かの判定 | R18 |
| RAND-01 | ランダムテスト | B | 広い入力空間を低コストで探索したい | ランダム入力、失敗seed | seed再現性、入力分布、実行数 | R6, R13 |
| FUZZ-01 | ブラックボックスファジング | A | 入力境界、パーサ、API、クラッシュ耐性を攻める | fuzz corpus、クラッシュ、例外 | 再現可能クラッシュ、重複排除 | R12, R13 |
| FUZZ-02 | カバレッジガイド付きグレーボックスファジング | A | コードカバレッジを使って深いパスを探索したい | corpus、coverage、crash | 新規パス、クラッシュ、時間あたり発見率 | R12, R13 |
| FUZZ-03 | 文法ベース / プロトコルファジング | A | 構造化入力、通信プロトコル、ファイル形式を扱う | grammar、生成入力 | 有効構文を保った深部探索 | R13 |
| SYM-01 | シンボリック実行 | B | パス条件を解いて入力を自動生成したい | パス条件、生成入力、反例 | パス爆発、制約解決、未探索理由 | R14 |
| CONC-01 | コンコリックテスト | B | 実行と制約解決を組み合わせて現実的に探索したい | concrete input、symbolic constraint | 分岐反転、到達パス、制約制限 | R15 |
| SBST-01 | 探索ベーステスト生成 | B | 遺伝的アルゴリズム等でカバレッジや欠陥発見を最大化したい | fitness、生成テスト | 目的関数、収束、再現性 | R17 |
| LLMGEN-01 | LLM支援テスト生成 | B | 仕様、コード、例からテスト案を生成したい | テスト案、テストコード、レビュー結果 | 人間レビュー、実行検証、オラクル妥当性 | R28 |

### 3.6 回帰・自動化・CI/CD

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| REG-01 | 回帰テスト選択 | S | 変更に関係するテストだけを選びたい | 選択テスト集合 | 変更影響、漏れリスク、時間削減 | R19 |
| REG-02 | テストケース優先順位付け | A | 早期に欠陥を見つけたい、CI時間が限られる | 実行順序 | 早期欠陥検出率、リスク順、履歴順 | R19 |
| REG-03 | テストスイート最小化 | B | 冗長テストを削減したい | 削減後スイート | カバレッジ維持、欠陥検出力維持 | R19 |
| REG-04 | テストインパクト分析 | A | 変更ファイル・依存関係から必要テストを推定したい | 影響範囲、対象テスト | false negative抑制、CI短縮 | R19 |
| REG-05 | スモーク / サニティテスト | S | ビルド・デプロイ後に最低限の健全性を確認 | 短時間テスト、結果 | 重要機能、起動、依存サービス疎通 | R1 |
| REG-06 | 継続的テスト / CI自動回帰 | S | 変更のたびに品質ゲートを動かしたい | CIパイプライン、品質ゲート | 安定性、実行時間、失敗分析 | R1, R19 |
| REG-07 | カナリア / Feature Flag検証 | A | 本番段階導入で影響を限定したい | カナリア指標、ロールバック条件 | 異常検知、段階拡大、停止条件 | R30 |

### 3.7 非機能・品質特性別技法

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| NF-PERF-01 | 性能 / 負荷テスト | S | 応答時間、スループット、同時接続が重要 | 性能結果、ボトルネック | SLA/SLO、p95/p99、リソース使用率 | R3 |
| NF-PERF-02 | ストレス / スパイク / 容量 / 耐久テスト | A | 限界、急増、長時間稼働、容量上限を確認 | 限界値、劣化点、障害挙動 | graceful degradation、回復、リーク | R3 |
| NF-REL-01 | 回復 / フェイルオーバーテスト | A | 障害、再起動、ノード切替、バックアップ復元 | 回復手順、RTO/RPO結果 | データ整合性、復旧時間、手順再現性 | R3, R30 |
| NF-REL-02 | カオスエンジニアリング | A | 分散システムの実耐性を制御実験で検証 | 仮説、実験、観測、改善 | steady state、blast radius、停止条件 | R30 |
| NF-SEC-01 | 脅威モデリング / STRIDE | A | 設計段階でセキュリティリスクを洗う | DFD、脅威一覧、対策 | 脅威カテゴリ、リスク、対策追跡 | R22, R23 |
| NF-SEC-02 | 脆弱性スキャン / DAST / API Security Test | A | Web/API公開面の脆弱性を検出 | 脆弱性レポート | 認証、認可、入力検証、セッション | R21, R22 |
| NF-SEC-03 | ペネトレーションテスト | A | 攻撃者視点で侵害可能性を確認 | 攻撃手順、証跡、影響 | 再現性、影響度、修正確認 | R21, R22 |
| NF-USAB-01 | ユーザビリティテスト | B | 利用者が目的を達成できるか確認 | 観察記録、課題、改善案 | 成功率、時間、エラー、満足度 | R3, R5 |
| NF-A11Y-01 | アクセシビリティテスト | A | WCAG、支援技術、キーボード操作が重要 | 指摘一覧、修正結果 | コントラスト、ラベル、フォーカス順 | R3 |
| NF-COMP-01 | 互換性 / クロスブラウザ / デバイスマトリクス | A | 環境差異のリスクが高い | 環境マトリクス、結果 | 対象市場、重要構成、t-wise | R3, R10 |
| NF-DATA-01 | データ品質 / ETL / 移行リコンシリエーション | A | データ移行、集計、分析、会計、在庫が重要 | 差分表、件数照合、整合性結果 | 件数、金額、参照整合、欠損、重複 | R3 |
| NF-I18N-01 | 国際化 / ローカライゼーションテスト | B | 多言語、時刻、通貨、住所、文字コードを扱う | locale別結果 | 表示崩れ、ソート、日付、桁区切り | R3 |
| NF-OPS-01 | 運用性 / 監視 / ログテスト | A | 障害検知、監査、運用対応が重要 | ログ確認、アラート確認 | 検知可能性、トレースID、監査証跡 | R3, R30 |
| NF-PRIV-01 | プライバシー / データ保持・削除テスト | A | 個人情報、同意、削除、匿名化が重要 | データフロー、削除確認 | 最小化、目的外利用防止、削除完全性 | R3 |

### 3.8 API・マイクロサービス・分散システム

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| API-01 | APIスキーマ / 契約テスト | S | OpenAPI、JSON Schema、gRPC、GraphQLなど | 契約テスト、スキーマ検証 | 後方互換性、必須項目、型、エラー | R20, R31 |
| API-02 | Consumer-Driven Contract Testing | A | 複数チーム・マイクロサービス間の互換性を守る | consumer pact、provider verification | consumer期待とprovider実装の一致 | R31 |
| API-03 | Idempotency / Retry / Timeoutテスト | A | 決済、注文、非同期API、ジョブ処理 | 再試行・重複テスト | 二重登録防止、タイムアウト、補償処理 | R3, R30 |
| API-04 | 非同期 / イベント駆動テスト | A | メッセージング、キュー、イベントソーシング | イベントシナリオ、順序テスト | 順序、重複、遅延、再配信、整合性 | R16, R30 |
| API-05 | 後方互換性テスト | A | API versioning、SDK、クライアント互換 | 互換性ケース | 破壊的変更検出、deprecated管理 | R31 |

### 3.9 安全・高信頼・制御系

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| SAFE-01 | FMEA / FMECAベーステスト | S | 故障モードと影響からテストを作る | 故障モード表、対策テスト | 重大故障モード、検出性、対策確認 | R5 |
| SAFE-02 | FTAベーステスト | A | トップ事象から原因組合せを逆算する | Fault Tree、原因テスト | カットセット、トップ事象防止 | R5 |
| SAFE-03 | STPA / STAMPベーステスト | S | 制御構造、相互作用、ハザードを扱う | UCA、loss scenario、テスト | unsafe control actionの検証 | R25 |
| SAFE-04 | ハザードシナリオ / フェイルセーフテスト | S | 危険状態で安全側に倒れるか確認 | ハザードシナリオ、結果 | safe state、警告、停止、回復 | R24, R25 |
| SAFE-05 | 独立V&V / トレーサビリティ検証 | S | 高い完全性・規制対応が必要 | トレーサビリティ、V&V証跡 | 要求-設計-コード-テスト-結果の連鎖 | R4 |

### 3.10 AI / ML / LLM システム向け

| ID | 技法 | 優先度 | 使う場面 | 主な出力 | 完了・評価の観点 | 参考 |
| --- | --- | --- | --- | --- | --- | --- |
| AI-01 | データセット検証 / データスライステスト | S | 学習・評価データの品質が結果を支配する | データ品質レポート、slice結果 | 欠損、重複、ラベル、偏り、分布 | R27 |
| AI-02 | MLメタモルフィックテスト | A | 正解が一意に定まらないML推論を検査する | 変換関係、違反例 | semantic preserving変換、期待変化 | R7, R27 |
| AI-03 | adversarial / robustness testing | A | ノイズ、摂動、攻撃、分布外入力に弱い | 摂動入力、ロバスト性指標 | 精度劣化、失敗パターン、閾値 | R27 |
| AI-04 | 公平性 / バイアススライステスト | A | 属性や集団ごとの品質差を確認したい | group metrics、差分結果 | 集団別性能、しきい値、説明責任 | R27 |
| AI-05 | Deep Learning white-box / neuron coverage | R | DL内部の活性化を使って入力生成したい | neuron coverage、生成入力 | カバレッジと誤動作の関係 | R26 |
| AI-06 | ドリフト検知 / 本番監視テスト | A | 本番データ分布や性能が変わる | drift report、canary指標 | 入力分布、出力分布、劣化検出 | R27 |
| LLM-01 | Prompt robustness / 意味保持変換テスト | A | 言い換え、順序変更、形式差で出力がぶれる | prompt変換、応答比較 | semantic invariance、一貫性、劣化 | R28, R29 |
| LLM-02 | RAG groundedness / hallucination test | A | RAGが根拠に基づいて回答しているか確認 | 質問、根拠、回答、判定 | citation一致、根拠外主張、矛盾 | R29 |
| LLM-03 | LLM red teaming / misuse safety eval | A | 安全性、脱獄、機密漏えい、危険出力を検査 | 攻撃プロンプト、リスク評価 | 方針違反率、拒否精度、漏えい防止 | R28 |
| LLM-04 | Eval harness / golden set / rubric judge | A | LLMアプリの回帰と品質を継続測定する | 評価セット、rubric、スコア | 再現性、judge品質、ドリフト | R28, R29 |

---

## 4. skills 化を優先すべき技法トップ20

| 順位 | 技法 | 理由 |
| --- | --- | --- |
| 1 | 同値分割 | ほぼ全機能テストの最小単位。 |
| 2 | 境界値分析 | 欠陥密度が高い境界を狙える。 |
| 3 | デシジョンテーブル | 業務ルールの組合せ漏れに強い。 |
| 4 | 状態遷移テスト | ステータス・ワークフロー・画面遷移に強い。 |
| 5 | リスクベーステスト | 限られた時間の配分を説明できる。 |
| 6 | 探索的テスト | 仕様にないリスクを拾える。 |
| 7 | 組合せテスト | 環境・設定・パラメータ爆発を抑える。 |
| 8 | 構造カバレッジ設計 | 単体・APIの抜けを測れる。 |
| 9 | テストオラクル設計 | 自動化の合否判定を設計できる。 |
| 10 | プロパティベーステスト | 大量入力と不変条件で強く攻められる。 |
| 11 | メタモルフィックテスト | 正解が作りにくい対象に強い。 |
| 12 | ミューテーションテスト | テスト自体の弱さを測れる。 |
| 13 | ファジング | クラッシュ、セキュリティ、入力処理に強い。 |
| 14 | モデルベーステスト | 状態・プロトコルの網羅性を作りやすい。 |
| 15 | 差分テスト | 複数実装・複数バージョンをオラクル化できる。 |
| 16 | 契約テスト | API・マイクロサービスの破壊的変更を防ぐ。 |
| 17 | 回帰テスト選択・優先順位付け | CI/CDの現実に合う。 |
| 18 | 脅威モデリング + セキュリティテスト | 設計段階から攻撃面を潰せる。 |
| 19 | カオスエンジニアリング | 分散システムの耐障害性を実験できる。 |
| 20 | ML/LLM向けメタモルフィック・ロバストネステスト | AI系の非決定性とオラクル問題に向く。 |

---

## 5. 個別スキルカード

### SKILL-BB-01: 同値分割でテスト条件を抽出する

```yaml
purpose: 入力や条件を同じ振る舞いを期待できる集合に分け、代表値を選ぶ
when_to_use:
- 入力値、状態、種別、権限、設定などが分類できる
- 全値を試せない
inputs:
- 仕様
- 入力項目一覧
- 制約条件
procedure:
- 有効同値クラスを列挙する
- 無効同値クラスを列挙する
- 各クラスから代表値を選ぶ
- 期待結果とオラクルを定義する
outputs:
- 同値クラス表
- 代表値テストケース
coverage_or_exit:
- 全同値クラスが少なくとも1回は代表される
pitfalls:
- 無効クラスを忘れる
- 業務的に異なる値を同じクラスに押し込める
combine_with:
- 境界値分析
- デシジョンテーブル
```

### SKILL-BB-02: 境界値分析でテストケースを作る

```yaml
purpose: 欠陥が集中しやすい境界近傍を検査する
when_to_use:
- 数値、日付、時刻、件数、文字数、金額、閾値がある
inputs:
- 範囲仕様
- 包含/排他条件
- 単位、丸め、精度
procedure:
- 最小値、最大値、境界値を抽出する
- 直前、境界、直後を選ぶ
- 必要に応じて2値境界/3値境界を選ぶ
outputs:
- 境界値テストケース
coverage_or_exit:
- 各境界のon/offポイントを確認
pitfalls:
- 日付、タイムゾーン、丸め誤差を無視する
combine_with:
- 同値分割
- ドメイン分析
```

### SKILL-BB-03: デシジョンテーブルで業務ルールを検証する

```yaml
purpose: 複数条件と結果の対応を網羅し、矛盾・欠落を見つける
when_to_use:
- 条件が複数ある
- 条件組合せで処理や出力が変わる
inputs:
- 業務ルール
- 条件一覧
- 結果/アクション一覧
procedure:
- 条件を行に並べる
- アクションを行に並べる
- 条件組合せを列として作る
- 不可能条件や同値な列を整理する
- 各列からテストケースを作る
outputs:
- デシジョンテーブル
- テストケース
coverage_or_exit:
- 実行可能な全ルール列を確認
pitfalls:
- 条件の依存関係を無視して組合せ爆発させる
combine_with:
- 原因結果グラフ
- 組合せテスト
```

### SKILL-BB-04: 状態遷移テストを設計する

```yaml
purpose: 状態、遷移、イベント、ガード条件の欠陥を検出する
when_to_use:
- 注文、申請、認証、チケット、ジョブなど状態を持つ
inputs:
- 状態一覧
- イベント一覧
- 遷移条件
- 禁止遷移
procedure:
- 状態遷移図または表を作る
- 妥当遷移を列挙する
- 不正遷移を列挙する
- 全状態/全遷移/遷移ペアなどの基準を決める
outputs:
- 状態遷移図
- 遷移テストケース
coverage_or_exit:
- 全状態、全妥当遷移、重要な不正遷移を確認
pitfalls:
- キャンセル、再実行、戻る、タイムアウトを忘れる
combine_with:
- モデルベーステスト
- 探索的テスト
```

### SKILL-COM-01: 組合せテストを設計する

```yaml
purpose: パラメータや構成の組合せ爆発を抑えつつ相互作用欠陥を狙う
when_to_use:
- 入力パラメータ、設定、環境、権限、端末などが多数ある
inputs:
- 因子一覧
- 水準一覧
- 制約条件
- リスクの高い組合せ
procedure:
- 因子と水準を定義する
- 無効な組合せ制約を定義する
- t値を選ぶ。通常は2-wiseから始める
- 生成ツールや表でケースを作る
- リスクの高い組合せを追加する
outputs:
- 組合せテスト表
coverage_or_exit:
- 指定t-wiseの網羅
pitfalls:
- 因子分解が雑で、有効なテストにならない
- 重要な3要因以上の相互作用を無視する
combine_with:
- リスクベーステスト
- 分類木
- 境界値分析
```

### SKILL-PROP-01: プロパティベーステストを作る

```yaml
purpose: 入出力例ではなく、不変条件・性質を大量の生成入力で検査する
when_to_use:
- 関数、API、変換処理、パーサ、計算ロジックに不変条件がある
inputs:
- 期待する性質
- 入力型
- 生成器
- shrinker方針
procedure:
- propertyを自然言語で定義する
- propertyを実行可能なアサーションにする
- 入力生成器を作る
- 乱数seedを記録して実行する
- 失敗時に反例を最小化する
outputs:
- property test
- 反例
- 生成器
coverage_or_exit:
- 重要性質、生成分布、反例再現性
pitfalls:
- 仕様をpropertyに落とせていない
- 生成器が現実的入力を作らない
combine_with:
- メタモルフィックテスト
- ファジング
- ミューテーションテスト
```

### SKILL-META-01: メタモルフィックテストを設計する

```yaml
purpose: 正解出力を直接作りにくい対象を、入力変換と出力関係で検査する
when_to_use:
- 検索、推薦、科学計算、画像処理、ML、LLM、RAGなど
inputs:
- 変換前入力
- metamorphic relation
- 変換関数
- 出力比較規則
procedure:
- 期待される関係を定義する
- 入力変換を定義する
- 元入力と変換後入力を実行する
- 出力関係を検査する
- 違反を最小化・分類する
outputs:
- metamorphic relation一覧
- 変換テスト
- 違反レポート
coverage_or_exit:
- 重要な変換カテゴリと入力カテゴリの網羅
pitfalls:
- 関係が強すぎて偽陽性だらけになる
- 関係が弱すぎて欠陥を見逃す
combine_with:
- プロパティベーステスト
- 差分テスト
- ML/LLM評価
```

### SKILL-MUT-01: ミューテーションテストでテストの強さを測る

```yaml
purpose: 人工欠陥を埋め込み、テストスイートがそれを検出できるか測定する
when_to_use:
- 単体テストの品質を上げたい
- 高リスクロジックのテスト不足を見つけたい
inputs:
- ソースコード
- 既存テストスイート
- mutation operator
procedure:
- mutantを生成する
- テストを実行する
- killed/survivedを分類する
- 生存mutantを分析し、テストを追加する
- 等価mutantを除外または記録する
outputs:
- mutation score
- 生存mutantリスト
- 追加テスト案
coverage_or_exit:
- 重要モジュールのmutation score目標
pitfalls:
- 等価mutantに時間を溶かす
- スコアだけ追って意味のないテストを増やす
combine_with:
- 構造カバレッジ
- プロパティベーステスト
```

### SKILL-FUZZ-01: ファジングキャンペーンを設計する

```yaml
purpose: 予期しない入力でクラッシュ、例外、メモリ破壊、セキュリティ欠陥を見つける
when_to_use:
- パーサ、API、プロトコル、ファイル形式、入力境界がある
inputs:
- seed corpus
- harness
-oracle: crash, sanitizer, assertion, property
- 実行予算
procedure:
- テストハーネスを作る
- seed corpusを準備する
- sanitizerや監視を有効化する
- fuzzを実行する
- crashを重複排除し、最小化する
- 修正後に回帰corpusへ追加する
outputs:
- crash corpus
- 再現手順
- regression corpus
coverage_or_exit:
- 新規カバレッジ停滞、時間予算、クラッシュ収束
pitfalls:
- harnessが浅く、入口で全部弾かれる
- crashを再現可能にしていない
combine_with:
- 文法ベース生成
- シンボリック実行
- ASan/UBSan等の検出器
```

### SKILL-MBT-01: モデルベーステストを生成する

```yaml
purpose: 仕様モデルから体系的にテストを生成し、状態・遷移・制約を網羅する
when_to_use:
- 状態機械、プロトコル、ワークフロー、業務状態が明確
inputs:
- 状態モデル
- 操作/イベント
- ガード条件
- 期待結果
procedure:
- 抽象モデルを作る
- カバレッジ基準を選ぶ
- テスト列を生成する
- 具体入力へ写像する
- 実行結果をモデルと照合する
outputs:
- モデル
- 生成テスト
- トレース
coverage_or_exit:
- 状態、遷移、遷移ペア、シナリオの網羅
pitfalls:
- モデルが実装と同じバグを持つ
- モデル維持コストが見積もられていない
combine_with:
- 状態遷移テスト
- 差分テスト
```

### SKILL-DIFF-01: 差分テストを設計する

```yaml
purpose: 複数実装や複数バージョンの出力差から欠陥を見つける
when_to_use:
- 同一仕様の実装が複数ある
- 旧版と新版、競合実装、複数モデルを比較できる
inputs:
- 比較対象
- 共通入力
- 正規化ルール
- 差分判定ルール
procedure:
- 比較対象を決める
- 入力生成方法を決める
- 出力を正規化する
- 差分を検出する
- 仕様・多数決・追加オラクルで原因分析する
outputs:
- 差分入力
- 差分レポート
- 欠陥候補
coverage_or_exit:
- 入力カテゴリ、バージョン、実装ペアの網羅
pitfalls:
- 差分が仕様許容差か欠陥かを判定できない
combine_with:
- ファジング
- メタモルフィックテスト
- プロパティベーステスト
```

### SKILL-SYM-01: シンボリック / コンコリック実行を使う

```yaml
purpose: パス条件を解いて、人手では作りにくい入力を生成する
when_to_use:
- 分岐が多く、特定パスへの到達条件が複雑
- セキュリティ境界や例外処理を深く探索したい
inputs:
- 対象コード
- 制約ソルバ
- 探索戦略
procedure:
- 入力をシンボル化する
- 実行パス条件を収集する
- 分岐条件を反転して制約を解く
- 新しい入力で実行する
- パス爆発を制御する
outputs:
- 生成入力
- 到達パス
- 反例
coverage_or_exit:
- 重要パス到達、時間予算、制約未解決理由
pitfalls:
- 外部I/O、環境依存、複雑な文字列制約で詰まる
combine_with:
- ファジング
- 構造カバレッジ
```

### SKILL-API-01: 契約テストを設計する

```yaml
purpose: API提供者と利用者の期待のズレ、破壊的変更を検出する
when_to_use:
- マイクロサービス
- 複数チーム開発
- API versioningがある
inputs:
- OpenAPI/GraphQL/gRPC schema
- consumer expectation
- provider implementation
procedure:
- 契約を定義する
- consumer側で期待リクエスト/レスポンスを記録する
- provider側で契約を検証する
- CI/CDで互換性ゲートを設ける
outputs:
- contract file
- provider verification result
coverage_or_exit:
- 主要consumerの期待を網羅
pitfalls:
- 契約が実利用と乖離する
- エラー応答や後方互換性を忘れる
combine_with:
- APIスキーマテスト
- 後方互換性テスト
```

### SKILL-REG-01: 回帰テストを選択・優先順位付けする

```yaml
purpose: 変更に対して実行すべきテストを選び、早く重要欠陥を見つける
when_to_use:
- CI時間が限られる
- 回帰テストが肥大化している
inputs:
- 変更差分
- 依存関係
- 過去失敗履歴
- テスト実行時間
- リスク
procedure:
- 変更影響範囲を特定する
- 関連テストを選ぶ
- リスク・履歴・カバレッジ・実行時間で順位付けする
- 実行結果からモデルを更新する
outputs:
- 選択テスト集合
- 実行順序
- 残存リスク
coverage_or_exit:
- 重要変更の関連テスト実行、漏れ許容リスクの明示
pitfalls:
- 速さだけ追って重大欠陥を逃す
combine_with:
- テストインパクト分析
- リスクベーステスト
```

### SKILL-SEC-01: 脅威モデリングからセキュリティテストを作る

```yaml
purpose: 設計段階で攻撃面と脅威を洗い、テストへ落とす
when_to_use:
- 認証、認可、個人情報、金銭、外部公開APIがある
inputs:
- DFD
- 資産一覧
- trust boundary
- STRIDE等の脅威分類
procedure:
- 資産と境界を定義する
- DFDを作る
- 各要素に脅威カテゴリを当てる
- リスクを評価する
- セキュリティテストを設計する
outputs:
- 脅威一覧
- 対策一覧
- セキュリティテストケース
coverage_or_exit:
- 高リスク脅威への対策と検証の紐付け
pitfalls:
- ツール実行だけで満足し、設計脅威を見ない
combine_with:
- SAST
- DAST
- ペネトレーションテスト
- ファジング
```

### SKILL-RES-01: カオスエンジニアリング実験を設計する

```yaml
purpose: 分散システムが現実的障害に耐えられるか、制御された実験で確かめる
when_to_use:
- 冗長化、フェイルオーバー、自動復旧、SLOが重要
inputs:
- steady state仮説
- 障害注入計画
- blast radius
- 停止条件
- 観測指標
procedure:
- 正常状態を指標で定義する
- 障害仮説を立てる
- 小さいblast radiusで実験する
- メトリクスとユーザー影響を観測する
- 弱点を修正し再実験する
outputs:
- 実験記録
- 弱点一覧
- 改善結果
coverage_or_exit:
- 重要依存、障害種類、復旧パスの検証
pitfalls:
- 停止条件なしに本番で暴れる
- 実験ではなく単なる障害を作る
combine_with:
- フェイルオーバーテスト
- 監視テスト
- SLOレビュー
```

### SKILL-SAFE-01: STPAから安全テストを作る

```yaml
purpose: 制御構造と相互作用からハザードにつながる不安全制御を検出する
when_to_use:
- 人命、設備、社会インフラ、制御系に関わる
inputs:
- loss
- hazard
- control structure
- unsafe control action
procedure:
- 損失とハザードを定義する
- 制御構造を描く
- unsafe control actionを抽出する
- loss scenarioを作る
- シナリオをテスト条件へ変換する
outputs:
- UCA一覧
- loss scenario
- 安全テスト
coverage_or_exit:
- 重大ハザードとUCAの検証紐付け
pitfalls:
- コンポーネント故障だけを見て相互作用を見ない
combine_with:
- FMEA
- FTA
- ハザードシナリオテスト
- MC/DC
```

### SKILL-LLM-01: LLMアプリのメタモルフィック・ロバストネステスト

```yaml
purpose: 言い換え、形式差、文脈差でLLMアプリの出力が不当に揺れないか検査する
when_to_use:
- LLM、RAG、エージェント、チャットボット、分類器を使う
inputs:
- 元プロンプト
- 意味保持変換
- 期待する不変条件
- 判定rubric
procedure:
-品質属性を選ぶ。例: 正確性、一貫性、根拠性、安全性、公平性
- metamorphic relationを定義する
- prompt変換を作る
- 応答を収集する
- rubricまたは外部オラクルで比較する
- 違反をクラスタリングする
outputs:
- prompt suite
- MR違反一覧
- 回帰評価セット
coverage_or_exit:
- 重要タスク、入力カテゴリ、変換カテゴリ、リスクカテゴリの網羅
pitfalls:
- LLM judgeを無批判に正解扱いする
- 非決定性を考慮せず単発結果で結論を出す
combine_with:
- RAG groundedness test
- golden set eval
- adversarial testing
- human review
```

---

## 6. 対象別の推奨技法セット

### 6.1 一般的なWeb/SaaS

必須:

- 要求レビュー
- 同値分割
- 境界値分析
- デシジョンテーブル
- 状態遷移
- シナリオテスト
- 探索的テスト
- リスクベーステスト
- APIスキーマテスト
- 回帰テスト
- セキュリティ基本テスト
- 性能・負荷テスト

追加推奨:

- 組合せテスト
- 契約テスト
- テストインパクト分析
- アクセシビリティテスト
- 監視・ログテスト

### 6.2 API / マイクロサービス

必須:

- API契約テスト
- Consumer-Driven Contract Testing
- エラー応答テスト
- 認証・認可テスト
- Idempotency / retry / timeout test
- 後方互換性テスト

追加推奨:

- ファジング
- 差分テスト
- カオスエンジニアリング
- 非同期イベントテスト

### 6.3 組込み・制御・安全クリティカル

必須:

- 静的解析
- 形式レビュー
- MC/DC
- データフローテスト
- FMEA/FMECA
- FTA
- STPA/STAMP
- ハザードシナリオ
- 独立V&V
- トレーサビリティ検証

追加推奨:

- 抽象解釈
- モデル検査
- フォールトインジェクション
- ランタイム検証

### 6.4 パーサ、コンパイラ、プロトコル

必須:

- 構文テスト
- 文法ベースファジング
- 差分テスト
- プロパティベーステスト
- メタモルフィックテスト

追加推奨:

- シンボリック/コンコリック実行
- カバレッジガイド付きファジング
- ミューテーションテスト

### 6.5 データ基盤・ETL・分析

必須:

- データ品質テスト
- 件数・金額・参照整合性照合
- 境界値分析
- メタモルフィックテスト
- 差分テスト
- 回帰テスト

追加推奨:

- プロパティベーステスト
- ドリフト監視
- サンプリング検査

### 6.6 ML / LLM / RAG

必須:

- データセット検証
- golden set / eval harness
- メタモルフィックテスト
- ロバストネステスト
- RAG groundedness / hallucination test
- 安全性・悪用テスト
- 本番ドリフト監視

追加推奨:

- 差分テスト
- adversarial testing
- fairness/bias slice testing
- LLM red teaming

---

## 7. 技法選択マトリクス

| 状況 | 第一候補 | 第二候補 |
| --- | --- | --- |
| 入力範囲がある | 境界値分析 | 同値分割、ドメイン分析 |
| 条件分岐が多い | デシジョンテーブル | 原因結果グラフ、組合せテスト |
| 状態を持つ | 状態遷移テスト | モデルベーステスト、探索的テスト |
| 環境・設定が多い | 組合せテスト | リスクベース、分類木 |
| 正解出力が作りにくい | メタモルフィックテスト | 差分テスト、プロパティベーステスト |
| テストが弱い気がする | ミューテーションテスト | カバレッジ分析、レビュー |
| 入力処理が危ない | ファジング | 構文テスト、SAST/DAST |
| 深い分岐に届かない | シンボリック/コンコリック実行 | ファジング、SBST |
| API互換性が壊れる | 契約テスト | 後方互換性テスト、差分テスト |
| CIが遅い | 回帰テスト選択 | 優先順位付け、最小化 |
| 分散システムが不安 | カオスエンジニアリング | フェイルオーバー、監視テスト |
| セキュリティが重要 | 脅威モデリング | SAST/DAST、ペネトレーション、ファジング |
| 安全が重要 | STPA/FMEA/FTA | MC/DC、独立V&V |
| LLMがぶれる | Prompt robustness test | メタモルフィック、golden set、RAG groundedness |

---

## 8. 参考文献・標準・資料

| Ref | 資料 | メモ |
| --- | --- | --- |
| R1 | [ISTQB Certified Tester Foundation Level v4.0](https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/) | ブラックボックス、ホワイトボックス、経験ベース、協調ベースの基本整理。 |
| R2 | [ISO/IEC/IEEE 29119-4:2021 Software testing - Test techniques](https://www.iso.org/standard/79430.html) | テスト設計技法の国際標準。 |
| R3 | [ISO/IEC 25010:2023 Product quality model](https://www.iso.org/obp/ui/en/) | 品質特性から非機能テスト観点を導く。 |
| R4 | [IEEE 1012-2024 Standard for System, Software, and Hardware Verification and Validation](https://standards.ieee.org/ieee/1012/7324/) | V&Vをライフサイクル活動として整理。 |
| R5 | [SQuBOK / JCSQE関連情報](https://www.juse.jp/jcsqe/study/) | ソフトウェア品質技術の体系。 |
| R6 | [Claessen & Hughes, QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs, 2000](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf) | プロパティベーステストの代表的基礎文献。 |
| R7 | [Segura et al., A Survey on Metamorphic Testing](https://eprints.whiterose.ac.uk/id/eprint/110335/1/segura16-tse.pdf) | メタモルフィックテストの包括的サーベイ。 |
| R8 | [Segura et al., Metamorphic Testing: Testing the Untestable](https://research.nottingham.edu.cn/files/31438001/293_combinepdf_2_.pdf) | 実践導入向けの解説。 |
| R9 | [Jia & Harman, An Analysis and Survey of the Development of Mutation Testing](https://dl.acm.org/doi/10.1109/TSE.2010.62) | ミューテーションテストの代表的サーベイ。 |
| R10 | [NIST Automated Combinatorial Testing for Software](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software) | 組合せテストの研究・実践資料。 |
| R11 | [Kuhn et al., Practical Combinatorial Testing](https://www.nist.gov/publications/practical-combinatorial-testing) | 実務向け組合せテスト解説。 |
| R12 | [Zhu et al., Fuzzing: A Survey for Roadmap, 2022](https://dl.acm.org/doi/abs/10.1145/3512345) | ファジング技術のサーベイ。 |
| R13 | [The Fuzzing Book](https://www.fuzzingbook.org/) | random, mutation-based, grammar-based, symbolic testing等の実装付き教材。 |
| R14 | [Cadar & Sen, Symbolic Execution for Software Testing: Three Decades Later](https://people.eecs.berkeley.edu/~ksen/papers/cacm13.pdf) | シンボリック実行の代表的解説。 |
| R15 | [Sen et al., CUTE: A Concolic Unit Testing Engine for C](https://dl.acm.org/doi/10.1145/1095430.1081750) | コンコリックテストの基礎文献。 |
| R16 | [Utting et al., A taxonomy of model-based testing approaches](https://dl.acm.org/doi/abs/10.1002/stvr.456) | MBTの分類と全体像。 |
| R17 | [McMinn, Search-Based Software Testing: Past, Present and Future](https://philmcminn.com/publications/mcminn2011.pdf) | 探索ベーステストの概観。 |
| R18 | [McKeeman, Differential Testing for Software, 1998](https://www.cs.tufts.edu/comp/150FP/archive/bill-mckeeman/DifferentailTesting.pdf) | 差分テストの古典的文献。 |
| R19 | [Yoo & Harman, Regression Testing Minimization, Selection and Prioritization](https://onlinelibrary.wiley.com/doi/abs/10.1002/stvr.430) | 回帰テスト最小化・選択・優先順位付けのサーベイ。 |
| R20 | [Barr et al., The Oracle Problem in Software Testing: A Survey](https://dl.acm.org/doi/10.1109/TSE.2014.2372785) | テストオラクル問題の代表的サーベイ。 |
| R21 | [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) | Webセキュリティテストの実務ガイド。 |
| R22 | [NIST SP 800-115 Technical Guide to Information Security Testing and Assessment](https://csrc.nist.gov/pubs/sp/800/115/final) | 情報セキュリティテスト・評価の技術ガイド。 |
| R23 | [Microsoft Threat Modeling Tool Overview](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool) | STRIDE等による脅威モデリング実務。 |
| R24 | [NASA, A Practical Approach to Modified Condition/Decision Coverage](https://ntrs.nasa.gov/api/citations/20040086014/downloads/20040086014.pdf) | MC/DCの実践的解説。 |
| R25 | [Leveson & Thomas, STPA Handbook](https://www.flighttestsafety.org/images/STPA_Handbook.pdf) | STPAのハンドブック。 |
| R26 | [Pei et al., DeepXplore: Automated Whitebox Testing of Deep Learning Systems](https://arxiv.org/abs/1705.06640) | DLシステムのwhite-boxテスト。 |
| R27 | [Zhang et al., Machine Learning Testing: Survey, Landscapes and Horizons](https://solar.cs.ucl.ac.uk/pdf/zhang2019machine.pdf) | MLテストの包括的サーベイ。 |
| R28 | [Wang et al., Software Testing With Large Language Models, 2024](https://www.computer.org/csdl/journal/ts/2024/04/10440574/1UGSj5dgwNO) | LLMを用いた/対象としたテストのサーベイ。 |
| R29 | [Metamorphic Testing for Fact-Conflicting Hallucination Detection in LLMs, 2024](https://dl.acm.org/doi/full/10.1145/3689776) | LLM hallucination検出へのメタモルフィックテスト応用。 |
| R30 | [Principles of Chaos Engineering](https://principlesofchaos.org/) | カオスエンジニアリングの原則。 |
| R31 | [Open Liberty: Testing microservices with consumer-driven contracts](https://openliberty.io/guides/contract-testing.html) | Pactによる契約テスト実践。 |
| R32 | [Woodcock et al., Formal Methods: Practice and Experience](https://epubs.stfc.ac.uk/manifestation/4234/fmsurvey.pdf) | 形式手法の実践と経験。 |
| R33 | [Sánchez et al., A Survey of Challenges for Runtime Verification](https://arxiv.org/abs/1811.06740) | ランタイム検証の課題と応用。 |
| R34 | [Su et al., A Survey on Data-Flow Testing](https://tingsu.github.io/files/data-flow-testing-survey.pdf) | データフローテストのサーベイ。 |

---

## 9. 次に作るとよい派生ファイル

- `skills/equivalence_partitioning.md`
- `skills/boundary_value_analysis.md`
- `skills/decision_table_testing.md`
- `skills/state_transition_testing.md`
- `skills/combinatorial_testing.md`
- `skills/property_based_testing.md`
- `skills/metamorphic_testing.md`
- `skills/mutation_testing.md`
- `skills/fuzz_testing.md`
- `skills/model_based_testing.md`
- `skills/differential_testing.md`
- `skills/contract_testing.md`
- `skills/regression_test_selection.md`
- `skills/security_threat_modeling.md`
- `skills/llm_metamorphic_testing.md`

---

## 10. 実務での注意

1. **テスト技法は選択理由と除外理由を記録する。**
    
    技法を使わなかったこと自体は罪ではない。理由を説明できないのが罪である。
    
2. **カバレッジは品質そのものではない。**
    
    100%カバレッジでも、オラクルが弱ければ欠陥は素通りする。人間も機械も、見ているふりが得意で困る。
    
3. **自動生成技法はオラクルとセットで設計する。**
    
    生成できても判定できなければ、ただの高速な混乱製造機になる。
    
4. **AI/LLMのテストは非決定性を前提にする。**
    
    単発の合否ではなく、分布、揺らぎ、再現性、意味保持変換、根拠性を扱う。
    
5. **安全・セキュリティ・個人情報は「機能テストのついで」にしない。**
    
    ついでに済ませたものは、だいたいついでに漏れる。