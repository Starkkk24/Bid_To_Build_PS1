# Distributed System Bug Report (Level 2) - Symptom Analysis

## 1. Duplicate Jobs Processing
* **Symptom:** The system frequently processes the exact same job multiple times, leading to massive inefficiencies and redundant operations under heavy load.

## 2. Missing/Lost Jobs
* **Symptom:** Users report that certain submitted jobs completely disappear. The dashboard says they are "Queued," but they never finish and no logs indicate they were processed.

## 3. Stuck Jobs (Stale State)
* **Symptom:** Many jobs get permanently stuck in "Queued" or "Processing" states. They never transition to "Printed" even after significant time has passed.

## 4. Unreliable Batch Submissions
* **Symptom:** When submitting a large batch of ID cards, the API returns a success message confirming all were queued. However, a portion of those jobs never actually enter the system at all.

## 5. Inconsistent User Interface
* **Symptom:** The top-level metrics (e.g., Total Jobs: 50) do not match the list view, which only ever displays a handful of jobs. Furthermore, the UI frequently freezes or lags behind the actual system state.

## 6. Jumbled User Data
* **Symptom:** Data appears visually swapped. Names show up in the department column, and departments show up in the name column. It is unclear if this is a display issue or if the data itself is corrupted in transit.
