# リポジトリ内 schema

`schemas/` は、このリポジトリの skill I/O artifacts と local quality-skill outputs のための JSON Schema を置く。

これらの schema は repo-local contracts であり、export candidates でもある。veridia runtime schemas ではない。将来 veridia が import または mapping する場合、その mapping は veridia 側の planning / implementation で扱う。

## Skill I/O schema

- `artifact-review-finding.schema.json`
- `assurance-statement.schema.json`
- `condition-assignment-matrix.schema.json`
- `coverage-item.schema.json`
- `detailed-test-condition.schema.json`
- `handoff-envelope.schema.json`
- `high-level-test-condition.schema.json`
- `release-decision.schema.json`
- `risk-item.schema.json`
- `routing-decision.schema.json`
- `stakeholder.schema.json`
- `test-architecture-element.schema.json`
- `test-case.schema.json`
- `test-space-matrix.schema.json`
- `traceability-matrix.schema.json`

## `handoff-envelope` の `content` と `items` の使い分け

各 skill は成果物を `handoff-envelope.schema.json` の `artifacts[]` に格納する。要素は `content`（object）か `items`（array）のどちらかで本体を表現する。使い分けは次のとおり。

- **`items`（array 形）**: 同種のレコードが並ぶ集合。各レコードが `^PREFIX-[0-9]+$` の一意 ID を持つトレースグラフのノード列（`StakeholderList` / `RiskRegister` / `HighLevelTestConditionList` / `DetailedTestConditionList` / `TestArchitectureElementList` / `CoverageItemList` / `TestCaseList` 等）。各レコードは対応する per-item schema（`risk-item` など）に個別準拠する。例外として `ArtifactReviewFindingList`（quality-artifact-review の所見一覧）はトレースグラフ非参加だが、一意 ID（`ARF-`）を持つ同種レコードの集合のため items 形＋per-item schema（`artifact-review-finding`）を用いる。
- **`content`（object 形）**: 単一の構造化オブジェクトで、ID 付きレコードの集合ではないもの（`RoutingDecision` / `ConditionAssignmentMatrix` / `TraceabilityMatrix` / `TestSpaceMatrix` / `release_decision` 等）。`handoff-envelope` の `content` は無制約 object のため、機械検証が要る場合は **repo-local の専用スキーマを別途用意し、skill が `schema_ref` でそれを指す**（envelope 経由では構造を強制できないため）。

**専用スキーマを持たない成果物**: ナラティブ／助言的で ID 体系もトレースグラフ参加もしないもの（`ThreeColorAnalysisReport` 等）は、専用スキーマを設けず `content` に置き、`schema_ref` に skill 定義またはテンプレートへのポインタを指定してよい。この場合、機械検証の対象は envelope 構造（type / schema_ref の存在）に留まる。

## ルール

- 各 schema は `description` または関連 documentation で canonical source を示す。
- 新しい構造を導入する前に、既存の canonical docs と established IDs を優先する。
- `docs/_research/` から schema を直接 derive しない。
- veridia 固有の `GatePolicy`、`OracleSpec`、`Evidence`、`ExecutionEvidence`、runtime gate mapping をこのディレクトリに混ぜない。
- export bundles は generated / versioned downstream artifacts として扱い、hand-edited runtime state にしない。

## レビュー観点

- schema は canonical docs または repo-local design document を指しているか。
- ID pattern は existing canonical ID guidance と整合しているか。
- schema はこのリポジトリの skills に必要なものか。veridia runtime concern ではないか。
- product-specific data を避けているか。
- research-only claim を source verification なしに promote していないか。

## 検証ハーネス

リポジトリルートで `bash scripts/validate-schemas.sh` を実行する。fixture の構成と strict 警告ポリシーは [tests/README.md](tests/README.md) を参照する。
