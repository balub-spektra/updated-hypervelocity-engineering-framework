# Exercise 03: Plan Phase - Turn Research into a Contract

### Estimated Duration: 25 Minutes

## 📘 Scenario

You now have a research document describing exactly how the Contoso pipeline's writer package works and how an Azure Blob Storage writer should fit into it. What you do not have is a sequence of work. Knowledge is not a plan.

In this exercise you will run the Plan phase. The Task Planner agent reads your research and produces a phased, checkable plan with success criteria. Once you approve it, that plan becomes a contract, and the Implement phase is expected to follow it.

## 📖 Overview

In this exercise, you will execute the second phase of the RPI workflow. You will invoke the Task Planner agent with `/task-plan`, point it at your research document, and inspect the three files it produces. You will read the planning log the planner keeps alongside its plan, and then apply your own human review before approving the plan.

By the end of this exercise, you will have an approved implementation plan organised into phases and steps, ready for execution.

## 🎯 Objectives

In this exercise, you will complete the following tasks:

- Task 1: Run the Plan phase
- Task 2: Inspect the plan and details files
- Task 3: Read the planning log
- Task 4: Apply your own human review and approve the plan

### Task 1: Run the Plan Phase

In this task, you will invoke the Task Planner agent using the `/task-plan` prompt.

1. Confirm you are in a **fresh Copilot Chat conversation**. If not, click the **+** icon at the top of the Copilot Chat panel.

    ![Fresh chat for the Plan phase](./media/hve-e3t1s1.png)

1. In the Explorer, right-click your research file under `.copilot-tracking/research/` and select **Copy Relative Path**.

    ![Copy the research file path](./media/hve-e3t1s2.png)

1. In the chat input box, type the following, pasting your research path in place of the placeholder, and press **Enter**:

    ```
    /task-plan research=.copilot-tracking/research/YYYY-MM-DD/<topic>-research.md
    ```

    ![Invoke task-plan](./media/hve-e3t1s3.png)

    >**Note:** The `research=` argument tells the planner exactly which document to build on. Without it, the planner looks in `.copilot-tracking/research/` and picks a file itself, which is fine here but can select the wrong file on a busy repository. Confirm that the agent picker now shows **Task Planner**.

1. Observe what the agent does first. It reads the research document and checks that it covers the requirements before it plans anything. If there is no research to build on, it creates only a lightweight one.

    ![Planner reads the research](./media/hve-e3t1s4.png)

    >**Note:** The planner writes only under `.copilot-tracking/`. It never edits your source code, so at the end of this phase `src/` is exactly as you left it.

1. Wait while the planner builds the plan and runs its own validation of the plan against the research. If it asks you to choose between options, read the trade-offs and answer, or accept its recommendation. It will report the file paths it has written when it finishes.

    ![Plan complete](./media/hve-e3t1s5.png)

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000006" />

### Task 2: Inspect the Plan and Details Files

In this task, you will open the plan artifacts. The Plan phase produces three files, each with a different job. You will read two of them now and the third in Task 3.

1. In the Explorer pane, expand **.copilot-tracking (1)**, then **plans (2)**, then **today's date (3)**. Open the plan file:

    ```
    .copilot-tracking/plans/YYYY-MM-DD/<task>-plan.instructions.md
    ```

    ![Open the plan file](./media/hve-e3t2s1.png)

    >**Note:** The `.instructions.md` ending is intentional. It is how HVE Core names plan files, and it is why the Implement phase can find the plan by name.

1. Read the plan. Confirm it opens with an **Overview** and **Objectives** split into **User Requirements** and **Derived Objectives**, and that its **Implementation Checklist** is organised into **numbered phases** and **numbered steps** within them, such as **Step 1.1**.

    ![Plan structure with numbered phases](./media/hve-e3t2s2.png)

    >**Note:** A typical plan for this backlog item breaks into three phases plus a final validation phase. Phase 1 creates the Blob Storage client wrapper. Phase 2 creates the `BlobWriter` class extending `WriterBase`. Phase 3 wires the new writer into the pipeline configuration and adds tests. The last phase runs the full test suite. Your plan may differ in detail, but it should follow this shape: dependencies first, integration last, validation at the end.

1. Look for the `parallelizable` marker on each phase.

    ![Parallelizable markers](./media/hve-e3t2s3.png)

    >**Note:** A phase marked `parallelizable: true` touches different files from the others and can run alongside them. Phases that depend on each other, such as a writer that needs the client wrapper, are marked `false` and run in order.

1. Scroll to the **Success Criteria** section at the end of the plan and confirm each criterion states how you will know the work is done, and traces back to a research item or a user requirement.

    ![Success criteria](./media/hve-e3t2s4.png)

    >**Note:** Success criteria are what make the plan a contract. Without them, "done" is a matter of opinion, and the Review phase would have nothing objective to check against.

1. Now open the details file in its dated folder:

    ```
    .copilot-tracking/details/YYYY-MM-DD/<task>-details.md
    ```

    ![Open the details file](./media/hve-e3t2s5.png)

1. Read the details file and note that it contains a section for each step, with the **file operations** to perform, **line-number references** into the existing codebase and research, and step-level success criteria. Then go back to the plan and find a **Details:** line under one of the steps.

    ![Line references in the details file](./media/hve-e3t2s6.png)

    >**Note:** The plan says *what* to do. The details file says *precisely where and how*. Each step in the plan points at a range of lines in the details file. This separation is why the Implement phase can execute without re-deciding anything.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000007" />

### Task 3: Read the Planning Log

In this task, you will read the third artifact, in which the planner records what it found awkward about its own plan.

1. Open the planning log:

    ```
    .copilot-tracking/plans/logs/YYYY-MM-DD/<task>-log.md
    ```

    ![Open the planning log](./media/hve-e3t3s1.png)

1. Read it. It typically contains:

    - A **discrepancy log**, meaning places where the plan differs from the research or where the research was thin.
    - **Implementation paths considered**, meaning the alternatives the planner weighed and why it chose one.
    - **Suggested follow-on work**, meaning ideas that were deliberately left out of this plan.

    ![Planning log contents](./media/hve-e3t3s2.png)

    >**Note:** Some steps in the details file refer back to numbered items in this log, so you can see which decisions a step depends on. The planner also ran an automatic validation of the plan against the research before it finished, and fixed anything serious. What remains in the log is the honest list of caveats.

1. For each item the log raises, decide whether it matters for your backlog item. Make a note of anything you want changed.

    ![Assess the log items](./media/hve-e3t3s3.png)

    >**Note:** This is a cheap check at the cheapest possible moment. Catching a missing requirement here costs one edit to a markdown file. Catching the same thing after implementation costs a rework cycle across several source files.

### Task 4: Apply Your Own Human Review and Approve the Plan

In this task, you will review the plan yourself and amend it. This is the human-in-the-loop control point of the entire workflow.

1. Return to the plan file, `<task>-plan.instructions.md`.

1. Read it once more as an engineer, not as an observer, and check the following:

    - Are the phases in a sensible order, with dependencies created before they are consumed?
    - Does any step bundle too much work to verify in one go?
    - Is anything missing that the planning log flagged?
    - Does the plan respect the conventions in `docs/conventions.md`?

    ![Human review of the plan](./media/hve-e3t4s2.png)

1. Make one deliberate amendment to the plan. Scroll to the **Success Criteria** section at the very end of the plan file, add the following bullet as a new line, then press **Ctrl+S** to save:

    ```
    * Tests must cover the partial-write failure path, matching LocalFileWriter behaviour. — Traces to: user requirement added during plan review
    ```

    ![Edit the plan success criteria](./media/hve-e3t4s3.png)

    >**Note:** You are editing the plan by hand, in the editor, not by asking the agent to change it. The plan is a document you own. This is the moment where your judgement enters the workflow, and it is the reason RPI produces a plan file at all rather than going straight from research to code.

    >**Note:** Edit the plan, not the details file. The plan refers to line numbers inside the details file, so adding lines to the details file would make those references point at the wrong place.

1. Confirm your edit is saved and the file shows no unsaved-changes indicator on its tab.

    ![Plan saved](./media/hve-e3t4s4.png)

1. Start a fresh chat by clicking the **+** icon at the top of the Copilot Chat panel, or by typing **/clear**.

    ![Clear context before the Implement phase](./media/hve-e3t4s5.png)

    >**Note:** The approved plan is on disk. The Implement phase will read it from there. Clearing context now also discards any half-formed ideas the planner explored, which is precisely what you want the implementer not to inherit.

<question source="Questions/question-05.md" />

## 🧾 Summary

In this exercise, you have successfully:

- Invoked the Task Planner agent using the `/task-plan` prompt and pointed it at your research document.
- Observed that planning wrote only to `.copilot-tracking/` and left your source code untouched.
- Inspected the plan file and its numbered phases and steps, parallelization markers and success criteria.
- Inspected the details file and its line-number references into the codebase.
- Read the planning log covering discrepancies, alternatives considered and suggested follow-on work.
- Applied your own human review and amended the plan's success criteria by hand.
- Cleared the chat context in preparation for the Implement phase.

### You have successfully completed the exercise. Click **Next >>** to continue to the next exercise.

![Next](./media/afg10.png)
