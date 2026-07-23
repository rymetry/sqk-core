# 探索的テストツアーチャーター作成前の観点ライブラリ一覧

用途: 探索的テストチャーターを作成する前に、利用可能な「ツアー観点」を整理・選定するための実務用カタログ

対象: QAエンジニア、テスト設計者、SET、QAリード、プロダクト品質責任者、AIエージェントによる探索的テスト設計者

---

## 0. 結論

チャーターを作成する前に、ツアー一覧を整理する価値は高い。

理由は、ツアーが「探索観点の辞書」であり、チャーターが「今回の探索ミッション」だからである。ツアー一覧が整っていない状態でチャーターを書き始めると、観点が個人の経験や思いつきに偏りやすい。逆に、ツアー一覧を先に整備しておくと、プロダクト特性、リスク、変更内容、品質特性に応じてチャーターを組み立てやすくなる。

ただし、ツアーはテストケースではない。ツアーは探索のレンズであり、実行単位にするにはチャーターへ変換する必要がある。

```
ツアー     = 探索観点、攻め方、テストアイデアの型
チャーター = 1回の探索セッションで何を、何を使って、何を発見するかのミッション
セッション = チャーターに基づき、時間を区切って実施する探索活動
```

---

## 1. この最終版で修正・補強した点

元ドキュメントは、James Whittaker系ツアーと実務拡張ツアーをかなり広く整理できていた。一方で、以下の点は修正した。

| 区分 | 修正内容 | 理由 |
| --- | --- | --- |
| 正確性 | Whittaker系の主要ツアーと、派生・実務拡張ツアーを分離 | すべてを「公式ツアー」のように扱うと出典上の正確性が落ちるため |
| 分類 | 「犯罪区域」は `Seedy District` の訳として「悪用区域 / 裏社会区域」を推奨 | 実務文書では過度に刺激的な表現を避けた方が説明しやすいため |
| 名称 | `TOGOF` は `Test One Get One Free Tour` を正式名として併記 | 元の「1個買ったら1個無料ツアー」だけでは英語名と対応しづらいため |
| 出典 | `FCC CUTS VIDS` を Michael Kelly系の補完ツアーとして明確化 | Whittaker系ではなく、別系統のツアーリングヒューリスティックであるため |
| 注意 | Blogger / Critic / Arrogant American / Morning Commute / Taxi系などは「派生・出典要確認」と明示 | 公開資料だけでは主要ツアーとして十分に裏取りしづらいため |
| 補強 | Documentation / Sample Data / Interruption / Continuous Use などの古典的ツアー観点を追加 | Bach / Kaner / Bolton / Kelly系の歴史的背景として有用なため |
| 現代化 | セキュリティ、アクセシビリティ、AI/LLM、観測可能性、権限境界などを実務拡張として整理 | 現代のWeb/SaaS/AIプロダクトでは古典的ツアーだけでは不足しやすいため |

---

## 2. 出典信頼度の扱い

このカタログでは、ツアーを次の3段階で扱う。

| ラベル | 意味 | 使い方 |
| --- | --- | --- |
| A: 出典確認済み | 書籍目次、専門家記事、比較的信頼できる記事で名称・位置づけを確認できるもの | 標準ツアーとして採用しやすい |
| B: 派生・要出典確認 | 元リストや一部資料で見かけるが、公開Web資料だけでは十分に裏取りしづらいもの | 実務用語として採用可。ただし「Whittaker公式」とは書かない |
| C: 実務拡張 | 標準・品質モデル・現代システムリスクからツアー形式に再構成したもの | 現代プロダクト向けの追加観点として採用する |

---

## 3. ツアーとチャーターの関係

### 3.1 推奨フロー

```
1. プロダクト、変更内容、リスク、利用者、運用条件を把握する
2. ツアー一覧から有効な観点を選ぶ
3. 選んだツアーを組み合わせてチャーターに変換する
4. セッションベースで探索する
5. セッション結果から次のツアー・チャーターを更新する
```

### 3.2 チャーター変換テンプレート

Elisabeth Hendricksonの `Explore / With / To discover` 型を基本にすると、ツアーをチャーターへ変換しやすい。

```
Explore: 探索対象
With: 使用するツアー、条件、データ、環境、ツール、観点
To discover: 発見したいリスク、不具合、不明点、品質情報
```

例:

```
Explore: 注文確定から請求作成までのデータ連携
With: FedEx Tour、Data Tour、通信遅延、複数タブ操作
To discover: 二重請求、請求漏れ、ステータス不整合が発生する条件
```

---

# Part A. James Whittaker系ツアー

James Whittakerのツアー型探索では、ソフトウェアを都市に見立て、目的に応じて探索する区域を分ける。代表的には次の6区域で整理される。

1. Business District
2. Historical District
3. Tourist District
4. Entertainment District
5. Hotel District
6. Seedy District

以下では、日本語名、英語名、目的、発見しやすい問題、チャーター化例、出典信頼度を整理する。

---

## A1. Business District / ビジネス区域

ビジネス上重要な機能、ユーザーが購入・契約・継続利用する理由になる機能、営業デモや主要業務で使われる機能を探索する区域。

| ツアー | 英語名 | 目的 | 発見しやすい問題 | チャーター化例 | 信頼度 |
| --- | --- | --- | --- | --- | --- |
| ガイドブックツアー | Guidebook Tour | マニュアル、ヘルプ、チュートリアル、オンボーディング通りに操作する | ドキュメント不整合、案内不足、初回利用の詰まり | ヘルプに従って初回設定を探索し、案内と実挙動の不一致を発見する | A |
| マネーツアー | Money Tour | 売上、契約、継続利用、顧客価値に直結する機能を重点的に探索する | 購入不能、契約不能、デモ崩壊、重大業務停止 | 決済フローを主要プラン・クーポン条件で探索し、売上影響のある不具合を発見する | A |
| 疑い深い顧客ツアー | Skeptical Customer Tour | 営業デモや顧客質問で出そうな「もし〜なら」を試す | 説明不能な挙動、想定外条件の欠陥、デモ崩壊 | 契約デモ機能を顧客の例外質問ベースで探索し、説明困難な挙動を発見する | A / Money Tourの派生 |
| ランドマークツアー | Landmark Tour | 主要機能を目印として、順序や組み合わせを変えながら巡る | 主要機能間の不整合、遷移不備、操作性問題 | 主要機能A/B/Cを順序変更しながら探索し、機能間の状態不整合を発見する | A |
| インテリツアー | Intellectual Tour | 複雑な条件、最大値、難しい入力でシステムの限界を探る | 境界条件、複雑条件、計算ロジック、性能劣化 | 複雑な割引条件と大量明細で見積作成を探索し、計算不整合を発見する | A |
| FedExツアー | FedEx Tour | データを荷物のように扱い、生成、加工、保存、利用、削除、連携を追跡する | データ欠落、反映漏れ、同期不整合、削除漏れ | 注文データを作成から請求・通知・履歴まで追跡し、データ不整合を発見する | A |
| アフター5ツアー | After-Hours Tour | バックアップ、アーカイブ、夜間バッチ、メンテナンス処理を見る | バッチ失敗、夜間処理漏れ、ロック競合 | 夜間バッチ後の請求ステータスを探索し、更新漏れを発見する | A |
| ごみ収集ツアー | Garbage Collector’s Tour | 機能やモジュールを最短経路で順番に巡り、明白な問題を素早く拾う | 表示不能、リンク切れ、起動不能、明白な機能不全 | 全メニューを最短経路で巡回し、表示不能・実行不能な機能を発見する | A |

### A1補足: 元リストに含まれていた派生候補

| 派生候補 | 推奨扱い | コメント |
| --- | --- | --- |
| ブロガーツアー / Blogger Tour | B: Guidebook / Claimsの派生 | 第三者記事、FAQ、社内ナレッジ、ブログ、レビューを起点にする観点として有用。ただし主要なWhittakerツアーとしては扱わない方が安全 |
| 批評家ツアー / Critic Tour | B: Guidebook / Claims / Customer feedbackの派生 | 低評価レビュー、問い合わせ、クレームを起点にする実務観点として有用 |
| 傲慢なアメリカ人ツアー / Arrogant American Tour | B: Intellectual / Antisocialの派生 | 名称は現代の実務文書には不向き。推奨名は「常識破りユーザーツアー」または「案内無視ツアー」 |
| 境界線サブツアー / Boundary Subtour | A: Pearson目次で確認可能 | Intellectual Tourのサブツアーとして扱うと自然 |
| 朝の通勤時間ツアー / Morning Commute Tour | B: After-Hoursの対になる派生 | 起動時、朝一ログイン、業務開始直後の集中アクセスを見る観点として有用 |

---

## A2. Historical District / 歴史区域

古いコード、過去バグ、旧バージョン、修正履歴など、プロダクトの歴史に基づいてリスクを探索する区域。

| ツアー | 英語名 | 目的 | 発見しやすい問題 | チャーター化例 | 信頼度 |
| --- | --- | --- | --- | --- | --- |
| 危険地域ツアー | Bad-Neighborhood Tour | 過去に不具合が多かった箇所、現在も問題が出ている箇所を重点確認する | 再発バグ、慢性不具合、複雑ロジックの欠陥 | 過去障害が多い請求計算を探索し、再発・副作用を発見する | A |
| 博物館ツアー | Museum Tour | 長年修正されていないレガシー機能や古いコードを確認する | レガシー不具合、暗黙仕様、担当者不在領域の欠陥 | レガシー管理画面を現行ブラウザで探索し、互換性問題を発見する | A |
| 旧バージョンツアー | Prior Version Tour | 旧バージョンで成立していたシナリオが新バージョンでも成立するか確認する | デグレード、後方互換性問題、仕様逸脱 | 旧版の主要操作を新版で探索し、互換性・退行を発見する | A |

---

## A3. Tourist District / 観光区域

新規ユーザーが通りやすい場所、見た目、到達しづらい場所、出力パターンなど、表層・導線・見え方に関する区域。

| ツアー | 英語名 | 目的 | 発見しやすい問題 | チャーター化例 | 信頼度 |
| --- | --- | --- | --- | --- | --- |
| 孤独なビジネスマンツアー | Lonely Businessman Tour | 目的地まで遠回りし、長い操作経路を試す | 長経路での状態喪失、セッション切れ、導線不備 | 商品購入まで遠回りの導線を探索し、カート状態喪失を発見する | A |
| スーパーモデルツアー | Supermodel Tour | 機能の中身より見た目、表示、レイアウト、第一印象に注目する | UI崩れ、視認性、文言、統一感 | 管理画面を複数解像度で探索し、表示崩れ・文言不統一を発見する | A |
| TOGOFツアー | Test One Get One Free Tour | 複数起動、複数タブ、複数セッションで干渉を見る | 同時操作、ロック競合、セッション共有、二重処理 | 複数タブで同一注文を編集し、競合・上書き・二重送信を発見する | A |
| スコットランド人のパブツアー | Scottish Pub Tour | 大規模アプリで見つけにくい機能、到達しづらい機能を探索する | 隠れ機能、深い階層、低到達導線、権限不備 | 深いメニュー配下の管理機能を探索し、到達不能・権限不備を発見する | A |
| コレクターズツアー | Collector’s / Collectors Tour | 出力、通知、エラー、帳票、一覧などの全パターンを集める | 出力漏れ、文言不整合、帳票・通知ミス | 申請ステータスごとの通知文を収集し、文言・宛先不備を発見する | A |

---

## A4. Entertainment District / エンターテイメント区域

主要機能そのものではないが、ユーザー体験や品質印象を大きく左右する周辺機能、低頻度機能、長時間利用を探索する区域。

| ツアー | 英語名 | 目的 | 発見しやすい問題 | チャーター化例 | 信頼度 |
| --- | --- | --- | --- | --- | --- |
| 脇役ツアー | Supporting Actor Tour | メイン機能の近くにある周辺機能を確認する | 周辺機能の不整合、補助機能の品質低下 | 購入後のレビュー・領収書・通知を探索し、周辺体験の破綻を発見する | A |
| 裏通りツアー | Back Alley Tour | 利用頻度の低い機能、深い設定、マイナー導線を確認する | 放置バグ、組み合わせ不具合、導線不備 | 古い設定画面と主要機能の組み合わせを探索し、予期しない影響を発見する | A |
| オールナイトツアー | All-Nighter Tour | 長時間起動・長時間処理・放置後の挙動を確認する | メモリリーク、セッション切れ、リソース枯渇、性能劣化 | 長時間起動後に検索・保存を探索し、性能劣化やクラッシュを発見する | A |

### A4補足: 元リストに含まれていた派生候補

| 派生候補 | 推奨扱い | コメント |
| --- | --- | --- |
| 混合目的ツアー / Mixed-Destination Tour | B: Back Alley + Landmarkの派生 | 高頻度機能と低頻度機能を混ぜる観点として有用。現代では「クロスシナリオツアー」と呼ぶ方が分かりやすい |

---

## A5. Hotel District / ホテル区域

システムが「休んでいる」またはユーザー操作が少ない状態で動く機能、キャンセル、中断、デフォルト操作を探索する区域。

| ツアー | 英語名 | 目的 | 発見しやすい問題 | チャーター化例 | 信頼度 |
| --- | --- | --- | --- | --- | --- |
| 雨天中止ツアー | Rained-Out Tour | 長い処理を開始後にキャンセル・中断・再開する | 中断不備、再開不能、中途半端な状態、二重処理 | ファイルアップロード中にキャンセル・再開し、不整合や残骸データを発見する | A |
| カウチポテトツアー | Couch Potato Tour | 入力や操作を最小限にし、デフォルト状態で進める | デフォルト値不備、未入力時バグ、else分岐の欠陥 | 必須項目以外を未入力で申請し、デフォルト処理の欠陥を発見する | A |

---

## A6. Seedy District / 悪用区域・裏社会区域

悪意ある操作、乱暴な操作、仕様外の値や順序、リソース遮断などによって堅牢性を探索する区域。

実務文書では「犯罪区域」よりも「悪用区域」「堅牢性区域」「ネガティブ探索区域」のような名称が扱いやすい。

| ツアー | 英語名 | 目的 | 発見しやすい問題 | チャーター化例 | 信頼度 |
| --- | --- | --- | --- | --- | --- |
| 破壊行為ツアー | Saboteur Tour | 必要なリソースを遮断し、処理を壊す | 通信断、強制終了、依存サービス停止、復旧不備 | 送信中に通信遮断し、再送・ロールバック・エラー表示の欠陥を発見する | A |
| 反社会的ツアー | Antisocial Tour | 仕様外、不正、常識外の値や手順を試す | 入力検証不備、例外処理漏れ、順序制御不備 | 不正な日時・桁数・順序で予約を探索し、バリデーション漏れを発見する | A |
| 脅迫観念ツアー | Obsessive-Compulsive Tour | 同じ操作を繰り返す | 二重送信、重複登録、レース条件、状態破壊 | 保存ボタンを連打し、重複保存・二重通知を発見する | A |

### A6補足: 元リストに含まれていた派生候補

| 派生候補 | 推奨扱い | コメント |
| --- | --- | --- |
| 正反対ツアー / Opposite Tour | B: Antisocialの派生 | 常識や業務ルールと反対の値を入れる。推奨名は「矛盾入力ツアー」 |
| 犯罪多発ツアー / Crime Spree Tour | B: Antisocialの派生 | 明らかに過剰な不正値を大量に試す。推奨名は「過剰不正入力ツアー」 |
| 間違った順番ツアー / Wrong Turn Tour | B: Antisocialの派生 | 不正な手順、順序逆転、前提未達で操作する。推奨名は「不正順序ツアー」 |
| タクシーツアー / Taxi Tour | B: 導線確認の派生 | 目的機能までの正規導線をすべて通る観点として有用 |
| タクシー通行止めツアー / Blocked Taxi Tour | B: 導線・到達不能確認の派生 | どの条件で目的地に到達できなくなるかを見る観点として有用 |

---

## A7. Hybrid / Practiceで確認できる追加ツアー

Whittakerの書籍目次では、章構成上、以下のツアーやサブツアーも確認できる。ただし、公開されている目次情報だけでは詳細説明が限られるため、実務上の意味づけを併記する。

| ツアー | 英語名 | 実務上の解釈 | 信頼度 |
| --- | --- | --- | --- |
| ツアークラッシャーツアー | Tour-Crasher Tour | 複数のツアーやシナリオを途中で横断・衝突させ、統合不具合を探す | A: 名称確認済み。詳細は実務解釈 |
| 境界線サブツアー | Boundary Subtour | Intellectual Tourの一部として、境界値・境界付近・丸め・桁あふれを探索する | A |
| 駐車場ツアー | Parking Lot Tour | 全体をざっと把握し、気になる箇所を駐車場にメモして2周目以降で深掘りする | A: 名称確認済み。詳細は実務解釈 |

---

# Part B. Michael Kelly系ツアー: FCC CUTS VIDS

Whittaker系ツアーに加えて、Michael Kellyの `FCC CUTS VIDS` は追加価値が高い。

`FCC CUTS VIDS` は次の頭文字からなる。

```
Feature
Complexity
Claims
Configuration
User
Testability
Scenario
Variability
Interoperability
Data
Structure
```

Whittaker系ツアーが「観光メタファーによる目的別探索」に強いのに対し、FCC CUTS VIDSは「初回理解、構造把握、設定、データ、相互運用、テスタビリティ」に強い。特に、初めて触るプロダクト、仕様が薄いプロダクト、複雑なSaaS、AIエージェントに探索させる前の観点整理に向いている。

| ツアー | 日本語名 | 目的 | 元リストとの差分 | チャーター化例 | 優先度 |
| --- | --- | --- | --- | --- | --- |
| Feature Tour | フィーチャーツアー | アプリ内のコントロール、画面、機能を一通り見つける | 駐車場ツアーに近いが、より機能棚卸し向き | 全画面の操作要素を探索し、未把握機能と明白な不具合を発見する | P1 |
| Complexity Tour | 複雑性ツアー | 最も複雑な箇所を見つけて探索する | インテリツアーより「複雑箇所の発見」に寄る | 複雑な条件分岐を持つ機能を探索し、仕様理解困難な挙動を発見する | P1 |
| Claims Tour | 主張検証ツアー | 製品内外の説明、広告、ヘルプ、UI文言の主張を検証する | ガイドブックツアーをLP・営業資料・UI文言まで拡張 | LP記載の機能主張を探索し、実挙動との差分を発見する | P0 |
| Configuration Tour | 設定ツアー | 設定可能項目を洗い出し、保持・反映・組み合わせを見る | 裏通りツアーより設定に特化 | 通知設定を変更し、保存・反映・初期化の不具合を発見する | P0 |
| User Tour | ユーザーツアー | 複数のユーザー像を想定し、それぞれの関心・目的で探索する | マネーツアーよりペルソナ/ロールに広い | 管理者・一般ユーザー・ゲスト視点で検索機能を探索し、期待差分を発見する | P1 |
| Testability Tour | テスタビリティツアー | テストを助ける機能、ログ、観測手段、ツール連携を探す | 元リストに不足しがちな観測可能性観点 | エラー発生時のログ・画面・通知を探索し、原因特定不能な箇所を発見する | P0 |
| Scenario Tour | シナリオツアー | 現実的な利用シナリオを複数想定して探索する | ランドマークツアーをユーザー目的寄りに拡張 | 新規顧客の初回購入シナリオを探索し、目的達成阻害要因を発見する | P1 |
| Variability Tour | 可変性ツアー | 変更できるものを探し、変更して影響を見る | 設定・表示・条件変更の副作用に強い | 並び順・フィルタ・表示件数を変更し、状態保持や表示不整合を発見する | P1 |
| Interoperability Tour | 相互運用ツアー | 外部システム、API、ブラウザ、OS、ファイル形式との相互作用を見る | FedExツアーより外部連携に特化 | CSV出力・API連携・通知連携を探索し、連携不整合を発見する | P0 |
| Data Tour | データツアー | 主要データ要素を特定し、生成・変換・保存・参照を追う | FedExツアーと近いが、データモデル理解に向く | 顧客データの作成・編集・削除・検索を探索し、整合性問題を発見する | P1 |
| Structure Tour | 構造ツアー | 物理構成、コード、ファイル、インターフェース、環境構成を把握する | 元リストに不足しがちなアーキテクチャ観点 | 画面/API/DB/ジョブの構成を探索し、影響範囲不明な接続点を発見する | P0 |

---

# Part C. 歴史的・古典的な補完ツアー観点

DevelopSenseの記事では、Whittaker以前または同時期の文脈として、Rapid Software TestingやBlack Box Software Testing由来のツアー観点にも触れられている。これらはWhittaker系の6区域に必ずしも属さないが、実務では非常に使いやすい。

| ツアー/観点 | 目的 | 既存ツアーとの関係 | 採用判断 |
| --- | --- | --- | --- |
| Documentation Tour | オンラインヘルプやユーザーマニュアルを起点に操作する | Guidebook / Claimsと重複 | Guidebook Tourに統合してよい |
| Sample Data Tour | サンプルデータを使い、特に複雑なサンプルで探索する | Data / Complexity / FedExを補強 | 追加推奨 |
| Variability Tour | 変えられるものを探して徹底的に変える | FCC CUTS VIDSにも含まれる | 追加推奨 |
| Complexity Tour | 複雑な機能やデータを探す | Intellectual Tourと近い | FCC CUTS VIDSとして採用推奨 |
| Continuous Use | リセットせず長時間使い続ける | All-Nighterと近い | All-Nighterに統合してよい |
| Interruption | 処理を途中で止める、中断する、邪魔を入れる | Rained-Out / Saboteurと近い | Rained-Outに統合してよい |
| Benefit Tour | ユーザーが得る便益に着目し、それを得やすいか探索する | Money / User / Scenario / Claimsに近い | 実務拡張として追加推奨 |

---

# Part D. 現代プロダクト向けの実務拡張ツアー

以下は古典的な正式ツアー名ではなく、Web/SaaS/モバイル/AIプロダクトで不足しやすい観点を、ツアー形式へ再構成したもの。ドキュメント上は必ず「実務拡張」と明記する。

---

## D1. ユーザージャーニーツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | ユーザーが目的を達成するまでの流れ全体を探索する |
| 見るもの | 初回利用、購入、申請、検索、問い合わせ、退会、再開 |
| 発見しやすい問題 | 体験の分断、導線不備、目的未達、離脱要因 |
| 組み合わせ推奨 | User Tour、Scenario Tour、Money Tour、Claims Tour |
| チャーター例 | 初回ユーザーの登録から初回購入までを探索し、目的達成を阻害する要因を発見する |

---

## D2. 状態遷移ツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | 作成中、申請中、承認済み、取消、失敗、期限切れなどの状態遷移を探索する |
| 見るもの | 状態遷移図、戻る、再開、取消、二重操作、期限切れ、ロック |
| 発見しやすい問題 | 不正状態、遷移漏れ、復旧不能、二重処理 |
| 組み合わせ推奨 | Rained-Out Tour、Obsessive-Compulsive Tour、TOGOF Tour |
| チャーター例 | 申請ワークフローを取消・再開・期限切れ条件で探索し、不正な状態遷移を発見する |

---

## D3. 権限・テナント境界ツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | ロール、所有者、組織、テナント、共有範囲の境界を探索する |
| 見るもの | 管理者/一般ユーザー/ゲスト、URL直打ち、API直接呼び出し、他人のデータ |
| 発見しやすい問題 | 認可漏れ、IDOR、情報漏洩、権限昇格 |
| 組み合わせ推奨 | Antisocial Tour、User Tour、Interoperability Tour、Privacy Tour |
| チャーター例 | 一般ユーザーで他ユーザーの詳細URL/APIを探索し、権限外データ参照を発見する |

---

## D4. アクセシビリティツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | キーボード、スクリーンリーダー、コントラスト、フォーカス、エラー理解容易性を探索する |
| 見るもの | WCAGの4原則: 知覚可能、操作可能、理解可能、堅牢 |
| 発見しやすい問題 | キーボード操作不能、フォーカス迷子、読み上げ不備、低コントラスト |
| 組み合わせ推奨 | Supermodel Tour、Couch Potato Tour、User Tour、Claims Tour |
| チャーター例 | キーボードのみで購入フローを探索し、操作不能箇所とフォーカス不備を発見する |

---

## D5. 性能・容量劣化ツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | データ量、同時操作、長時間利用、複雑条件で性能が劣化する条件を探索する |
| 見るもの | 応答時間、タイムアウト、メモリ、CPU、検索件数、ページング、大量入力 |
| 発見しやすい問題 | 遅延、タイムアウト、メモリリーク、表示不能、容量上限超過 |
| 組み合わせ推奨 | All-Nighter Tour、Intellectual Tour、TOGOF Tour、Data Tour |
| チャーター例 | 大量データと複雑フィルタで一覧検索を探索し、性能劣化・タイムアウト条件を発見する |

---

## D6. レジリエンス・復旧ツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | 障害、通信断、外部サービス停止、タイムアウト後の復旧を探索する |
| 見るもの | 再試行、冪等性、ロールバック、エラー表示、補償処理、手動復旧 |
| 発見しやすい問題 | 中途半端な状態、二重処理、復旧不能、データ欠落 |
| 組み合わせ推奨 | Saboteur Tour、Rained-Out Tour、FedEx Tour、Interoperability Tour |
| チャーター例 | 決済処理中に外部API障害を発生させ、再試行・ロールバックの不整合を発見する |

---

## D7. 観測可能性・診断性ツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | 不具合発生時に原因を特定できる情報が残るか探索する |
| 見るもの | ログ、監査証跡、エラーID、トレース、通知、サポート用情報 |
| 発見しやすい問題 | 原因不明、再現不能、ログ不足、PIIログ出力、監査不能 |
| 組み合わせ推奨 | Testability Tour、After-Hours Tour、FedEx Tour、Saboteur Tour |
| チャーター例 | 失敗系操作を探索し、サポート担当者が原因特定できるログ・エラー情報が残るか確認する |

---

## D8. プライバシー・機密情報ツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | 個人情報、認証情報、機密情報が画面・ログ・通知・URL・外部連携に漏れないか探索する |
| 見るもの | レスポンス、画面、通知、エラーメッセージ、ログ、ダウンロードファイル、外部連携 |
| 発見しやすい問題 | 情報漏洩、マスキング不足、ログ露出、URL露出、権限外参照 |
| 組み合わせ推奨 | Antisocial Tour、Interoperability Tour、Data Tour、Permission Boundary Tour |
| チャーター例 | エラー・通知・CSV出力を探索し、個人情報や機密情報の露出を発見する |

---

## D9. セキュリティ悪用ツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | OWASP WSTG/ASVS的な観点で、Webアプリの悪用可能性を探索する |
| 見るもの | 認証、認可、セッション、入力検証、エラー処理、ファイルアップロード、ビジネスロジック |
| 発見しやすい問題 | XSS、SQLi、IDOR、CSRF、認可漏れ、セッション不備、機密情報露出 |
| 組み合わせ推奨 | Antisocial Tour、Saboteur Tour、Permission Boundary Tour、Privacy Tour |
| チャーター例 | 管理画面の検索・詳細表示APIを権限違いユーザーで探索し、認可漏れと情報露出を発見する |

---

## D10. 国際化・ローカライゼーションツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | 言語、地域、タイムゾーン、通貨、日付形式、文字種の違いで破綻しないか探索する |
| 見るもの | 多言語表示、文字化け、桁区切り、通貨、住所、電話番号、日付、祝日、タイムゾーン |
| 発見しやすい問題 | 文字化け、日時ずれ、金額表示不整合、翻訳欠落、RTL表示崩れ |
| 組み合わせ推奨 | Supermodel Tour、Data Tour、Configuration Tour、Claims Tour |
| チャーター例 | 日本語・英語・タイムゾーン差分で予約作成を探索し、日時・通知・表示の不整合を発見する |

補足: 元リストの「多文化ツアー」は、このツアーに統合すると実務文書として扱いやすい。

---

## D11. 時間・カレンダーツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | 時刻、期限、予約、周期処理、タイムアウト、日跨ぎ、月末月初、閏年などを探索する |
| 見るもの | 期限切れ、予約変更、日跨ぎ処理、月末締め、サマータイム、長期放置、スケジュール実行 |
| 発見しやすい問題 | 期限判定ミス、日付丸め、通知遅延、バッチ実行漏れ、時差バグ |
| 組み合わせ推奨 | After-Hours Tour、All-Nighter Tour、State Transition Tour、FedEx Tour |
| チャーター例 | 月末締め処理と予約変更を日跨ぎ条件で探索し、締め・通知・履歴の不整合を発見する |

---

## D12. 通知・コミュニケーションツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | メール、Push通知、Slack/Webhook、画面通知、履歴の整合性を探索する |
| 見るもの | 宛先、文言、タイミング、重複、失敗時再送、配信停止、言語設定 |
| 発見しやすい問題 | 誤通知、通知漏れ、重複通知、個人情報漏洩、文言不一致 |
| 組み合わせ推奨 | Collector’s Tour、FedEx Tour、Configuration Tour、Privacy Tour |
| チャーター例 | 注文キャンセル時のメール・画面通知・履歴を探索し、通知漏れと文言不一致を発見する |

---

## D13. 変更影響・Feature Flagツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | 直近変更、Feature Flag、設定差分、段階リリースが既存機能へ与える影響を探索する |
| 見るもの | ON/OFF差分、ロールアウト対象、旧UI/新UI、キャッシュ、DB移行、互換性 |
| 発見しやすい問題 | デグレード、フラグ条件漏れ、環境差分、既存ユーザーだけの不具合 |
| 組み合わせ推奨 | Prior Version Tour、Configuration Tour、Structure Tour、Bad-Neighborhood Tour |
| チャーター例 | 新旧Feature Flagを切り替えながら請求画面を探索し、設定差分による退行を発見する |

---

## D14. AI/LLMリスクツアー

| 項目 | 内容 |
| --- | --- |
| 目的 | LLM/AIエージェントの出力・自律操作・外部入力に起因するリスクを探索する |
| 見るもの | Prompt Injection、機密情報漏洩、過剰な自律操作、根拠不明、出力の揺らぎ、監査ログ |
| 発見しやすい問題 | 指示乗っ取り、不正なツール実行、誤回答、秘密情報の露出、監査不能、過信 |
| 組み合わせ推奨 | Claims Tour、Testability Tour、Saboteur Tour、Antisocial Tour、Privacy Tour |
| チャーター例 | 悪意あるIssue本文をAIエージェントに読ませ、不要なコード変更・秘密情報出力・権限外操作を発見する |

---

# Part E. ツアー選定ガイド

## E1. 目的別の推奨ツアー

| 目的 | 優先するツアー |
| --- | --- |
| 初めてプロダクトを理解する | Feature Tour、Structure Tour、Parking Lot Tour、Guidebook Tour |
| 仕様・説明の正しさを確認する | Claims Tour、Guidebook Tour、Documentation Tour、Critic派生 |
| ビジネス影響の大きい不具合を探す | Money Tour、Landmark Tour、User Journey Tour、Skeptical Customer Tour |
| データ不整合を探す | FedEx Tour、Data Tour、Interoperability Tour、State Transition Tour |
| 回帰リスクを見る | Bad-Neighborhood Tour、Prior Version Tour、Museum Tour、Change Impact Tour |
| UI/UX問題を見る | Supermodel Tour、Lonely Businessman Tour、Couch Potato Tour、Accessibility Tour |
| 同時操作・競合を見る | TOGOF Tour、Obsessive-Compulsive Tour、State Transition Tour |
| 障害・中断・復旧を見る | Saboteur Tour、Rained-Out Tour、Resilience Tour、After-Hours Tour |
| セキュリティ/悪用を見る | Antisocial Tour、Security Abuse Tour、Permission/Tenant Boundary Tour、Privacy Tour |
| 運用・サポート観点を見る | Testability Tour、Observability Tour、After-Hours Tour、All-Nighter Tour |
| 国際化・日時を見る | i18n/L10n Tour、Time/Calendar Tour、Configuration Tour、Data Tour |
| AI/LLMプロダクトを見る | AI/LLM Risk Tour、Claims Tour、Testability Tour、Privacy Tour、Permission Boundary Tour |

---

## E2. プロダクト状態別の推奨ツアー

| 状態 | 推奨ツアー |
| --- | --- |
| 新規開発初期 | Feature、Structure、Guidebook、User、Scenario |
| MVP直後 | Money、Landmark、Claims、Couch Potato、Supermodel |
| リリース前 | Bad-Neighborhood、FedEx、Rained-Out、Saboteur、TOGOF |
| 障害対応後 | Bad-Neighborhood、Prior Version、FedEx、Observability、Resilience |
| 大規模改修後 | Structure、Interoperability、Prior Version、State Transition、Feature Flag |
| 運用安定化期 | After-Hours、All-Nighter、Testability、Observability、Privacy |
| AI機能追加後 | AI/LLM Risk、Privacy、Claims、Testability、Permission Boundary |

---

## E3. チャーター作成時の最小セット

実務で最初に整備するなら、次の15個をP0として採用する。

| 優先 | ツアー | 採用理由 |
| --- | --- | --- |
| P0 | Money Tour | 事業影響が大きい不具合を狙える |
| P0 | Landmark Tour | 主要機能間の組み合わせに強い |
| P0 | FedEx Tour | データ連携・状態不整合に強い |
| P0 | Bad-Neighborhood Tour | 過去バグ・慢性不具合に強い |
| P0 | Rained-Out Tour | 中断・キャンセル・再開に強い |
| P0 | Saboteur Tour | 障害・通信断・復旧に強い |
| P0 | Antisocial Tour | 入力検証・不正手順に強い |
| P0 | Claims Tour | 仕様・ヘルプ・UI文言・LPの不一致を見つけやすい |
| P0 | Configuration Tour | 設定・Feature Flag・個人設定の不具合に強い |
| P0 | Testability Tour | 探索結果を再現・報告・運用に乗せやすい |
| P0 | Interoperability Tour | 外部連携・API・ファイル・通知の不整合に強い |
| P0 | Structure Tour | アーキテクチャや影響範囲の理解に強い |
| P0 | State Transition Tour | ワークフロー、非同期処理、キャンセル、再開に強い |
| P0 | Permission/Tenant Boundary Tour | 認可・情報漏洩リスクに強い |
| P0 | AI/LLM Risk Tour | AIプロダクトでは必須級 |

---

# Part F. ツアーからチャーターへの変換例

## F1. EC/決済

```
Explore: カート投入から決済完了、請求作成、通知までの一連の流れ
With: Money Tour、FedEx Tour、Rained-Out Tour、TOGOF Tour、通信断、複数タブ、クーポン
To discover: 二重決済、請求漏れ、通知不整合、キャンセル後の残骸データ
```

## F2. 管理画面/権限

```
Explore: 管理画面のユーザー検索・詳細表示・CSV出力
With: Permission/Tenant Boundary Tour、Antisocial Tour、Data Tour、権限違いユーザー
To discover: 他ユーザー情報の露出、テナント境界越え、CSV出力の認可漏れ
```

## F3. SaaS設定

```
Explore: 通知設定とFeature Flagの組み合わせ
With: Configuration Tour、Feature Flag Tour、Collector’s Tour、複数ロール
To discover: 設定保存漏れ、通知漏れ、旧UI/新UI差分、ロール別表示不整合
```

## F4. AIエージェント

```
Explore: AIエージェントのIssue修正提案からPull Request作成まで
With: AI/LLM Risk Tour、Claims Tour、Testability Tour、Permission Boundary Tour、悪意あるIssue本文
To discover: Prompt Injection、過剰な自律操作、秘密情報露出、監査不能な変更
```

## F5. アクセシビリティ

```
Explore: 新規登録から初回購入までの主要フロー
With: Accessibility Tour、Supermodel Tour、Couch Potato Tour、キーボードのみ操作、スクリーンリーダー
To discover: キーボード操作不能、フォーカス不備、読み上げ不備、エラー理解困難な箇所
```

---

# Part G. 運用ルール

## G1. ツアー一覧の管理

ツアー一覧は固定資産ではなく、プロダクトとチームに合わせて育てる。

推奨する管理項目:

| 項目 | 内容 |
| --- | --- |
| ツアー名 | 日本語名と英語名 |
| 種別 | Whittaker系 / FCC CUTS VIDS / 古典補完 / 実務拡張 |
| 信頼度 | A / B / C |
| 対象品質 | 機能、データ、性能、セキュリティ、アクセシビリティ、運用、AIなど |
| 向くプロダクト | Web、SaaS、モバイル、組込み、AI、基幹系など |
| チャーター例 | Explore / With / To discover形式 |
| 過去実績 | バグ検出数、重大度、学び、向かなかった条件 |

## G2. セッションベースド探索的テストとの接続

ツアーは、セッションベースド探索的テストと組み合わせると管理しやすい。

```
ツアー選定
  ↓
チャーター作成
  ↓
タイムボックス付きセッション
  ↓
セッションノート
  ↓
デブリーフィング
  ↓
次チャーター更新
```

## G3. ツアーを使うときの注意

| 注意点 | 説明 |
| --- | --- |
| ツアーを網羅リストと誤解しない | ツアーは探索観点であり、完全なテストケース集合ではない |
| 名前の面白さに引っ張られない | 重要なのはメタファーではなく、どんなリスクを発見したいか |
| 出典と実務拡張を混ぜない | 公式・派生・独自拡張を分けないと、教育やレビューで混乱する |
| チャーターを詳細手順書にしすぎない | 詳細化しすぎると探索の自由度が消える |
| 結果を記録する | ツアー名、チャーター、実施条件、発見、未解決疑問を残す |

---

# Part H. 最終推奨構成

実務では、次の構成でツアーライブラリを運用するのがよい。

```
探索的テストツアーライブラリ
├── 1. Whittaker系ツアー
│   ├── Business District
│   ├── Historical District
│   ├── Tourist District
│   ├── Entertainment District
│   ├── Hotel District
│   └── Seedy District
│
├── 2. Michael Kelly系ツアー
│   └── FCC CUTS VIDS
│
├── 3. 古典補完ツアー
│   ├── Documentation
│   ├── Sample Data
│   ├── Variability
│   ├── Interruption
│   └── Continuous Use
│
├── 4. 実務拡張ツアー
│   ├── User Journey
│   ├── State Transition
│   ├── Permission / Tenant Boundary
│   ├── Accessibility
│   ├── Performance / Capacity
│   ├── Resilience / Recovery
│   ├── Observability / Diagnosability
│   ├── Privacy / Confidentiality
│   ├── Security Abuse
│   ├── i18n / L10n
│   ├── Time / Calendar
│   ├── Notification
│   ├── Change Impact / Feature Flag
│   └── AI / LLM Risk
│
└── 5. チャーター変換テンプレート
    ├── Explore / With / To discover
    ├── SBTMセッションシート
    └── セッションノート / デブリーフィング
```

---

# Part I. 参考資料

## Whittaker系ツアー

- James A. Whittaker, *Exploratory Software Testing: Tips, Tricks, Tours, and Techniques to Guide Test Design*, Pearson/Addison-Wesley.
    - Pearson Table of Contents: https://www.pearson.de/media/muster/toc/toc_9780321647788.pdf
- Xray Blog, “Using test tours in exploratory testing strategy for QA teams”.
    - https://www.getxray.app/blog/test-tours-exploratory-testing-strategy-qa-teams

## FCC CUTS VIDS / 歴史的背景

- DevelopSense, Michael Bolton, “Of Testing Tours and Dashboards”.
    - https://developsense.com/blog/2009/04/of-testing-tours-and-dashboards
- Michael Kelly, “Touring Heuristic” / FCC CUTS VIDS.
    - DevelopSense記事内で参照されているが、元URLは現在取得困難な場合がある。

## チャーター / SBTM

- Kenst Testing Guide, “Writing Exploratory Charters”.
    - https://guides.kenst.com/exploration/writing_exploratory_charters
- Satisfice, James Bach, “Session-Based Test Management”.
    - https://www.satisfice.com/download/session-based-test-management
- Ahmad Nauman Ghazi, Ratna Pranathi Garigapati, Kai Petersen, “Checklists to Support Test Charter Design in Exploratory Testing”, XP 2017 / arXiv.
    - https://arxiv.org/abs/1704.00988

## 国内参考

- SHIFT Group 技術ブログ, “探索的テストには、ツアーリング探索的テストを使おう”.
    - https://note.shiftinc.jp/n/n9a6644f69ed8
- SHIFT Group 技術ブログ, “探索的テストには、セッションベースド探索的テストを使おう”.
    - https://note.shiftinc.jp/n/nc09a0349569b
- ベリサーブ HQW!, “探索的テストとは？目的や観点、やり方、モンキーテストとの違いなど解説”.
    - https://www.veriserve.co.jp/helloqualityworld/media/20241120001/

## 品質特性・セキュリティ・アクセシビリティ・AI

- ISO/IEC 25010 quality model overview.
    - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- ISO/IEC 25059 AI quality model overview.
    - https://iso25000.com/index.php/en/iso-25000-standards/iso-25059
- OWASP Web Security Testing Guide.
    - https://owasp.org/www-project-web-security-testing-guide/
- OWASP Top 10 for Large Language Model Applications / OWASP GenAI Security Project.
    - https://owasp.org/www-project-top-10-for-large-language-model-applications/
- W3C Web Accessibility Initiative, WCAG Overview.
    - https://www.w3.org/WAI/standards-guidelines/wcag/

---

# Appendix. 元リストからの扱い変更一覧

| 元リストの項目 | 最終版での扱い |
| --- | --- |
| ガイドブックツアー | Whittaker系 A |
| ブロガーツアー | 派生 B。Guidebook / Claims派生 |
| 批評家ツアー | 派生 B。Claims / Customer feedback派生 |
| マネーツアー | Whittaker系 A |
| 疑い深い顧客ツアー | Money Tour派生 A |
| ランドマークツアー | Whittaker系 A |
| インテリツアー | Whittaker系 A |
| 傲慢なアメリカ人ツアー | 派生 B。名称変更推奨 |
| 境界線サブツアー | A。Intellectual Tourのサブツアー |
| FedExツアー | Whittaker系 A |
| アフター5ツアー | Whittaker系 A |
| 朝の通勤時間ツアー | 派生 B。After-Hoursの対になる実務観点 |
| ごみ収集ツアー | Whittaker系 A |
| 危険地域ツアー | Whittaker系 A |
| 博物館ツアー | Whittaker系 A |
| 旧バージョンツアー | Whittaker系 A |
| コレクターツアー | Whittaker系 A |
| 孤独なビジネスマンツアー | Whittaker系 A |
| スーパーモデルツアー | Whittaker系 A |
| 脇役ツアー | Whittaker系 A |
| 裏通りツアー | Whittaker系 A |
| 混合目的ツアー | 派生 B。Back Alley + Landmark派生 |
| 1個買ったら1個無料ツアー | TOGOF TourとしてWhittaker系 A |
| スコットランド人のパブツアー | Whittaker系 A |
| オールナイトツアー | Whittaker系 A |
| 雨天中止ツアー | Whittaker系 A |
| カウチポテトツアー | Whittaker系 A |
| 破壊行為ツアー | Whittaker系 A |
| 反社会的ツアー | Whittaker系 A。実務では「仕様外操作ツアー」などに改名してもよい |
| 正反対ツアー | 派生 B。Antisocial派生 |
| 犯罪多発ツアー | 派生 B。Antisocial派生。名称変更推奨 |
| 間違った順番ツアー | 派生 B。Antisocial派生 |
| 脅迫観念ツアー | Whittaker系 A |
| タクシーツアー | 派生 B。導線確認観点 |
| タクシー通行止めツアー | 派生 B。到達不能確認観点 |
| 多文化ツアー | 実務拡張 C。国際化・ローカライゼーションツアーに統合推奨 |
| 駐車場ツアー | A。名称確認済み。詳細は実務解釈 |