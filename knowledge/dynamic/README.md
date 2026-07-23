# knowledge/dynamic/ — 動的ナレッジ

## 目的

このディレクトリは、対象プロダクトに固有の機微情報（社内用語・品質基準・欠陥履歴・プロダクト文脈）を置く場所です。`docs/` と `knowledge/`（`dynamic/` を除く）が業界標準・技法・プロセスといった**どのプロジェクトにも通用する静的ナレッジ**であるのに対し、ここは**特定プロジェクトに紐づく動的ナレッジ**を扱います。

## 実データはコミット禁止（gitignore済み）

本リポジトリは MIT ライセンスの公開ナレッジベースです。このディレクトリ配下は `.gitignore` により以下のみがコミット対象です。

- `knowledge/dynamic/README.md`（本ファイル）
- `knowledge/dynamic/_templates/` 配下の空スキーマテンプレート

`_templates/` 以外に置いた実データファイル（例: `company-terms.yaml` を直下に作成した場合）は git の追跡対象になりません。**空スキーマ以外のデータをこのディレクトリへコミットしないでください。**

## `_templates/` の使い方

1. `_templates/` 配下のファイルを `knowledge/dynamic/` 直下にコピーする（例: `_templates/company-terms.yaml` → `knowledge/dynamic/company-terms.yaml`）。
2. コピー先のファイルに実データを記入する。コピー先は gitignore 対象なのでコミットされない。
3. 各スキルは `knowledge/dynamic/company-terms.yaml` のような固定パスを参照するため、実データの中身が変わってもスキル側の参照コードは変更不要。

## プライベートリポジトリへの symlink 昇格パス

実運用では、対象プロダクトごとにプライベートリポジトリで動的ナレッジの実データを管理し、それを本リポジトリの `knowledge/dynamic/` へ symlink する運用を想定しています。

```
knowledge/dynamic/company-terms.yaml -> /path/to/private-repo/company-terms.yaml
```

symlink の向き先がローカルテンプレートの複製かプライベートリポジトリの実データかに関わらず、スキル側が参照する相対パスは不変です。昇格は symlink 操作1回で完結します。詳細な根拠は [knowledge-management-design.md §1.3](../../docs/agent-ecosystem/knowledge-management-design.md#13-プライベートリポジトリへの-symlink-昇格パス) を参照してください。

## 静的→動的の参照順序と出所の明示

各スキルは、ナレッジを参照する際に**必ず静的→動的の順**で参照します。

1. まず `docs/` と `knowledge/`（`dynamic/` を除く）を確認する（標準・技法・プロセスの一般知識）。
2. その後に `knowledge/dynamic/`（プロジェクト固有の前提・用語・基準）を確認する。

出力（ハンドオフエンベロープ等）には、主張の根拠がどちらのレイヤに由来するかを明示してください。例えば「本判定は ISO/IEC 25010:2023（静的）とプロジェクト固有の品質基準 `quality-criteria.yaml`（動的）の両方に基づく」のように書きます。動的ナレッジは検証されていない・実データが空である可能性が高いため、出所を明示しないと判断が「業界標準に基づく一般論」なのか「プロジェクト固有の前提に基づく特殊解」なのか利用者が区別できなくなります。

詳細な設計根拠は [knowledge-management-design.md §1](../../docs/agent-ecosystem/knowledge-management-design.md#1-静的ナレッジと動的ナレッジの分離方針) を参照してください。
