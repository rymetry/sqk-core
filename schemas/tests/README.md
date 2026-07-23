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

現在は `assurance-statement.schema.json` のユニオン型により `allowUnionTypes` の strict 警告が1件発生する。これは既知のベースラインであり、T12-3 で解消予定である。警告を失敗として扱う場合は次を実行する。

```bash
AJV_STRICT_WARNINGS=fail bash scripts/validate-schemas.sh
```

invalid fixture のファイル名には、`id-pattern-violation.json` のように違反内容を表す名前を付ける。
