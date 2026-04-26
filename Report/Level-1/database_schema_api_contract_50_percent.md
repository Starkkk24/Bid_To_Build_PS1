# Database Schema & API Contract (50% Visibility)

## Partial Database Schema

* `id_cards` table contains fields for job tracking, user details, and status.

## API Endpoints

### `POST /api/upload`
* Accepts form data containing user details and an image.
* Returns success message on completion.

### `GET /api/status`
* Returns a list of all processed ID cards and their current state.
