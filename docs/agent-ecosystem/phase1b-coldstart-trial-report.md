> **v2 status**: final report — Phase 1b コールドスタートトライアルの完了報告（記録）。

# Phase 1b コールドスタート検証 結果レポート

## 位置づけ

本書は [roadmap-status.md「完了の意味と検証の限界」](./roadmap-status.md) および
[phase1-integration-trial-report.md「未検証事項」](./phase1-integration-trial-report.md#未検証事項)
が「マージ後の実運用またはコールドスタート専用の追加試行で埋める」とした
**コールドスタート系分岐の追加試行**の実行結果である。T12（統合試行）は上流成果物ありの
ハッピーパス1本であり、各スキルの「上流成果物なし時の振る舞い」は一度も発火していなかった。
本試行はその未発火分岐を**狙い撃ちで発火**させ、成果物のスキーマ妥当性まで機械検証した。

## 試行の設定

- **題材**: 「パスワードリセット機能」（T12 の決済API とは別ドメイン。上流成果物を一切与えない）。
- **実行日**: 2026-07-07
- **実行形態**: 単一エージェント（本セッション）による、各スキルの SKILL.md「上流成果物なし時の
  振る舞い」節に忠実に従ったロールプレイ試行。T12 と同じく実 Claude Code セッションでの
  `description` 自動発火・対話的なユーザー応答は発生していない（「未検証事項」節参照）。
- **検証方法**: 各分岐が生成する成果物を JSON で構築し、`schemas/*.schema.json`（JSON Schema
  draft 2020-12）に対し Python `jsonschema`（`Draft202012Validator`）で検証。**SKILL.md の文言に
  忠実な版**と**スキーマ準拠版**を対にして構築し、どちらが通るかを機械確認した。
- **成果物出力先**: 本リポジトリ外のスクラッチディレクトリ。本リポジトリには本レポートのみコミットする。

## 発火させた分岐と結果サマリ

| 対象スキル | 発火させたコールドスタート分岐 | 発火 | 成果物のスキーマ検証 |
|---|---|---|---|
| quality-orchestrator | 曖昧依頼「品質をよくしたい」→ 明確化質問1回 → 無回答 → フォールバック（最上流フェーズへ） | ✅ | RoutingDecision エンベロープ valid（`clarification_asked`/`fallback_applied` を content に記録） |
| risk-analysis | 上流（欠陥履歴・変更差分）なし → 3件質問 → 無回答 → 業界一般パターンから仮説リスク提示 | ✅ | **文言どおり版（item に `assumption:true` 付与）は INVALID**／エンベロープ退避版は valid（→改善点 CS-1） |
| test-requirement-analysis | 上流（RiskRegister）なし → 3件質問 → 無回答 → DTC の `risk_refs` に仮識別子 | ✅ | detailed-test-condition valid（`status:"provisional"`・`risk_refs:["RISK-assume-001"]`） |
| test-architecture-design | 上流（DTC）なし → 3件質問 → 無回答 → 簡易 TAE をインライン合成（1グループ） | ✅ | test-architecture-element valid（数値id 使用時）／エンベロープ valid |
| test-design-implementation | 上流（TAE）なし → 3件質問 → 無回答 → 簡易 TAE インライン合成 → COV → TC → 保証ステートメント | ✅ | **SKILL 明示の id `TAE-inline-001` は INVALID**／COV・TC・assurance は valid（→改善点 CS-2） |

機械検証は全13ケースを実行し、**期待（valid/invalid の別）と実結果が全件一致**した
（不一致 0 件）。うち意図的に「文言どおり版は invalid になる」ことを期待した2ケース
（CS-1・CS-2）が、そのとおり invalid となって欠陥を確定させた。

## 発見された改善点

いずれも本試行で新規に判明したものであり、ハッピーパスの T12 では構造上到達不能だった。

### CS-1【要修正・横断】`assumption: true` の「付与」先が item スキーマと衝突する

- **事象**: risk-analysis / test-requirement-analysis / test-architecture-design の各コールドスタート
  手順は、仮説として提示した成果物に「`assumption: true` を**付与**し」と規定する
  （[risk-analysis/SKILL.md L119](../../skills/risk-analysis/SKILL.md)、
  [test-requirement-analysis/SKILL.md L158](../../skills/test-requirement-analysis/SKILL.md)、
  [test-architecture-design/SKILL.md L140](../../skills/test-architecture-design/SKILL.md)）。
  しかし `risk-item` / `detailed-test-condition` / `test-architecture-element` の各スキーマは
  `additionalProperties: false` かつ `assumption` プロパティを持たない。
- **確認結果**: `risk-item` に `assumption: true` を付与した版は
  `Additional properties are not allowed ('assumption' was unexpected)` で **INVALID**。
  同じリスク項目から `assumption` を外し、前提をエンベロープ必須配列 `assumptions[]` に退避した版は
  valid。**文言どおりに実行するとスキーマ検証に落ちる**。
- **非対称性の記録**: 例外は保証ステートメントで、`assurance-statement` は本体に nested
  `assumptions[]` を持つため、test-design-implementation のコールドスタート前提は保証
  ステートメント内に正しく退避できる（item レベルで前提を保持できるのはこの1スキーマのみ）。
- **正典との照合（元プラン方針）**: 設計プラン §4 は**一貫してエンベロープ側での記録**を意図していた。
  具体 JSON 例（[skill-ecosystem-design-plan.md:327](./skill-ecosystem-design-plan.md#L327)）は
  `"assumptions": [{ "field": "risk_level", "value": "unknown", "reason": "risk-analysis 未実行のため暫定" }]`
  と**エンベロープ `assumptions[]` に `{field, value, reason}` オブジェクト**で持つ形を示し、
  同 §4 本文（[:388](./skill-ecosystem-design-plan.md#L388)）も「…`assumption: true` として**エンベロープに
  記録する**」、根拠（[:337](./skill-ecosystem-design-plan.md#L337)）も「`assumptions`/`open_questions` は
  …上流成果物なし状態を後から検出・補完可能にするための**必須フィールド**」と述べる。
  **スキーマはこのプラン方針を正しく実装しており、逸脱したのは SKILL.md 文言側**（「エンベロープに記録」を
  「item に付与」と言い換えた）。
- **推奨対応（改訂 PR・プラン準拠）**: 3スキルの「`assumption: true` を付与」を、
  **「前提はエンベロープの `assumptions[]`（保証ステートメントは nested `assumptions[]`）に、可能なら
  プラン §4 例に倣い `{field, value, reason}` 形式で記録する。個別 item には `assumption` フィールドを
  追加しない」** と改める（スキーマ改変ゼロ）。item スキーマへ任意 `assumption`（boolean）を足す代替案は、
  元プランの「暫定性はエンベロープで表す」方針に反し8スキーマ横断改変になるため**非採用**。

### CS-2【要修正】インライン合成 TAE の id 形式 `TAE-inline-001` がスキーマ pattern に不適合

- **事象**: test-design-implementation のコールドスタート手順3は「合成した TAE の `id` は
  **`TAE-inline-001` のように**区別可能な形にする」と**明示**する
  （[test-design-implementation/SKILL.md L154](../../skills/test-design-implementation/SKILL.md)）。
  しかし `test-architecture-element.schema.json` の `id` パターンは `^TAE-[0-9]+$`
  （`TAE-` の後は数字のみ）。
- **確認結果**: `TAE-inline-001` は `'TAE-inline-001' does not match '^TAE-[0-9]+$'` で **INVALID**。
  数値のみの id（例 `TAE-901`）に変えると valid。**最も強調された未検証分岐（簡易 TAE インライン
  合成）を SKILL 文言どおり実行すると、生成 TAE がスキーマ検証に落ちる**。T12 が使った
  `TAE-001` は pattern に適合していたため、この衝突はハッピーパスでは露見しなかった。
- **波及範囲の限定**: id パターン制約を持つのは TAE 自身の `id` のみ。COV の
  `architecture_element_id` や TC の参照は自由文字列のため、`TAE-inline-001` を**参照**しても
  それ自体は valid（TAE の `id` フィールドだけが落ちる）。
- **正典との照合（元プラン方針）**: TAE の id 体系はデータ契約 §6.1 ID体系表・§6.3 JSON例
  （[test-process-research-summary-test-design.md:686](../test-techniques/test-process-research-summary-test-design.md#L686)、
  [:715](../test-techniques/test-process-research-summary-test-design.md#L715)）で**一貫して `TAE-001`
  （数値のみ）**。スキーマ `^TAE-[0-9]+$` はこれを忠実に実装している。**`TAE-inline-001` はプランにも
  データ契約にも存在せず、[test-design-implementation/SKILL.md:154](../../skills/test-design-implementation/SKILL.md)
  で SKILL 執筆時に初めて持ち込まれた語**であり、確立済みの id 規約からの逸脱にあたる。
- **推奨対応（改訂 PR・プラン準拠）**: 案(a)を採る。SKILL の id 例を pattern 適合の数値 id に改める
  （例: インライン合成専用に `TAE-900` 番台を予約し `TAE-901` 等を用いると規定）。手順3が意図した
  「区別可能性」は、CS-1 と同じく**エンベロープ `assumptions[]` に「当該 TAE はインライン合成の暫定要素」と
  記録する**ことで担保する（id 本文には持たせない）。スキーマ pattern を緩める案(b)は元の ID 体系規約に
  逆行するため**非採用**。

### CS-3【軽微・明文化不足】truly-empty 時のフォールバック着地先が一意に定まらない

- **事象**: orchestrator 手順4のフォールバックは「**入力が揃っている最上流フェーズへ**ルーティング」
  と規定する（[quality-orchestrator/SKILL.md L93-97](../../skills/quality-orchestrator/SKILL.md)）。
  相談文が「品質をよくしたい」のみで**どのスキルの最小入力も満たさない** truly-empty ケースでは、
  「入力が揃っているフェーズ」が存在せず、着地先が test-requirement-analysis（フェーズ順で①要求が
  最上流）か risk-analysis かを一意に決められない。
- **本試行の扱い**: フェーズ順の最上流として test-requirement-analysis へルーティングし、
  その先で TRA 自身のコールドスタート3件質問に委ねる、という解釈で出力を成立させた
  （`fallback_applied: true`）。この解釈で運用は回るが、SKILL 本文に truly-empty 時の
  具体的着地先の規定がない。
- **正典との照合（元プラン方針）**: このフォールバック規定自体は設計プラン §4
  （[skill-ecosystem-design-plan.md:306-307](./skill-ecosystem-design-plan.md#L306)）の
  「曖昧な場合は明確化質問を1回まで…それでも定まらない場合は入力が揃っている最上流フェーズへ」＋根拠
  「**情報が少ないときほど上流から手当てする**」を SKILL が忠実にコピーしたもの。**truly-empty 時の着地先が
  未規定なのは SKILL の逸脱ではなくプラン由来のギャップ**であり、設計思想（上流へ倒す）から意図は明白。
- **推奨対応（プラン準拠の明文化）**: 手順4に「どのスキルの最小入力も満たさない場合は、フェーズ順最上流の
  test-requirement-analysis へルーティングし、以降は当該スキルのコールドスタート分岐に委ねる」の
  1文を追記すれば曖昧さは消える（方針変更ではなくプラン思想の明文化。軽微）。

### 正典照合のまとめ：CS-1・CS-2 は同一の逸脱

CS-1（`assumption:true` フィールド）と CS-2（`TAE-inline-` id 接頭辞）は、どちらも
**SKILL 執筆者が「暫定であること」を item 側の即席マーカーで表そうとした**同根の逸脱である。
元プランは最初から、暫定性を**エンベロープ `assumptions[]` だけで表現し、item 成果物はスキーマ準拠に
保つ**設計だった（プラン §4:327 の JSON 例・:388・:337、データ契約 §6.1/§6.3 の id 体系）。したがって
両件を貫く単一の修正原則は次のとおりで、**改訂 PR の「文言修正で寄せる（スキーマ据え置き）」方針が
正典準拠であること**が確定する（先送りしていた「文言 vs スキーマ緩和」の二択は、正典側が既に決めていた）。

> **暫定性・前提はエンベロープ `assumptions[]`（プラン §4 例に倣い `{field, value, reason}` 形式）に
> 集約する。個別 item はスキーマ準拠のまま保ち、`assumption` フィールドも `-inline-` id も足さない。**

## 確認できたこと（机上レビューではなく発火＋機械検証で確認）

1. **3件質問→無回答→必ず出力**のパスは、risk-analysis / TRA / TAD / TDD-TI の4スキルすべてで
   迷いなく分岐に到達でき、各スキルの規定（業界一般パターン／仮識別子 `RISK-assume-001`／
   インライン合成）で「無出力にしない」を満たせた。
2. **アンチパターン（TAE を飛ばして直接テストケース生成）を踏まなかった**。TDD-TI のコールドスタートで
   簡易 TAE（インライン）→ COV → TC → 保証ステートメントの順に生成でき、id 問題（CS-2）を除けば
   チェーン構造は妥当。保証ステートメントの `technique` は複数技法配列 `["BB-02","BB-01"]` で valid。
3. **オーケストレーターの明確化質問1回制約**（他スキルの3件より厳格）に沿って、質問を1点に絞り
   2回目を行わずフォールバックへ進む流れを実行できた。`clarification_asked`/`fallback_applied` は
   RoutingDecision の content に記録でき、handoff-envelope として valid。
4. **前提の退避チャネルは機能する**。CS-1 の準拠版が示すとおり、エンベロープ必須配列 `assumptions[]`
   に前提を集約すれば、コールドスタート成果物は全スキーマで valid になる。仕組み自体は健全で、
   問題は SKILL 文言が item への「付与」を指示している点に限局する。

## 未検証事項（本試行でも埋まらない。実 Claude Code セッションが必要）

以下は T12 から引き続き未検証であり、ロールプレイでは原理的に確認できない。**実運用での確認は
利用者側の実インタラクティブセッションに残る**。

- 実 Claude Code セッションでの各スキルの `description` による**自動発火の精度**（本試行もスキルを
  名指しして SKILL.md 手順を人手で追跡したものであり、自然言語相談文からの自動トリガーは未検証）。
- 明確化質問（1回まで／3件まで）を実際に利用者へ提示し、**回答を待って処理を継続する対話フロー**の
  実挙動（本試行は一貫して「回答が得られない場合」の代替パスを実行したもので、質問→応答待ち→再開の
  UX は未検証）。
- 複数スキルが個別サブエージェント・別プロセスとして起動された場合のハンドオフエンベロープ受け渡しの
  実装（本試行は単一エージェント内でのファイルベース受け渡しの模擬）。

## 受入基準チェック

- [x] 各スキルのコールドスタート分岐（orchestrator 明確化1回＋フォールバック／risk・TRA・TAD・TDD-TI の
      3件質問＋無回答パス／TAD・TDD-TI の簡易 TAE インライン合成）を1回以上発火させた
- [x] 発火時に生成される成果物をスキーマ検証し、valid/invalid の別が期待と全件一致（13/13）
- [x] コールドスタート固有の欠陥を検出（CS-1: `assumption` 付与とスキーマ衝突／CS-2: インライン TAE の
      id 形式不適合）し、それぞれ修正方向を機械確認した
- [x] 本レポートがコミットされている

## Phase 2 改訂 PR への申し送り（本試行の産物）

[phase1-integration-trial-report.md の既存3件](./phase1-integration-trial-report.md#発見された改善点)
（RoutingDecision 形状／thickness 語彙の揺れ／assurance-statement の technique ユニオン型）に加え、
本試行の **CS-1・CS-2（要修正）** と **CS-3（軽微）** を同一の改訂 PR で扱う。**CS-1・CS-2 の方針は
正典照合により確定済み（上記「正典照合のまとめ」）＝ SKILL 文言・例を修正し、スキーマは据え置く**。
実装者は二択を検討する必要はなく、上記の単一原則に沿って SKILL.md 側を直せばよい。
