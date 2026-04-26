# Performance Benchmark Targets (50% Visibility)

## Expectations
* Adding more workers to the distributed pool should increase processing speed linearly.
* The system should reliably ingest large JSON batches without data loss.
* The UI dashboard must reflect real-time infrastructure state.

## Current System Failures
* Adding workers seemingly slows down the system or causes erratic behavior.
* Severe data loss is evident, with jobs routinely disappearing from the queue.
* The UI is completely unreliable for monitoring the actual state of the deployment.
