# Database Schema

**Provider:** MongoDB Atlas (M0 Free)  
**Database:** `trust_split`

## Collection: `sessions`

```json
{
  "_id": "ObjectId",
  "name": "Cầu lông 19/04",
  "cost_items": [
    { "name": "Sân", "total": 216000 },
    { "name": "Cầu", "total": 28000 }
  ],
  "members": [
    {
      "name": "Loan",
      "amount": 32000,
      "confirmed": false,
      "confirmed_at": null
    },
    {
      "name": "Diệu",
      "amount": 62000,
      "confirmed": true,
      "confirmed_at": "2026-04-25T10:00:00Z"
    }
  ],
  "created_at": "2026-04-25T09:00:00Z"
}
```

## API → DB mapping

| API | MongoDB operation |
|-----|-------------------|
| `POST /api/sessions` | `insert_one` vào `sessions` |
| `GET /api/sessions/:id` | `find_one` theo `_id` |
| `POST /api/sessions/:id/confirm` | `update_one` members array, set `confirmed=true` |
