# トレーサビリティ検査 ポインタ表

## 位置づけ

本ファイルは `traceability-management` スキルの手順（[../SKILL.md](../SKILL.md)）
で参照する早見表である。ノード間関係・トレース項目・テスト空間3軸の解説は
docs/ 側の該当節が正典であり、本ファイルはそこへのポインタのみを提供する。
新規の解説は書かない。

## ノード間関係と双方向トレース（quality-knowledge-schema.md §1.4）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| ID体系 | `REQ-`/`STK-`/`RISK-`/`QC-`/`AC-`/`TEST-`/`MET-`/`EV-`/`REL-`/`MON-` の10ノードプレフィックスと既存テスト設計チェーン（`HTC-`〜`RUN-`）との対応 | [quality-knowledge-schema.md §1.2 ID体系と既存データ契約との対応](../../../docs/quality-models/quality-knowledge-schema.md#12-id-体系と既存データ契約との対応) |
| 関係の多重度 | REQ↔STK・RISK↔QC・AC↔TEST 等が多対多であること（1対1前提で検査すると誤検出する） | [quality-knowledge-schema.md §1.4 ノード間関係と双方向トレース](../../../docs/quality-models/quality-knowledge-schema.md#14-ノード間関係と双方向トレース) |
| フォワードトレース | REQ→MON方向。未検証の要求（AC/TESTにリンクのないREQ）の検出に使う | 同上 |
| バックワードトレース | MON→REQ方向。目的を説明できないテスト・監視項目の検出に使う | 同上 |

## チェーンが切れていると何が言えなくなるか（§1.5）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| ノード別の欠落影響表 | STK/RISK/QC/AC/TEST/MET/EV/REL/MON それぞれが欠けたときに言えなくなること・典型症状 | [quality-knowledge-schema.md §1.5 チェーンが切れていると何が言えなくなるか](../../../docs/quality-models/quality-knowledge-schema.md#15-チェーンが切れていると何が言えなくなるか) |

## 最低限のトレースチェーンとトレース項目（test-process §7）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| チェーン全体像 | REQ→HTC→DTC→TAE→COV→TC→TPR→RUN→DEC、RISK→DTC/TAE/COV、RUN↔BUG→DEC | [test-process-research-summary-test-design.md §7.1 最低限のトレースチェーン](../../../docs/test-techniques/test-process-research-summary-test-design.md#71-最低限のトレースチェーン) |
| 接続別の目的 | 各接続（要求→ハイレベル条件、条件→アーキテクチャ要素 等）が何を示すか | [test-process-research-summary-test-design.md §7.2 トレース項目](../../../docs/test-techniques/test-process-research-summary-test-design.md#72-トレース項目) |
| 基本ID体系 | `REQ`/`RISK`/`HTC`/`DTC`/`TP`/`TAE`/`COV`/`TC`/`TPR`/`RUN`/`BUG` の対応表 | [test-process-research-summary-test-design.md §6.1 基本ID体系](../../../docs/test-techniques/test-process-research-summary-test-design.md#61-基本-id-体系) |

## テスト空間3軸マトリクス（knowledge-management-design.md §6）

| 項目 | 内容 | 出典 |
| --- | --- | --- |
| 3軸の定義 | `test_level`（コンポーネント/統合/システム/受入）・`test_type`（ISO/IEC 25010:2023の9特性+機能+変更関連）・`test_process`（TRA/TAD/TDD-TI/TE/MON） | [knowledge-management-design.md §6.2 3軸の定義](../../../docs/agent-ecosystem/knowledge-management-design.md#62-3軸の定義) |
| セル形式とテンプレート | `{status: covered\|partial\|none, evidence: [ID,...], notes}`、`CHT-` プレフィックスによるチャーター参照 | [knowledge-management-design.md §6.3 セル形式とマトリクステンプレート（YAML）](../../../docs/agent-ecosystem/knowledge-management-design.md#63-セル形式とマトリクステンプレートyaml)、[knowledge/test-space/matrix-template.yaml](../../../knowledge/test-space/matrix-template.yaml) |
| 描画とインスタンスの置き場所 | 本スキルが描画（Markdownヒート表/Mermaid、CSVエクスポート）を担当。インスタンスは対象プロジェクト側 `quality-artifacts/` か `knowledge/dynamic/` に置き、本リポジトリにはコミットしない | [knowledge-management-design.md §6.4 描画とインスタンスの置き場所](../../../docs/agent-ecosystem/knowledge-management-design.md#64-描画とインスタンスの置き場所) |

## レビュー観点（本スキル固有の自己点検）

| 観点 | チェック内容 | 出典 |
| --- | --- | --- |
| 双方向性 | フォワード・バックワードの両方向を検査したか | [quality-knowledge-schema.md §1.4](../../../docs/quality-models/quality-knowledge-schema.md#14-ノード間関係と双方向トレース) |
| 多重度の誤認 | 多対多関係を1対1前提で誤検出していないか | 同上 |
| ID体系不明の扱い | 既知プレフィックスに一致しない成果物を推測で埋めず「未接続」として報告したか | [test-process-research-summary-test-design.md §6.1 基本ID体系](../../../docs/test-techniques/test-process-research-summary-test-design.md#61-基本-id-体系) |
