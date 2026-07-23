# Claude Code / Cowork 向け導入

品質スキル・エコシステムを Claude Code（および同じ SKILL.md 形式を消費する
Cowork）へ導入する手順と検証観点の要約。詳細は必ずリンク先を参照すること。

## 導入方法

正典である `skills/` 配下の SKILL.md 群を複製せず、リポジトリ直下に
シンボリックリンクを張ることで Claude Code の発見規約に適合させる。

```
.claude/skills -> ../skills
```

これは既存の `CLAUDE.md -> AGENTS.md` シンボリックリンクと同一のアダプター
思想であり、`skills/` を単一のソースのまま複数プラットフォームへ展開する
という本エコシステムの原則に従う。

Cowork は Claude Code と同じ SKILL.md 形式（frontmatter の `name` /
`description` による発見）を消費するため、上記のシンボリックリンク配置のみで
追加の変換作業なしに利用できる。

## 単体実行の検証観点

スキルを単体で起動した際、疎結合設計が実際に機能しているかを次の4観点で
確認する。

- 証跡ゼロでの起動時の振る舞い
- 証跡過多での起動時の判定結果
- カウンターメトリクス欠落の検出
- 出力エンベロープの再取込可能性

各観点の具体的な確認手順・合格基準は本 README では再掲しない。

## 詳細

- 導入手順・シンボリックリンクの根拠・単体実行の検証観点（4項目）の完全な記述:
  [`docs/agent-ecosystem/portability-design.md` §3](../../docs/agent-ecosystem/portability-design.md)
- スキル一覧・ロードマップ:
  [`docs/agent-ecosystem/skill-ecosystem-design-plan.md`](../../docs/agent-ecosystem/skill-ecosystem-design-plan.md)
