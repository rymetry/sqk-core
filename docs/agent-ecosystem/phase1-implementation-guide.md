> **v2 status**: historical — Phase 1 実装時の手順書。現行手順としては参照しない。

# Phase 1 実装ガイド（タスク分解と受入基準）

## 位置づけ

本書は [スキル・エコシステム設計プラン](./skill-ecosystem-design-plan.md)（ハブ）・[ナレッジマネジメント設計](./knowledge-management-design.md)・[ポータビリティ設計](./portability-design.md) の3文書を、**追加の設計判断なしで実装可能にするための実行補助文書**である。新しい設計判断は一切含まない。設計3文書が「何を作るか・なぜそう作るか」を定め、本書は「どの順序で・どの出典から・何をもって完成とするか」だけを固定する。

**根拠**: 設計3文書のレビューで、実行者の判断に委ねられる箇所が3つ特定された——(1) `schemas/` 8ファイルの正規出典が複数文書に散在、(2) オーケストレーターのルーティング表の中身が未執筆、(3) スキル別の受入基準が quality-gate-release-judgment 以外に存在しない。これらを本書で固定しないと、実行セッションごとに解釈がブレる。

**実行前提**:

- 設計3文書の PR がマージ済みであること
- 新ブランチ（例: `feat/phase1-mvp-skills`）で作業し、PR 経由で main に反映する（直 push 禁止）
- スキル作成には **skill-creator スキルを使用**する
- 長文文書（943行・1040行・2500行）は `grep -n "^#"` で見出し確認→該当セクションのみ Read。全文読みしない

---

## T1: 足場作成

1. ディレクトリ作成: `skills/` `schemas/` `knowledge/terminology/` `knowledge/mappings/` `knowledge/test-space/` `knowledge/dynamic/_templates/` `platforms/claude-code/` `platforms/codex/` `platforms/gpts/`
2. `.gitignore` に追記:

   ```gitignore
   # 動的ナレッジ（社内情報の混入防止。knowledge-management-design.md §1.2）
   knowledge/dynamic/*
   !knowledge/dynamic/README.md
   !knowledge/dynamic/_templates/
   ```

3. シンボリックリンク作成: `.claude/skills -> ../skills`（`ln -s ../skills .claude/skills`）
4. `platforms/` 配下に README 3件を作成。内容は [ポータビリティ設計](./portability-design.md) §3（claude-code）・§4（codex）・§5（gpts）の該当節を要約し、詳細は同文書へのリンクで済ませる（コピーしない）

**受入基準**: `.claude/skills` 経由で `skills/` 配下が参照できる。`git status` で `knowledge/dynamic/` 配下のテンプレート以外が untracked に出ない。

## T2: schemas/ 8ファイルの作成

各 JSON Schema の**正規出典**は以下のとおり。出典の構造をそのまま JSON Schema（draft 2020-12）に正規化する。フィールドの追加・削除・改名はしない。

| スキーマファイル | 正規出典 |
|---|---|
| `handoff-envelope.schema.json` | [ハブ §4「ハンドオフエンベロープ」](./skill-ecosystem-design-plan.md)の JSON 例（source_skill / phase / artifacts[] / trace_ids[] / assumptions[] / open_questions[] / gate_status 3値） |
| `detailed-test-condition.schema.json` | [test-process-research-summary-test-design.md §6.2](../test-techniques/test-process-research-summary-test-design.md) `DetailedTestCondition` |
| `test-architecture-element.schema.json` | 同文書 §6.3 `TestArchitectureElement` |
| `coverage-item.schema.json` | 同文書 §6.4 `CoverageItem` |
| `test-case.schema.json` | 同文書 §6.5 `TestCase` |
| `assurance-statement.schema.json` | [testing-standards-and-assurance-concepts.md §9](../test-techniques/testing-standards-and-assurance-concepts.md) の保証ステートメント YAML テンプレート（YAML→JSON Schema 化） |
| `risk-item.schema.json` | [quality-knowledge-schema.md §1.3](../quality-models/quality-knowledge-schema.md) RISK ノードのデータ契約 |
| `release-decision.schema.json` | [ハブ §3 #6](./skill-ecosystem-design-plan.md) の入出力定義（`REL-nnn`、`go`/`no_go`/`conditional_go`、根拠証跡リンク・残存リスク・例外事項）＋[ポータビリティ設計 §3](./portability-design.md) の出力エンベロープ例の `release_decision` 部 |

ID 体系（`id` フィールドのパターン制約）は [test-process §6.1](../test-techniques/test-process-research-summary-test-design.md) と [quality-knowledge-schema §1.2](../quality-models/quality-knowledge-schema.md) の両方に整合させる。

**受入基準**: 8ファイルすべてが JSON Schema バリデーター（例: `ajv compile`）を通る。ハブ §4 の JSON 例が `handoff-envelope.schema.json` に対してバリデート成功する。

## T3: knowledge/ シード作成

| 成果物 | 作成方法 |
|---|---|
| `knowledge/index.md` | [ナレッジマネジメント設計 §5.2](./knowledge-management-design.md) の形式例を初期形とし、MVP 7スキルの `knowledge_refs` が指す文書・見出しを最低20行分登録する |
| `knowledge/terminology/term-map.yaml` | 同文書 §3.2 のサンプル2エントリ（test-condition / test-basis）を**そのまま**シードとして採用 |
| `knowledge/mappings/iso25010-2011-2023.yaml` | 同文書 §4.2 のサンプル3特性分を起点に、[iso25010-product-quality-model.md](../quality-models/iso25010-product-quality-model.md) の「2011年版からの変更点」節から**残りの全特性分**を抽出して完成させる（正典は docs/ 側。再調査しない） |
| `knowledge/test-space/matrix-template.yaml` | 同文書 §6.3 の YAML を**そのまま**採用（サンプル3セルは `# 記入例` コメント化） |
| `knowledge/dynamic/README.md` + `_templates/` 4件 | 同文書 §1.2 の方針に従い、company-terms.yaml / quality-criteria.yaml / defect-history.yaml / product-context.md の空スキーマテンプレートを作成 |

**受入基準**: YAML 全ファイルがパーサを通る。`index.md` の参照先（`docs/<file>#<見出し>`）が全行実在する。

## T4: ルーティング表シード

`skills/quality-orchestrator/references/routing-table.md` の初期内容として以下の表を採用する。判断に迷った場合の追加・変更は Phase 1 中は禁止し、統合試行（T12）の結果を根拠に PR で改訂する。

**根拠**: ルーティング表は全スキルの `description` と整合しなければならず、場当たりで書き換えるとトリガー精度の検証（未解決論点5）が不能になる。シードを固定し、変更は証拠ベースで行う。

| チェーンノード | 意図（代表的な動詞・依頼文） | ルーティング先 | Phase |
|---|---|---|---|
| REQ, AC | テスト条件を出す／仕様を分析する／観点を洗い出す | test-requirement-analysis | MVP |
| RISK | リスクを洗い出す／優先度・厚みを決めたい | risk-analysis | MVP |
| TEST | テストを構造化する／どの粒度・順序・環境でやるか設計する | test-architecture-design | MVP |
| TEST | テストケースを作る／技法を選ぶ | test-design-implementation | MVP |
| TEST | テストを実行した結果をまとめる／flaky を切り分ける | test-execution-support | P2 |
| TEST | 探索的にテストしたい／チャーターを選びたい | exploratory-testing-support | P2 |
| （全ノード） | 紐づきを確認する／カバレッジを可視化する | traceability-management | MVP |
| EV, REL | リリース判定する／品質ゲートを通してよいか | quality-gate-release-judgment | MVP |
| QC | 非機能をレビューする／特性間のバランスを見る | nfr-review | P2 |
| MON, MET | SLO/SLI を設計する／DORA 指標を解釈する | sre-quality-ops | P2 |
| TEST（コード差分） | PR・コードをレビューする／静的解析結果を優先度付けする | code-review | P2 |
| RISK, MON | 障害・欠陥を分析する／RCA・ポストモーテム | defect-analysis-rca | P2 |
| QC, TEST（AI/LLM） | LLM/AI 機能の評価を設計する | ai-system-quality-eval | P2 |
| EV | 成果物一式が整合しているかメタレビューする | quality-artifact-review | P2 |
| MET | 事業指標（NPS/チャーン等）と品質の相関を見る | business-quality-metrics | P3 |

フォールバック規則（[ハブ §4](./skill-ecosystem-design-plan.md) のとおり）: 曖昧な場合は明確化質問1回まで → それでも定まらない場合は入力が揃っている最上流フェーズへ。P2/P3 スキル宛と判定された場合、Phase 1 時点では「該当スキルは未実装。手動で `docs/` の該当文書（ルーティング表の Phase 列参照）を参照すること」と案内する。

## T5〜T11: MVP 7スキルの作成（skill-creator 使用）

### 作成順序

```
T5: #6 quality-gate-release-judgment   ← 最初
T6: #2 risk-analysis
T7: #1 test-requirement-analysis
T8: #3 test-architecture-design
T9: #4 test-design-implementation
T10: #5 traceability-management
T11: #0 quality-orchestrator           ← 最後
```

**根拠**: #6 は [ポータビリティ設計 §3](./portability-design.md) に完成形サンプルが丸ごと存在するため、skill-creator の使い方と受入プロセスを最小工数で1周検証できる。#0 オーケストレーターは全スキルの `description` が確定しないとルーティング表との整合を検証できないため最後に作る。#2→#1→#3→#4→#5 はパイプラインの依存順（risk が TRA のゲート入力、TRA→TAD→TDD/TI の工程一貫性）に従う。

### 全スキル共通の受入基準（5項目）

1. SKILL.md に**必須3セクション**（最小入力契約／上流成果物なし時の振る舞い／出力エンベロープ）が存在する
2. コールドスタート起動で質問が3件以内に収まり、必ず何らかの出力（`gate_status: blocked` を含む）を返す。無限質問・無回答は不合格
3. 出力エンベロープが `schemas/handoff-envelope.schema.json` に適合する
4. frontmatter が [ポータビリティ設計 §1](./portability-design.md) の仕様（`name`/`description`/`version`/`inputs`/`outputs`/`capabilities`/`knowledge_refs`）に適合し、`capabilities` が必要最小限、`knowledge_refs` の全パスが実在する
5. SKILL.md 本体が500行未満で、`docs/` の内容を再記述せず参照（ポインタ）で済ませている

### スキル別の追加受入観点

| スキル | 追加受入観点 |
|---|---|
| #6 release-judgment | [ポータビリティ設計 §3「単体実行の検証観点」](./portability-design.md)の4観点（証跡ゼロ起動／証跡過多起動／カウンターメトリクス欠落検出／エンベロープ再取込可能性）をそのまま適用 |
| #2 risk-analysis | 出力が `RISK-nnn` 形式で影響度×発生確率を持つ。FMEA/FTA/STPA/STRIDE のどれを選んだかの理由が出力に明記される |
| #1 TRA | 3色ボールペン分析（赤=重要箇所／青=構成要素／緑=疑問・矛盾）のタグ付き分析結果と**質問リストが必ず**出力される。DTC が HTC 経由で導出され、各 DTC に根拠（どの仕様記述・リスクから来たか）が付く |
| #3 TAD | DTC→TAE の割当マトリクスが出力される。DTC なしの単体起動で質問3件以内→簡易 TAE をインライン合成し `assumption: true` が付く |
| #4 TDD/TI | 生成した**全テストケース**に保証ステートメント（`assurance-statement.schema.json` 適合）が付与される。使用技法がカタログの技法 ID（BB-01 等）で引用される。TAE 入力なしで起動した場合、分析から直接生成せず、簡易 TAE のインライン合成を経由したことが出力に明記される |
| #5 traceability | 故意にリンクを切ったチェーン（例: DTC が REQ を参照しない）を与えて「未接続」を検出できる。テスト空間3軸マトリクスの Markdown ヒート表が出力される |
| #0 orchestrator | 代表的な依頼文10ケース（T4 のルーティング表の各行から1文ずつ）を与え、表どおりのスキルに分類される。曖昧な依頼で質問が1回だけ発生する。ゲート判定が3値（passed / passed-with-risks / blocked）で返る |

## T12: 統合試行

1. サンプル題材を1つ用意する（例: 架空の決済 API 仕様書 1〜2 ページ。実プロダクトの仕様がある場合はそちらを優先し、`knowledge/dynamic/` 経由で渡す）
2. オーケストレーター経由で TRA→TAD→TDD/TI パイプラインを一気通しで実行し、各段のゲート判定とハンドオフエンベロープを確認する
3. traceability-management でチェーンのリンク検証とテスト空間3軸マトリクスを描画する
4. 成果物一式が対象プロジェクト側の `quality-artifacts/`（本リポジトリ外）に出力されることを確認する
5. 結果（ルーティングの誤分類・質問数超過・ゲート誤判定）を記録し、ルーティング表・SKILL.md の改訂 PR の根拠とする

## Phase 1 完了チェックリスト

- [ ] `skills/` に7ユニット（SKILL.md + references/）が存在し、全スキルが共通受入基準5項目を満たす
- [ ] `schemas/` 8ファイルが JSON Schema バリデーターを通る
- [ ] `knowledge/` シード一式（index / term-map / iso25010 マッピング / matrix-template / dynamic テンプレート）が存在し、YAML が全てパース可能
- [ ] `.gitignore` に `knowledge/dynamic/` の除外設定があり、テンプレート以外がコミットされない
- [ ] `.claude/skills` シンボリックリンク経由で Claude Code がスキルを発見できる
- [ ] スキル別の追加受入観点がすべて確認済み
- [ ] 統合試行（T12）が1本完了し、改善点が記録されている
- [ ] （任意）AGENTS.md への品質スキル索引の追記（[ポータビリティ設計 §4](./portability-design.md)。Codex 利用を始めるタイミングでよい）

## 関連ドキュメント

- [スキル・エコシステム設計プラン](./skill-ecosystem-design-plan.md) — スキル定義・オーケストレーション設計の正典
- [ナレッジマネジメント設計](./knowledge-management-design.md) — knowledge/ 配下の構造とシード内容の正典
- [ポータビリティ設計](./portability-design.md) — SKILL.md 仕様と実装例の正典
- ADR-0001 設計プラン意思決定記録 — 本設計に至った調査過程のアーカイブ
