# Bug Report (Level 1) - Complete Analysis

## 1. Status Lifecycle Reversal
* **Severity:** High
* **Category:** Business Logic
* **Affected Component:** Backend (Upload/Processing Workflow)
* **Root Cause:** The database status is updated out of order. It is marked as 'Printed' immediately after record creation, and later downgraded to 'Processing' after the print job finishes.

## 2. Unrestricted Duplicate Submissions
* **Severity:** Medium
* **Category:** Concurrency / Validation
* **Affected Component:** Frontend & Backend
* **Root Cause:** The frontend submission button does not enter a disabled state during an active request. The backend blindly accepts all incoming requests without validating uniqueness (name/department combination), leading to duplicate database records being freely created.

## 3. Silent File Storage Failure
* **Severity:** High
* **Category:** Error Handling
* **Affected Component:** Backend (File IO)
* **Root Cause:** File save operations randomly fail due to simulated I/O errors. These exceptions are caught and swallowed. The system continues execution, saving the intended file path to the database even though the file does not exist on disk, resulting in broken image references.

## 4. Partial DB Write Inconsistency
* **Severity:** Critical
* **Category:** State Management
* **Affected Component:** Backend (Upload Endpoint)
* **Root Cause:** Following the initial 'Pending' database insertion, there is a probability of the request prematurely returning a 200 OK response to the client. This orphans the record in the 'Pending' state indefinitely, as the status update and processing function are bypassed.

## 5. False Positive Success Responses
* **Severity:** High
* **Category:** Error Handling
* **Affected Component:** Backend (Print Job Processing)
* **Root Cause:** The print processing simulator randomly throws exceptions (simulating hardware jams). The calling function catches these exceptions but ignores them, returning a successful response to the client despite the job failing.

## 6. Non-Deterministic Processing Latency
* **Severity:** Low
* **Category:** Performance
* **Affected Component:** Backend (Print Simulator)
* **Root Cause:** The simulated print job processing incorporates a random variable delay (between 0.5 and 4.0 seconds) rather than a fixed processing time, leading to unpredictable response times.

## 7. Stale User Interface State
* **Severity:** Medium
* **Category:** UI/UX
* **Affected Component:** Frontend (Form Component)
* **Root Cause:** The callback responsible for triggering a re-fetch of the status list is not invoked after a successful form submission. The UI requires manual intervention (refreshing) to display newly added records.

## 8. Payload Mapping Inversion
* **Severity:** Medium
* **Category:** Data Integrity
* **Affected Component:** Frontend (API Integration)
* **Root Cause:** When constructing the `FormData` for the API request, the values for 'name' and 'department' are appended to the incorrect keys (swapped).
