> **v2 status**: backlog material — Phase 2 の keep/merge/defer/drop 再評価（ROADMAP 参照）の素材。

# Phase 2 実装ガイド（タスク分解と受入基準）

## 位置づけ

本書は [スキル・エコシステム設計プラン](./skill-ecosystem-design-plan.md)（ハブ）・[ナレッジマネジメント設計](./knowledge-management-design.md)・[ポータビリティ設計](./portability-design.md) の設計3文書を、**Phase 2 スコープについて追加の設計判断なしで実装可能にするための実行補助文書**である。[Phase 1 実装ガイド](./phase1-implementation-guide.md)と同形式で、「どの順序で・どの出典から・何をもって完成とするか」だけを固定する。

**Phase 1 との違い（本書の基礎）**: 本書は設計3文書に加えて、Phase 1 の**実測結果**を基礎に置く——[統合試行レポート](./phase1-integration-trial-report.md)（T12・ハッピーパス）と [コールドスタート検証レポート](./phase1b-coldstart-trial-report.md)（Phase 1b）。ロードマップの設計決定「Phase 2/3 の実装ガイドは事前に作らず、各 Phase 開始時に前 Phase の実測を反映して作成する」（roadmap-status.md）に従い、Phase 2 開始時点の本書で両レポートの改善点を受入基準へ落とし込んでいる。

**根拠**: Phase 2 で実行者判断に委ねられうる箇所を本書で固定する——(1) Phase 1 申し送り6件（改訂 PR）の修正方針・対象・検証、(2) 新規8スキルの作成順序と共通/個別受入基準、(3) 不足ナレッジ文書3件の正規出典、(4) ゲート判定の委譲・テスト空間マトリクス描画という2つの実装タスクの完成条件。これらを固定しないと実行セッションごとに解釈がブレる。

**Phase 2 スコープ**（正典は [ハブ §5 段階的ロードマップ](./skill-ecosystem-design-plan.md#5-段階的ロードマップ)）: 残り8スキル（#7〜#14）＋不足ナレッジ文書3件（コードレビュー技法／ODC 欠陥タクソノミー／日本発テスト設計技法）＋ゲート判定の quality-artifact-review への委譲＋テスト空間マトリクス描画実装。

> **superseded**: この Execution freeze は v1 で宣言されたもので、v2 では失効している（[DECISIONS.md](../../DECISIONS.md) の D-006 として記録）。v1 原文は Release `archive-sqkb-v1` の bundle を参照。

> **実行前レビュー反映（2026-07-08）**: 本ガイドは Phase 2 着手前の多角的レビュー（検証・批判・governance適合・adversarial・Codex・correctness の6視点）を反映して改訂した。主な変更: (1) 検証ハーネスを前提タスク化、(2) T12-2 を enum 追加から**軽量修正**へ改訂、(3) MON のフィールド契約を [quality-knowledge-schema.md §1.3](../quality-models/quality-knowledge-schema.md) に明示、(4) T1 に #1/#3 の `knowledge_refs` 再配線ステップを追加、(5) T3a にマージ順制約、(6) T12-1 の検証機構を明確化。

## 実行前提

- 設計3文書・Phase 1 成果物（`skills/` 7ユニット・`schemas/` 8ファイル・`knowledge/` シード）がマージ済みであること
- repository concept guardrails（root README / docs README / `knowledge/` / `skills/` / `schemas/` / `_research` の責務境界）が反映済みであること。**本ガイドの T1、T2 および T4〜T11 に着手する前にこの guardrail 改訂をマージする**
- **タスクごとに新ブランチ**で作業し、PR 経由で main に反映する（直 push 禁止・force push 禁止。`.claude/hooks/pre-tool-use-policy.sh` でブロック）
- **T0（改訂 PR）を最優先**で実施・マージしてから T4〜T11 に着手する。新規スキルのコールドスタート節は既存スキル（#2/#3/#4/#5）の「上流成果物なし時の振る舞い」記述を雛形にコピーするため、誤った文言（`assumption: true` の item 付与）を先に是正しておく必要がある
- **検証ハーネスを T0 着手前にコミットする**（前提タスク）: T0/T2 の `strict` schema 検証・往復フィクスチャ受入はこれに依存する。リポジトリを Node プロジェクト化しない——ツールは vendor せず pinned invoke、fixtures は `schemas/tests/`、lockfile は repo root 以外に隔離、CI は任意。required checksはrepository policyとactual GitHub readbackに従い、`.github/scripts/setup-repo.sh`は既存branch protectionを変更しない。schemas は veridia の export candidate ゆえ validator 非依存（標準 draft 2020-12）に保つ
- **共有ファイルの編集順序**: `skills/quality-orchestrator/SKILL.md` は T0（CS-3・T12-1）→ T3a（P2/P3 フォールバック文言）→ T12（ゲート委譲）の順で編集し、別 PR 間のマージコンフリクトを避ける
- スキル作成には **skill-creator スキルを使用**する
- 長文文書は `grep -n "^#"` で見出し確認→該当セクションのみ Read。全文読みしない
- 新規ナレッジ文書は**プロンプト記憶の再記述ではなく出典参照方式**で書く（[ハブ §6 未解決の論点](./skill-ecosystem-design-plan.md)の #4 引用ライセンス方針）

---

## T0: 改訂 PR（Phase 1 申し送り6件の先行修正）— 前提タスク

Phase 1 の統合試行・コールドスタート試行で確定した6件を、Phase 2 スキルが誤った文言をコピーする前に適用する。**方針は正典照合で確定済み**（ただし **T12-2 は実行前レビューで enum 追加から軽量修正へ改訂**。下表 T12-2 行参照）。統一原則は次のとおり:

> **暫定性・前提はエンベロープ `assumptions[]`（[ハブ §4](./skill-ecosystem-design-plan.md#4-オーケストレーション設計) の JSON 例に倣い `{field, value, reason}` 形式）に集約する。個別 item はスキーマ準拠のまま保ち、item に `assumption` フィールドも `-inline-` id も足さない。スキーマは据え置く。**

**根拠**: [コールドスタート検証レポート「正典照合のまとめ」](./phase1b-coldstart-trial-report.md#発見された改善点) が、CS-1・CS-2 は「SKILL 執筆者が暫定性を item 側の即席マーカーで表そうとした同根の逸脱」であり、元プランは最初から暫定性をエンベロープ `assumptions[]` だけで表現し item はスキーマ準拠に保つ設計だった、と確定している。よって「SKILL 文言を直す（スキーマ据え置き）」が正典準拠。

| ID | 対象 | 確定した修正 | 受入（検証） |
|---|---|---|---|
| **CS-1** | risk-analysis / test-requirement-analysis / test-architecture-design / traceability-management の各 SKILL.md（`assumption: true` 記述の**横断スイープ**） | `grep -rn 'assumption: true' skills/` の全該当を監査し、**item/成果物へ `assumption: true` を付与**するよう指示する箇所を「前提はエンベロープ `assumptions[]` に `{field,value,reason}` で記録。item に `assumption` を足さない」へ改める。エンベロープ層の `assumptions[]` を指す既存記述は保持。**スキーマ据え置き** | **item 付与を指示する既知の対象行**（`risk-analysis:94,119`／`test-requirement-analysis:23,122,158`／`test-architecture-design:140`／`traceability-management:151`）を列挙し各行がエンベロープ集約へ変更済みであることを確認する。エンベロープ層の `assumptions[]` を指す既存記述（例 `test-requirement-analysis:237` の説明文中の "assumption: true"）は保持する（**bare grep の残存ゼロは受入にしない**＝正当な言及も文字列一致するため）。機械検証は `risk-item` / `detailed-test-condition` / `test-architecture-element` の往復フィクスチャで「準拠 item が valid・`assumption` 付き版が INVALID」を確認 |
| **CS-2** | test-design-implementation/SKILL.md（インライン合成 TAE の id 例） | id 例 `TAE-inline-001` を数値のみの予約帯へ変更（`TAE-900` 番台をインライン合成用に予約し「**現行成果物集合で未使用の最初の `TAE-9xx` を選ぶ**」と明記）。合成した旨は envelope `assumptions[]` に記録。同節の「`assumption: true` 相当」文言も CS-1 と同じく `assumptions[]` 集約へ統一。**pattern `^TAE-[0-9]+$` 据え置き** | `TAE-901` が pattern に valid・`TAE-inline-001` が INVALID。合成 id が既存 TAE 集合（現状 `TAE-001`/`TAE-002`）と非競合 |
| **CS-3** | quality-orchestrator/SKILL.md 手順4（フォールバック） | 1文追記: どのスキルの最小入力も満たさない truly-empty 時はフェーズ順最上流 `test-requirement-analysis` に着地し、以降は当該スキルのコールドスタート分岐に委ねる（[ハブ §4「上流から手当てする」](./skill-ecosystem-design-plan.md#4-オーケストレーション設計)） | 「品質をよくしたい」のみの相談で着地先が一意に定まる |
| **T12-1** | quality-orchestrator/SKILL.md（RoutingDecision 形状） | 複合フロー時の `routed_skill` を**スキル名の順序付き配列**と規定（単体ルーティング＝要素1の配列）。単体例に加え複合フロー用の出力形状例を追加。人間可読名が要れば任意 `flow_label` 文字列を補足 | ※`handoff-envelope` の `content` は無制約 object のため **ajv では配列形を強制できない**。**`routing-decision.schema.json`（repo-local）を追加し orchestrator が `schema_ref` で参照する、または検証ハーネス内に `content.routed_skill` の `Array.isArray` 専用アサーションを置く**（どちらかを着手時に確定。ajv フィクスチャ扱いにしない） |
| **T12-2** | test-architecture-element.schema.json（`thickness`）＋正典 [test-process §6.3](../test-techniques/test-process-research-summary-test-design.md) の JSON 例 | **【実行前レビューで軽量修正へ改訂】** `thickness` の description に4値（`thick`/`standard`/`narrow`/`delegate`）を列挙し例示 `deep` を除去。§6.3 の JSON 例 `"thickness": "deep"` を `"thick"` へ正規化（`deep` は SKILL の語彙集合の非メンバー）。**free-string 維持（`enum` は追加しない）**。規範源は [`test-architecture-design/SKILL.md` 手順4](../../skills/test-architecture-design/SKILL.md)（`thick/standard/narrow/delegate`）。＜`enum` 化は**任意の将来強化**：語彙が Phase 2 で実運用（T14）された後に、§6.3 へ値集合＋拡張ポリシー散文を明記し正典の深さ policy と対応付けてから close するのが安全。実測（[統合試行レポート](./phase1-integration-trial-report.md)）は description 整合を要求し enum は未要求。承認 ADR も「enum 無し description 整合のみ」の軽量案を留保済み＞ | schema description・§6.3 例・SKILL 本文の語彙が4値で一致し、`deep` が正典・schema から除去される。Phase 1 統合試行の TAE 例（`thick`）が valid のまま |
| **T12-3** | assurance-statement.schema.json（`technique`） | ユニオン型 `["string","array"]` を `oneOf: [{type:string},{type:array,items:{type:string}}]` へリファクタし AJV strict の `allowUnionTypes` 警告を解消。description はカンマ区切り文字列・配列の両形の説明を維持。複数技法引用の配列実例（例 `["BB-02","BB-03"]`）を test-design-implementation/SKILL.md の保証ステートメント出力例に追加し配列形を実際に exercise | `ajv --strict=true` で `allowUnionTypes` 警告が出ない。文字列例・配列例の双方が valid |

**受入基準**: 6修正が適用され、**コミット済み検証ハーネス（実行前提参照）**で strict compile が全件通過し（`allowUnionTypes` 警告0は T12-3 適用後に達成）、CS-1／CS-2 の「文言どおり版が invalid・準拠版が valid」だった不整合が往復フィクスチャの機械再検証で解消する。`routing-table.md` / `pipeline-gates.md` の実スキル昇格は本タスクでは行わない（T3a で扱う。改訂 PR は6件の欠陥修正に限定）。

## T1: 不足ナレッジ文書3件の新規作成

Phase 1 スキルで「プロンプト由来・要出典補強」とタグ付けした3領域を、出典付きで `docs/` に文書化する。3領域はいずれも [ハブ §1 不足領域リスト](./skill-ecosystem-design-plan.md#不足領域リスト)で「Phase 2 で新規文書化」と指定され、[§C 対応表](./skill-ecosystem-design-plan.md)が担当スキルとの対応を示す。

HQW v3 など `_research` 由来の材料を使う場合は、研究カードから直接本文化しない。`source-verification-backlog.md` の `source_records` で claim scope・版・license note・確認結果を確認し、確認済み範囲だけを license-safe paraphrase として canonical docs へ入れる。研究カードの `source_layers[]` は出典カテゴリであり、それだけでは採用根拠にしない。

| 文書（提案パス） | 内容 | 主な引用元スキル |
|---|---|---|
| `docs/quality-management/code-review-techniques.md` | IEEE 1028 レビュー体系・SAST/DAST 結果の解釈・所見の重大度付け | #9 code-review |
| `docs/quality-management/defect-taxonomy-odc.md` | ODC（直交欠陥分類）・欠陥トリガー/impact 属性・欠陥密度分析 | #10 defect-analysis-rca |
| `docs/test-techniques/japanese-test-design-methods.md` | 3色ボールペン分析／要求のメタモデル分析／ゆもつよメソッド／Tiramis 8要素／ラルフチャート（HAYST）／観点・フレーム・コンテナ階層化 | #1 TRA・#3 TAD |

**根拠**: [ハブ §1 不足領域リスト](./skill-ecosystem-design-plan.md#不足領域リスト)がこの3領域を「Phase 2 で新規文書化」と明記する。#9/#10 は自スキルの `knowledge_refs` がこれらを指すため、**当該スキル（T6/T7）より前に文書を用意する**（T4〜T11 の依存前提）。配置ディレクトリは既存ドメイン構成に合わせる（上表は提案。着手時に確定）。

**既存スキルへの再配線（必須）**: `japanese-test-design-methods.md` 作成後、#1 `test-requirement-analysis` と #3 `test-architecture-design` の frontmatter `knowledge_refs` に同 doc を追記し、本文の「文書化予定／出典補強待ち」記述を「文書化済み・参照」へ反転する（現状これらの `knowledge_refs` は同 doc を指しておらず、doc 作成だけでは受入が空虚に充足するため）。新規3 doc は `docs/README.md` の索引に登録する（`knowledge/index.md` は topic→section 索引のため対象外）。

**受入基準**: 3文書が §見出しアンカー付きで存在し、[ハブ §1 不足領域リスト](./skill-ecosystem-design-plan.md#不足領域リスト)が指定する3領域（ODC 欠陥タクソノミー／コードレビュー専用文書／日本発テスト設計技法）を漏れなくカバーする。#1/#3/#9/#10 の `knowledge_refs` の全パスが実在する（**#1/#3 は新規 `japanese-test-design-methods.md` を含み、本文の予定／補強待ち記述が解消済み**）。新規3 doc が `docs/README.md` 索引に登録済み。記述が出典参照方式（プロンプト記憶の再記述をしない）。

## T2: schemas/ 追記（新構造ノードの契約化・content/items 使い分け明文化）

#7〜#14 の出力（[ハブ §3](./skill-ecosystem-design-plan.md#3-スキル定義一覧)の各スキル入出力欄）を棚卸しし、**正典が ID を定義済みかつトレースグラフに参加する構造ノード**のみ専用スキーマを追加する。ナラティブ／助言的成果物は handoff-envelope の `content`/`items` に留める。

| 追加スキーマ（draft 2020-12） | 正規出典 | 備考 |
|---|---|---|
| `test-execution-log.schema.json`（RUN） | [test-process §6.1 ID表](../test-techniques/test-process-research-summary-test-design.md)（`RUN-001`）＋[ハブ §3 #7](./skill-ecosystem-design-plan.md#3-スキル定義一覧) | TC→RUN のチェーン末端。テスト空間の「プロセス軸」に必要 |
| `sli-slo-definition.schema.json`（MON） | [quality-knowledge-schema.md §1.3 MON](../quality-models/quality-knowledge-schema.md)（`id`/`name`/`signal_type` enum/`qc_refs`/`ac_refs`/`threshold`/`owner`/`feedback_target_refs` の**完全フィールド契約**）＋主参照 [production-quality-sre-observability.md](../operations-quality/production-quality-sre-observability.md)＋[ハブ §3 #12](./skill-ecosystem-design-plan.md#3-スキル定義一覧)（`MON-nnn` ID） | **契約は T2 で確定的に固める（正典契約が既存）**。記入例のみ #12（T9）実装時に補完 |
| `artifact-review-finding.schema.json` | [ハブ §3 #14](./skill-ecosystem-design-plan.md#3-スキル定義一覧)（`ArtifactReviewFindingList` 5観点） | ゲート委譲（T12）で 3値 `gate_status` の機械的根拠となる |

**id パターン**は既存規約（`^PREFIX-[0-9]+$`）に整合させる。専用スキーマ不要と判断した成果物（RCA レポート・チャーター推奨・欠陥候補リスト等）は、handoff-envelope の `content`（オブジェクト形式）/`items`（配列形式）のどちらで表現するかを **`schemas/README.md` の "content vs items" 節へ明文化**する（[統合試行レポート](./phase1-integration-trial-report.md)で未明文化だった点の解消）。RiskRegister 更新は既存 `risk-item` を再利用する。

**フィールド設計の指針**: MON は上記の完全な正典契約（[quality-knowledge-schema.md §1.3](../quality-models/quality-knowledge-schema.md)）に従い**発明しない**。RUN（test-process §6.1 は ID 行のみ）と `artifact-review-finding`（ハブ §3 #14 は5観点リストのみ）はフィールドレベル正典が無いため、既存スキーマの**ハウススタイル**（`description` 内に設計判断の根拠を記録。例: `test-architecture-element.schema.json` の桁数・自由文字列の断り書き）に倣い最小導出する。MON スキーマは **skill-handoff 知識成果物**であり veridia の runtime evidence／`ExecutionEvidence` 契約ではない旨を `description` に明記し、product-specific data を含めない。

**受入基準**: 追加3スキーマが全件バリデーターを通り、既存 id 体系・envelope 契約と整合する。各対応スキルの出力例が該当スキーマに valid。専用スキーマ不要とした成果物について `content`/`items` の使い分けが明記されている。追加スキーマは `schemas/README.md` の repo-local schema rule に従い、veridia runtime schema、`GatePolicy`、`OracleSpec`、`Evidence`、`ExecutionEvidence`、runtime gate mapping を混ぜない。`docs/_research/` 由来の候補を使う場合も、canonical docs または repo-local design document へ昇格・整理してから schema source とする。

## T3a: ルーティング表の凍結解除と改訂

Phase 1 で変更凍結していた `skills/quality-orchestrator/references/routing-table.md` を、実測結果（統合試行・コールドスタート）を根拠に改訂し、#7〜#14 を「未実装案内」から実ルーティング先へ昇格する。

> **【マージ順制約】** この T3a の昇格 PR は **#7〜#14（T4〜T11）が main に存在してからマージ**する。作業は並行してよいが、スキル未作成のまま「実装済み」を宣伝する状態を main に作らない（T3a を T4〜T11 より先にマージしない）。

1. ルーティング表の **P2 行（既存8行＝#7〜#14）** の案内を「実装済み」に更新し、フォールバックの「未実装。手動で `docs/` を参照」案内を削除する。
2. `business-quality-metrics`（#15）は **P3 のまま据え置く**（Phase 2 で昇格しない）。orchestrator/SKILL.md の P2/P3 フォールバック文言も #7〜#14 を routable に、#15 は future/blocked のまま更新する。
3. 変更は[統合試行レポートの改善点](./phase1-integration-trial-report.md#発見された改善点)に紐づく行のみに限定し、場当たり変更をしない。

**根拠**: ルーティング表は全スキルの `description` と整合しなければならず、トリガー精度の検証根拠になる。証拠ベースでのみ改訂する。

**受入基準**: ルーティング表の P2 8行が実スキル名を指し、フォールバック案内が実装済み前提に更新される。#15 は P3 表記のまま。変更が全て試行レポートの根拠に紐づく。

## T4〜T11: 8スキル #7〜#14 の作成（skill-creator 使用）

### 作成順序（依存順）

```
T4:  #14 quality-artifact-review    ← 最初（ゲート委譲 T12 の受け皿・全スキル成果物のメタレビュー基盤）
T5:  #7  test-execution-support (TE)  （4段階複合フローの末端。TC→RUN）
T6:  #9  code-review                （T1 コードレビュー技法文書に依存）
T7:  #10 defect-analysis-rca        （T1 ODC 文書に依存）
T8:  #11 nfr-review                 （1スキル+4レンズ）
T9:  #12 sre-quality-ops
T10: #13 ai-system-quality-eval
T11: #8  exploratory-testing-support  （役割境界「探索実行主体は AI エージェント（実行系）、スキルは選定・設計・後処理」を厳守。D-012 で改訂）
```

**根拠**: #14 を最初に置くのは、後続 T12（ゲート委譲）の受け皿であり、メタレビュー観点が他スキルの受入観点の土台になるため（SKILL.md 作成は正典/schema に対して行い、実成果物は不要。メタレビューの受入試験は T14 で実施）。#9/#10 は T1 のナレッジ文書に依存するので文書完成後。残りは `docs/` の充実度が高くデータ契約リスクが低い順に並べる。

### 全スキル共通の受入基準（Phase 2 版・10項目）

1. SKILL.md に**必須3セクション**（最小入力契約／上流成果物なし時の振る舞い／出力エンベロープ）が存在する（[ハブ §4](./skill-ecosystem-design-plan.md#4-オーケストレーション設計)）。
2. コールドスタート起動で質問が**3件以内**（オーケストレーターは1回）に収まり、**必ず何らかの出力**（`gate_status: blocked` を含む）を返す。無限質問・無回答は不合格。
3. 出力エンベロープが `schemas/handoff-envelope.schema.json` に適合する。
4. **暫定性・前提はエンベロープ `assumptions[]` に `{field,value,reason}` 形式で記録し、個別 item はスキーマ準拠のまま保つ**（item に `assumption` フィールドや `-inline-` 接頭辞を足さない。CS-1/CS-2 準拠）。生成 item は全て該当スキーマに valid。
5. frontmatter が [ポータビリティ設計 §1](./portability-design.md) の仕様（`name`/`description`/`version`/`inputs`/`outputs`/`capabilities`/`knowledge_refs`）に適合し、`capabilities` が必要最小限、`knowledge_refs` の全パスが実在する（T1 新規文書を含む）。
6. SKILL.md 本体が500行未満で、`docs/` を再記述せず参照（ポインタ）で済ませている。
7. SKILL.md は runtime-neutral blueprint として書き、veridia `qa-skills` 実行パッケージ、veridia runtime adapter、または veridia orchestration 実装として書かない。
8. `knowledge_refs` に `docs/_research/` を含めない。研究候補は canonical docs へ昇格してから参照する。
9. `knowledge_refs` に `knowledge/` を含める場合は、対応する source canonical docs / section が明示された derived artifact に限る。`knowledge/` に独自の `verification_state` は導入しない。
10. veridia runtime artifact / evidence / gate mapping（例: `GatePolicy`, `OracleSpec`, `Evidence`, `ExecutionEvidence`）をスキルの出力契約へ混ぜない。必要なら将来の veridia 側 import/mapping 計画に送る。

### スキル別の追加受入観点

| スキル | 追加受入観点 |
|---|---|
| #14 quality-artifact-review | [ハブ §3 #14](./skill-ecosystem-design-plan.md#3-スキル定義一覧)の5観点（文書点・工程一貫性・トレーサビリティ・説明責任・技術的妥当性）を `artifact-review-finding` で出力する。前工程成果物の欠落自体を最重要所見として報告する。3値 `gate_status` を返し、ゲート委譲（T12）の受け皿として機能する |
| #7 test-execution-support (TE) | 実行ログのみで起動する。TC なし時はログからケース相当を逆推定し前提を `assumptions[]` に記録する。`RUN-nnn`（`test-execution-log`）＋flaky 判定＋欠陥候補を出力する |
| #9 code-review | diff のみで起動する。静的解析結果なし時は目視レビューのみである旨を明記する。所見が重大度付き（正確性/セキュリティ/保守性）で、`docs/quality-management/code-review-techniques.md`（T1 で新規作成）を引用する |
| #10 defect-analysis-rca | RCA 手法（5Whys／フィッシュボーン／FTA／STPA）の選定理由を出力する。ブレームレスな記述で、`docs/quality-management/defect-taxonomy-odc.md`（T1 で新規作成）で欠陥分類する。RiskRegister 更新提案（`risk-item`）を返す |
| #11 nfr-review | 1スキル+4レンズ構成。未指定時は全4レンズを実施し対象外を「非該当」と明記する。**トレードオフマトリクスを必須出力**する（[ハブ §3 #11](./skill-ecosystem-design-plan.md#3-スキル定義一覧)） |
| #12 sre-quality-ops | サービス概要のみで起動する。既存メトリクスなし時は業界標準 SLO を仮提案し前提を `assumptions[]` に記録する。`MON-nnn`（`sli-slo-definition`）＋エラーバジェットポリシー＋バーンレート警報＋DORA5指標解釈を出力する |
| #13 ai-system-quality-eval | AI 機能説明のみで起動する。既存評価データなし時はゴールデンセット設計指針に留める。pass@k/pass^k・LLM-judge バイアス・メタモルフィックテスト・多段CI を含む評価設計を出力する |
| #8 exploratory-testing-support | 対象機能説明のみで起動する。リスク情報なし時は汎用チャーターを優先する。[チャーターカタログ](../exploratory-testing/exploratory-testing-charter-catalog-by-tour.md)の `CHT-Cnn` 表記で推奨チャーターとデブリーフ要約を出力し、**「探索実行主体は AI エージェント（veridia 等の実行系）であり、本スキルは実行しない。価値判断・重大度・リリース可否の最終判断は人間」の役割境界を出力に明記**する（[D-012](../../DECISIONS.md#d-012-土台先行のベース作成と再評価ループ)で改訂） |

**各タスクの受入基準**: 各 T は「共通受入基準10項目」＋「上表の該当スキル1行」を満たすことをもって完成とする。

## T12: ゲート判定の quality-artifact-review(#14) への委譲

MVP でオーケストレーター内蔵だったゲート判定を #14 へ移す（[ハブ §4](./skill-ecosystem-design-plan.md#4-オーケストレーション設計)：「MVP ではゲート判定をオーケストレーター内蔵とし、Phase 2 で quality-artifact-review スキルへ委譲する」）。**#14 が存在してから（T4 の後）**実施する。

1. `quality-orchestrator/SKILL.md` の各段ゲート判定ロジックを #14 呼び出しへ置換し、オーケストレーターは進行管理に専念する。
2. pipeline-gates のゲート観点（TRA/TAD/TDD/TI レビュー）を #14 の入力チェックリストとして参照する。
3. 3値ゲート（passed / passed-with-risks / blocked）の呼び出し境界を明記する。

**受入基準**: オーケストレーターがゲート判定を #14 に委譲し、複合フロー各段で #14 が 3値 `gate_status` を返す。[Phase 1 統合試行](./phase1-integration-trial-report.md)の判定結果（passed-with-risks×4・blocked×1）が委譲後も再現する。

## T3b: pipeline-gates の最終化（T12 と整合）

T12 でゲート判定を #14 に委譲した後、`skills/quality-orchestrator/references/pipeline-gates.md` を委譲後の参照構造に更新する（T3a のルーティング表更新とは別段階）。

**受入基準**: ゲート観点が #14 の入力チェックリストとして参照され、委譲後の呼び出し構造と整合する。凍結解除は Phase 2 改訂の範囲内（Phase 1 限定の凍結制約は解除済み）。

## T13: テスト空間3軸マトリクス描画の実装（#5 traceability-management）

[ハブ §3 #5](./skill-ecosystem-design-plan.md#3-スキル定義一覧)の3軸（レベル×タイプ×プロセス）Markdown ヒート表／Mermaid 描画を #5 に実装する。Phase 1 では出力自体はされたが描画が十分に exercise されなかった（[統合試行レポート](./phase1-integration-trial-report.md)）。既存 #5 の改訂であり新スキルに非依存のため T4〜T11 と並行可。

1. `knowledge/test-space/matrix-template.yaml` を入力に、3軸マトリクスの Markdown ヒート表レンダリングを #5 に実装する。
2. セル密度（該当 TC 数）の可視化と、空セル（未カバー領域）の強調を規定する。
3. Mermaid 代替表現のフォールバックを明記する。

**受入基準**: 実チェーン（統合試行の成果物）に対し3軸ヒート表が生成され、未カバーセルが視認でき、Phase 1 で「描画未検証」だった点が解消する。

## T14: Phase 2 統合試行（複合フロー拡張＋コールドスタート）＋実セッション・トリガー観点の follow-up 登録

Phase 1 の T12／Phase 1b が積み残した項目を、Phase 2 スキルを含めて検証する。

1. 4段階複合フロー（TRA→TAD→TDD/TI→**TE**、[ハブ §4](./skill-ecosystem-design-plan.md#4-オーケストレーション設計)）を一気通しで実行し、末端 TE（#7）まで RUN 生成とゲート委譲（#14）を確認する。
2. #9〜#13 の単体起動を各1本、#14 のメタレビューを成果物一式に対し1本実施する。
3. コールドスタート: 新8スキルの「上流成果物なし→3件以内質問→必ず出力（blocked 可）」を発火＋スキーマ機械検証（Phase 1b と同方式）。生成 item は schema-valid で、前提は `assumptions[]` のみに記録されること。
4. **実セッション・トリガー観点の follow-up 登録（非ゲート）**: 実 Claude Code セッションでの `description` 自動発火の精度と、明確化質問→応答待ち→再開の対話フローは、ロールプレイでは原理的に検証できない（roadmap-status.md「完了の意味と検証の限界」）。**Phase 2 完了の必須ゲートにはせず**、別建ての follow-up として登録し受入観点にのみ明記する。実インタラクティブ運用で埋める。
5. 結果（誤分類・質問数超過・ゲート誤判定・トリガー精度）を Phase 2 試行レポートに記録する。

**受入基準**: 4段階複合フローが末端 TE まで通り全 envelope が valid。8新スキルのコールドスタートが全て schema-valid な item を生成しつつ前提を `assumptions[]` のみに記録する。実セッションのトリガー精度・対話フローは follow-up として登録・記録される（完了ゲートではない）。

---

## 正規出典対応表（Phase 2 成果物 → 正規出典）

| 成果物／文書 | 正規出典 |
|---|---|
| `test-execution-log.schema.json`（RUN） | [test-process §6.1 ID表](../test-techniques/test-process-research-summary-test-design.md)（`RUN-001`）＋[ハブ §3 #7](./skill-ecosystem-design-plan.md#3-スキル定義一覧) |
| `sli-slo-definition.schema.json`（MON） | [quality-knowledge-schema.md §1.3 MON](../quality-models/quality-knowledge-schema.md)（完全フィールド契約）＋主参照 [production-quality-sre-observability.md](../operations-quality/production-quality-sre-observability.md)＋[ハブ §3 #12](./skill-ecosystem-design-plan.md#3-スキル定義一覧)（`MON-nnn`） |
| `artifact-review-finding.schema.json` | [ハブ §3 #14](./skill-ecosystem-design-plan.md#3-スキル定義一覧)（`ArtifactReviewFindingList` 5観点。フィールドレベル正典が無いためハウススタイルで最小導出） |
| コードレビュー技法 文書 | 新規（IEEE 1028 等）。[ハブ §1 不足領域リスト](./skill-ecosystem-design-plan.md#不足領域リスト)（コードレビュー専用文書） |
| ODC 欠陥タクソノミー 文書 | 新規。[ハブ §1 不足領域リスト](./skill-ecosystem-design-plan.md#不足領域リスト)・§C 対応表 |
| 日本発テスト設計技法 文書 | 新規（3色ボールペン／ゆもつよ／Tiramis／ラルフチャート／メタモデル分析／観点階層化）。[ハブ §C 対応表](./skill-ecosystem-design-plan.md) |
| #7〜#14 の各 SKILL.md | [ハブ §3 スキル定義一覧](./skill-ecosystem-design-plan.md#3-スキル定義一覧)の該当スキル節＋[ポータビリティ設計 §1](./portability-design.md) |
| ルーティング表 P2 行の改訂 | [統合試行レポート「発見された改善点」](./phase1-integration-trial-report.md#発見された改善点) |
| ゲート委譲 | [ハブ §4 オーケストレーション設計](./skill-ecosystem-design-plan.md#4-オーケストレーション設計) |

## Phase 2 完了チェックリスト

- [ ] **検証ハーネス**がコミットされ（pinned invoke・`schemas/tests/` フィクスチャ・CI 任意）、現行8スキーマの strict compile と往復フィクスチャが通る
- [ ] **T0 改訂 PR** がマージされ、コミット済み検証ハーネスで strict compile が全件通過（`allowUnionTypes` 警告0）し、CS-1/CS-2 の不整合が往復フィクスチャで機械再検証・解消
- [ ] `docs/` に不足ナレッジ文書3件（コードレビュー技法／ODC／日本発テスト設計技法）が存在し、#1/#3/#9/#10 の `knowledge_refs` が実在化（**#1/#3 は新規 japanese-test-design-methods.md を参照、`docs/README.md` 索引に登録**）
- [ ] `schemas/` に追加3スキーマ（test-execution-log／sli-slo-definition／artifact-review-finding）が存在しバリデーター通過
- [ ] `skills/` に8ユニット（#7〜#14。SKILL.md + references/）が存在し、全スキルが共通受入基準10項目を満たす
- [ ] スキル別の追加受入観点がすべて確認済み
- [ ] ルーティング表の P2 8行が実スキルへ昇格し、#15 は P3 据え置き
- [ ] ゲート判定が #14 へ委譲され、複合フロー各段で 3値 `gate_status` を返す
- [ ] pipeline-gates（T3b）が #14 委譲後の参照構造に更新され、ゲート観点が #14 の入力チェックリストとして参照される
- [ ] テスト空間3軸マトリクスの Markdown ヒート表描画が #5 に実装され、未カバーセルが視認できる
- [ ] Phase 2 統合試行（複合フロー＋コールドスタート）が1本完了し、改善点が記録されている
- [ ] （follow-up・非ゲート）実 Claude Code セッションでの `description` 自動発火精度・対話フローの実測項目が登録されている

## 関連ドキュメント

- [スキル・エコシステム設計プラン](./skill-ecosystem-design-plan.md) — スキル定義（§3）・オーケストレーション設計（§4）・ロードマップ（§5）の正典
- [ナレッジマネジメント設計](./knowledge-management-design.md) — knowledge/ 配下の構造とシード内容の正典
- [ポータビリティ設計](./portability-design.md) — SKILL.md 仕様と実装例の正典
- [Phase 1 実装ガイド](./phase1-implementation-guide.md) — 本書の形式雛形
- [統合試行レポート](./phase1-integration-trial-report.md) — T12（ハッピーパス）の結果と改善点（T12-1/2/3）
- [コールドスタート検証レポート](./phase1b-coldstart-trial-report.md) — Phase 1b の結果と改善点（CS-1〜CS-3）・正典照合の結論
- ADR-0002 Phase 2 計画意思決定記録 — 本ガイドに至った設計判断・レビュー経緯・承認時プランのスナップショット
- ロードマップ俯瞰・進捗トラッキング — 全 Phase の現在地
