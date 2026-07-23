# sqk-core v2 ロードマップ

この文書は v2 の作業順序を示す。詳細な受入基準は各作業の着手時に定め、事前に作り込まない。

## Phase 1 実績要約

現在のリポジトリには、Phase 1 の成果として次が移植されている。

- `quality-orchestrator` と6つの専門スキルからなる [skills 7ユニット](./skills/)
- skill I/O の [schemas 8件](./schemas/README.md)
- index、terminology、mappings、test-space からなる [`knowledge/` シード](./knowledge/)
- [skill ecosystem](./docs/agent-ecosystem/skill-ecosystem-design-plan.md)、[knowledge management](./docs/agent-ecosystem/knowledge-management-design.md)、[portability](./docs/agent-ecosystem/portability-design.md) の設計3文書
- T12 の統合試行を記録した [Phase 1 統合試行レポート](./docs/agent-ecosystem/phase1-integration-trial-report.md)
- Phase 1b のコールドスタート検証を記録した [Phase 1b コールドスタート検証レポート](./docs/agent-ecosystem/phase1b-coldstart-trial-report.md)

最後の2文書は完了報告であり、現行の作業手順ではない。

## v2 の作業順序

### 1. 既知欠陥6件の修正

Phase 1 / 1b レポートから申し送られた CS-1、CS-2、CS-3、T12-1、T12-2、T12-3 を先に修正する。具体的な対象と確定済み方針は、backlog material である [Phase 2 実装ガイド](./docs/agent-ecosystem/phase2-implementation-guide.md) の T0 節を参照する。

### 2. vertical slice

1つの実タスクを既存のスキルチェーンで通し、成果物の有用性、handoff、traceability、release judgment までの実用性を確認する。

### 3. Phase 2 の keep / merge / defer / drop 再評価

[D-007](./DECISIONS.md) に従い、vertical slice の結果を根拠として Phase 2 の backlog material を再評価する。残り8スキル、ナレッジ文書3件、schema や routing の候補を、そのまま実装対象とはみなさない。

### 4. 再評価後の実装

keep または merge と判断した項目だけを、依存順とリスクに応じて実装する。各項目の受入基準は着手時に定める。

### 5. Phase 3 素材

Phase 3 相当の export、platform 展開などは素材のみ保持する。着手判断は Phase 2 の実装と実測が終わった後に行う。
