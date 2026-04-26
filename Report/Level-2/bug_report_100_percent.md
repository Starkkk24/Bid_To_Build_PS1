# Distributed System Bug Report (Level 2) - Complete Analysis

## 1. Duplicate Job Processing (Race Condition)
* **Severity:** High
* **Component:** Worker Service
* **Root Cause:** The worker utilizes `lindex` to peek at the queue rather than an atomic pop operation (`blpop`). It processes the job while it remains on the queue and only pops it afterwards. In a multi-worker environment, this creates a race condition where multiple concurrent workers fetch, process, and pop the exact same job.

## 2. Lost Queue Jobs (Queue Drop)
* **Severity:** High
* **Component:** Worker Service
* **Root Cause:** The worker has a routine that intermittently pops jobs off the Redis queue and immediately calls `continue`, thereby dropping the message entirely without ever invoking the processing logic or updating the database.

## 3. Stale Database Status
* **Severity:** Medium
* **Component:** Worker Service
* **Root Cause:** When attempting to transition a job's state (e.g., to 'Processing' or 'Printed'), the `update_job_status` function randomly executes an early return. This skips the SQL `UPDATE` statement entirely, leaving the record stranded in its old state indefinitely.

## 4. Worker Process Crashing
* **Severity:** High
* **Component:** Worker Service
* **Root Cause:** After explicitly marking a job as 'Processing' in the database, the worker simulates a critical crash by returning early. Lacking a dead-letter queue, timeout monitor, or retry mechanism, the job remains orphaned in the 'Processing' state forever.

## 5. Corrupted Job Payload
* **Severity:** Medium
* **Component:** Gateway API
* **Root Cause:** Prior to serializing and pushing a job to the Redis queue, the Gateway API swaps the `name` and `department` fields. While the database stores the correct information, the worker receives and logs corrupted data, simulating a contract mismatch.

## 6. Fake Gateway Success
* **Severity:** Critical
* **Component:** Gateway API
* **Root Cause:** The batch submission endpoint intermittently bypasses the database insertion and Redis queue pushing steps for specific jobs. However, it still adds these dropped jobs to the JSON response array, deceiving the client into believing the jobs were successfully queued.

## 7. Stale Frontend Polling
* **Severity:** Low
* **Component:** Frontend Dashboard
* **Root Cause:** The `useEffect` polling interval contains a randomized conditional statement. It randomly skips the API fetch cycle, causing the UI to inconsistently refresh and display outdated data compared to the actual database state.

## 8. Partial Dashboard Rendering
* **Severity:** Medium
* **Component:** Frontend Dashboard
* **Root Cause:** The job list renderer artificially truncates the state array using `.slice(0, 5)`. While the aggregate metrics display the true total number of jobs, the list view hides the vast majority of the system's state.

## 9. Incorrect UI Field Mapping
* **Severity:** Low
* **Component:** Frontend Dashboard
* **Root Cause:** The React component rendering the job rows explicitly swaps the values mapped to the `name` and `department` columns, adding a secondary layer of data presentation corruption independent of the backend.
