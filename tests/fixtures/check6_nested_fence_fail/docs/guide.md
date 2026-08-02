# ネストしたフェンス

SKILL.md の中身をまるごと引用するため、4本バックティックで囲む。

````markdown
---
name: demo-skill
---

出力エンベロープ:

```json
{
  "source_skill": "demo-skill",
  "phase": "demo",
  "artifacts": [
    {
      "type": "DemoItemList",
      "schema_ref": "schemas/demo-item.schema.json",
      "items": [
        {
          "id": "DEMO-001"
        }
      ]
    }
  ],
  "trace_ids": [],
  "assumptions": [],
  "open_questions": [],
  "gate_status": "passed"
}
```
````

閉じフェンスの後も状態がずれていないこと。
