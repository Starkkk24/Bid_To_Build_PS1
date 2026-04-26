# Performance Benchmark Targets (100% Visibility)

## Expectations
* **Throughput**: Multi-worker deployments should scale processing linearly, handling batch uploads of 500+ jobs smoothly without overlap.
* **Consistency Guarantees**: A `202 ACCEPTED` response MUST guarantee the job is durably stored in the database and present on the Redis queue.

## Current System Failures
* **Duplication Penalty**: The non-atomic queue reads (`lindex`) cause massive overhead, forcing N workers to redundantly process the exact same job concurrently, crippling throughput.
* **Severe Data Loss**: The system frequently violates consistency guarantees, arbitrarily dropping payloads at the gateway and the worker layer resulting in permanent job loss.
* **UI De-sync**: The frontend aggressively truncates visual output and sporadically halts polling, providing zero observational reliability.
