# 欠陥タクソノミーと ODC — 直交欠陥分類・トリガー/インパクト属性・欠陥分布分析

## エグゼクティブサマリ

欠陥は、1件ずつ物語として読むだけでは工程の診断になりません。ODC(Orthogonal Defect Classification、直交欠陥分類)は、IBM Research の Chillarege らが 1992 年に提案した、**欠陥を少数の直交する属性で分類し、その分布から開発プロセスの状態(工程シグネチャ)を読み取る in-process 測定手法**です。個々の欠陥の根本原因を深掘りする代わりに、欠陥ストリーム全体を統計的に扱うことで、「どの工程が欠陥を作り込んでいるか」「どのテスト活動が想定どおり欠陥を検出できているか」を、開発の進行中に低コストで診断します。

実務上の要点は四つです。第一に、**ODC の情報は2時点で採れる**ことです。欠陥を発見した時点(opener)では「何をしていて(Activity)、何が引き金で表面化し(Trigger)、顧客に何が起きるか(Impact)」が分かり、修正した時点(closer)では「何を直したか(Target・Defect Type・Qualifier・Source・Age)」が分かります。第二に、**分類は直交(相互排他・網羅的)で、値の意味は工程と結びついている**ことです。たとえば欠陥タイプの Function は設計段階の作り込み、Assignment は実装段階の作り込みを示唆するため、タイプ分布が工程の進行と整合しないとき、それが是正すべきシグナルになります。第三に、**トリガー分布はテストの診断装置である**ことです。トリガーは「その欠陥を表面化させるのに必要だった条件」であり、テストレベルごとに期待されるトリガーの偏りから、テスト戦略の弱点(たとえばシステムテストで単機能欠陥が多発=機能テストの取りこぼし)を特定できます。第四に、**ODC は個別 RCA の代替ではなく補完である**ことです。ODC で欠陥ストリーム全体から問題領域を絞り、代表欠陥にだけ深掘り RCA を行う組み合わせが、コストとカバレッジの両立点です。

本ドキュメントは、欠陥分類の考え方と標準の系譜(§1)、ODC の構造(§2)、opener 属性(§3)、closer 属性(§4)、分布分析のパターン(§5)、RCA との関係(§6)、運用と AI エージェント適用の注意(§7)を扱います。欠陥密度・欠陥流出率などのメトリクス定義は[品質管理実務リファレンス](./software-quality-management-practical-reference.md)、件数・密度メトリクスの誤用とゲーミングは[品質メトリクスの落とし穴](./quality-metrics-pitfalls.md)、実行ログからの欠陥候補抽出は test-execution-support スキルの `DefectCandidateList` を正とし、本ドキュメントでは重複させません。

## 1. 欠陥分類の考え方と標準の系譜

欠陥データを組織の学習に変える方法は、大きく2系統あります。

| 系統 | 代表 | 特徴 | コスト |
| --- | --- | --- | --- |
| 個別深掘り(因果分析) | RCA(5 Whys・フィッシュボーン・FTA・STPA 等) | 1件の欠陥・障害の因果連鎖を深く追う。是正は具体的 | 高い。全欠陥には適用できず、対象選定にバイアスが入る |
| 分類・統計(タクソノミー) | ODC、IEEE 1044 系の異常分類 | 全欠陥を少数属性で分類し、分布の形から工程を診断する。網羅的・継続的 | 1件あたり数分程度の分類コスト。洞察は集合レベル |

標準の系譜としては、IEEE 1044-2009(Standard Classification for Software Anomalies)がソフトウェア異常(anomaly)分類の統一アプローチを定めていました(1993 年版を置き換え。現在は inactive-reserved 状態であり、現行プロジェクトの規範としてではなく分類スキーム設計の参照点として扱います)。一方 ODC は、標準ではなく **IBM Research 発の測定手法**として発展し、属性設計が「分類のための分類」ではなく「工程へのフィードバック」に最適化されている点が特徴です。本リポジトリでは、欠陥分類の実務語彙として ODC を主参照とします。

分類が測定として機能するための条件は、1992 年の原論文が「直交性」として定式化しています。すなわち、(1) 各属性の値が相互排他で、どの欠陥も一意に分類できること、(2) 値の集合がプロセスに対して十分網羅的であること、(3) 分類が特定プロダクトや組織に依存せずプロセス横断で安定していること、です。値を現場ごとに増改築すると分布の比較可能性(=測定であること)が壊れるため、ODC の運用では **Activity(自組織の工程)は組織が定義するが、Trigger の値集合は再定義しない**というルールが明示されています(ODC v5.2)。

## 2. ODC の構造 — 2時点・8属性

ODC v5.2(Software Design and Code 向け)は、欠陥1件につき8属性を、情報が自然に手に入る2時点に分けて記録します(ODC v5.2 §2)。

| 時点 | 属性 | 何を捉えるか |
| --- | --- | --- |
| opener(発見時) | Activity | 欠陥発見時に実際に行っていた欠陥除去活動 |
| opener(発見時) | Trigger | 欠陥を表面化させるのに必要だった環境・条件(再現に何が要るか) |
| opener(発見時) | Impact | 流出した場合に顧客へ及ぶ(または及んだ)影響の種類 |
| closer(修正時) | Target | 修正した実体の種別(要求・設計・コード等) |
| closer(修正時) | Defect Type | 修正の実際の内容(何を直したか) |
| closer(修正時) | Qualifier | 欠落(Missing)・誤り(Incorrect)・余分(Extraneous)の別 |
| closer(修正時) | Source | 修正対象の開発来歴(内製・再利用・外注・移植) |
| closer(修正時) | Age | 修正対象コードの年代(既存・新規・書き直し・再修正) |

opener 属性は欠陥票の起票時に、closer 属性は修正完了時に記録します。発見時に判断できない属性は unknown で開き、判明時に埋めます(未記録のまま放置しない)。severity・phase-found・コンポーネントなど、欠陥管理システムが持つ非 ODC 属性は ODC 分析と併用します(ODC v5.2 §5.1)。

## 3. opener 属性 — Activity・Trigger・Impact

### 3.1 Activity

欠陥発見時に実際に行っていた活動です。カレンダー上のフェーズではなく実際の活動を選びます(システムテスト期間中にコードインスペクションで見つけたなら Activity はコードインスペクション)。v5.2 の設計・コード向け標準値は、**設計レビュー/コードインスペクション/単体テスト/機能テスト/システムテスト**の5種です。フィールド欠陥(顧客報告)には「本来どの工程活動が捕捉すべきだったか」を割り当てます(§3.3)。

### 3.2 Trigger — 欠陥を表面化させた条件

Trigger は「その欠陥が表面化するために存在しなければならなかった環境・条件」であり、ODC の中で最もテスト診断に直結する属性です。値は Activity ごとに対応づけられた21種で、組織はこの値集合を再定義しません(ODC v5.2 §2.1・§3.2)。

| Activity | Trigger(v5.2) | 概要 |
| --- | --- | --- |
| 設計レビュー/コードインスペクション | Design Conformance / Logic-Flow / Backward Compatibility / Lateral Compatibility / Concurrency / Internal Document / Language Dependency / Side Effect / Rare Situations | 前工程成果物との突合、ロジック・データフローの検査、旧版・隣接プロダクトとの互換、共有資源の直列化、内部文書整合、言語仕様、波及効果、稀な状況の予見 |
| 単体テスト | Simple Path / Complex Path | コード内部の分岐知識に基づく単純パス/複合パスの実行 |
| 機能テスト | Test Coverage / Test Variation / Test Sequencing / Test Interaction | 単機能の素直な実行/入力バリエーション(不正値・境界値)/特定順序の実行/複数機能の相互作用 |
| システムテスト | Workload-Stress / Recovery-Exception / Startup-Restart / Hardware Configuration / Software Configuration / Blocked Test | 資源限界近傍の負荷/例外・回復処理の起動/起動・再起動/ハード構成/ソフト構成/基本問題によるシナリオ実行不能 |

読み方の要点は「**トリガーはテスト技法の到達範囲を表す**」ことです。機能テスト系トリガー(単機能・バリエーション)の欠陥がシステムテストやフィールドで見つかっているなら、機能テストの網羅に穴があります。逆に、レビュー系トリガー(Design Conformance・Logic/Flow)の欠陥が後工程で大量に出るなら、レビュー・インスペクションの実効性が疑われます。Butcher らの IBM 3事例(2002)は、この trigger 分布の分析からテスト戦略の弱点を特定し、テスト強化やリリース時期の判断につなげた実例です。

### 3.3 フィールド欠陥への適応

顧客報告欠陥では、顧客は設計文書やコード内部にアクセスしないため、内部知識系トリガー(Logic/Flow・Simple/Complex Path 等)は通常選ばれず、Blocked Test は使いません。主観を抑えるため、v5.2 は (1) 欠陥の表面化に必要だった条件に最も合う Trigger を全リストから選ぶ、(2) 組織の activity→trigger 対応表から、その Trigger の捕捉に一次責任を持つ工程活動を Activity として割り当てる、という順序を規定しています(§3.1.6・§5.3)。この「本来捕捉すべきだった活動」への割り戻しが、フィールド欠陥を工程改善のシグナルに変換します。

### 3.4 Impact — 顧客影響の種類

流出時に顧客へ及ぶ影響の種類です。in-process 欠陥では「流出していたら何が起きたか」を、フィールド欠陥では実際の影響を選びます。v5.2 の値は **Installability / Integrity-Security / Performance / Maintenance / Serviceability / Migration / Documentation / Usability / Standards / Reliability / Requirements / Accessibility / Capability** の13種です。これは IBM の伝統的な品質特性系の語彙であり、ISO/IEC 25010:2023 の9特性と一対一対応しません。本リポジトリで品質特性として扱う場合は [iso25010-product-quality-model.md](../quality-models/iso25010-product-quality-model.md) の語彙へマッピングして使い、Impact 属性は「欠陥データ側の分類」として保持します(両者の混用が語彙衝突の典型源です)。

## 4. closer 属性 — Target・Defect Type・Qualifier・Source・Age

### 4.1 Target と Defect Type

Target は修正した実体の種別(Requirements / Design / Code / Build-Package / Information Development / National Language Support)です。Defect Type は Target=Design/Code の場合の「修正の実際の内容」で、v5.2 では7値です。**Defect Type は欠陥の症状ではなく修正内容で分類する**ことが最重要ルールです(症状は Trigger・Impact が捉えます)。

| Defect Type | 修正の内容 | 関連づく工程(シグネチャ解釈) |
| --- | --- | --- |
| Assignment/Initialization | 値の代入・初期化の誤り・欠落 | 実装(低位) |
| Checking | パラメーター・データの検証(条件文)の欠落・誤り | 実装 |
| Algorithm/Method | 設計変更を要さない範囲のアルゴリズム・局所データ構造の是正 | 詳細設計〜実装 |
| Function/Class/Object | 正式な設計変更を要する能力・外部/製品インターフェース・グローバル構造の是正 | 上流設計 |
| Timing/Serialization | 共有資源の直列化の欠落・誤った資源・誤った手法 | 設計(並行性) |
| Interface/O-O Messages | モジュール・コンポーネント・オブジェクト間の連絡(呼び出し・引数・メッセージ)の誤り | 結合設計 |
| Relationship | 手続き・データ構造・オブジェクト間の関係(前提・継承・多重度)の誤り | 設計 |

各タイプが工程と結びついているため、タイプ分布は「どの工程が作り込み源か」を示します(§5.1)。

### 4.2 Qualifier・Source・Age

- **Qualifier**: 修正が補ったものの性質。Missing(欠落=作為の不在)/ Incorrect(誤り=作為の誤り)/ Extraneous(余分=不要物の存在)。同じ Checking でも「チェックが無かった」と「チェック条件が誤っていた」では、レビュー・テストの対策が異なります。
- **Source**: 修正対象の来歴。Developed In-House / Reused From Library / Outsourced / Ported。再利用部品・外注部品・移植部品に欠陥が偏っていれば、受け入れ検証やサプライヤー管理の問題として扱います([セキュア開発とサプライチェーン](../secure-development/secure-development-and-supply-chain.md)の依存関係リスク管理と接続)。
- **Age**: 修正対象コードの年代。Base(今回未変更の既存部=潜在欠陥)/ New(新規)/ Rewritten(書き直し)/ ReFixed(過去の修正の修正)。**ReFixed の比率は修正プロセス自体の品質指標**であり、高止まりは修正時のレビュー・回帰テスト不足を示します。Base が多い場合は、今回の変更とは別に既存資産の劣化(または新しい使われ方による顕在化)が進んでいるシグナルです。

## 5. 分布分析のパターン

ODC の価値は分類そのものではなく、分布を読む分析にあります。代表パターンを挙げます。いずれも「単一の数値目標」ではなく「分布の形と時間変化」を見ます(件数・密度を目標化したときの歪みは[品質メトリクスの落とし穴](./quality-metrics-pitfalls.md)の通りです)。

1. **Defect Type の工程シグネチャ**: 開発の進行に伴い、タイプ分布は上流型(Function 等)から下流型(Assignment・Checking 等)へ移行していくことが期待されます。工程後半になっても Function/Class/Object(設計変更を要する修正)が減らないなら、設計の安定化が遅れており、テストを増やしても解決しません(1992 年原論文の中心概念)。
2. **Trigger によるテスト診断**: テストレベルごとの期待トリガーと実測トリガーのずれを見ます(§3.2)。システムテスト工程で Coverage / Variation トリガー(機能テスト級)の欠陥が多発していれば機能テストの強化を、フィールドで Workload/Stress・Recovery が多ければシステムテストの環境・負荷設計の見直しを検討します。
3. **Trigger × Defect Type の二元分析**: 「何が引き金で、何を直したか」の掛け合わせは、単独属性より診断を絞り込みます。例: Concurrency トリガー × Timing/Serialization タイプの集中は並行設計の系統的な弱さを、Design Conformance トリガー × Missing 修飾子の集中は仕様の伝達不全(書かれていない・読まれていない)を示唆します。
4. **Age / Source 分析**: ReFixed 率の推移(修正品質)、Base 欠陥の比率(既存資産の劣化)、Source 別の欠陥率(部品来歴別の品質)を追います。
5. **欠陥密度との併用**: 欠陥密度(件数/規模)は「どこに多いか」しか語らず、「なぜ多いか・何が捕まえたか」は ODC 属性が語ります。密度の定義・分母の扱いは[品質管理実務リファレンス](./software-quality-management-practical-reference.md)を、分母操作・比較の罠は[品質メトリクスの落とし穴](./quality-metrics-pitfalls.md#欠陥密度の分母問題)を参照してください。密度で領域を絞り、ODC 分布でその領域の性質を診断する、という順で併用します。

分析の前提となるサンプル規模について、分布の解釈は欠陥数十件からが目安であり、数件レベルでは個別レビュー(または §6 の RCA)のほうが適切です。少数データで分布を語ることは、平均値の罠([品質メトリクスの落とし穴](./quality-metrics-pitfalls.md#mttrインシデントメトリクスの限界))と同型の誤りです。

## 6. RCA との関係 — 代替ではなく補完

古典的な RCA(5 Whys・フィッシュボーン・FTA・STPA など。手法自体は [domain-specific-quality-and-safety-standards.md](../governance-compliance/domain-specific-quality-and-safety-standards.md#2-hazard-analysis-の手法) を参照)は、1件の欠陥・障害に対して深い因果連鎖と具体的な是正を与えますが、コストが高く、全欠陥には適用できません。Chillarege は、抽象度を上げて分析を体系化することで、古典的 RCA に対し時間と欠陥ストリームのカバレッジの両面で一桁の生産性向上を狙う手法として ODC を位置づけています("ODC - a 10x for Root Cause Analysis", 2006)。

実務の組み合わせ方は次の通りです。

1. **ODC で全量を分類**し、分布から問題領域(工程×タイプ×トリガーの集中)を特定する。
2. 集中領域から**代表欠陥を少数選び、深掘り RCA** を行う(選定が分布に基づくため、声の大きい欠陥・直近の欠陥に引きずられるバイアスを避けられる)。
3. RCA の是正策の効果を、**次期間の ODC 分布の変化で検証**する(是正が効けば該当セルの集中が解消するはず)。

この運用はブレームレス原則を前提とします。欠陥データを個人・チームの評価に使った時点で、起票抑制・分類操作が始まり、分布は診断能力を失います(バグ件数を評価に使うことの帰結は[品質メトリクスの落とし穴](./quality-metrics-pitfalls.md#バグ件数の解釈問題)、ブレームレスポストモーテムの実践は[本番品質・SRE・可観測性](../operations-quality/production-quality-sre-observability.md)を参照)。

## 7. 運用と AI エージェント適用の注意

- **分類の一貫性が測定の生命線**: 分類者ごとのぶれは分布を汚します。値の定義と例を短い判定ガイドとして共有し、定期的に相互チェック(同一欠陥の独立分類の一致率確認)を行います。判断に迷う欠陥は unknown のまま開き、確定時に埋めます(誤った確定分類より未確定の明示が優ります)。
- **属性を増改築しない**: ローカルな「便利な値」の追加は直交性と比較可能性を壊します。組織カスタマイズは activity→trigger 対応の定義に限定します(§1)。
- **分類の目標化を避ける**: 「Checking 欠陥を減らす」等の分類別目標は、分類操作(付け替え)を誘発します。目標は是正策(例: 入力検証の設計規約とレビュー観点の導入)に置き、分布は観察用に保ちます([品質メトリクスの落とし穴](./quality-metrics-pitfalls.md#健全なメトリクス設計--落とし穴を避ける実務プロトコル)の観察用/制御用分離)。
- **AI エージェントが分類を担う場合**: (1) 各分類に根拠(Trigger なら再現に必要だった条件の記述箇所、Defect Type なら修正 diff の内容)を必ず付し、根拠を構成できない属性は unknown とする。(2) 症状からの Type 推定(修正を見ずに分類)をしない — closer 属性は修正情報が入力にあるときだけ確定する。(3) 分類結果は助言であり、欠陥 DB への登録・運用は実行系が担う(本リポジトリは分類・分析手順のブループリントに留まる)。
- **入力データの契約**: テスト実行結果からの欠陥候補抽出は test-execution-support(RUN・`DefectCandidateList`)が担い、本タクソノミーはその下流の分類・分析語彙を提供します。リスク登録簿への反映(欠陥傾向→リスク項目の更新)は risk-analysis の `RiskRegister` 契約に従います。

## 主要参考文献

ODC 一次資料:

- Ram Chillarege et al., "Orthogonal Defect Classification - A Concept for In-Process Measurements"(IEEE Transactions on Software Engineering 18(11), 1992): https://doi.org/10.1109/32.177364
- IBM, "Orthogonal Defect Classification v 5.2 for Software Design and Code"(2013、属性・値定義の実務リファレンス): https://s3.us.cloud-object-storage.appdomain.cloud/res-files/70-ODC-5-2.pdf
- Chillarege Inc, ODC 解説(論文集約ページ): https://www.chillarege.com/odc.html
- Ram Chillarege, "ODC - a 10x for Root Cause Analysis"(2006): http://chillarege.com/articles/odc-10x-root-cause-analysis.html

適用事例・関連標準:

- Mark Butcher, Hilora Munro, Theresa Kratschmer, "Improving software testing via ODC: Three case studies"(IBM Systems Journal 41(1), 2002): https://doi.org/10.1147/sj.411.0031
- IEEE 1044-2009, IEEE Standard Classification for Software Anomalies(inactive-reserved): https://standards.ieee.org/ieee/1044/4607/

## 関連ドキュメント

- [品質管理実務リファレンス](./software-quality-management-practical-reference.md) — 欠陥密度・欠陥流出率等のメトリクス定義と運用
- [品質メトリクスの落とし穴](./quality-metrics-pitfalls.md) — バグ件数・欠陥密度の誤用、観察用/制御用の分離、重大度インフレ
- [ドメイン別品質・安全規格](../governance-compliance/domain-specific-quality-and-safety-standards.md) — FMEA/FTA/STPA 等の hazard analysis・RCA 手法
- [本番品質・SRE・可観測性](../operations-quality/production-quality-sre-observability.md) — ブレームレスポストモーテムとインシデントからの学習
- [ISO/IEC 25010 製品品質モデル](../quality-models/iso25010-product-quality-model.md) — Impact 属性をマッピングする際の品質特性の正典語彙
