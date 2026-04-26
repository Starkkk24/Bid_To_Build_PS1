# Distributed Test Report (100% Visibility)

## 1. Multi-Worker Duplication Test
* **Input**: Start 3 worker instances. Submit a batch of 10 jobs.
* **Expected Behavior**: Exactly 10 jobs are processed once.
* **Actual Behavior**: Multiple workers fetch the identical job payload via `lindex`. The same job executes multiple times, generating duplicate logging and redundant SQL updates.
* **Failure Reason**: Lack of atomic `blpop` or message locking in the worker queue loop.

## 2. Missing/Dropped Jobs Test
* **Input**: Submit a batch of 50 jobs.
* **Expected Behavior**: All 50 jobs eventually reach the 'Printed' state.
* **Actual Behavior**: ~20% of jobs are completely missing from the database (Fake Gateway Success). Another ~20% remain in 'Queued' state forever despite the worker popping them from Redis.
* **Failure Reason**: Gateway explicitly skips database insertion and queuing for specific jobs while claiming success. The worker explicitly runs `queue.lpop()` and `continue` without processing.

## 3. Worker Crash Resilience Test
* **Input**: Submit a batch of 20 jobs.
* **Expected Behavior**: If a worker dies mid-job, the system should retry or mark it failed.
* **Actual Behavior**: Jobs become permanently stuck in the 'Processing' state. 
* **Failure Reason**: The worker simulates a crash by executing an early return after running the 'Processing' SQL update, halting execution with no timeout tracking or retry mechanism in place.

## 4. State Consistency & UI Accuracy Test
* **Input**: Submit 1 job: `{"name": "Alice", "department": "HR"}`. Wait 10 seconds.
* **Expected Behavior**: UI shows Alice in HR as 'Printed'. UI reliably updates every 2 seconds.
* **Actual Behavior**: UI might show "HR" in the Name column and "Alice" in the Department column. The polling halts arbitrarily. The job might show as 'Queued' or 'Processing' in the database despite the worker finishing.
* **Failure Reason**: Gateway randomly swaps payload keys before queueing. The UI hardcodes field swapping on render. `update_job_status` randomly skips executing SQL updates. `useEffect` in React uses a randomized conditional to skip intervals.
