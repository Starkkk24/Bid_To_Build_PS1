# Level 1 Architecture Diagram (100% Visibility)

## Core Components
1. **Frontend**: React SPA
2. **Backend**: Monolithic Flask API
3. **Database**: SQLite
4. **Storage**: Local File System

## Request Lifecycle & Bug Intersections

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant SQLite
    participant FileSystem

    User->>Frontend: Fills Form & Clicks Submit
    Note over User, Frontend: BUG: Button not disabled (Spamming possible)
    Frontend->>Backend: POST /api/upload (FormData)
    Note over Frontend, Backend: BUG: Name and Department keys swapped

    Backend->>FileSystem: file.save(image)
    Note over Backend, FileSystem: BUG: Randomly fails, backend ignores error

    Backend->>SQLite: INSERT (status: 'Pending')
    
    Note over Backend: BUG: Randomly exits early here, leaving DB in 'Pending'

    Backend->>SQLite: UPDATE (status: 'Printed')
    Note over Backend, SQLite: BUG: Status updated too early

    Backend->>Backend: process_print_job()
    Note over Backend: BUG: Random delay (0.5s - 4.0s)
    Note over Backend: BUG: Random crash ignored (Fake Success)

    Backend->>SQLite: UPDATE (status: 'Processing')
    Note over Backend, SQLite: BUG: Status reversed at the end

    Backend-->>Frontend: 200 OK (Processed Successfully)
    Note over Frontend: BUG: Does not refresh StatusList
```
