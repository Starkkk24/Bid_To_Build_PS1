# Distributed Architecture Flow (50% Visibility)

## Core Components
1. **Frontend Dashboard**
2. **Gateway Service**
3. **Message Broker (Queue)**
4. **Worker Pool**
5. **Database**

## Simplified Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Queue
    participant Workers
    participant Database

    Client->>Gateway: Submit Batch
    Gateway->>Database: Save Records
    Gateway->>Queue: Enqueue Jobs
    Gateway-->>Client: Return Success
    
    Workers->>Queue: Fetch Job
    Workers->>Workers: Process Job
    Workers->>Database: Update Status
```
