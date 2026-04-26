# System Logs - 100% Visibility

```log
[2026-04-27 10:15:22,104] INFO in app: 127.0.0.1 - - "POST /api/upload HTTP/1.1" 200 -
[2026-04-27 10:15:22,106] WARNING in app: Database commit for job_id 8a4b-11ec-b909-0242ac120002 successful. Status: Pending.
[2026-04-27 10:15:22,108] ERROR in app: [WinError 32] The process cannot access the file because it is being used by another process: 'uploads/8a4b-11ec-b909-0242ac120002_profile.jpg'
[2026-04-27 10:15:22,110] WARNING in app: Suppressed Exception. Continuing execution.
[2026-04-27 10:15:22,112] INFO in app: Status updated to 'Printed' for job_id 8a4b-11ec-b909-0242ac120002.
[2026-04-27 10:15:22,550] ERROR in process_print_job: Exception: Simulated printer jam on job 8a4b-11ec-b909-0242ac120002
[2026-04-27 10:15:22,552] WARNING in app: Print job exception caught. Response returned as 200 OK.
[2026-04-27 10:15:35,420] INFO in app: 127.0.0.1 - - "POST /api/upload HTTP/1.1" 200 -
[2026-04-27 10:15:35,421] INFO in app: Database commit for job_id 9c3d-11ec-b909-0242ac120003 successful. Status: Pending.
[2026-04-27 10:15:35,422] INFO in app: Early exit triggered. Response sent to client before processing. Job 9c3d-11ec-b909-0242ac120003 orphaned.
[2026-04-27 10:15:40,111] INFO in app: 127.0.0.1 - - "GET /api/status HTTP/1.1" 200 -
[2026-04-27 10:16:02,999] INFO in app: 127.0.0.1 - - "POST /api/upload HTTP/1.1" 200 -
[2026-04-27 10:16:03,005] INFO in app: 127.0.0.1 - - "POST /api/upload HTTP/1.1" 200 - (DUPLICATE DETECTED IN LOGS)
```
