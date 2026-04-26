# Test Execution Report (100% Visibility)

## 1. Duplicate Submission Test
* **Input**: Rapidly clicking the submit button 3 times.
* **Expected Behavior**: Only one request is processed; button is disabled during submission.
* **Actual Behavior**: 3 distinct requests are sent and processed. 3 duplicate records appear in the database.
* **Failure Reason**: Missing disabled state on frontend button; lacking deduplication/unique constraints on backend.

## 2. Broken Image Handling Test
* **Input**: Upload a valid image file.
* **Expected Behavior**: Image is saved to disk and accessible via URL.
* **Actual Behavior**: Intermittently (50% probability), the file is not saved to disk, but the database records the file path.
* **Failure Reason**: Simulated disk errors are explicitly caught and bypassed without returning an error to the user.

## 3. Status Inconsistency Test
* **Input**: Submit a valid ID card form.
* **Expected Behavior**: Status goes `Pending` -> `Processing` -> `Printed`.
* **Actual Behavior**: Status briefly appears as `Printed` on creation, and then permanently settles on `Processing`. Alternatively, the record is stuck permanently on `Pending`.
* **Failure Reason**: SQL `UPDATE` statements are executed in the incorrect order. Additionally, an early exit routine randomly aborts the workflow immediately after the initial `INSERT`.

## 4. API Payload Mismatch Test
* **Input**: Name="John", Department="Engineering".
* **Expected Behavior**: Record created with Name="John", Dept="Engineering".
* **Actual Behavior**: Record created with Name="Engineering", Dept="John".
* **Failure Reason**: `FormData.append()` keys are inverted in the React component.
