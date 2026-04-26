# Database Schema & API Contract (100% Visibility)

## Database Schema (SQLite)

### Table: `jobs`
| Column Name  | Data Type | Constraints               |
|--------------|-----------|---------------------------|
| `id`         | INTEGER   | PRIMARY KEY AUTOINCREMENT |
| `job_id`     | TEXT      | UNIQUE                    |
| `name`       | TEXT      | None                      |
| `department` | TEXT      | None                      |
| `status`     | TEXT      | None                      |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

## API Endpoints

### 1. `POST /api/batch`
**Content-Type:** `application/json`
**Payload:** Array of Objects
```json
[
  { "name": "Stark", "department": "Engineering" }
]
```

**Worker Redis Payload (MISMATCH DUE TO BUG):**
```json
{
  "job_id": "uuid",
  "name": "Engineering",
  "department": "Stark"
}
```

**Response (Success):** `202 ACCEPTED`
```json
{
  "message": "Successfully queued X jobs.",
  "jobs": [
    {
      "job_id": "uuid-string",
      "name": "Stark",
      "department": "Engineering"
    }
  ]
}
```

### 2. `GET /api/status`
**Response:** `200 OK`
```json
[
  {
    "job_id": "uuid-string",
    "name": "Stark",
    "department": "Engineering",
    "status": "Queued",
    "created_at": "timestamp"
  }
]
```
