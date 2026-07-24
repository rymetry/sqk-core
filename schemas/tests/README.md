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
