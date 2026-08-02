# demo-skill

出力エンベロープの例:

```json
{
  "source_skill": "demo-skill",
  "phase": "demo",
  "artifacts": [
    {
      "type": "DemoItemList",
      "schema_ref": "schemas/demo-item.schema.json",
      "content": {
        "id": "DEMO-002",
        "label": "content 形状の内包 payload"
      }
    }
  ],
  "trace_ids": ["DEMO-002"],
  "assumptions": [],
  "open_questions": [],
  "gate_status": "passed"
}
```

エンベロープではない JSON は対象外:

```json
{
  "id": "DEMO-003"
}
```
