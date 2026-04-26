# Smart ID Card System - Level 2 (Distributed System)

This is a clean, fully functional distributed application.
It acts as the baseline for the Level 2 hackathon challenge before bugs are injected.

## Project Structure
* `docker-compose.yml`: Orchestrates Redis, Gateway, and Workers.
* `gateway/`: Flask API Gateway that handles batch uploads and pushes to Redis.
* `worker/`: Custom Python worker that polls Redis and processes jobs.
* `frontend/`: React dashboard to view live queue metrics and upload batches.
* `shared/`: Volume directory where the SQLite database is stored.

## Prerequisites
* Docker and Docker Compose
* Node.js (v18+)

## Setup Instructions

### 1. Run the Backend Services
Open a terminal and navigate to the `Level-2/` directory:
```bash
docker-compose up --build
```
This will start:
* Redis (port 6379)
* Gateway (port 5001)
* Worker (1 instance by default)

To scale workers (e.g., to 3 instances):
```bash
docker-compose up --build --scale worker=3
```

### 2. Run the Frontend Dashboard
Open a new terminal and navigate to the `Level-2/frontend/` directory:
```bash
npm install
npm run dev
```
The dashboard will be accessible at `http://localhost:5173`.

## Functional Flow
1. User pastes a JSON batch of users and clicks "Submit Batch".
2. The `gateway` inserts them into SQLite as `Queued` and pushes job payloads to Redis.
3. The `worker` containers BLPOP from Redis, picking up jobs.
4. The `worker` updates the DB to `Processing`, sleeps for 1s, and updates to `Printed`.
5. The React dashboard polls the gateway every 2 seconds to update live metrics.
