# System Logs - 100% Visibility

```log
[2026-04-27 10:20:15,001] INFO in gateway: 127.0.0.1 - - "POST /api/batch HTTP/1.1" 202 -
[2026-04-27 10:20:15,005] INFO in gateway: Successfully queued 4 jobs.
[2026-04-27 10:20:15,006] WARNING in gateway: Job ID 5f8b-11ec-b909 dropped intentionally. Client informed of success.
[2026-04-27 10:20:15,200] INFO in worker_1: [6c4a-11ec-b909] Picked up job for Engineering
[2026-04-27 10:20:15,201] INFO in worker_2: [6c4a-11ec-b909] Picked up job for Engineering
[2026-04-27 10:20:16,210] INFO in worker_1: [6c4a-11ec-b909] Finished job for Engineering
[2026-04-27 10:20:16,212] INFO in worker_2: [6c4a-11ec-b909] Finished job for Engineering
[2026-04-27 10:20:16,500] INFO in worker_1: Queue Drop: An item was lost from the queue.
[2026-04-27 10:20:17,100] INFO in worker_2: [7d5b-11ec-b909] Picked up job for Stark
[2026-04-27 10:20:17,105] ERROR in worker_2: [7d5b-11ec-b909] CRITICAL WORKER CRASH! Execution halted.
[2026-04-27 10:20:18,000] INFO in gateway: 127.0.0.1 - - "GET /api/status HTTP/1.1" 200 -
```
