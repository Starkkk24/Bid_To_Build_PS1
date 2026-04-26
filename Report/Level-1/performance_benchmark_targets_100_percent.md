# Performance Benchmark Targets (100% Visibility)

## Expectations
* **Response Time**: API requests for `/api/upload` should ideally process within 1-2 seconds reliably.
* **Handling Duplicates**: The system should gracefully reject or debounce concurrent submissions for the exact same payload.
* **Consistency**: Database writes and file writes must be highly consistent; an image path in the DB MUST guarantee a file exists on disk.

## Current Issues
* **Delays**: Processing logic contains a randomized `time.sleep()` causing delays varying up to 4.0 seconds, severely impacting throughput predictability.
* **Inconsistent Results**: File I/O drops cause severe database-to-filesystem inconsistencies. Early-exit bugs cause database records to orphan in a "Pending" state, ruining queue metrics.
