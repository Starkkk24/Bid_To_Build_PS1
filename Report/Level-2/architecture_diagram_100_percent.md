# Distributed Architecture Flow (100% Visibility)

## Core Distributed Components
1. **Frontend Dashboard**: React SPA with metrics and batch submission
2. **Gateway Service**: Flask API handling batch ingestion
3. **Message Broker**: Redis Queue
4. **Worker Service(s)**: Python workers for distributed processing
5. **Database**: Shared SQLite DB

## Request Lifecycle & Bug Intersections

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Gateway
    participant Redis
    participant SQLite
    participant Worker

    User->>Frontend: Submits Batch JSON
    Frontend->>Gateway: POST /api/batch
    
    Note over Gateway: BUG: Randomly marks job successful but drops it entirely
    Gateway->>SQLite: INSERT (status: 'Queued')
    Note over Gateway, Redis: BUG: Randomly swaps 'name' and 'department' payload fields
    Gateway->>Redis: rpush(job_data)
    
    Gateway-->>Frontend: 202 ACCEPTED

    Note over Worker, Redis: BUG: Worker uses lindex() instead of blpop().<br/>Causes race condition on multi-worker read.
    Worker->>Redis: read queue
    
    Note over Worker: BUG: Worker randomly drops job entirely after reading
    
    Worker->>SQLite: UPDATE status='Processing'
    Note over Worker: BUG: Randomly skips SQL updates (Stale State)
    
    Note over Worker: BUG: Simulates crash and halts mid-execution
    
    Worker->>Worker: process_job()
    Worker->>SQLite: UPDATE status='Printed'
    
    Note over Worker, Redis: BUG: Pops job AFTER execution, leaving window open for duplicate processing.
    Worker->>Redis: lpop()

    Note over Frontend: BUG: Randomly skips polling interval.
    Frontend->>Gateway: GET /api/status
    Gateway->>SQLite: SELECT *
    Gateway-->>Frontend: Returns Jobs
    
    Note over User, Frontend: BUG: UI hardcodes slice(0,5), hiding most jobs.
    Note over User, Frontend: BUG: UI maps 'name' and 'department' to incorrect columns.
```
