> **v2 status**: active — v2 でも設計の正典として参照する。

# ナレッジマネジメント設計（品質スキル・エコシステム）

## エグゼクティブサマリ

品質エージェント・エコシステムのナレッジは、**静的（正典の散文＋機械可読抽出）と動的（プロジェクト固有・非公開）を構造的に分離**する。参照は常時コンテキストの SKILL.md から始め、必要になった時だけ索引を経由して該当ドキュメントを読みにいく**3段階プログレッシブディスクロージャ**で行い、ベクトル検索・埋め込みDBは使わない。さらに「テストの空間」という考え方に基づき、テストレベル・テストタイプ・テストプロセスの**3軸マトリクス**でどこにカバレッジが厚く・薄いかを可視化する仕組みを用意する。以下、この3本柱を中心に、用語対応・規格マッピング・更新プロセスまでを設計する。

なお本文書が定義するディレクトリ構造・スキーマ例は**目標レイアウト**であり、`skills/` `schemas/` `knowledge/` の実体作成はロードマップ Phase 1 の作業である。本文書自体はそれらを作成せず、設計のみを行う。

---

## §1 静的ナレッジと動的ナレッジの分離方針

品質エージェント・エコシステムが扱う情報は、性質がまったく異なる2種類に分かれる。ひとつは業界標準・技法・プロセスといった**どのプロジェクトにも通用する正典知識**、もうひとつは対象プロダクトの仕様・過去の不具合履歴・社内品質基準といった**特定プロジェクトに紐づく機微情報**である。この2つを同じ場所に置くと、公開リポジトリへ社内情報が混入するリスクと、正典知識がプロジェクト固有の前提で汚染されるリスクの両方を抱える。したがって本設計では、保存場所そのものを分離することでこのリスクを構造的に排除する。

### 1.1 静的ナレッジ = `docs/` + `knowledge/`

- **`docs/`**: 正典の散文。23ファイルの調査文書群であり、標準・技法・プロセスの解説と根拠が人間可読な形で書かれている。スキルはここに書かれた内容を再記述せず、参照するにとどめる。
- **`knowledge/`**: `docs/` から抽出した機械可読データ（YAML）と、検索を高速化する索引（`index.md`）。あくまで `docs/` の派生物であり、正典ではない。

**根拠**: `docs/` は既に見出し構造が整備された23ファイルであり、人間のレビュー・PR経由の更新が前提になっている。これをそのまま正典に据え、機械可読な形が必要な箇所（用語表、規格対応表、マトリクステンプレート）だけを `knowledge/` に薄く抽出することで、「同じ内容を2箇所で保守する」二重管理を避ける。

### 1.2 動的ナレッジ = `knowledge/dynamic/`（gitignore、テンプレートのみコミット）

対象プロダクトの仕様書・過去の不具合データ・社内品質基準・組織固有の用語定義は、**本リポジトリには一切実データを置かない**。`knowledge/dynamic/` はディレクトリごと `.gitignore` に登録し、コミットされるのは以下のみとする。

- `knowledge/dynamic/README.md`（運用方法の説明）
- `knowledge/dynamic/_templates/`（空スキーマのみのテンプレート群）

**根拠**: 本リポジトリは MIT ライセンスの公開ナレッジベースである。プロダクト仕様・不具合履歴・社内基準はほぼ確実に機密情報を含むため、公開リポジトリに置くことは許容できない。gitignore による構造的排除は「うっかりコミット」を防ぐ最も確実な手段であり、レビュー担当者の注意力に依存しない。

### 1.3 プライベートリポジトリへの symlink 昇格パス

実運用では、対象プロダクトごとにプライベートリポジトリで動的ナレッジの実データ（社内用語集、品質基準、不具合履歴）を管理し、それを `knowledge/dynamic/` に symlink する昇格パスを用意する。スキル側が参照するパスは `knowledge/dynamic/company-terms.yaml` のように固定されたままなので、symlink の向き先がローカルテンプレートかプライベートリポジトリの実データかに関わらず、スキルの参照コードは変更不要である。

**根拠**: 「後から実データを繋ぎ込める」ことをテンプレート設計の時点で保証しておかないと、Phase 1 のテンプレートが Phase 3 で作り直しになる。相対パスを不変に保つことで、昇格は symlink 操作1回で完結する。

### 1.4 スキルの参照順序と出所レイヤの明示

各スキルは、ナレッジを参照する際に**必ず静的→動的の順**で参照する。すなわち、まず `docs/` と `knowledge/`（標準・技法・プロセスの一般知識）を確認し、その後に `knowledge/dynamic/`（プロジェクト固有の前提・用語・基準）を確認する。そして出力（ハンドオフエンベロープ等）には、主張の根拠がどちらのレイヤに由来するかを明示する。例えば「本判定は ISO/IEC 25010:2023（静的）とプロジェクト固有の品質基準 `quality-criteria.yaml`（動的）の両方に基づく」のように書く。

**根拠**: 動的ナレッジは検証されていない・実データが空である可能性が高い（未解決論点参照）。出所を明示しないと、AIエージェントの判断が「業界標準に基づく一般論」なのか「プロジェクト固有の前提に基づく特殊解」なのか利用者が区別できず、誤った一般化や誤った適用範囲の理解につながる。

---

## §2 保存形式・ディレクトリ構造

目標ディレクトリレイアウトを以下に示す。**この構造は Phase 1 で実際に作成するものであり、本文書執筆時点ではまだ存在しない。**

```
skills/                                  # 正典（プラットフォーム中立）
  quality-orchestrator/
    SKILL.md
    references/routing-table.md          # (ノード×意図×フェーズ)→スキル
    references/pipeline-gates.md         # 段階別 入口/出口ゲート基準
  test-requirement-analysis/
    SKILL.md
    references/tra-checklist.md
  （他スキルも同型：SKILL.md + references/）
schemas/                                 # JSON Schema（test-process 文書§6の契約を正規化）
  handoff-envelope.schema.json
  detailed-test-condition.schema.json
  test-architecture-element.schema.json
  coverage-item.schema.json
  test-case.schema.json
  assurance-statement.schema.json
  risk-item.schema.json
  release-decision.schema.json
knowledge/
  index.md                               # トピック→docs/<file>#<見出し> 検索索引
  terminology/term-map.yaml              # 複数標準並記用語表
  mappings/iso25010-2011-2023.yaml       # 既存文書から機械可読抽出
  test-space/matrix-template.yaml
  dynamic/                               # gitignore（README と _templates/ のみコミット）
    README.md
    _templates/{company-terms,quality-criteria,defect-history}.yaml, product-context.md
platforms/
  claude-code/README.md                  # symlink 手順＋パッケージング
  codex/README.md                        # AGENTS.md 追記＋プロンプト変換レシピ
  gpts/README.md                         # ナレッジ結合ビルドレシピ
.claude/skills -> ../skills              # シンボリックリンク（アダプター）
docs/                                    # 変更なし（正典の静的ナレッジ）
```

### 2.1 各ディレクトリの役割

- **`skills/`**: プラットフォーム中立な形式で書かれたスキル定義の正典。`SKILL.md`（frontmatter＋手順＋ポインタ）と `references/`（詳細な補助資料）で構成される。
- **`schemas/`**: スキル間でやり取りされるデータの構造を定義する JSON Schema 群。既存の `test-process-research-summary-test-design.md` §6 が定義したデータ契約（`HTC-`〜`RUN-` チェーン）を正規化したもの。
- **`knowledge/`**: 本文書が主に扱う機械可読ナレッジ層。索引・用語表・規格マッピング・マトリクステンプレートを格納する。
- **`platforms/`**: プラットフォームごとの導入手順書。実装本体ではなく「どう繋ぎ込むか」のレシピ集。
- **`.claude/skills -> ../skills`**: Claude Code がスキルを自動発見するためのシンボリックリンク。

### 2.2 なぜ `.claude/skills` でなく `skills/` が正典か

`.claude/` ディレクトリは Claude Code というプラットフォームに固有の規約である。もしスキル実体を `.claude/skills/` に直接置いてしまうと、Codex や GPTs など他プラットフォームへの展開時に「Claude Code 専用ディレクトリの中身を他プラットフォームが読みにいく」という不自然な依存が生まれる。

**根拠**: 本リポジトリには既に `CLAUDE.md -> AGENTS.md` という前例があり、プラットフォーム固有ファイルをプラットフォーム中立ファイルへのシンボリックリンクとして扱うパターンが確立している。`skills/` を正典にし `.claude/skills` をそのアダプターとすることで、この既存パターンをそのまま拡張できる。新しい規約を発明する必要がない。

### 2.3 なぜポインタ参照でコピー禁止か

スキルが `docs/` や `knowledge/` の内容を自分の `SKILL.md` 内に転記・複製することを禁止し、常に相対パス参照（ポインタ）で済ませる。

**根拠**: 複製は静かにドリフトする。`docs/` の内容が PR で更新されても、スキル側にコピーされた記述は追随せず、気づかれないまま古い情報を使い続けることになる。単一の真実源（single source of truth）を維持するには、参照は常にポインタでなければならない。唯一の例外は GPTs へのエクスポート時であり、そこではナレッジを結合ファイルとして生成する必要がある（20ファイル制限のため）。ただしこれは**ビルド成果物**として扱い、手編集を禁止する（ポータビリティ設計 `portability-design.md` §5 参照）。

---

## §3 複数標準の用語対応表設計

品質エンジニアリングでは、同じ用語が標準によって異なる定義を持つことが少なくない。代表例が「テスト条件（Test Condition）」であり、JSTQB（ISTQB シラバスの日本語版）と ISO/IEC/IEEE 29119 とで定義の重点が微妙に異なる。この揺れを無視して単一の定義に統合してしまうと、標準の原典を参照する利用者が混乱し、逆に定義の違いを無視した誤った類推が生まれる。そこで本設計では、**複数の定義を並記し、単一の正解を強制しない**用語対応表を `knowledge/terminology/term-map.yaml` として設計する。

### 3.1 スキーマ定義

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `id` | string | canonical ID（用語を一意に識別するキー） |
| `ja` | string | 日本語の代表表記 |
| `en` | string | 英語の代表表記 |
| `definitions` | map | 出典キー（`jstqb_istqb_v4` / `iso29119` / `iso25010_2023` / `inhouse` 等）ごとの要約定義 |
| `divergence_note` | string | 定義がどう食い違うか、実務上何に注意すべきかの解説 |
| `do_not_conflate` | boolean | true の場合、AIエージェントは複数定義を安易に同一視してはならない |
| `source_refs` | list | 各定義の出典（規格名・版・章番号など。原文引用はしない） |

### 3.2 サンプルエントリ（YAML）

```yaml
# knowledge/terminology/term-map.yaml
terms:
  - id: test-condition
    ja: "テスト条件"
    en: "Test Condition"
    definitions:
      jstqb_istqb_v4:
        summary: >
          テストベースから識別される、テスト対象の項目・機能・振る舞いのうち
          テスト可能な側面。「何をテストするか」を粒度の粗いレベルで表現する。
        source_refs:
          - "JSTQB Foundation Level シラバス v4.0 用語集"
      iso29119:
        summary: >
          テスト条件は、1つ以上のテストケースによって充足されうる、
          テストアイテムの特性またはテストアイテムに関する条件。
          カバレッジアイテムの導出元として、より形式的なトレーサビリティの
          単位として位置づけられる。
        source_refs:
          - "ISO/IEC/IEEE 29119-1:2022"
          - "ISO/IEC/IEEE 29119-3:2021（テストケース仕様との関係）"
      iso25010_2023:
        summary: >
          直接の用語定義なし。品質特性・サブ特性が「何を条件として
          確認すべきか」の上流input として参照されるのみ。
        source_refs:
          - "ISO/IEC 25010:2023"
      inhouse:
        summary: "（動的レイヤ。プロジェクト固有の用語定義がある場合はここに追記）"
        source_refs:
          - "knowledge/dynamic/company-terms.yaml 参照"
    divergence_note: >
      JSTQB は「テスト対象の側面」という認識論的な粒度を強調するのに対し、
      29119 は「テストケースによって充足されうる条件」というトレーサビリティ
      上の役割を強調する。29119 準拠のテスト設計プロセス（TRA→TAD→TDD/TI）では
      後者の定義を採用し、DTC（Detailed Test Condition）IDのトレース起点とする。
      JSTQB の定義は教育・共通言語としての役割にとどめ、ID体系には使わない。
    do_not_conflate: true

  - id: test-basis
    ja: "テストベース"
    en: "Test Basis"
    definitions:
      jstqb_istqb_v4:
        summary: "テスト条件を識別するための情報源となるすべての知識・成果物。"
        source_refs:
          - "JSTQB Foundation Level シラバス v4.0 用語集"
      iso29119:
        summary: "テストの導出に用いられる文書、その他の作業成果物。"
        source_refs:
          - "ISO/IEC/IEEE 29119-1:2022"
    divergence_note: "両者の定義は実務上ほぼ同義。乖離は軽微。"
    do_not_conflate: false
```

### 3.3 設計思想: 単一の正解を強制しない

用語対応表は「JSTQB が正しい」「29119 が正しい」という優劣をつけない。`divergence_note` に実務上どちらの定義をどの文脈で使うべきかを書き添えることで、利用者（人間・AIエージェントの双方）が状況に応じて適切な定義を選べるようにする。

**根拠**: これはユーザー要求と参照資料（山﨑氏の指摘とされる「フィーチャー/テスト条件の定義揺れ」）の要点そのものである。標準間の定義揺れは誤りではなく、それぞれの標準が想定する利用文脈の違いを反映している。単一の定義に強制収束させると、原典を参照する利用者にとって「この用語対応表は何の標準に基づいているのか」が不透明になり、かえって混乱を招く。`do_not_conflate: true` のフラグは、AIエージェントが出力の中でこの用語を使う際に「どの定義を採用したか」を明示する義務を負わせるためのシグナルである。

### 3.4 ISO/ISTQB 原文引用のライセンス配慮

`term-map.yaml` の `definitions.*.summary` は、規格原文の逐語引用ではなく**要約**として書く。原文の条文そのものが必要な場合は `source_refs` に規格名・版・章番号のみを記載し、原文の参照は利用者自身が正規のライセンス契約下で規格文書を参照する前提とする。

**根拠**: ISO 規格および ISTQB シラバスは著作権保護された商用文書であり、本リポジトリは MIT ライセンスの公開リポジトリである。原文をそのまま複製・再配布することはライセンス違反のリスクを伴う。要約・出典参照方式にすることで、規格の要点を実務で使える形にしつつ、ライセンスに抵触しない構成にする。

---

## §4 ISO/IEC 25010 新旧マッピングの機械可読化

`docs/quality-models/iso25010-product-quality-model.md` には、ISO/IEC 25010:2011 から 2023 年版への変更点を整理した対応表（同文書「2011 年版からの変更点」節）が既に存在する。この対応表は散文形式のテーブルであり、人間が読むには適しているが、AIエージェントがプログラム的に「旧特性名から新特性名を引く」「新設特性を検出する」といった処理を行うには不向きである。そこで、この対応表の内容を `knowledge/mappings/iso25010-2011-2023.yaml` として機械可読な形に抽出する。

### 4.1 抽出方針

`docs/quality-models/iso25010-product-quality-model.md` の対応表が**正典**であり、`knowledge/mappings/iso25010-2011-2023.yaml` は**派生物**である。抽出は一度きりの機械的な変換作業であり、対応表の内容自体を再調査・再検証することはしない（プランの調査フェーズで既に検証済みのため）。`docs/` 側の対応表が将来更新された場合は、`knowledge/mappings/iso25010-2011-2023.yaml` も追随して更新する（§7 の更新プロセス参照）。

### 4.2 YAML 形式例（実際の対応表から3特性分のサンプル）

```yaml
# knowledge/mappings/iso25010-2011-2023.yaml
# 出典（正典）: docs/quality-models/iso25010-product-quality-model.md
#              「2011 年版からの変更点」節の対応表
source_document: "docs/quality-models/iso25010-product-quality-model.md#2011-年版からの変更点"
revision_summary: >
  2023年改訂は用語変更にとどまらず、規格の分割（製品品質=25010、
  利用時品質=25019、モデルの使い方=25002）と特性体系の再編を伴う。
mappings:
  - change_type: "特性名変更"
    id_2011: "usability"
    name_2011_ja: "使用性"
    name_2011_en: "Usability"
    id_2023: "interaction-capability"
    name_2023_ja: "インタラクション容易性"
    name_2023_en: "Interaction Capability"
    jis_status: "◎（JIS X 25010:2025 序文で確認された公式訳語）"
    practical_impact: >
      「ユーザビリティ要求」は、製品側（対話能力）と利用時品質側（成果、
      ISO/IEC 25019 に分離）とに分けて書き直す必要がある。
    subcharacteristic_changes:
      added: ["インクルーシビティ", "自己記述性"]
      replaced:
        - from: "ユーザインタフェース快美性"
          to: "ユーザエンゲージメント（利用者関与性）"

  - change_type: "特性名変更"
    id_2011: "portability"
    name_2011_ja: "移植性"
    name_2011_en: "Portability"
    id_2023: "flexibility"
    name_2023_ja: "柔軟性"
    name_2023_en: "Flexibility"
    jis_status: "◎（JIS X 25010:2025 序文で確認された公式訳語）"
    practical_impact: >
      移植性テンプレートに拡張性（スケーラビリティ）観点を追加する必要がある。
    subcharacteristic_changes:
      added: ["拡張性"]
      replaced: []

  - change_type: "新設特性"
    id_2011: null
    name_2011_ja: null
    name_2011_en: null
    id_2023: "safety"
    name_2023_ja: "安全性"
    name_2023_en: "Safety"
    jis_status: "◎（JIS X 25010:2025 序文で確認された公式訳語）"
    practical_impact: >
      安全関連システムでなくても、要求分析の段階で安全性の要否判断を
      組み込む必要がある。2011年版ベースのテンプレートを使い続けると
      この観点が構造的に抜け落ちる。
    subcharacteristic_changes:
      added: []
      replaced: []
```

### 4.3 文書が正典・YAML は派生であることの明記

`knowledge/mappings/iso25010-2011-2023.yaml` の冒頭には、上記例のように `source_document` フィールドを必ず含め、どの `docs/` ファイルのどの見出しから抽出したかを機械可読な形でも記録する。AIエージェントがこの YAML を参照した際は、詳細な文脈や根拠が必要であれば `source_document` の指すセクションに遡って `docs/` 側を読みにいく。

**根拠**: YAML は「新特性名を素早く引く」ための高速な参照層にすぎず、変更の背景や実務への影響の詳細な解説は `docs/` 側にしかない。派生物であることをデータ自体に明記しておかないと、将来 YAML だけが更新されて `docs/` との整合が崩れるリスクや、逆に YAML だけを見て文脈を誤解するリスクがある。

---

## §5 実行時のナレッジ検索・参照方法

23本の `docs/` ファイルと将来追加されるナレッジに対し、AIエージェントがどうやって必要な情報にたどり着くかを設計する。本設計では**ベクトルDB・埋め込み検索を採用せず**、3段階のプログレッシブディスクロージャ（段階的開示）方式を採る。

### 5.1 3段階プログレッシブディスクロージャ

1. **第1段階: `SKILL.md`（常時コンテキスト）**
   各スキルの `SKILL.md` は 500 行未満に抑え、詳細な知識そのものは書かず、手順とナレッジへのポインタ（相対パス＋見出しアンカー）のみを書く。これは常にエージェントのコンテキストに載っている前提の情報である。

2. **第2段階: `knowledge/index.md`（オンデマンド読込）**
   `SKILL.md` に書かれたポインタだけで足りない場合、トピックから該当ドキュメントの該当セクションを引く索引ファイルを読み込む。索引は「トピック → `docs/<file>#<見出し>`」の対応表形式であり、必要になったときだけ読み込まれる。

3. **第3段階: 該当セクションの grep/Read**
   索引で該当ファイル・見出しが分かったら、`grep -n "^#"` で見出し行を確認し、該当セクションのみを `Read` する。943行・1040行・2500行といった長大文書の全文読みは避け、常に狙った範囲だけを読む。

**根拠**: `docs/` の23ファイルは既に見出し構造が整備されており、`grep` による狙い撃ちが十分に機能する。埋め込みベクトル検索を導入すると、埋め込みモデルの選定・インデックス再構築・類似度閾値のチューニングといった追加の保守コストが発生し、かつ「なぜこの結果が返ったか」を人間が検証しづらくなる（監査可能性の低下）。プログレッシブディスクロージャ方式は、索引ファイルの中身をレビュー担当者がそのまま読んで検証できる、プラットフォーム間の移植性も高い（埋め込みDBのような専用インフラに依存しない）という利点がある。

### 5.2 `knowledge/index.md` の形式例

```markdown
# ナレッジ索引（トピック → 参照先）

| トピック | 参照先 |
| --- | --- |
| テスト条件の定義（JSTQB/29119差異） | knowledge/terminology/term-map.yaml#test-condition |
| ISO/IEC 25010 新旧特性対応 | docs/quality-models/iso25010-product-quality-model.md#2011-年版からの変更点 |
| リスクベーステスト戦略 | docs/test-techniques/testing-standards-and-assurance-concepts.md#リスクベーステスト |
| flaky test の実証データ | docs/test-techniques/testing-standards-and-assurance-concepts.md#flaky-test |
| DORA 5指標 | docs/operations-quality/production-quality-sre-observability.md#dora-5指標 |
| 探索的テストチャーター一覧（C01–C50） | docs/exploratory-testing/exploratory-testing-charter-catalog-by-tour.md |
| Goodhart の法則とメトリクスゲーミング | docs/quality-management/quality-metrics-pitfalls.md#goodhartの法則 |
| テスト空間3軸マトリクスの考え方 | knowledge/test-space/matrix-template.yaml |
```

### 5.3 なぜ埋め込み検索でなくこの方式か

- **監査可能性**: 索引もマッピングもすべて人間可読なテキスト（Markdown / YAML）であり、PR レビューでそのまま差分確認できる。埋め込みベクトルはブラックボックスであり、検索結果の妥当性を人間が検証しづらい。
- **移植性**: Claude Code・Codex・GPTs のいずれでも「ファイルを grep/Read する」能力は共通して存在する。ベクトルDBは環境ごとに用意が必要で、GPTs のような閉じた環境では利用できない場合がある。
- **保守コスト**: 索引ファイルの更新は「行を1行追加する」程度の作業であり、`docs/` 変更 PR のチェックリスト（§7）に組み込める。埋め込みインデックスは `docs/` の変更のたびに再計算が必要で、CI パイプラインの追加投資を要する。

---

## §6 テスト空間3軸マトリクスによる品質カバレッジ可視化

### 6.1 「テストの空間」という考え方

テストは「レベル」「タイプ」「プロセス」という複数の軸を持つ多次元の活動であり、どれか1軸だけを見て「テストは十分か」を判断すると、実際には手薄な領域を見落とす。この「テストの空間」を3軸で捉え、手薄な領域を可視化するという考え方は、参照資料が指摘する「テストの空間3軸（レベル×タイプ×プロセス）」の要点に基づく。本設計ではこれを `knowledge/test-space/matrix-template.yaml` というテンプレートとして機械可読化する。

### 6.2 3軸の定義

- **`test_level`**（テストレベル）: コンポーネント／統合／システム／受入
- **`test_type`**（テストタイプ）: ISO/IEC 25010:2023 の9品質特性＋機能テスト＋変更関連テスト（リグレッション等）
- **`test_process`**（テストプロセス）: TRA（テスト要求分析）／TAD（テストアーキテクチャ設計）／TDD-TI（テスト詳細設計・実装）／TE（テスト実行）／MON（本番監視）

### 6.3 セル形式とマトリクステンプレート（YAML）

各セルは `{status, evidence, notes}` の3フィールドで構成する。`evidence` はテストケースIDやチャーターIDのリストである。テストケース ID（`TC-`）は [品質知識スキーマ](../quality-models/quality-knowledge-schema.md) §1.2 の既存 ID 体系をそのまま利用する。チャーターは [チャーターカタログ](../exploratory-testing/exploratory-testing-charter-catalog-by-tour.md) の `C01`〜`C50` を、テストケース等の他 ID との衝突・混同を避けるため**本設計が新規に導入する** `CHT-` プレフィックス付きで参照する（例: `CHT-C07` はカタログの C07 を指す。`CHT-` は既存文書には定義がない本設計発の表記である）。

```yaml
# knowledge/test-space/matrix-template.yaml
# セル形式: {status: covered|partial|none, evidence: [ID, ...], notes: string}
axes:
  test_level:
    - component
    - integration
    - system
    - acceptance
  test_type:
    # ISO/IEC 25010:2023 の9特性 + 機能 + 変更関連
    - functional-suitability
    - performance-efficiency
    - compatibility
    - interaction-capability     # 旧: usability
    - reliability
    - security
    - maintainability
    - flexibility                # 旧: portability
    - safety                     # 2023年新設
    - change-related             # リグレッション等
  test_process:
    - TRA
    - TAD
    - TDD-TI
    - TE
    - MON

matrix:
  - test_level: system
    test_type: security
    test_process: TDD-TI
    status: covered
    evidence: ["TC-0142", "TC-0143"]
    notes: "OWASP ASVS 5.0 レベル2準拠のテストケースで充足。"

  - test_level: system
    test_type: safety
    test_process: TRA
    status: none
    evidence: []
    notes: >
      安全性（2023年新設特性）に対応するテスト条件が未識別。
      TRA スキル再実行時に要求分析へ安全性観点を追加する必要あり。

  - test_level: integration
    test_type: interaction-capability
    test_process: TE
    status: partial
    evidence: ["CHT-C07"]
    notes: >
      探索的テストチャーター C07（探索的テストチャーターカタログ参照）で
      部分的にカバー。自動テストケースへの落とし込みは未実施。
```

### 6.4 描画とインスタンスの置き場所

`traceability-management` スキル（スキル一覧 #5）が、上記テンプレートに基づくマトリクスのインスタンスを Markdown のヒート表または Mermaid 図に描画し、CSV エクスポートも提供する。マトリクスの**インスタンス**（実際に埋まったセルデータ）は対象プロジェクト側（`<project>/quality-artifacts/`）か、本リポジトリの `knowledge/dynamic/` に置く。本リポジトリにコミットされるのは**テンプレートのみ**である。

**根拠**: マトリクスのインスタンスはプロジェクト固有のテストケースID・カバレッジ状況を含むため、動的ナレッジと同じ扱いとなる（§1.2）。本リポジトリが提供すべきは「どういう軸でカバレッジを見るべきか」という型であり、実データではない。

---

## §7 更新・メンテナンスプロセス

`docs/` の変更 PR には、以下2点をチェックリストに追加する。

- [ ] **`knowledge/index.md` の該当行を更新したか**: 見出しの追加・変更・削除があった場合、索引の参照先（`docs/<file>#<見出し>`）がリンク切れになっていないか確認する。
- [ ] **`term-map.yaml` への影響を確認したか**: 用語の定義・使用箇所に変更があった場合、`knowledge/terminology/term-map.yaml` の該当エントリ（`definitions.*` や `divergence_note`）に更新が必要ないか確認する。特に ISO/IEC 25010 の対応表（§4）を変更する PR では、`knowledge/mappings/iso25010-2011-2023.yaml` も同時に更新する。

**根拠**: `knowledge/` 配下のファイルはすべて `docs/` の派生物であるため、`docs/` 側の変更が `knowledge/` 側に反映されないままだと、派生物が正典からドリフトし、§1.1 で避けようとした二重管理の問題が別の形で再発する。チェックリスト化することで、レビュー担当者が機械的に確認できるようにし、更新漏れを PR の段階で捕捉する。

---

## 関連ドキュメント

- [スキル・エコシステム設計プラン（ハブ）](./skill-ecosystem-design-plan.md) — 文書目録・スキル一覧・オーケストレーション設計・ロードマップ
- [ポータビリティ設計](./portability-design.md) — プラットフォーム中立なスキル定義・Claude Code 実装例
