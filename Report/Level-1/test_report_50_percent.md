# Test Execution Report (50% Visibility)

## 1. Duplicate Submission Test
* **Scenario**: Submit the same form multiple times very quickly.
* **Result**: FAIL. The system creates duplicate entries instead of preventing spam.

## 2. Broken Image Handling Test
* **Scenario**: Standard ID card submission.
* **Result**: FAIL. Images frequently appear broken when trying to view them later.

## 3. Status Inconsistency Test
* **Scenario**: Monitor status of newly created cards.
* **Result**: FAIL. Status jumps around unpredictably or gets stuck on "Pending".

## 4. Form Data Accuracy Test
* **Scenario**: Verify data in the queue matches user input.
* **Result**: FAIL. The data displayed is visually jumbled compared to the input.
