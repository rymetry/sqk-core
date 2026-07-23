# 探索的テストツアー一覧の検証結果と最終版マークダウン

## 調査結論

結論として、元の『探索的テストツアー一覧』は**実務上の出発点としては有用**ですが、厳密な観点では、**Whittaker系ツアー、Michael Kelly の学習ツアー、SBTMベースのチャーター設計、そして近年の品質・セキュリティ・AIリスク観点が同じレイヤーで混在していた**ため、そのままでは「正確で網羅的」とまでは言いにくい構成でした。James Bach の SBTM はチャーターをセッションの明確なミッションとして位置づけており、Elisabeth Hendrickson 系の表現では `Explore / With / To discover` が有効です。さらに Ghazi らの研究は、チャーター設計に 30 の要因と 35 の内容要素があり、**チャーターに情報を入れ過ぎると探索空間が狭まる**ことを示しています。したがって、**先にツアー一覧を整理し、その後にチャーターへ変換する**という進め方は妥当です。

今回の最終版では、Whittaker 系を「地区別ツアー」として、Michael Kelly の FCC/CUTS/VIDS を「製品学習用ツアー」として分離し、その上に HTSM/SFDIPOT、FEW HICCUPPS、RCRCRC、ISO/IEC 25010:2023、ISO/IEC 25059:2023、WCAG 2.2、OWASP WSTG/ASVS、OWASP LLM Top 10、i18n、観測性、運用、権限、回帰といった現代的観点を**補助ツアー群**として追加しました。これは、現在のソフトウェア品質が機能テストだけでは足りず、アクセシビリティ、国際化、セキュリティ、AI/LLM 特有リスク、運用時の観測性まで含めて評価されるべきだからです。

## 妥当性評価

Whittaker の書籍プレビューからは、Money Tour、Landmark Tour、Intellectual Tour、Back Alley Tour、Obsessive-Compulsive Tour、All-Nighter Tour、Saboteur、Collectors Tour、Supermodel Tour、Supporting Actor Tour、Rained-Out Tour、Tour-Crasher Tour などの主要ツアーが直接確認できます。また、実践章・目次レベルでは FedEx Tour、TOGOF Tour、Garbage Collector’s Tour、Parking Lot Tour も確認できます。

一方で、Guidebook Tour、Bad-Neighborhood Tour、Museum Tour、Prior Version Tour、Lonely Businessman Tour、Scottish Pub Tour、Couch Potato Tour、Antisocial Tour、そして Blogger’s / Pundit’s / Competitor’s といった変種は、手元で確認できる原典プレビューでは十分に出そろわないものの、Whittaker本の要約レビュー、主要実務記事、講義資料で繰り返し確認できます。反対に、Taxi Cab Tour のような名称は近年の Microsoft Test & Feedback の文脈では例示されているものの、今回優先した原典・公式・主要論文セットでは定義の追跡が弱かったため、**中核カタログからは外し、補足扱い**にするのが妥当だと判断しました。

Michael Kelly の 2006 年記事では、学習のための最初のツアーとして Feature Tour、Variability Tour、Complexity Tour が示され、続いて Claims、Structure、User、Scenario などの拡張ツアーが説明されます。Rapid Software Testing 系の資料では、これが FCC/CUTS/VIDS として Feature, Complexity, Claims, Configuration, User, Testability, Scenario, Variability, Interoperability, Data, Structure へ整理されており、これは Whittaker の地区別ツアーと**用途が違う別系統**として扱う方が実務的です。

また、国内実務資料として SHIFT は、探索的テストをセッションベースド探索的テストとツアーリング探索的テストの組み合わせで行うことを推奨し、セッション時間、目的、ふりかえり、次セッションへの接続を重視しています。このため、今回の最終版は「ツアー辞典」ではなく、**チャーター生成のベースカタログ**として再構成しました。

## 作成した最終版マークダウン

最終版のマークダウンは、カテゴリ別に整理したツアー一覧、各ツアーの定義・目的・代表的テスト活動・適用場面・チャーター変換例、元ファイルとの差分一覧、そして主要出典リストを含む構成で作成しました。mermaid で、**原典系ツアー、チャーター設計フレーム、現代的補助ツアーが最終的にチャーターへ収束する関係**も図示しています。

> **注記（2026-07-06 リポジトリ整理時に追記。原文ではない）:** 元の「最終版Markdownをダウンロード」リンクは失効。最終版の内容は [exploratory-testing-perspective-library.md](exploratory-testing-perspective-library.md)（ツアー観点ライブラリ）として収録されている。ただし本文で言及されている mermaid 図は未収録。

この最終版では、SBTM と `Explore / With / To discover` をチャーターの基本枠に据えたうえで、Ghazi 2017 の知見を使い、チャーターに何を入れ過ぎると探索を縛ってしまうのかを反映しました。つまり、ツアーは発想の源泉、チャーターは時間箱のあるセッションミッション、という役割分担を明確にしています。

## 重要な補正ポイント

| 補正テーマ | 最終判断 | 根拠 |
| --- | --- | --- |
| Whittaker系と Kelly系の分離 | 分離すべき | Whittaker は地区別メタファー、Kelly は製品学習の観点群として整理されているため。 |
| ツアー一覧を先に整理する必要性 | ある | SBTM ではチャーターがセッションのミッションで、Ghazi 2017 は内容過多で探索空間が狭まると示すため。 |
| Guidebook 変種の扱い | Blogger’s / Pundit’s / Competitor’s を明示 | 二次資料で反復確認でき、元一覧より厳密に整理できるため。 |
| Skeptical Customer の位置づけ | Money Tour の変種として採用 | 主要実務記事と引用断片で一致しているため。 |
| Taxi Cab Tour の扱い | 補足扱いに留める | 最近のツール文脈では言及されるが、優先ソースでは定義の裏取りが弱いため。 |
| 多文化ツアーの強化 | W3C i18n と結びつけて採用 | W3C は国際化を早期に取り組む品質アプローチとし、i18n checker も提供しているため。 |
| アクセシビリティ観点 | WCAG 2.2 ベースで追加 | 4原則、13ガイドライン、A/AA/AAA 適合の枠があり、最新利用が推奨されるため。 |
| セキュリティ観点 | OWASP WSTG / ASVS を追加 | 認証、認可、セッション、入力検証、API などを系統立てて補えるため。 |
| AI/LLM 観点 | OWASP LLM Top 10 を追加 | Prompt Injection、Sensitive Information Disclosure、Excessive Agency など従来ツアーだけでは捉えにくいリスクがあるため。 |
| 観測性・運用観点 | 補助ツアー群として追加 | OpenTelemetry は observability を内部状態を出力から理解する能力と定義し、Google SRE は latency, traffic, errors, saturation を重要シグナルとして示しているため。 |

## 主要根拠

今回の判断で特に荷重の大きかったのは、Whittaker 本の目次プレビューと補完的な主要記事、Michael Kelly の原典記事、James Bach の SBTM、`Explore / With / To discover` のチャーター表現、Ghazi 2017 のチャーター設計研究、そして ISO/IEC 25010:2023・ISO/IEC 25059:2023・WCAG 2.2・OWASP WSTG/ASVS・OWASP LLM Top 10・W3C i18n・OpenTelemetry/Google SRE です。これらを組み合わせると、**「伝統的な探索的テストツアーの再整理」と「現代品質要求への拡張」**の両方を満たせます。

日本語ソースについては、SHIFT の探索的テスト解説と W3C 日本語の i18n 資料を優先的に参照しつつ、原典や公式に近い英語ソースで裏づけを補いました。結果として、最終版は**日本語で運用しやすく、かつ原典系譜を崩さない**構成になっています。