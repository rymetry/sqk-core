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

[D-007](./DECISIONS.md#d-007-phase-2-の再ベースライン) に従い、vertical slice（m0 Viewer Analytics のテスト設計）の結果を根拠として Phase 2 の backlog material を再評価した。結果は [D-011](./DECISIONS.md#d-011-phase-2-backlog-の再評価vertical-slice-根拠) に記録する。方針は「幅（8新スキル）より先に、実証済みチェーンの深さ（構造的欠落の解消・機械検証範囲の拡張）を作りきる」。

### 4. 再評価後の実装

keep と判断した「深さ」4件を、依存順で実装する。各項目の受入基準は着手時に定める。

1. `StakeholderList` の schema 追加と risk-analysis の生成手当て（RISK→STK の接続）
2. `schemas/README.md` の content/items 明文化と HTC/マトリクス系の専用 schema 追加
3. traceability-management の随時起動→末尾一括への文言修正
4. テスト空間3軸マトリクス描画の稼働確認

keep 4件の完了後、再評価キュー先頭の #14 quality-artifact-review を slice 成果物への dry-run で再評価し、keep（実装）へ格上げした（[D-011 フェーズB追記](./DECISIONS.md#d-011-phase-2-backlog-の再評価vertical-slice-根拠)）。実装は `skills/quality-artifact-review/` ＋ `artifact-review-finding` schema。ルーティング表 #14 行の実装済みへの昇格（T3a 相当・単行）、および orchestrator ゲート判定の #14 への委譲（T12 相当。pipeline-gates の委譲後更新 = T3b 相当を含む）はいずれも実施済みであり、フェーズB の follow-up は完了した。

新スキル7件（#7〜#13）とナレッジ文書3件は defer 継続とし、ROADMAP から削除せず「ドメイン別再評価待ち」として保持する（[D-011](./DECISIONS.md#d-011-phase-2-backlog-の再評価vertical-slice-根拠)）。該当ドメインの実タスクが現れた時が各項目の再評価タイミングである。

### 5. Phase 3 素材

Phase 3 相当の export、platform 展開などは素材のみ保持する。着手判断は Phase 2 の実装と実測が終わった後に行う。
