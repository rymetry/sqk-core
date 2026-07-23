> **v2 status**: active — v2 でも設計の正典として参照する。

# ポータビリティ設計（品質スキル・エコシステム）

本書は [スキル・エコシステム設計プラン](skill-ecosystem-design-plan.md) の一部として、品質スキル群を Claude Code / Cowork / Codex / ChatGPT・GPTs の4実行環境へ**単一のソースから**展開するための移植方針を定める。対象読者は、スキルを新規実行環境へ持ち込む実装者と、`skills/` 配下のファイル構造を設計するレビュアーである。

**注意**: 本書は設計文書であり、`skills/` ディレクトリや実際の SKILL.md ファイルは本書の作成時点では存在しない。ディレクトリ作成・スキル実体化は [ロードマップ](skill-ecosystem-design-plan.md) の Phase 1 で `skill-creator` スキルを用いて行う後続作業である。本書に掲載する SKILL.md は Phase 1 実装時の**設計上の完成形サンプル**として提示するものである。

## エグゼクティブサマリ

品質スキル・エコシステムのポータビリティ方針は3つの柱からなる。

1. **可搬スキルユニット＝ SKILL.md 1ファイル**。frontmatter に Claude Code ネイティブのキー（`name`, `description` 等）と、プラットフォーム中立なキー（`inputs`, `outputs`, `capabilities`, `knowledge_refs`）を同居させる。Claude Code は自身が解釈しないキーを単に無視するため、1ファイルが「Claude Code スキル」と「プラットフォーム中立マニフェスト」を兼用できる。
   **根拠**: マニフェストを別ファイルに分離すると、SKILL.md 本文とマニフェストの内容が独立に編集されドリフトする。1ファイル方式は構造的にドリフトを起こせない。
2. **能力の抽象化**。スキルが要求する実行環境機能を `file_read` / `file_write` / `shell` / `web_search` のような抽象能力名で宣言し、各プラットフォームの具体ツール名（Read/Bash 等）には一切依存しない。
   **根拠**: 具体ツール名を frontmatter に書くと、ツール名が変わるたび（あるいはプラットフォームが変わるたび）に全スキルを書き換える必要が生じる。抽象能力は変換レシピ側の責務にする。
3. **プラットフォーム別アダプター方式**。正典（SKILL.md 本文＋ナレッジ参照）は1つに保ち、プラットフォームごとに「読み方」または「変換手順」を用意する。Claude Code はシンボリックリンクによる直接消費、Codex は AGENTS.md 経由の索引化、ChatGPT/GPTs はビルド時結合という、プラットフォームの制約に応じた3段階の縮退レベルを設ける。
   **根拠**: 正典を複製すると保守コストが実行環境数倍になる。既存の `CLAUDE.md -> AGENTS.md` シンボリックリンクパターンをスキル層にも拡張することで、リポジトリ全体で一貫したアダプター思想を維持できる。

以下、§1で可搬スキルユニットの仕様を定義し、§2で能力とプラットフォームの対応関係を表にまとめ、§3で MVP スキルの一つを完全な実装例として掲載し、§4・§5でそれぞれ Codex・ChatGPT/GPTs 向けの変換レシピを示す。

## §1 可搬スキルユニットの定義

可搬スキルユニットは **SKILL.md 1ファイル**である。ファイルは YAML frontmatter と Markdown 本文からなり、frontmatter が構造化されたマニフェストとして、本文が人間可読な手順書として機能する。

### frontmatter 仕様

| キー | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `name` | string | ○ | スキル識別子。ケバブケース。ディレクトリ名と一致させる |
| `description` | string | ○ | **トリガー文言**。いつこのスキルを使うべきかを一人称でなく三人称的に記述し、Claude Code の自動発火判定と、他プラットフォームでの手動選択の両方に使う |
| `version` | string | ○ | セマンティックバージョン。ナレッジ参照先の破壊的変更と同期させる |
| `inputs` | object | ○ | 入力契約。キーごとに型・必須可否・説明を記す（後述§3のスキーマ参照） |
| `outputs` | object | ○ | 出力契約。`schemas/` 配下の JSON Schema ファイルへの相対パス参照で表す。実体をここに再記述しない |
| `capabilities` | array<string> | ○ | 抽象能力名のリスト。`file_read`, `file_write`, `shell`, `web_search` のうち**必要最小限のみ**を宣言する |
| `knowledge_refs` | array<string> | ○ | リポジトリ相対パス（`docs/...`）のリスト。スキルが判断根拠として参照する静的ナレッジ |

**`capabilities` を必要最小限にする根拠**: 過大宣言は ChatGPT/GPTs 変換時に不要な縮退判定（§5参照）を誘発し、また監査時に「このスキルは何ができるか」の見通しを悪化させる。読み取り専用で完結するスキルには `shell` を書かない。

**`knowledge_refs` をリポジトリ相対パスにする根拠**: 絶対パスは実行環境ごとにチェックアウト位置が異なるため機能しない。相対パスであれば Claude Code のファイル読み取り、Codex のワークスペースアクセス、GPTs のビルド時結合のいずれからも同じ文字列で解決できる。

### Claude Code が未知キーを無視する挙動への依存

Claude Code は SKILL.md frontmatter のうち `name` と `description` を主に用いてスキルを発見・発火させ、それ以外のキーは無視して害を及ぼさない。したがって `inputs` / `outputs` / `capabilities` / `knowledge_refs` を同じ frontmatter に追記しても、Claude Code 上での動作は変化しない。この性質により、1ファイルが「Claude Code 用スキル定義」と「プラットフォーム中立マニフェスト」の二役を、追加の変換ステップなしで兼務できる。

**根拠**: 二重保守（SKILL.md とは別に manifest.yaml を持つ設計）は、Phase 2 以降でスキル数が16まで増える計画（[スキル一覧](skill-ecosystem-design-plan.md)参照）において、変更のたびに2ファイルを同期させる作業コストを生む。1ファイル方式はこのコストをゼロにする。

### `description`（トリガー文言）の設計指針

`description` は Claude Code の自動発火判定に直接使われる唯一のフィールドであるため、他のキー以上に慎重に書く必要がある。次の3要素を含めることを標準形とする。

1. **利用者が発する問いの言い換え**（例:「このリリースは出してよいか」）を1〜2パターン含め、意図解釈の揺れを吸収する
2. **入力として想定するもの**（証跡ファイル、仕様書等）を名詞で列挙し、スキルが何を材料に動くかを明示する
3. **出力の性格**（判定、一覧、指摘等）を動詞で示し、他スキルとの境界を明確にする

**根拠**: [未解決論点](skill-ecosystem-design-plan.md)に記載の通り、`description` の日英併記や表現粒度はプラットフォーム横断でのトリガー精度が未実測である。実測が済むまでの暫定策として、上記3要素を型として固定し、少なくとも記述の一貫性は担保する。実測は `skill-creator` の eval 機能を用いて Phase 1 で行う。

### 汎用単位「システムプロンプト＋ツール定義＋ナレッジ」との対応

AI エージェントに何らかの振る舞いを与える最小単位は、プラットフォームを問わず次の3要素に分解できる。

- **システムプロンプト相当** = SKILL.md 本文の「目的」「手順」節。エージェントに何をどの順序で行わせるかの自然言語指示
- **ツール定義相当** = `capabilities` フィールド。エージェントが呼び出してよい能力の宣言（抽象名）
- **ナレッジ相当** = `knowledge_refs` フィールドが指す `docs/` 配下の静的文書。判断根拠となる事実・カタログ・チェックリスト

この対応関係により、プラットフォーム変換とは「本文をそのまま/要約して転記し、`capabilities` を具体ツールへ解決し、`knowledge_refs` の指す内容を読める形で持ち込む」という機械的な作業に還元される。変換のたびに手順を再設計する必要がない。

## §2 能力→プラットフォーム対応表

抽象能力名は、実行環境ごとに次の具体ツール・機構へ解決する。この対応表は、Phase 1 で `skill-creator` を使って SKILL.md を実体化する際に、`capabilities` フィールドから各プラットフォームの実装詳細を導出するための参照表として機能する。表を見て「このスキルは Codex ではこの能力が使えない」と判断できることが目的であり、実装コードそのものはここには書かない（実装コードはプラットフォームアダプター側の責務）。

| 抽象能力 | Claude Code / Cowork | Codex | ChatGPT / GPTs |
| --- | --- | --- | --- |
| `file_read` | `Read` ツール | ワークスペースのファイル読み取り（サンドボックス内） | file-search（アップロード済みナレッジファイルの検索）。対象がリポジトリ外なら手動貼り付けに縮退 |
| `file_write` | `Write` / `Edit` ツール | ワークスペースのファイル書き込み（サンドボックス内） | code-interpreter のスクラッチ領域書き込み、または「手動でこの内容を保存してください」という代替手順テキストに縮退 |
| `shell` | `Bash` ツール | サンドボックス shell 実行 | 実行手段なし。「以下のコマンドを手元の端末で実行し、結果を貼り付けてください」という**手動代替手順テキスト**に縮退 |
| `web_search` | `WebSearch` / `WebFetch` ツール | ネットワークアクセスが許可された環境でのみ shell 経由の取得、既定は無効 | code-interpreter に付随する場合があるが既定では不可。GPTs の browsing 機能が有効な場合のみ利用、それ以外は手動代替 |

**Claude Code / Cowork を同列に置く根拠**: Cowork は Claude Code と同じ SKILL.md 形式・同じツール名の体系を消費するため、変換作業が発生しない。両者は「同一形式を消費するプラットフォーム」として1セルにまとめられる。

**Codex の `shell` を条件付きにする根拠**: Codex はサンドボックス shell を持つが、ネットワークアクセスは環境設定に依存し既定で制限される場合がある。`web_search` を要求するスキルは Codex 環境では実行不可になり得るため、変換時に注意喚起が必要（§4参照）。

**GPTs の縮退を3段階で表現する根拠**: GPTs は `file_read` に近い file-search、`file_write`/`shell` の一部に近い code-interpreter を持つが、任意コマンド実行やネットワークアクセスは持たない。能力ごとに「代替ツールがある」「手動代替で凌ぐ」を明示することで、変換作業者が場当たり的な判断をせずに済む。

### 能力宣言の粒度チェック（スキル作成時のレビュー観点）

`capabilities` を宣言する際は、次の問いに答えられるかを確認する。

- そのスキルが実際に呼び出す操作は、宣言した抽象能力のどれに対応するか一意に説明できるか（例:「証跡ファイルを開く」は `file_read` であって `shell` ではない）
- 宣言した能力のうち、GPTs で「手動代替」に縮退するものはどれか。縮退した場合でもスキルの中核的価値（判定・分析・生成）が失われないか
- 将来 Phase 2/3 で追加するスキルが `capabilities` を増やす場合、既存の4分類（`file_read`/`file_write`/`shell`/`web_search`）で表現しきれない能力（例: 画像生成、外部API呼び出し）が出た時点で本表を拡張する

**根拠**: 能力分類を早い段階で厳密にしておくことで、Phase 2 で8スキルを追加する際に分類の見直しコストが発生しない。4分類は MVP 7スキルの実際の要求（すべて `file_read` 中心、一部 `shell`）から導出した最小集合であり、抽象化のしすぎ（能力を細分化しすぎて表が肥大化する）と抽象化不足（`tool_use` のような曖昧な1分類にまとめてしまう）の中間を狙っている。

## §3 Claude Code / Cowork 向け実装例（フル掲載）

MVP 7スキル（[スキル一覧](skill-ecosystem-design-plan.md)の #0〜6）のうち `quality-gate-release-judgment` を完全実装例として掲載する。

**選定根拠**: このスキルは上流スキル（TRA/TAD/TDD-TI/TE）の成果物がゼロでも、証跡ファイル群さえあれば単体で Go/No-Go 判定という完結した価値を出せる。MVP の中でも「疎結合な単体実行」という設計原則（[オーケストレーション設計](skill-ecosystem-design-plan.md)（ハブ§4）参照）を最も端的に検証できるスキルであるため、実装例として選んだ。

````markdown
---
name: quality-gate-release-judgment
description: >
  リリース判定・CI/CD品質ゲートでの Go/No-Go 判断が必要なとき、
  または「このリリースは出してよいか」「品質ゲートを通すべきか」
  という問いに答える必要があるときに使う。証跡ファイル（テスト結果、
  カバレッジレポート、リスク登録簿、脆弱性台帳等）を根拠として判定し、
  判定不能な項目は assumption として明示する。
version: 0.1.0
inputs:
  release_summary:
    type: string
    required: true
    description: 対象リリースの変更概要（何を、なぜ、影響範囲）
  evidence_files:
    type: array<path>
    required: false
    description: >
      入手可能な証跡ファイルのパス一覧（テスト結果、カバレッジレポート、
      リスク登録簿、脆弱性台帳、SLI/SLO文書等）。空でも起動可能。
  gap_checklist_scope:
    type: array<string>
    required: false
    description: >
      優先確認したいアーティファクト種別（例: "セキュリティ要求表",
      "性能試験計画・結果"）。未指定なら全カテゴリを確認する。
outputs:
  handoff_envelope:
    schema: ../../schemas/handoff-envelope.schema.json
  release_decision:
    schema: ../../schemas/release-decision.schema.json
capabilities:
  - file_read
knowledge_refs:
  - docs/quality-management/software-quality-gap-analysis-report.md
  - docs/quality-management/quality-metrics-pitfalls.md
  - docs/quality-models/iso25010-product-quality-model.md
---

# quality-gate-release-judgment

## 目的

リリース対象の変更に対して、収集可能な証跡に基づき Go / No-Go / 条件付き Go
を判定し、判定根拠・残存リスク・判定不能項目を後から監査できる形で出力する。
「証跡なき品質は品質なし」という原則（[ソフトウェア品質ギャップ分析報告書](../../docs/quality-management/software-quality-gap-analysis-report.md)）
に基づき、証跡が存在しない主張を判定の根拠にしない。

## 手順

1. **証跡収集**: `evidence_files` を読み込み、各ファイルがどのアーティファクト
   種別（品質属性一覧、リスク登録簿、カバレッジレポート、脅威分析、SLI/SLO文書等）
   に該当するかを分類する。ファイルが与えられない場合は「上流成果物なし時の
   振る舞い」節の手順に従う。
2. **ギャップチェックリスト照合**: [ギャップ分析報告書の証跡チェックリスト](../../docs/quality-management/software-quality-gap-analysis-report.md#収集すべきアーティファクトチェックリスト)
   の優先度 A 項目を基準に、収集できた証跡と欠落している証跡を仕分ける。
   欠落項目は `open_questions` または `assumptions` に振り分ける（§後述）。
3. **カウンターメトリクス確認**: 提示された指標（カバレッジ率、テスト件数、
   バグクローズ件数等）が単独で使われていないかを確認する。[品質メトリクスの
   誤用と落とし穴の原則3](../../docs/quality-management/quality-metrics-pitfalls.md#原則-3-カウンターメトリクス対になる指標)
   に基づき、主指標に対応するカウンターメトリクス（ミューテーションスコア、
   変更失敗率、再オープン率等）が併記されているかを確認し、なければ
   「この指標は単独では判定に使えない」旨を判定コメントに含める。
4. **Go/No-Go 判定と残存リスク明示**: 収集した証跡・カウンターメトリクス確認
   結果をもとに `gate_status` を決定する。判定理由は証跡の ID・ファイル名を
   引用して記述し、証跡がない主張をしない。残存リスクは
   [ISO/IEC 25010 のトレードオフ](../../docs/quality-models/iso25010-product-quality-model.md)
   の観点も踏まえ、対処せずに出荷した場合に何が起こり得るかを1文で書く。

## 最小入力契約

コールドスタート（他スキルの成果物が一切ない状態）で本スキルを起動するために
最低限必要な入力は次の2つのみである。

- **対象リリースの変更概要**（`release_summary`）: 何を変更し、なぜ変更し、
  影響範囲がどこかを1〜3文で記述したもの
- **入手可能な証跡ファイル群**（`evidence_files`）: 0件でも起動可能。0件の
  場合は「上流成果物なし時の振る舞い」に従う

この2つ以外（トレーサビリティチェーンの ID、DTC、テストアーキテクチャ等）は
一切前提にしない。

## 上流成果物なし時の振る舞い

トレーサビリティチェーンのリンクや DTC（詳細テスト条件）などの上流成果物が
存在しない場合、次の手順で判定を継続する。

1. **質問は最大3件まで**とし、それ以上は聞かない。優先して聞くべき質問は
   (a) 変更の影響範囲、(b) 既知の重大リスクの有無、(c) 直近の類似リリースで
   問題が起きたかどうか、の3つに絞る。
2. 回答が得られない、または利用者が回答不能な場合は、**入手可能な証跡のみで
   判定する**。証跡がゼロの場合でも `gate_status: blocked` を返し、
   「証跡なしでの Go 判定はできない」ことを理由に明記する。
3. 判定できなかった項目（例: セキュリティ要求表が存在せず脆弱性の有無を
   判定できない）は `assumptions` または `open_questions` に **unknown** と
   して明示し、`gate_status` の理由文にも反映する。あいまいな沈黙で
   判定を通さない。

## 出力エンベロープ

本スキルは単体実行・オーケストレーター経由実行のいずれでも、下記形式の
ハンドオフエンベロープ（[schemas/handoff-envelope.schema.json](../../schemas/handoff-envelope.schema.json)
準拠）を必ず出力する。これにより、後から `quality-orchestrator` や
`quality-artifact-review` に再取り込みできる。

```json
{
  "source_skill": "quality-gate-release-judgment",
  "phase": "release-judgment",
  "artifacts": [
    {
      "type": "release_decision",
      "schema_ref": "schemas/release-decision.schema.json",
      "content": {
        "gate_status": "passed-with-risks",
        "summary": "決済APIのタイムアウト値変更。負荷試験結果とロールバック手順は確認済み。",
        "evidence_used": [
          "loadtest-2026-07-01.md",
          "risk-register.csv"
        ],
        "residual_risks": [
          "セキュリティ要求表が未提出のため、認可まわりの回帰は未確認"
        ]
      }
    }
  ],
  "trace_ids": [],
  "assumptions": [
    "セキュリティ要求表が存在しないため、認可関連の非機能要求は変更前と同等と仮定した"
  ],
  "open_questions": [
    "直近3リリースで同種のタイムアウト変更に起因する障害はあったか"
  ],
  "gate_status": "passed-with-risks"
}
```

`gate_status` は `passed` / `passed-with-risks` / `blocked` の3値のいずれかを
とる。証跡が著しく不足する場合は `blocked` とし、Go 判定を出さない。
````

### 導入手順（Claude Code / Cowork）

Phase 1 で `skills/quality-gate-release-judgment/SKILL.md` を実体化した後、リポジトリ直下に次のシンボリックリンクを張ることで Claude Code が自動発見する。

```
.claude/skills -> ../skills
```

**根拠**: `.claude/` はプラットフォーム固有ディレクトリだが、その配下を `skills/`（正典）へのシンボリックリンクにすることで、正典を複製せずに Claude Code の発見規約に適合させられる。既存の `CLAUDE.md -> AGENTS.md` シンボリックリンクと同一のアダプター思想であり、リポジトリ内で一貫したパターンになる。

Cowork も同じ SKILL.md 形式（frontmatter の `name`/`description` を用いた発見）を消費するため、上記シンボリックリンク配置のみで追加変換なしに利用できる。Cowork 固有のパッケージング（プラグイン化）が必要になった場合は、[ロードマップ](skill-ecosystem-design-plan.md) Phase 3 で検討する。

### 単体実行の検証観点

`quality-gate-release-judgment` を Claude Code 上で単体起動する際、疎結合設計（[オーケストレーション設計](skill-ecosystem-design-plan.md)（ハブ§4）の「単体利用の必須3セクション」）が実際に機能しているかを次の観点で確認する。

- **証跡ゼロでの起動**: `evidence_files` を空にして起動し、質問が3件以内に収まるか、それでも `gate_status` が出力されるか（`blocked` を含めて何らかの判定が返ることが必須で、無回答や無限の追加質問は不合格）
- **証跡過多での起動**: ギャップチェックリストの優先度 A 項目すべてに対応する証跡を与え、`gate_status: passed` が根拠付きで返るか
- **カウンターメトリクス欠落の検出**: カバレッジ率のみを証跡として与え、ミューテーションスコアや欠陥流出率が併記されていない場合に、判定コメントで指摘されるか（[品質メトリクスの誤用と落とし穴](../../docs/quality-management/quality-metrics-pitfalls.md#原則-3-カウンターメトリクス対になる指標)の原則3が実際に適用されているかの確認）
- **エンベロープの再取込可能性**: 出力された JSON がそのまま `quality-orchestrator` や `quality-artifact-review`（Phase 2）の入力として解釈可能な形式か（`schemas/handoff-envelope.schema.json` との整合）

この4観点は Phase 1 の実装完了直後に手動で一度実施し、以後は回帰確認として使う。

## §4 Codex への変換レシピ

Codex は `AGENTS.md` をネイティブに読み取る。本リポジトリは既に `CLAUDE.md -> AGENTS.md` のシンボリックリンクでエージェント向け指示を一本化しているため、スキル層でも同じ入口を再利用する。

### 手順

1. **AGENTS.md への「品質スキル索引」セクション追加**。各スキルの `name` / `description` / `knowledge_refs` を要約した表を追記し、Codex が起動時にどのスキルが存在し、いつ使うべきかを把握できるようにする。

   ```markdown
   ## 品質スキル索引

   | スキル | 使うとき | 参照ナレッジ |
   | --- | --- | --- |
   | quality-gate-release-judgment | リリースの Go/No-Go 判定が必要なとき | docs/quality-management/software-quality-gap-analysis-report.md, docs/quality-management/quality-metrics-pitfalls.md |
   | test-requirement-analysis | 仕様からテスト条件を導出したいとき | docs/test-techniques/test-process-research-summary-test-design.md |
   | ...（16ユニット分） | | |
   ```

2. **SKILL.md 本文の Codex カスタムプロンプト化**。SKILL.md の「目的」「手順」「最小入力契約」「上流成果物なし時の振る舞い」「出力エンベロープ」の5節をほぼそのままカスタムプロンプト（Codex のタスク指示テキスト）として転記する。転記は要約ではなく本文の再掲でよい。**根拠**: この5節は既にプラットフォーム中立な自然言語で書かれており、Codex 固有の言い回しへの翻訳を必要としない。
3. **`capabilities` の解決**。`file_read`/`file_write` はワークスペースアクセスとしてそのまま利用可能。`shell` は Codex のサンドボックス shell として利用可能だが、`web_search` を要求するスキル（例: 将来追加される規格改定確認系のスキル）は、ネットワークアクセスが許可された Codex 環境でのみ有効である旨を索引表の備考に明記する。
4. **`knowledge_refs` の解決**。Codex はリポジトリへのファイルアクセスを持つため、`docs/...` の相対パスはそのまま `file_read` 相当の操作で解決できる。GPTs のような結合ファイル生成は不要。

**根拠（AGENTS.md 追記という選択）**: 新規ファイル（例: `codex-skill-index.md`）を作らず既存 AGENTS.md に追記するのは、Codex の読み取り起点を1つに保つため。索引を分散させると、Codex がどちらを読むべきか曖昧になる。

### Codex 環境固有の限界

Codex 変換において特に注意すべき制約は次の2点である。

- **自動発火の不在**: Claude Code の `description` によるトリガーに相当する自動発火機構を Codex は持たない。利用者またはオーケストレーター役の Codex セッションが、索引表を読んでスキルを選択する能動的な操作が必要になる。これはポータビリティ上の劣化ではなく、Codex の設計思想（明示的な指示に従う）に合わせた変換結果であることを利用者に伝える
- **`web_search` 実行不可時のフォールバック**: ネットワークアクセスが無効な Codex 環境では、`web_search` を要求するスキルの該当手順を「最新情報が必要な場合は利用者に確認する」という手動確認ステップに置き換える。§2の対応表における Codex 列の「既定は無効」表記はこのフォールバックを前提にしている

## §5 ChatGPT/GPTs への変換レシピ

GPTs はファイルアップロード数に上限（20ファイル）があり、任意コマンド実行やリポジトリへの直接アクセスを持たない。したがって変換は「実行時参照」ではなく「ビルド時結合」を基本方針とする。

### システムプロンプトの構成

GPTs のシステムプロンプト欄には、次の3要素を結合したテキストを設定する。

1. **オーケストレーター SKILL.md 本文**（`quality-orchestrator` の目的・8ステップ推論手順）
2. **ルーティング表**（ノード×意図動詞×ライフサイクルフェーズ→スキル、[オーケストレーション設計](skill-ecosystem-design-plan.md)（ハブ§4）参照）
3. **対象スキル本文**（GPTs 1体に持たせたいスキルの SKILL.md 本文。複数スキルを1 GPT に持たせる場合は連結する）

GPT 1体に全16ユニットを詰め込むのではなく、MVP 7スキル（[スキル一覧](skill-ecosystem-design-plan.md)の #0〜6）を1体の GPT にまとめ、Phase 2 以降の横断スキル群は別 GPT として分割することを既定方針とする。

**根拠**: システムプロンプトへ全16スキルの本文を結合すると、GPTs のシステムプロンプト実務上の長さの目安を超え、指示の埋没（後半の指示が参照されにくくなる現象）が起きやすい。MVP 単位での分割は、[ロードマップ](skill-ecosystem-design-plan.md)の Phase 区分とも一致するため、GPT の追加も段階的に行える。

### ナレッジアップロードの構成

`docs/` の8ドメインディレクトリ（quality-models / quality-management / test-techniques / exploratory-testing / secure-development / operations-quality / governance-compliance / human-centered-quality）を、ドメインごとに1ファイルへ結合し、**8結合ファイル**を作る。これに用語表（`term-map.yaml` 相当をテキスト化したもの）・索引（`knowledge/index.md`）・技法カタログ（135技法カタログの結合版）を加えて、合計 **11〜12ファイル**とする。

**根拠**: GPTs のアップロード上限20ファイルに対し、11〜12ファイルなら十分な余裕を残せる。8ドメイン単位での結合は、[ナレッジマネジメント設計](knowledge-management-design.md)の静的ナレッジ分類（`docs/` = 正典の散文）と1対1対応するため、結合ロジックが単純になる。

### 能力の縮退

`shell` を要求する手順（例: テスト実行支援スキルの一部）は、GPTs では実行手段がないため、**助言のみに縮退**する。SKILL.md 本文の該当ステップを「以下のコマンドを実行し、結果をこのチャットに貼り付けてください」という代替指示テキストに置き換える。`file_write` も同様に、成果物をチャット出力として提示し「この内容を保存してください」と案内する形に縮退する。

### 結合ファイルの生成物としての扱い

8結合ファイルおよび用語表・索引・カタログの結合版は**生成物であり手編集を禁止**する。編集は必ず `docs/` の元ファイルに対して行い、結合ファイルはビルドスクリプトで再生成する。

**根拠**: 手編集を許すと、結合ファイルと `docs/` の間にドリフトが生じ、GPTs 側だけ古い記述が残るリスクがある。[ナレッジマネジメント設計](knowledge-management-design.md)が定める「静的ナレッジは `docs/` が正典」という原則を GPTs 変換でも維持するため、結合はビルド時の派生生成物として扱う。ビルドスクリプト自体の実装は [ロードマップ](skill-ecosystem-design-plan.md) Phase 3 の作業とする。

### 未解決論点（ファイルサイズ）

8ドメイン結合ファイルの実際のサイズ（特に `test-techniques/` と `exploratory-testing/` は元ファイルが900〜2500行規模）は未実測である。GPTs のファイルサイズ制限に抵触する可能性があり、Phase 3 のビルドスクリプト実装時に実測し、抵触する場合はドメイン内でのさらなる分割（例: `test-techniques` を技法カタログとプロセス文書で2分割）を検討する必要がある。この論点は [スキル・エコシステム設計プランの未解決論点](skill-ecosystem-design-plan.md)にも記載する。

## 関連ドキュメント

- [スキル・エコシステム設計プラン](skill-ecosystem-design-plan.md) — 本書が参照するスキル一覧・オーケストレーション設計・ロードマップを含むハブ文書
- [ナレッジマネジメント設計](knowledge-management-design.md) — 静的/動的ナレッジ分離、用語対応表、`docs/` 結合方針の詳細設計
