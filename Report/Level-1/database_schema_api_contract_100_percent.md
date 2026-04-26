# Database Schema & API Contract (100% Visibility)

## Database Schema (SQLite)

### Table: `id_cards`
| Column Name  | Data Type | Constraints               |
|--------------|-----------|---------------------------|
| `id`         | INTEGER   | PRIMARY KEY AUTOINCREMENT |
| `job_id`     | TEXT      | UNIQUE                    |
| `name`       | TEXT      | None                      |
| `department` | TEXT      | None                      |
| `image_path` | TEXT      | None                      |
| `status`     | TEXT      | None                      |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

## API Endpoints

### 1. `POST /api/upload`
**Content-Type:** `multipart/form-data`
**Payload:**
* `name` (string)
* `department` (string)
* `image` (file)

**Response (Success):** `200 OK`
```json
{
  "message": "ID Card processed successfully",
  "job_id": "uuid-string",
  "status": "Printed"
}
```

### 2. `GET /api/status`
**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "job_id": "uuid-string",
    "name": "Stark",
    "department": "Engineering",
    "image_path": "uploads/uuid-string_image.jpg",
    "status": "Processing"
  }
]
```
