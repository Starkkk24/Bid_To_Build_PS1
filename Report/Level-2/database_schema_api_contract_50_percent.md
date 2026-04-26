# Database Schema & API Contract (50% Visibility)

## Partial Database Schema

* `jobs` table tracks standard string metadata and statuses.

## API Endpoints

### `POST /api/batch`
* Accepts JSON arrays containing user requests.
* Enqueues data to Redis and returns success.

### `GET /api/status`
* Returns current queue backlog and completed jobs list.
