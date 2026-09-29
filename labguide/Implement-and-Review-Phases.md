# Exercise 04: Implement and Review Phases

### Estimated Duration: 40 Minutes

## 📘 Scenario

You have an approved plan. The Contoso backlog item is now fully specified: which files to create, which patterns to follow, which line references to work from, and how each step will be judged complete.

In this exercise you will execute that plan and then validate the result. The Task Implementor agent works phase by phase rather than generating everything at once, and you can ask it to pause after each phase, which gives you control points along the way. The Task Reviewer agent then checks the finished work against the written specification rather than against the conversation. Finally, you will use the RPI Agent to discover the follow-up work the workflow surfaced.

## 📖 Overview

In this exercise, you will complete the RPI cycle. You will execute the plan one phase at a time, intervene mid-run to see how stop controls work, inspect the change log, run the test suite, and validate the implementation against the plan. You will close by running the RPI Agent's Discover step and routing the follow-up items.

By the end of this exercise, you will have a working Azure Blob Storage writer, a passing test suite, a change log, and a review log, all produced through a controlled workflow rather than a single large prompt.

## 🎯 Objectives

In this exercise, you will complete the following tasks:

- Task 1: Execute the first plan phase
- Task 2: Execute the remaining plan phases
- Task 3: Inspect the change log and run the tests
- Task 4: Run the Review phase
- Task 5: Discover and route follow-up work

### Task 1: Execute the First Plan Phase

In this task, you will run the Implement phase with a stop after every phase, so you can see the granularity the workflow operates at.

1. Confirm you are in a **fresh Copilot Chat conversation**. If not, click the **+** icon at the top of the panel.

1. You need the exact path of your plan file. In the Explorer, right-click the plan file under `.copilot-tracking/plans/` and select **Copy Relative Path**.

    ![Copy relative path](./media/hve-e4t1s2.png)

1. In the chat input box, type the following, pasting your plan path in place of the placeholder. Press **Shift+Enter** after each line, then press **Enter** to send:

    ```
    /task-implement plan=.copilot-tracking/plans/YYYY-MM-DD/<task>-plan.instructions.md phaseStop=true

    Treat every item in the plan's Success Criteria section as binding. That includes the partial-write test requirement I added by hand.
    ```

    ![Invoke task-implement with a phase stop](./media/hve-e4t1s3.png)

    >**Note:** `phaseStop=true` makes the implementer pause after each phase for your review. There is also `stepStop=true`, which pauses after every single step. Omit both and it works through the whole plan continuously. Confirm that the agent picker now shows **Task Implementor**.

1. Watch the implementer work. It reads the plan, the details file and the research, creates the change log, and then carries out the first phase. It follows the details file rather than designing anything itself.

    ![Implementer executing a phase](./media/hve-e4t1s4.png)

    >**Note:** Notice that it is not designing anything. Every decision was made in the Plan phase. This is constrained execution, and it is why the output follows your existing patterns instead of introducing new ones.

1. When the first phase completes, the implementer stops and summarises what it did. Review the diff of the files it created or changed. In the Source Control view (**Ctrl+Shift+G**), click a changed file to open the diff.

    ![Review the diff](./media/hve-e4t1s5.png)

1. Check the code against the conventions in `docs/conventions.md`. Confirm the naming, type hints, docstrings and error handling match what the existing `LocalFileWriter` does.

    ![Compare against conventions](./media/hve-e4t1s6.png)

1. Open the plan file and confirm that the steps of Phase 1 are now ticked `[x]`.

    ![Plan checkboxes ticked](./media/hve-e4t1s7.png)

    >**Note:** The implementer updates the plan as it goes. A ticked step and an entry in the change log are your evidence that the step was really done.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000008" />

### Task 2: Execute the Remaining Plan Phases

In this task, you will let the implementer work through the rest of the plan.

1. Stay in the **same Copilot Chat conversation**. The implementer needs continuity across phases within a single Implement session.

1. Type the following and press **Enter**:

    ```
    Continue with the next phase.
    ```

    ![Continue implementation](./media/hve-e4t2s2.png)

1. Watch the implementer work through the phase, then review what it changed the same way you did in Task 1. Repeat the message above after each phase stops, until only the final validation phase remains. For that last stretch you can send:

    ```
    Continue with all remaining phases without stopping.
    ```

    ![Implementer progressing through phases](./media/hve-e4t2s3.png)

    >**Note:** This step takes the longest in the lab, typically eight to twelve minutes. Use the time to keep reading the plan file alongside the chat, so you can see the mapping between planned steps and actual edits.

1. If the implementer pauses to ask a question, answer it and let it continue. If it appears to drift from the plan, stop it by typing:

    ```
    Stop. Return to the plan and complete only the steps it specifies.
    ```

    ![Stop control](./media/hve-e4t2s4.png)

    >**Note:** These stop controls are part of the design. You are meant to be able to interrupt, correct and resume. An engineer who reads the diffs as they land catches drift in seconds. An engineer who waits until the end reviews a large change with no context.

    >**Note:** Not every departure from the plan is drift. When the implementer finds that reality differs from what the plan assumed, it records the difference in the change log under additional or deviating changes, adds it to the planning log's discrepancy log, and may add new steps to the plan. That trail is what lets the reviewer judge the deviation later.

1. Wait until the implementer reports that all plan phases are complete.

    ![Implementation complete](./media/hve-e4t2s5.png)

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000009" />

### Task 3: Inspect the Change Log and Run the Tests

In this task, you will read what the implementer recorded and confirm the code actually works.

1. Open the change log file:

    ```
    .copilot-tracking/changes/YYYY-MM-DD/<task>-changes.md
    ```

    ![Open the change log](./media/hve-e4t3s1.png)

1. Read it. Confirm it lists every file created and every file modified, with a short statement of what changed in each, and that it ends with a release summary.

    ![Change log contents](./media/hve-e4t3s2.png)

    >**Note:** This is the artifact that makes a pull request reviewable. A reviewer reading this file knows the intent behind each change before opening a single diff. It is also one of the inputs the Review phase uses. The implementer also offers a commit message when it finishes. Keep it, but do not commit anything yet.

1. Open the integrated terminal at the repository root (**Ctrl+`**) and run the test suite:

    ```
    pytest -q
    ```

    ![Run the test suite](./media/hve-e4t3s3.png)

1. Confirm all tests pass, including the new tests covering the blob writer.

    ![Tests passing](./media/hve-e4t3s4.png)

    >**Note:** If any test fails, do not fix it by hand. Report the failure to the implementer in chat and let it correct the work against the plan. Hand-patching breaks the audit trail that the change log and review log depend on.

1. Run the test suite once more with verbose output to see the new test names:

    ```
    pytest -v
    ```

    ![Verbose test output](./media/hve-e4t3s5.png)

    >**Note:** Look for a test covering the partial-write failure path. That is the success criterion **you** added by hand in Exercise 03, Task 4. Seeing it here is the proof that a human edit to the plan propagated all the way into the delivered code. If you cannot find one, do not add it yourself. Continue to the Review phase, which is designed to catch exactly this kind of gap.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000010" />

### Task 4: Run the Review Phase

In this task, you will run the fourth RPI phase.

1. Start a **fresh Copilot Chat conversation** by clicking the **+** icon, or by typing **/clear**.

    ![Fresh chat for the Review phase](./media/hve-e4t4s1.png)

    >**Note:** This clear matters more than any of the others. A reviewer that can still see the implementer's reasoning will tend to accept it. A reviewer starting cold has to check the code against the written specification, which is the entire point.

1. Type the following, pasting your plan path in place of the placeholder, and press **Enter**:

    ```
    /task-review plan=.copilot-tracking/plans/YYYY-MM-DD/<task>-plan.instructions.md
    ```

    ![Invoke task-review](./media/hve-e4t4s2.png)

    >**Note:** The reviewer can locate the related research, details and change log from the plan's name and date. Naming the plan removes any doubt about which one it should review. Confirm that the agent picker now shows **Task Reviewer**.

1. Watch the reviewer work. It will read the plan, read the change log, validate each phase of the plan against the code, assess implementation quality and convention compliance, and run the project's tests.

    ![Reviewer working](./media/hve-e4t4s3.png)

1. Open the review log it produces:

    ```
    .copilot-tracking/reviews/YYYY-MM-DD/<task>-plan-review.md
    ```

    ![Open the review log](./media/hve-e4t4s4.png)

1. Read the review. Confirm it covers the following:

    - Whether each plan phase was completed, with evidence.
    - Findings graded **critical**, **major** or **minor**, with counts.
    - Convention compliance against `docs/conventions.md`.
    - Results of the lint, build and test commands it ran.
    - **Follow-up items**, separated into work deferred from the plan and work discovered during the review.
    - An **overall status** of Complete, Needs Rework, or Blocked.

    ![Review log contents](./media/hve-e4t4s5.png)

    >**Note:** Findings are routed, not just listed. Critical and major findings go back to implementation as corrections. Minor findings and follow-up items become later work. A finding such as a missing docstring on a new public method is a typical minor item. The reviewer also leaves per-phase validation files under `.copilot-tracking/reviews/rpi/`.

    >**Note:** If the overall status is **Needs Rework**, use the review log to drive a fix. Start a fresh chat, open the review log, and run `/task-implement Address the findings found in the review document`, then run `/task-review` again.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000011" />

### Task 5: Discover and Route Follow-up Work

In this task, you will use the RPI Agent's Discover step to look for follow-up work and decide where each item should go. Discover is the fifth step of the RPI Agent's cycle, and it is a useful last look before a pull request.

1. Start a **fresh Copilot Chat conversation** by clicking the **+** icon.

1. In the chat input box, type the following and press **Enter**:

    ```
    /rpi suggest
    ```

    ![Invoke rpi suggest](./media/hve-e4t5s2.png)

    >**Note:** `/rpi` starts the **RPI Agent**, and `suggest` sends it straight to the Discover step. It reads the artifacts in `.copilot-tracking/` and the code, then proposes a short numbered list of next work. If it begins to implement something instead, stop it with the stop message from Task 2. This task is only about reading its suggestions.

1. Read the list it presents. Typical suggestions concern retry behaviour, credential handling, large-file streaming, and concurrent write conflicts, alongside any follow-up items from your review log.

    ![Suggested next work](./media/hve-e4t5s3.png)

    >**Note:** Do not reply with an option number. Replying with a number starts a new RPI cycle for that item, which is not part of this lab. Not every suggestion is worth acting on. Its value is that it makes the next steps visible while the context is fresh.

1. Compare the suggestions with the follow-up items in your review log and the **suggested follow-on work** in your planning log. For each item you would act on, decide where it belongs, using the routing below:

    | What the item is | Where it goes | Prompt |
    |---|---|---|
    | The delivered code is wrong or a criterion was missed | Implement | `/task-implement` |
    | Scope that the plan left out | Plan | `/task-plan` |
    | Missing technical knowledge | Research | `/task-research` |
    | Valid work outside this change | A separate backlog item | A new RPI cycle |

    ![Route the follow-up](./media/hve-e4t5s4.png)

    >**Note:** The Task Reviewer offers the same routes as buttons when it finishes: **Research More**, **Revise Plan** and **Implement Immediately**. Routing a finding to the right phase keeps it from being lost in a comment thread.

1. Review the six artifacts you produced across this lab. Open each one in turn:

    ```
    .copilot-tracking/research/YYYY-MM-DD/<topic>-research.md
    .copilot-tracking/plans/YYYY-MM-DD/<task>-plan.instructions.md
    .copilot-tracking/details/YYYY-MM-DD/<task>-details.md
    .copilot-tracking/plans/logs/YYYY-MM-DD/<task>-log.md
    .copilot-tracking/changes/YYYY-MM-DD/<task>-changes.md
    .copilot-tracking/reviews/YYYY-MM-DD/<task>-plan-review.md
    ```

    ![The RPI artifacts](./media/hve-e4t5s5.png)

    >**Note:** Read as a set, these files tell the complete story of a change: what was known, what was decided, what was done, and what was verified. That trail is what makes AI-assisted work auditable, and it is the strongest argument for adopting HVE on a team rather than leaving prompting to individual habit.

<question source="Questions/question-06.md" />

## 🧾 Summary

In this exercise, you have successfully:

- Executed the first plan phase with `/task-implement`, using an explicit plan path and a phase stop.
- Reviewed the resulting diff against the team's documented conventions.
- Executed the remaining plan phases and practised the stop controls for interrupting a drifting run.
- Inspected the change log and confirmed the test suite passes, including the criterion you added by hand.
- Ran the Review phase with `/task-review` and read the review log covering findings, conventions, test results, follow-up items and overall status.
- Used the RPI Agent's Discover step to find follow-up work, and routed each item to the right phase.
- Reviewed the six RPI artifacts as a single audit trail.

## 🏁 Lab Conclusion

In this lab, you learned what Hypervelocity Engineering is and applied the RPI workflow end to end to deliver a real change to a real codebase.

The takeaway is not that the AI wrote a blob storage writer. Plain Copilot would also have written something. The takeaway is *how* it was written: grounded in evidence you can trace, sequenced by a plan you approved and amended, executed under constraints you controlled, and validated against a written specification rather than a chat transcript. The artifacts in `.copilot-tracking/` are the durable record of that process.

To take this further with your own team, review the HVE Core documentation at **https://microsoft.github.io/hve-core/**, and in particular the Team Adoption Guide.

>**Note:** HVE Core is described by Microsoft as highly opinionated and rapidly evolving. This lab was written against version 3.2.2, and later versions have already begun to change the prompts and artifacts. Treat HVE Core as a source of patterns to adapt rather than a stable production dependency, and pin a version when you standardise on it.

### You have successfully completed the lab.

![Complete](./media/afg10.png)
