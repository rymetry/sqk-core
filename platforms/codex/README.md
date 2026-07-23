# Codex 向け変換

品質スキル・エコシステムを Codex へ持ち込むための変換レシピの要約。Codex は
`AGENTS.md` をネイティブに読み取るため、この入口を再利用する。詳細は必ず
リンク先を参照すること。

## 変換手順の要約

1. **AGENTS.md への「品質スキル索引」セクション追加**。各スキルの `name` /
   `description` / `knowledge_refs` を要約した表を追記し、Codex が起動時に
   どのスキルが存在し、いつ使うべきかを把握できるようにする。新規ファイルは
   作らず、既存 AGENTS.md に追記する（読み取り起点を1つに保つため）。
2. **SKILL.md 本文の Codex カスタムプロンプト化**。「目的」「手順」
   「最小入力契約」「上流成果物なし時の振る舞い」「出力エンベロープ」の
   5節をほぼそのままカスタムプロンプトとして転記する。要約ではなく本文の
   再掲でよい。
3. **`capabilities` の解決**。`file_read` / `file_write` はワークスペース
   アクセスとして、`shell` はサンドボックス shell としてそのまま利用可能。
   `web_search` を要求するスキルは、ネットワークアクセスが許可された Codex
   環境でのみ有効である旨を索引表の備考に明記する。
4. **`knowledge_refs` の解決**。`docs/...` の相対パスはリポジトリへの
   ファイルアクセスでそのまま解決できる。GPTs のような結合ファイル生成は
   不要。

## Codex 環境固有の限界

- **自動発火の不在**: Claude Code の `description` によるトリガーに相当する
  自動発火機構を Codex は持たない。利用者またはオーケストレーター役の Codex
  セッションが、索引表を読んでスキルを選択する能動的操作が必要になる。
- **`web_search` 実行不可時のフォールバック**: ネットワークアクセスが無効な
  環境では、該当手順を「利用者に確認する」手動確認ステップに置き換える。

## 詳細

- 変換手順・環境固有の限界の完全な記述:
  [`docs/agent-ecosystem/portability-design.md` §4](../../docs/agent-ecosystem/portability-design.md#4-codex-への変換レシピ)
- 能力→プラットフォーム対応表:
  [`docs/agent-ecosystem/portability-design.md` §2](../../docs/agent-ecosystem/portability-design.md#2-能力プラットフォーム対応表)
