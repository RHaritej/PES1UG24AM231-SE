# Use-Case Flow Specification

## Use Case: Upload Project Submission

**Use-Case ID:** UC-01
**Primary Actor:** Student
**Secondary Actors:** System (Test Runner, Rubric Engine), Faculty Evaluator (receives output)
**Related Use Cases:**
- «include» Execute Test Suite
- «include» Assign Peer Reviews
- «extend» Request Resubmission (extends this use case when resubmission is permitted)

---

### Brief Description
A Student uploads a zipped project submission before the assignment deadline. The system queues the file, automatically triggers the test suite execution and rubric scoring workflow, and assigns peer reviewers — without any manual intervention from the Faculty Evaluator.

---

### Preconditions
- PRE-1: The Student is authenticated and enrolled in the course/assignment.
- PRE-2: The assignment submission window is currently open (current time ≤ deadline).
- PRE-3: A rubric configuration and unit test suite have already been set up by the Faculty Evaluator for this assignment.
- PRE-4: The Student has a valid project archive (.zip) ready on their local device.

### Postconditions
- POST-1 (Success): The submission is stored, queued, evaluated, an itemized rubric score breakdown is generated, and peer reviewers are assigned to the submission.
- POST-2 (Success): The Student can view their rubric results, and the submission becomes visible to assigned peer reviewers.
- POST-3 (Failure): No partial or corrupted submission record is persisted; the Student is informed of the failure reason and prompted to retry.

---

### Main Success Scenario
1. The Student navigates to the assignment page and selects **Upload Submission**.
2. The Student selects a project `.zip` file from their device and confirms the upload.
3. The system validates the file (format, size limit, non-empty archive).
4. The system stores the file and adds it to the processing queue with a timestamp.
5. The system triggers the **Execute Test Suite** use case *«include»*, running the pre-configured unit tests against the submission.
6. The system generates an itemized rubric score breakdown based on the test results and static rubric criteria.
7. The system triggers the **Assign Peer Reviews** use case *«include»*, allocating the submission to peer reviewers under double-blind rules.
8. The system displays a confirmation message to the Student, including the submission timestamp and queue position.
9. The Student later views the rubric score breakdown once evaluation completes (within 10 seconds per NFR target).

**Use case ends successfully.**

---

### Alternate Flow A1: Invalid or Corrupted File
*Triggered at step 3 of the Main Success Scenario.*

1. The system detects that the uploaded file is not a valid `.zip`, exceeds the size limit, or is empty/corrupted.
2. The system rejects the upload and displays a specific error message (e.g., "Invalid file format" or "File exceeds 50 MB limit").
3. The system does **not** add the file to the processing queue.
4. The Student is prompted to select a new file and re-attempt the upload.
5. The flow returns to step 2 of the Main Success Scenario.

*(If the deadline has since passed during retries, the extending use case* **Request Resubmission** *governs whether a late upload is still permitted.)*

---

### Alternate Flow A2: Submission Deadline Passed
*Triggered at step 1, before file selection.*

1. The Student attempts to access the upload interface after the deadline has elapsed.
2. The system checks whether late submission / resubmission is enabled for this assignment (per Faculty Evaluator configuration).
3. If disabled, the system blocks the upload and displays "Submission window closed."
4. If enabled, control passes to the **Request Resubmission** extension point, which governs late-window eligibility and any penalty rules before resuming at step 2 of the Main Success Scenario.

---

### Special Requirements
- Response time for steps 3–4 (validation and queuing) must not exceed 2 seconds under normal load.
- The system must support concurrent uploads from up to 100 students without dropping queue items (per NFR-001).

### Frequency of Use
High — this is the primary entry point into the system and is expected to be triggered by every enrolled student, once per submission attempt, near each assignment deadline.
