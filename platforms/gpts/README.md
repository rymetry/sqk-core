# ChatGPT / GPTs 向け変換

品質スキル・エコシステムを ChatGPT/GPTs へ持ち込むための変換レシピの要約。
GPTs はファイルアップロード数の上限（20ファイル）があり、任意コマンド実行や
リポジトリへの直接アクセスを持たないため、変換は「実行時参照」ではなく
「ビルド時結合」を基本方針とする。詳細は必ずリンク先を参照すること。

## 結合方針の要約

- **システムプロンプト**: オーケストレーター SKILL.md 本文＋ルーティング表＋
  対象スキル本文を結合して設定する。MVP 7スキルを1体の GPT にまとめ、
  Phase 2 以降の横断スキル群は別 GPT として分割する。
- **ナレッジアップロード**: `docs/` の8ドメインディレクトリをドメインごとに
  1ファイルへ結合し、用語表・索引・技法カタログを加えて合計 **11〜12
  ファイル**とする（アップロード上限20に対し余裕を残す）。
- **能力の縮退**: `shell` を要求する手順は「以下のコマンドを実行し、結果を
  このチャットに貼り付けてください」という助言のみに縮退する。`file_write`
  も同様に、成果物をチャット出力として提示し保存を案内する形に縮退する。

## 結合ファイルの扱い

8結合ファイルおよび用語表・索引・カタログの結合版は**生成物であり手編集を
禁止**する。編集は必ず `docs/` の元ファイルに対して行い、結合ファイルは
ビルドスクリプトで再生成する（ビルドスクリプト自体は Phase 3 で実装）。

## 詳細

- システムプロンプト構成・ナレッジ結合方針・能力の縮退・生成物としての扱いの
  完全な記述:
  [`docs/agent-ecosystem/portability-design.md` §5](../../docs/agent-ecosystem/portability-design.md#5-chatgptgpts-への変換レシピ)
- 能力→プラットフォーム対応表:
  [`docs/agent-ecosystem/portability-design.md` §2](../../docs/agent-ecosystem/portability-design.md#2-能力プラットフォーム対応表)
- 静的ナレッジ分類（`docs/` = 正典の散文）の詳細:
  [`docs/agent-ecosystem/knowledge-management-design.md`](../../docs/agent-ecosystem/knowledge-management-design.md)
