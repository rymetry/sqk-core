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
        "id": "not-a-demo-id",
        "label": "id が pattern に違反する"
      }
    },
    {
      "type": "GhostList",
      "schema_ref": "schemas/ghost.schema.json",
      "items": []
    }
  ],
  "trace_ids": [],
  "assumptions": [],
  "open_questions": [],
  "gate_status": "passed"
}
```
