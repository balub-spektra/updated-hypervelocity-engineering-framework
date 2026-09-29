# Exercise 04: Implement and Review Phases

### Estimated Duration: 40 Minutes

## 📘 Scenario

You have an approved plan. The Contoso backlog item is now fully specified: which files to create, which patterns to follow, which references to work from, and what evidence will show that each task is done.

In this exercise you will execute that plan and then validate the result. `/rpi-implement` works one approved scope at a time, which gives you control points along the way. `/rpi-review` then performs a read-only acceptance review of the finished work against the written requirements rather than against the conversation. Finally, you will use `/rpi-challenger` to expose assumptions nobody verified, and route the follow-up.

## 📖 Overview

In this exercise, you will complete the RPI lifecycle. You will execute the plan one task at a time, intervene mid-run to see how stop controls work, inspect the change log, run the test suite, and run the acceptance review. You will close by running `/rpi-challenger` and routing the findings the lifecycle surfaced to the right destination.

By the end of this exercise, you will have a working Azure Blob Storage writer, a passing test suite, a change log, and a review record, all produced through a controlled lifecycle rather than a single large prompt.

## 🎯 Objectives

In this exercise, you will complete the following tasks:

- Task 1: Execute the first plan task
- Task 2: Execute the remaining plan tasks
- Task 3: Inspect the change log and run the tests
- Task 4: Run the Review phase
- Task 5: Challenge the finished work and route follow-up

### Task 1: Execute the First Plan Task

In this task, you will run the Implement phase against a single task from your plan, so you can see the granularity the lifecycle operates at.

1. Confirm you are in a **fresh Copilot Chat conversation**. If not, click the **+** icon at the top of the panel.

1. You need the exact path of your plan file. In the Explorer, right-click the plan file and select **Copy Relative Path**.

    ![Copy relative path](./media/hve-e4t1s2.png)

1. In the chat input box, type the following, substituting your real plan path (including today's date and task slug), and press **Enter**:

    ```
    /rpi-implement Execute task P01-T01 from .copilot-tracking/plans/YYYY-MM-DD/{task_slug}-plan.md
    ```

    ![Invoke rpi-implement for a single task](./media/hve-e4t1s3.png)

    >**Note:** `/rpi-implement` executes an **approved `Pxx` or `Pxx-Txx` scope**. Naming a single task keeps the run tight. Naming a whole phase, or omitting the scope, lets the implementer work through more of the plan in one go.

    >**Note:** If your plan numbered its first task differently, use the identifier that actually appears in your plan file rather than `P01-T01`.

1. Watch the implementer work. It will read the plan and the references it cites, then create or modify only the files that task calls for.

    ![Implementer executing a task](./media/hve-e4t1s4.png)

    >**Note:** Notice that it is not designing anything. Every decision was made in the Plan phase. This is constrained execution, and it is why the output follows your existing patterns instead of introducing new ones.

1. When the task completes, review the diff of the file it created or changed. In the Source Control view (**Ctrl+Shift+G**), click the changed file to open the diff.

    ![Review the diff](./media/hve-e4t1s5.png)

1. Check the code against the conventions in `docs/conventions.md`. Confirm the naming, error handling and type hints match what the existing `LocalFileWriter` does.

    ![Compare against conventions](./media/hve-e4t1s6.png)

1. Open the plan file and look at task **P01-T01**. Confirm its checkbox is now ticked and that the change log records evidence for it.

    ![Task checkbox updated](./media/hve-e4t1s7.png)

    >**Note:** Checkboxes update **only after evidence exists**. A ticked box with nothing behind it in the change log would be a defect in the run.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000008" />

### Task 2: Execute the Remaining Plan Tasks

In this task, you will let the implementer work through the rest of the plan.

1. Stay in the **same Copilot Chat conversation**. The implementer needs continuity across tasks within a single phase.

1. Type the following and press **Enter**:

    ```
    Continue with the remaining tasks in the plan.
    ```

    ![Continue implementation](./media/hve-e4t2s2.png)

1. Watch the implementer work through the remaining phases. It will tick off tasks as it completes them, and only once the evidence for each exists.

    ![Implementer progressing through tasks](./media/hve-e4t2s3.png)

    >**Note:** This step takes the longest in the lab, typically eight to twelve minutes. Use the time to keep reading the plan file alongside the chat, so you can see the mapping between planned tasks and actual edits.

1. If the implementer pauses to ask a question, answer it and let it continue. If it appears to drift from the plan, stop it by typing:

    ```
    Stop. Return to the plan and complete only the tasks it specifies.
    ```

    ![Stop control](./media/hve-e4t2s4.png)

    >**Note:** These stop controls are part of the design. You are meant to be able to interrupt, correct and resume. An engineer who reads the diffs as they land catches drift in seconds. An engineer who waits until the end reviews a large change with no context.

    >**Note:** Not every departure from the plan is drift. If the implementer finds that reality genuinely differs from what the plan assumed, the correct behaviour is a **material departure** procedure: it records the discovery in the change log, waits for a decision, updates the affected plan tasks **after** that decision, and pauses **only the dependent work**. Independent tasks can continue. It does not quietly improvise, and it does not rewrite the plan critique, which stays historical.

1. Wait until the implementer reports that all plan tasks are complete.

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
    .copilot-tracking/changes/YYYY-MM-DD/{task_slug}-changes.md
    ```

    ![Open the change log](./media/hve-e4t3s1.png)

1. Read it. Confirm it lists every file created and every file modified, with a short statement of what changed in each, and the validation evidence for each completed task. If any material departure occurred, confirm it is recorded here.

    ![Change log contents](./media/hve-e4t3s2.png)

    >**Note:** This is the artifact that makes a pull request reviewable. A reviewer reading this file knows the intent behind each change before opening a single diff. It is also the change validation evidence that the Review phase uses.

1. Open the integrated terminal at the repository root (**Ctrl+`**) and run the test suite:

    ```
    pytest -q
    ```

    ![Run the test suite](./media/hve-e4t3s3.png)

1. Confirm all tests pass, including the new tests covering the blob writer.

    ![Tests passing](./media/hve-e4t3s4.png)

    >**Note:** If any test fails, do not fix it by hand. Report the failure to the implementer in chat and let it correct the work against the plan. Hand-patching breaks the audit trail that the change log and review record depend on.

1. Run the test suite once more with verbose output to see the new test names:

    ```
    pytest -v
    ```

    ![Verbose test output](./media/hve-e4t3s5.png)

    >**Note:** Look for a test covering the partial-write failure path. That is the requirement **you** added by hand in Exercise 03, Task 4. Seeing it here is the proof that a human edit to the plan propagated all the way into the delivered code.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000010" />

### Task 4: Run the Review Phase

In this task, you will run the read-only acceptance review.

1. Start a **fresh Copilot Chat conversation** by clicking the **+** icon.

    ![Fresh chat for the Review phase](./media/hve-e4t4s1.png)

    >**Note:** This reset matters more than any of the others. A reviewer that can still see the implementer's reasoning will tend to accept it. A reviewer starting cold has to check the work against the written record, which is the entire point.

1. Type the following and press **Enter**:

    ```
    /rpi-review {task_slug}
    ```

    ![Invoke rpi-review](./media/hve-e4t4s2.png)

    >**Note:** Use the same task slug that appears in your artifact filenames. If your files are named `azure-blob-storage-*`, use `azure-blob-storage`. `/rpi-review` is **read-only**. It reports on the work and never changes source code.

1. Watch the reviewer work. It compares the requirements and acceptance criteria, plan completion, critique dispositions, and change validation evidence, and it runs the project's lint, build and test commands.

    ![Reviewer working](./media/hve-e4t4s3.png)

1. Open the review record it produces:

    ```
    .copilot-tracking/reviews/logs/YYYY-MM-DD/{task_slug}-review.md
    ```

    ![Open the review record](./media/hve-e4t4s4.png)

1. Read the review. Confirm it covers the following:

    - Whether each task's requirements and acceptance criteria were met.
    - Whether the plan is complete, and how each critique disposition was handled.
    - Convention compliance against `docs/conventions.md`.
    - Validation evidence from the change log and the lint, build and test commands.
    - **Findings** with severity-graded `RV-xxx` identifiers, each with a designated destination.

    ![Review record contents](./media/hve-e4t4s5.png)

1. Find the **Execution Status** and the **Outcome** in the record. They are recorded separately:

    | Field | Possible values |
    |---|---|
    | **Execution Status** | `Complete`, `Partial`, `Blocked` |
    | **Outcome** | `Conformant`, `Conformant with justified divergence`, `Defects found`, `Residual work`, `Not accepted` |

    ![Execution status and outcome](./media/hve-e4t4s6.png)

    >**Note:** These answer different questions. Execution Status asks whether the planned work was carried out. Outcome asks whether what was delivered is acceptable. A run can be `Complete` and still have `Defects found`, and it can be `Conformant with justified divergence` when a recorded material departure was reasoned and accepted.

    >**Note:** Findings are routed, not just listed. A defect goes back to implementation, a decision gap goes to planning, an evidence gap goes to research, and residual work becomes a distinct backlog item. A missing docstring on a new public method is a typical residual-work item.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000011" />

### Task 5: Challenge the Finished Work and Route Follow-up

In this task, you will use `/rpi-challenger` to expose assumptions before you open a pull request, and then route the findings. The challenger is optional but valuable at the stage where confidence is highest and scrutiny is usually lowest.

1. Start a **fresh Copilot Chat conversation** by clicking the **+** icon.

1. In the chat input box, type **/rpi-challenger** and select it from the list.

    ![Select rpi-challenger](./media/hve-e4t5s2.png)

1. After the prompt name, type the following and press **Enter**:

    ```
    The Azure Blob Storage writer is ready for a pull request. What assumptions were made that were not verified, and what would break in production?
    ```

    ![Challenge the implementation](./media/hve-e4t5s3.png)

1. Answer the questions it asks you. Read the challenges it raises. Typical findings concern retry behaviour, credential handling, large-file streaming, and concurrent write conflicts.

    ![Challenger findings](./media/hve-e4t5s4.png)

    >**Note:** The challenger asks **adaptive skeptical questions** and is deliberately adversarial, so not every point it raises is worth acting on. Its value is that it makes hidden assumptions visible while you can still decide what to do about them.

1. Route each finding you decided to act on, from both the review record and the challenger. Use the follow-up rules:

    | Finding | Route to |
    |---|---|
    | The delivered code is wrong or a requirement was not met | Implementation |
    | A decision was never made, such as a retry policy | Planning |
    | Something was never established, such as SDK throttling limits | Research |
    | Valid work that is out of scope for this change | A distinct backlog item |

    ![Follow-up routing](./media/hve-e4t5s5.png)

    >**Note:** Follow-up is where the lifecycle ends up, not a phase you can skip. Routing a finding to the right place stops it from being lost in a comment thread.

1. Review the five durable artifacts you produced across this lab. Open each one in turn:

    ```
    .copilot-tracking/research/YYYY-MM-DD/{task_slug}-research.md
    .copilot-tracking/plans/YYYY-MM-DD/{task_slug}-plan.md
    .copilot-tracking/reviews/plans/YYYY-MM-DD/{task_slug}-plan-critique.md
    .copilot-tracking/changes/YYYY-MM-DD/{task_slug}-changes.md
    .copilot-tracking/reviews/logs/YYYY-MM-DD/{task_slug}-review.md
    ```

    ![The five RPI artifacts](./media/hve-e4t5s6.png)

    >**Note:** Read as a set, these files tell the complete story of a change: what was known, what was decided and independently checked, what was done, and what was verified. That trail is what makes AI-assisted work auditable, and it is the strongest argument for adopting HVE on a team rather than leaving prompting to individual habit.

<question source="Questions/question-06.md" />

## 🧾 Summary

In this exercise, you have successfully:

- Executed a single plan task with `/rpi-implement` by naming an approved `Pxx-Txx` scope.
- Reviewed the resulting diff against the team's documented conventions.
- Executed the remaining plan tasks, practised the stop controls, and learned how material departures are handled.
- Inspected the change log and confirmed the test suite passes, including the requirement you added by hand.
- Ran the read-only Review phase with `/rpi-review` and read the review record, including `RV-xxx` findings and the separate Execution Status and Outcome.
- Ran `/rpi-challenger` to expose unverified assumptions in the completed work.
- Routed follow-up to implementation, planning, research, or the backlog.
- Reviewed the five RPI artifacts as a single audit trail.

## 🏁 Lab Conclusion

In this lab, you learned what Hypervelocity Engineering is and applied the RPI lifecycle end to end to deliver a real change to a real codebase.

The takeaway is not that the AI wrote a blob storage writer. Plain Copilot would also have written something. The takeaway is *how* it was written: grounded in evidence you can trace, sequenced by a plan you approved and amended, independently critiqued before it was implemented, executed under constraints you controlled, and accepted against a written record rather than a chat transcript. The durable artifacts in `.copilot-tracking/` are the record of that process.

To take this further with your own team, review the RPI documentation at **https://github.com/microsoft/hve-core/blob/main/docs/rpi/README.md** and the HVE Core documentation at **https://microsoft.github.io/hve-core/**, and in particular the Team Adoption Guide.

>**Note:** HVE Core is described by Microsoft as highly opinionated and rapidly evolving. Treat it as a source of patterns to adapt rather than a stable production dependency, and pin a version when you standardise on it.

### You have successfully completed the lab.

![Complete](./media/afg10.png)
