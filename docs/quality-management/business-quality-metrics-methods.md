# 事業品質メトリクス — VOC・NPS・チャーン・LTV と品質シグナルの相関分析

## エグゼクティブサマリ

品質活動の事業価値は、「品質シグナル（欠陥密度・SLO 違反・クラッシュ率など）が、事業指標（VOC・NPS・チャーン・LTV）とどうつながっているか」を示せて初めて経営の言葉になります。本ドキュメントは、その接続に使う4系統の事業指標の定義・手法・限界と、品質シグナルとの相関分析の組み方を扱います。

実務上の要点は四つです。第一に、**事業指標は遅行指標である**ことです。NPS やチャーンの変化はリリース品質の劣化から数週間〜数四半期遅れて現れるため、先行指標（品質シグナル）とラグを設計した突合が必要です。第二に、**NPS を単独 KPI にしない**ことです。NPS の原主張（成長の最良予測子）は、その後の縦断研究で「他指標に対する明確な優位性」を再現できていません（Keiningham らの 2007 年の追試）。第三に、**チャーン・LTV は平均値の外挿ではなく確率モデルで扱う**ことです。顧客ごとの解約傾向は異質であり、集計平均の単純外挿はリテンション曲線を系統的に誤ります（Fader & Hardie の sBG/BG-NBD 系モデル）。第四に、**相関は主張してよいが、因果は主張しない**ことです。観察データから言えるのは「関連の強さと時間的先行」までであり、因果の断定には介入（実験）が必要です。

本ドキュメントは、位置づけとスコープ（§1）、VOC（§2）、NPS（§3）、チャーン（§4）、LTV（§5）、GQM による相関分析の設計（§6）、運用と AI エージェント適用の注意（§7）を扱います。SUS・CSAT を含む質問紙の運用は[アクセシビリティ・UX・人間中心品質](../human-centered-quality/accessibility-ux-human-centered-quality.md)、メトリクス誤用とゲーミング対策は[品質メトリクスの落とし穴](./quality-metrics-pitfalls.md)、GQM の品質管理全般での位置づけと COQ は[品質管理実務リファレンス](./software-quality-management-practical-reference.md)、品質シグナル側（SLI/SLO・DORA）の定義は[本番品質・SRE・可観測性](../operations-quality/production-quality-sre-observability.md)を正とし、本ドキュメントでは重複させません。

## 1. 位置づけとスコープ

本ドキュメントが扱うのは**手法**です。実データ（自社の NPS 実測値・解約率・顧客名簿）は動的ナレッジであり、このリポジトリには置きません（設計原則 P5）。分析の実行・データ収集・ダッシュボード構築は実行系・分析基盤が担い、本ドキュメントと #15 business-quality-metrics スキルは、分析の枠組み（GQM 構造・指標の選定・相関設計・解釈の限界）を提供します。

4指標の関係は次のとおりです。VOC は**言語データ**（顧客が何に困っているか）、NPS は**態度データ**（推奨意向）、チャーンは**行動データ**（実際に離脱したか）、LTV は**行動を金額換算した予測**です。左から右へ行くほど事業インパクトに近く、品質シグナルからは遠く（遅く）なります。相関分析ではこの階層を意識し、「品質シグナル → VOC/NPS（態度）→ チャーン（行動）→ LTV（金額）」の順に接続を確かめると、飛躍の少ない議論になります。

## 2. VOC — 顧客の声の構造化

VOC（Voice of the Customer）は、Griffin と Hauser が QFD（品質機能展開）の文脈で定式化した概念で、顧客ニーズの**識別・構造化・優先度付け**の3タスクからなります（Marketing Science, 1993）。感想の寄せ集めではなく、「顧客自身の言葉で表現されたニーズの階層構造」を作る活動です。

実務の目安として、同研究は、セグメントが明確に定義されていれば **20〜30 件のインタビューで当該セグメントのニーズの大部分を捕捉できる**こと、インタビューからは **100〜200 のニーズ表現（フレーズ）** が得られることを報告しています。少数の営業経由の伝聞や声の大きい顧客の要望を「VOC」と呼ぶ運用は、この手法水準を満たしません。

品質活動への接続は次の2方向で行います。

- **フォワード**: VOC のニーズ階層を品質特性（ISO/IEC 25010）・受入基準へマッピングし、テスト・NFR レビューの優先度根拠にする。
- **バックワード**: 欠陥・障害・サポートチケット・解約理由の自由記述を VOC のニーズカテゴリでタグ付けし、「どのニーズが品質問題で毀損されているか」を分布として見る。チャーン分析（§4）の理由切り分けの語彙にもこのカテゴリを使う。

## 3. NPS — 定義と限界

NPS（Net Promoter Score）は、Reichheld が 2003 年に Harvard Business Review で提唱した指標です（"The One Number You Need to Grow"）。「この会社（製品）を友人や同僚に薦める可能性はどのくらいですか」を 0〜10 で尋ね、9〜10 を推奨者（promoter）、7〜8 を中立者（passive）、0〜6 を批判者（detractor）と区分し、**NPS ＝ 推奨者% − 批判者%** で算出します。原論文は、購買・紹介行動と成長データへの接続調査に基づき、この1問が成長の最良予測子になりうると主張しました。

ただしこの優位性の主張は、その後の検証で強い留保が付いています。Keiningham らは、ノルウェー顧客満足バロメーターの縦断データ（21社・15,500 件超のインタビュー）で Net Promoter 研究の分析を追試し、**Reichheld らが模範例として挙げた業種でも、他の満足度指標に対する「明確な優位性」を再現できなかった**と報告しました（Journal of Marketing, 2007。同誌の実務貢献賞を受賞した追試研究です）。

このため、本リポジトリでの NPS の扱いは次の原則に従います。

- **単独 KPI にしない**。満足度指標群（CSAT・SUS 等）と行動指標（チャーン・継続利用）のセットの一部として扱う。
- **遅行指標として扱う**。リリースと重ねた推移監視・品質退行の検知に使い、原因究明は自由記述の VOC 分類と品質シグナルの突合で行う（[アクセシビリティ・UX 文書の運用シグナル節](../human-centered-quality/accessibility-ux-human-centered-quality.md)と同じ原則）。
- **スコアの絶対値ではなく、同一測定条件下の変化を見る**。質問の位置・チャネル・母集団が変わるとスコアは比較不能になる。
- **目標値化にはゲーミング耐性の設計を必須とする**（[品質メトリクスの落とし穴](./quality-metrics-pitfalls.md)のカウンターメトリクス強制）。

## 4. チャーン — 定義と分析手法

チャーン（churn）は、一定期間内に顧客が利用をやめる割合です。分析の第一原則は**コホートで見る**ことです。加入時期の異なる顧客を混ぜた全体解約率は、顧客基盤の成長・縮小に応じて品質と無関係に動くため、品質との相関分析には「同時期に加入した集団の残存曲線」を使います。

第二原則は、**リテンション曲線の射影に確率モデルを使う**ことです。Fader と Hardie の shifted-beta-geometric（sBG）モデルは、「各顧客が期末に確率 θ で離脱し、θ は顧客ごとに異なり Beta 分布に従う」という2仮定だけで残存曲線を射影します（Journal of Interactive Marketing, 2007）。観測初期の平均解約率を将来へ単純外挿すると、「離脱しやすい顧客が先に抜け、残った集団の解約率は下がっていく」という異質性の効果を無視して残存を過小評価します。sBG は表計算で実装できる軽さで、この系統誤差を避けられます。

第三に、**契約型と非契約型を区別する**ことです。サブスクリプションのような契約型は離脱が観測できますが、都度購入型（非契約型）は「離脱したのか、たまたま買っていないのか」が観測できません。非契約型は §5 の BG/NBD 系モデルで「生存しているか」を購買パターンから推定します。

品質起因チャーンの切り分けは、(a) 解約理由の自由記述を VOC カテゴリ（§2）でタグ付けする、(b) 解約前の一定期間における品質イベント（障害遭遇・SLO 違反・クラッシュ・サポート起票）の有無でコホートを層別する、の2経路で行います。層別後の残存曲線の差が、品質シグナルとチャーンの関連の一次証拠になります（因果の断定はしない。§6）。

## 5. LTV — 顧客生涯価値

LTV（CLV: Customer Lifetime Value）は、**顧客から得られる将来収益の割引現在価値の期待値**です（Gupta, Lehmann, Stuart, Journal of Marketing Research, 2004）。「平均収益 × 平均継続期間」のような簡易式は、マージン・リテンションが一定という強い前提を置いた近似であり、使う場合は前提を明示します。

- **契約型**: リテンション曲線（§4 の sBG 等）に期間あたりマージンと割引率を乗じて合算する。
- **非契約型**: Fader, Hardie, Lee の **BG/NBD モデル**（Marketing Science, 2005）が、購買頻度と生存の確率モデルとして事実上の標準です。先行する Pareto/NBD（Schmittlein et al. 1987）とほぼ同等の結果を、大幅に容易な実装（表計算可能）で得られることが示されています。

品質投資の説明材料として重要なのは、Gupta らによる感度比較です。公開データ5社の実証で、**リテンション 1% の改善は企業価値を約 5% 改善**し、これはマージン 1% 改善（約 1%）、獲得コスト 1% 改善（約 0.1%）、資本コスト 1% の変化（リテンションの約 1/5 のインパクト）を大きく上回りました。品質シグナルがチャーン（＝リテンション）と関連することを §4 の層別で示せれば、この感度が「品質投資はどの経営レバーに効くか」の橋渡しになります。

## 6. 品質シグナルとの相関分析 — GQM で設計する

相関分析は指標の寄せ集めではなく、GQM（Goal-Question-Metric）で **Goal から下ろして**設計します（Basili, Caldiera, Rombach, 1994）。GQM は測定を、概念レベルの Goal（目的・対象・視点・環境）、運用レベルの Question、定量レベルの Metric の3層で導出する枠組みです。

構造の例:

- **Goal**: リリース品質の劣化がチャーンへ与える影響を、SaaS プロダクト X の月次コホートの視点で把握する
- **Question 1**: 障害・SLO 違反に遭遇した顧客のコホートは、遭遇しなかったコホートと残存曲線が異なるか
  - Metric: SLO 違反時間（MON 系）、障害遭遇顧客フラグ、コホート別残存率（sBG 射影付き）
- **Question 2**: 品質起因の解約理由は VOC カテゴリのどこに集中しているか
  - Metric: 解約理由の VOC カテゴリ分布、対応する欠陥・障害の件数
- **Question 3**: NPS の低下はリリース・品質イベントに時間的に後続しているか
  - Metric: リリース・障害と重ねた NPS 推移（測定条件固定）、批判者の自由記述分類

分析設計の原則は次のとおりです。

1. **ラグを設計する**: 事業指標は遅行する。品質イベントから態度・行動への反映までの時間窓（例: 障害後 30/60/90 日の解約率）を仮説として明示し、複数窓で確認する。
2. **コホート・セグメントを固定する**: 顧客基盤の構成変化（新規流入・プラン構成）が相関を偽装する。比較は同一コホート・同一セグメント内で行う。
3. **交絡を記録する**: 価格改定・営業施策・競合イベント・季節性は、品質と事業指標の双方に効く。分析期間の交絡イベントを列挙し、所見に併記する。
4. **カウンターメトリクスを置く**: 事業指標を目標化した瞬間からゲーミングが始まる（[品質メトリクスの落とし穴](./quality-metrics-pitfalls.md)）。NPS には測定条件の監査、チャーンには救済オファー除外集計などの対を設計する。
5. **因果は主張しない**: 層別・ラグ・交絡記録を尽くしても、観察データから言えるのは「関連の強さ・方向・時間的先行」までである。所見は「相関」「関連」の語彙で記述し、因果を主張したい場合は介入設計（A/B テスト・段階的ロールアウト）を別途提案する。

## 7. 運用と AI エージェント適用の注意

- **実データはリポジトリ外**: 本ドキュメントの手法を実データへ適用するのは実行系・分析基盤の責務です。AI エージェント（#15 business-quality-metrics スキル）は、GQM 構造の提案・指標選定・相関設計・所見の解釈枠組みまでを出力し、確定的な経営判断（価格・投資・撤退）の根拠には人間の検証を必須とします。
- **サンプル規模と分割の限界**: コホート・セグメントを細かく切るほど各セルの件数は減り、相関は不安定になります。数十件規模のセルで係数を断定しない。区間・不確かさを添えて報告します。
- **モデルの前提を出力に明記する**: sBG（契約型・θ の Beta 異質性）、BG/NBD（非契約型・購買と生存の独立性）等の前提が対象ビジネスに合うかを確認し、合わない場合はその旨を assumption として残します。
- **指標の定義ドリフトに注意**: チャーンの分母・NPS の質問文・LTV の割引率など、定義の変更は時系列比較を壊します。定義変更があった時点を分析所見に必ず記録します。

## 主要参考文献

VOC・NPS:

- Abbie Griffin, John R. Hauser, "The Voice of the Customer"（Marketing Science 12(1), 1993): https://doi.org/10.1287/mksc.12.1.1
- Frederick F. Reichheld, "The One Number You Need to Grow"（Harvard Business Review 81(12), 2003): https://hbr.org/2003/12/the-one-number-you-need-to-grow
- Timothy L. Keiningham, Bruce Cooil, Tor Wallin Andreassen, Lerzan Aksoy, "A Longitudinal Examination of Net Promoter and Firm Revenue Growth"（Journal of Marketing 71(3), 2007): https://doi.org/10.1509/jmkg.71.3.039

チャーン・LTV:

- Sunil Gupta, Donald R. Lehmann, Jennifer Ames Stuart, "Valuing Customers"（Journal of Marketing Research 41(1), 2004): https://doi.org/10.1509/jmkr.41.1.7.25084
- Peter S. Fader, Bruce G. S. Hardie, "How to Project Customer Retention"（Journal of Interactive Marketing 21(1), 2007): https://doi.org/10.1002/dir.20074
- Peter S. Fader, Bruce G. S. Hardie, Ka Lok Lee, "'Counting Your Customers' the Easy Way: An Alternative to the Pareto/NBD Model"（Marketing Science 24(2), 2005): https://doi.org/10.1287/mksc.1040.0098

測定の構造化:

- Victor R. Basili, Gianluigi Caldiera, H. Dieter Rombach, "The Goal Question Metric Approach"（Encyclopedia of Software Engineering, Wiley, 1994）: https://onlinelibrary.wiley.com/doi/10.1002/0471028959.sof142

## 関連ドキュメント

- [accessibility-ux-human-centered-quality.md](../human-centered-quality/accessibility-ux-human-centered-quality.md) — SUS/NPS/CSAT の質問紙運用・運用シグナルの品質還流（先行指標とのセット原則）
- [quality-metrics-pitfalls.md](./quality-metrics-pitfalls.md) — Goodhart/Campbell の法則・ゲーミング耐性・カウンターメトリクス
- [software-quality-management-practical-reference.md](./software-quality-management-practical-reference.md) — GQM の品質管理文脈・COQ
- [production-quality-sre-observability.md](../operations-quality/production-quality-sre-observability.md) — 品質シグナル側（SLI/SLO・エラーバジェット・DORA）の正典
