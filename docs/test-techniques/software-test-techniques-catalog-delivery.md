# ソフトウェアテスト技法カタログ納品

## 結論

既存ドラフトを棚卸しし、**原案95技法**を基点に、標準・規格・査読研究で裏づけを付け直したうえで、**LLM/skills 利用向けの完全な skill-card 形式**へ再構成した検証版 Markdown と、**技法ごとの状態判定 CSV** を作成しました。JSTQB/ISTQB Foundation v4.0 はブラックボックス、ホワイトボックス、経験ベース、協調ベースのアプローチを明示し、ISO/IEC/IEEE 29119-4:2021 は requirements-based、scenario、state transition、syntax、random、combinatorial、metamorphic、branch、decision、MC/DC、data flow、statement などを定義しています。さらに ISO/IEC 25010:2023 は製品品質モデルを9特性で定義し safety を追加しており、IEEE 1012-2024 は V&V を testing だけでなく analysis、review、inspection、assessment を含むライフサイクル活動として扱います。JCSQE 初級シラバスも、レビュー、テスト設計、組合せ技法、状態遷移、リスク識別、安全性技法、品質分析技法を含んでいます。

## 検証の要点

今回の検証では、原案の広いカバレッジ自体は強みとして維持しつつ、個票が主に「ID・技法・優先度・使う場面・主な出力・完了/評価観点・参考」の7列にとどまっていた点を補い、各技法に **目的、適用条件、入力、手順、成果物、オラクル設計、注意点、推奨ツール、カバレッジ指標、優先度、主要参照** を付与しました。特に 29119-4 で明示される requirements-based testing や、NIST が継続的に発展させている combinatorial methods と event sequence testing を反映したことで、標準との整合性と実務展開性がかなり改善されています。

原案に対して重要だった追加は、**要求ベーステスト、シーケンスカバリングアレイ、状態付きプロパティベーステスト、不変条件推定オラクル、差分ファジング、デルタデバッグ、フレーキーテスト検知・隔離、OpenAPI/GraphQL 由来のスキーマ駆動プロパティテスト、Intramorphic Testing、MR自動合成** です。これらは、古典的なシラバス中心の整理だけでは拾いにくい一方で、近年の研究と実務で有効性が強く示されています。Property-based testing は近年の実務研究で広く使われており、Metamorphic Testing はオラクル問題への主要アプローチとして定着しています。Mutation Testing はコスト削減と実務知見が体系化され、Fuzzing は統一的な分類を持つ成熟分野になっています。Symbolic Execution、Differential Testing、Chaos Engineering、Contract Testing、Fairness Testing、LLM-based Testing も近年のサーベイや実務文書で有力な領域として整理されています。

AI/ML/LLM 系は、重要度は高いものの、**confidence は保守的**に扱いました。理由は、たとえば neur on coverage 系は DeepXplore や DeepGauge で提案されてきた一方、後続研究で「欠陥発見能力の有意味な指標とは限らない」という批判が示されているためです。また、LLM testing は急速に拡大しているものの、評価セット汚染、judge bias、非決定性、安全性評価の再現性が依然として課題です。そこで、検証版では AI/LLM 個票に注意点と適用条件を明示し、過度な一般化を避けています。

## 主要な追加と修正

今回の版で特に価値が高い修正は三つあります。第一に、**標準の芯を揃えたこと**です。JSTQB/ISTQB、29119-4、25010、1012、JCSQE の観点を技法単位にマッピングし、どの技法がどの品質特性や V&V 観点を支えるかを見える化しました。第二に、**オラクル設計と自動化の粒度を上げたこと**です。PBT、MT、差分、契約、RAG groundedness、red teaming など、従来の「技法名だけ知っている」状態では実装に落ちない領域を、実行可能なカードに分解しました。第三に、**近年の実務問題を埋めたこと**です。NIST の sequence covering arrays、Pact 系 contract testing、Schemathesis の schema-driven property testing、flaky test survey、delta debugging、intramorphic testing などを追加し、現代の CI/CD・API・生成AI 実務に繋がる形へ更新しました。

## 成果物

検証済み Markdown ファイル

> **注記（2026-07-06 リポジトリ整理時に追記。原文ではない）:** 検証版 Markdown（135技法の skill-card 形式 `software_test_techniques_validated_ja.md`）は本リポジトリに未収録。現存する [test-techniques-skill-catalog.md](test-techniques-skill-catalog.md) は検証前の原案（95技法）に相当する。

状態判定 CSV ファイル

[test-technique-status-assessment.csv](test-technique-status-assessment.csv)（原案95技法＋追加提案40技法＝135技法の状態判定）

## 根拠にした標準と研究

主要根拠は、JSTQB Foundation Level v4.0、ISO/IEC/IEEE 29119-4:2021、ISO/IEC 25010:2023、IEEE 1012-2024、JCSQE 初級シラバス、NIST combinatorial testing、OWASP WSTG/ASVS/API Security、PBT・MT・Mutation・Fuzzing・Symbolic Execution・Differential Testing・Chaos Engineering・Contract Testing・Fairness Testing・LLM Testing の主要サーベイと査読論文です。これにより、基礎技法だけでなく、API・分散・安全・AI/LLM まで含めた現代的なテスト技法体系として、かなり実務再利用しやすい内容になっています。