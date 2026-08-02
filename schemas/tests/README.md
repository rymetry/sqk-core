# Schema 検証 fixture

`schemas/tests/fixtures/<name>/` に、`schemas/<name>.schema.json` と対応する fixture を置く。

```text
fixtures/
└── <name>/
    ├── valid/
    │   └── *.json
    └── invalid/
        └── *.json
```

リポジトリルートから次を実行すると、全 schema の strict compile と valid / invalid fixture の往復検証を行う。

```bash
bash scripts/validate-schemas.sh
```

validator は `npx --yes ajv-cli@5.0.0` で pinned invoke する。このリポジトリを Node プロジェクト化せず、`package.json`、lockfile、`node_modules` は置かない。

strict 警告の既知部分文字列は `schemas/tests/strict-warnings-baseline.txt` で管理する。コメント行と空行は無視され、収集した警告行がいずれかの部分文字列に一致すれば既知として扱う。baseline に一致しない新規警告、または今回の実行でどの警告にも一致しない stale baseline entry がある場合、通常実行でも失敗する。

既知警告を追加するときは、警告を一意に識別できる固定部分文字列を1行で追加する。警告を解消したときは対応行を削除する。現在の既知警告は0件で、baseline に有効なエントリはない。

baseline 一致を含む警告すべてを失敗として扱う場合は次を実行する。

```bash
AJV_STRICT_WARNINGS=fail bash scripts/validate-schemas.sh
```

invalid fixture のファイル名には、`id-pattern-violation.json` のように違反内容を表す名前を付ける。

## エンベロープ内包 payload の検証

`handoff-envelope` は2層の契約を持ち、層ごとに検証ハーネスが分かれている。

| 層 | 対象 | 担当 |
| --- | --- | --- |
| transport 構造 | `handoff-envelope.schema.json` への適合 | `scripts/validate-schemas.sh` |
| payload 契約 | `artifacts[].items[]` / `artifacts[].content` の、`artifacts[].schema_ref` が指すスキーマへの適合 | `scripts/check.py` の CHECK6（実装は `scripts/check_envelopes.py`） |

envelope schema の `artifacts[].items` は制約のない array であるため、transport 層の
検証だけでは宣言（`schema_ref`）と実体（payload）の不一致を検出できない。CHECK6 は
この継ぎ目を検証し、`fixtures/handoff-envelope/valid/*.json` に加えて Markdown 中の
json コードブロックに書かれたエンベロープ例（SKILL.md の出力例等）も対象にする。
エンベロープとみなす条件は、文字列の `source_skill` と配列の `artifacts` を持つ
JSON オブジェクトであることとする。

検査対象の拾い方は次のとおり。

- `valid/` の fixture がエンベロープ形状でない場合は、読み飛ばさずエラーにする。
- SKILL.md 全体を ` ````markdown ` で引用するブロック（portability-design.md の実装例）
  の内側にある出力例も、1段の入れ子まで追って検査する。consumer はこの引用例も契約として読む。
- Markdown のエンベロープ例は payload だけでなく `handoff-envelope.schema.json` 自体にも
  当てる。fixture は `validate-schemas.sh` が見るが、Markdown の例は CI で他に見る者がいない。

`schema_ref` の解決規則は次のとおり。

- repo-root 相対パスのみを受け付ける。絶対パス・`..`・symlink による木の外への脱出は拒否する
  （`root / 絶対パス` は root 自体を無視するため、素通りさせない）。
- 参照先が存在しない場合はエラーにする。宣言だけあって実体が無い状態を防ぐ。
- `*.schema.json` への fragment（`...schema.json#/$defs/foo`）は未対応としてエラーにする。
  fragment を捨ててルートスキーマで検証すると、宣言とは別の契約を検査してしまうため。
- `*.schema.json` 以外（散文の出典）を指す場合は、payload の構造検証は行わない。
  JSON Schema が未定義の成果物種別を許容するため。この場合も参照は解決させ、
  fragment が付いていれば見出しアンカーの実在まで確認する。

CHECK6 を `validate-schemas.sh` ではなく `check.py` に置く理由は
[D-014](../../DECISIONS.md#d-014-エンベロープ内包-payload-の検証層)に記す。
