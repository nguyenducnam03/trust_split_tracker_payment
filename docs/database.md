# Database Schema

**Provider:** MongoDB Atlas (M0 Free)  
**Database:** `trust_split`

## Collection: `users`

```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "password_hash": "bcrypt hash",
  "name": "Nguyen Van A",
  "created_at": "2026-04-25T09:00:00Z"
}
```

## Collection: `sessions`

```json
{
  "_id": "ObjectId",
  "owner_id": "ObjectId (ref users)",
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
| `POST /api/auth/register` | `insert_one` vào `users` |
| `POST /api/auth/login` | `find_one` theo `email`, verify password |
| `POST /api/auth/refresh` | verify refresh token → trả access token mới |
| `POST /api/sessions` | `insert_one` vào `sessions` (cần auth) |
| `GET /api/sessions/:id` | `find_one` theo `_id` |
| `POST /api/sessions/:id/confirm` | `update_one` members array, set `confirmed=true` |
