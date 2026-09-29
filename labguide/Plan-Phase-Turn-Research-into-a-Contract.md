# Exercise 03: Plan Phase - Turn Research into a Contract

### Estimated Duration: 25 Minutes

## 📘 Scenario

You now have a research document describing exactly how the Contoso pipeline's writer package works and how an Azure Blob Storage writer should fit into it. What you do not have is a sequence of work. Knowledge is not a plan.

In this exercise you will run the Plan phase. `/rpi-plan` turns the adequate evidence into a sequenced, verifiable implementation strategy without touching source code, and an independent critique checks that plan before you see it. Once you approve it, the plan becomes the contract that the Implement phase executes against.

## 📖 Overview

In this exercise, you will execute the second phase of the RPI lifecycle. You will invoke `/rpi-plan`, watch it confirm that adequate evidence exists before it proceeds, and inspect the plan it produces. You will read the independent plan critique and its disposition, and then apply your own human review before approving the plan.

By the end of this exercise, you will have an approved implementation plan organised into stable `Pxx` phases and `Pxx-Txx` tasks, ready for execution.

## 🎯 Objectives

In this exercise, you will complete the following tasks:

- Task 1: Run the Plan phase
- Task 2: Inspect the plan structure
- Task 3: Read the plan critique
- Task 4: Apply your own human review and approve the plan

### Task 1: Run the Plan Phase

In this task, you will invoke `/rpi-plan` for the Azure Blob Storage backlog item.

1. Confirm you are in a **fresh Copilot Chat conversation**. If not, click the **+** icon at the top of the Copilot Chat panel.

    ![Fresh chat for the Plan phase](./media/hve-e3t1s1.png)

1. In the chat input box, type the following and press **Enter**:

    ```
    /rpi-plan
    ```

    ![Invoke rpi-plan](./media/hve-e3t1s2.png)

    >**Note:** You do not need to tell the planner what to plan. It locates the research document for your task in `.copilot-tracking/research/` on its own. This is artifact-driven handoff working as designed. If the planner asks which task to use, give it the task slug you noted in Exercise 02.

1. Observe the first thing the agent does. Before planning anything, it **checks that adequate evidence exists**. If the evidence is inadequate, it stops and sends you back to Research instead of planning against assumptions.

    ![Planner validates evidence exists](./media/hve-e3t1s3.png)

    >**Note:** This is a guardrail, not a convenience check. A plan built on assumptions rather than evidence produces exactly the failure mode RPI exists to avoid. The planner also never modifies source code, so at the end of this phase `src/` is exactly as you left it.

1. Wait while the planner reads the research and constructs the plan. It will then run an independent critique of the plan. It will report the file paths it has written when it finishes.

    ![Plan complete](./media/hve-e3t1s4.png)

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000006" />

### Task 2: Inspect the Plan Structure

In this task, you will open the plan and read how it is built. Everything the implementer needs is in this one document.

1. In the Explorer pane, expand **.copilot-tracking (1)**, then **plans (2)**, then **today's date (3)**. Open the plan file:

    ```
    .copilot-tracking/plans/YYYY-MM-DD/{task_slug}-plan.md
    ```

    ![Open the plan file](./media/hve-e3t2s1.png)

1. Read the top of the plan. Confirm it opens with an **executive summary**, followed by a **Phase Checklist** that includes a **Mermaid diagram** of the phases.

    ![Executive summary and phase checklist](./media/hve-e3t2s2.png)

    >**Note:** The Mermaid diagram is repeated for each phase with the current phase highlighted, so you can see at a glance where a phase sits in the dependency order. Use **Ctrl+Shift+V** to open the Markdown preview if you want to see the diagram rendered.

1. Scroll through the plan and confirm it is organised into **stable phases** and **stable tasks** within those phases, using identifiers such as **P01** and **P01-T01**. Each carries an HTML comment marker beginning `<!-- rpi:`.

    ![Plan structure with Pxx and Pxx-Txx identifiers](./media/hve-e3t2s3.png)

    >**Note:** A typical plan for this backlog item breaks into three phases. **P01** creates the Blob Storage client wrapper. **P02** creates the `BlobWriter` class extending `WriterBase`. **P03** wires the new writer into the pipeline configuration and adds tests. Your plan may differ in detail, but it should follow this shape: dependencies first, integration last. The identifiers are stable, so `/rpi-implement` and the review record can refer to exactly the same work later.

1. Open one task and confirm it contains all of the following blocks:

    - **Goals:** what the task is meant to achieve.
    - **Requirements:** the checkable record for the task, against which completion is judged.
    - **Details:** precisely where and how, including the file paths and patterns to follow.
    - **References:** the research findings, files, and line ranges the task relies on.
    - **Dependencies:** which other phases or tasks must be complete first.

    ![Task blocks: Goals, Requirements, Details, References, Dependencies](./media/hve-e3t2s4.png)

    >**Note:** The **Requirements** block is what makes the plan a contract. Without it, "done" is a matter of opinion, and the Review phase would have nothing objective to check against. The **Details** and **References** blocks are why the Implement phase can execute without re-deciding anything.

1. Confirm the task checkboxes are all unchecked.

    ![Unchecked task boxes](./media/hve-e3t2s5.png)

    >**Note:** Checkboxes are updated only **after evidence exists** that the work is done. An unchecked plan at this stage is the correct state.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000007" />

### Task 3: Read the Plan Critique

In this task, you will read the second artifact of the Plan phase, an independent check of the plan that you receive alongside it.

1. Open the plan critique file:

    ```
    .copilot-tracking/reviews/plans/YYYY-MM-DD/{task_slug}-plan-critique.md
    ```

    ![Open the plan critique](./media/hve-e3t3s1.png)

1. Find the **disposition**. The critique records exactly one of the following:

    | Disposition | Meaning |
    |---|---|
    | `Pass` | The plan is sound to implement as written. |
    | `Revise` | The plan needs changes before it should be implemented. |
    | `Blocked` | The plan cannot proceed until a missing decision or missing evidence is resolved. |

    ![Critique disposition](./media/hve-e3t3s2.png)

    >**Note:** A `Blocked` disposition caused by missing evidence sends you back to Research. One caused by an unresolved decision is a Planning problem. This is the same routing rule you will meet again in the Review phase.

1. Read the rest of the critique. It typically raises gaps, risky assumptions, or areas where the research was thin. For each point, decide whether it matters for your backlog item, and make a note of anything you want changed.

    ![Plan critique contents](./media/hve-e3t3s3.png)

    >**Note:** This is a cheap check at the cheapest possible moment. Catching a missing requirement here costs one edit to a markdown file. Catching the same thing after implementation costs a rework cycle across several source files. Once implementation begins, the critique remains **historical**. It is not re-run or rewritten, and it stays as the record of what was known at approval time.

### Task 4: Apply Your Own Human Review and Approve the Plan

In this task, you will review the plan yourself and amend it. This is the human-in-the-loop control point of the entire lifecycle.

1. Return to the plan file, `{task_slug}-plan.md`.

1. Read it once more as an engineer, not as an observer, and check the following:

    - Are the phases in a sensible order, with dependencies created before they are consumed?
    - Does any task bundle too much work to verify in one step?
    - Is anything missing that the critique flagged?
    - Does the plan respect the conventions in `docs/conventions.md`?
    - Would each **Requirements** block let a reviewer decide, with evidence, whether the task is done?

    ![Human review of the plan](./media/hve-e3t4s2.png)

1. Make one deliberate amendment to the plan. In the **Requirements** block of the task that covers tests, add the following requirement, then press **Ctrl+S** to save:

    ```
    Tests must cover the partial-write failure path, matching LocalFileWriter behaviour.
    ```

    ![Edit the plan requirements](./media/hve-e3t4s3.png)

    >**Note:** You are editing the plan by hand, in the editor, not by asking an agent to change it. The plan is a document you own. This is the moment where your judgement enters the lifecycle, and it is the reason RPI produces a plan file at all rather than going straight from research to code.

1. Confirm your edit is saved and the file shows no unsaved-changes indicator on its tab.

    ![Plan saved](./media/hve-e3t4s4.png)

1. Start a fresh chat by clicking the **+** icon at the top of the Copilot Chat panel, or by typing **/clear** and pressing **Enter**.

    ![Clear context before the Implement phase](./media/hve-e3t4s5.png)

    >**Note:** The approved plan is on disk. The Implement phase will read it from there. Resetting context now also discards any half-formed ideas the planner explored, which is precisely what you want the implementer not to inherit.

<question source="Questions/question-05.md" />

## 🧾 Summary

In this exercise, you have successfully:

- Invoked `/rpi-plan` and observed it confirm that adequate evidence existed before planning.
- Confirmed that planning did not modify any source code.
- Inspected the plan's executive summary, Phase Checklist, Mermaid diagram, and `Pxx` and `Pxx-Txx` structure.
- Identified the Goals, Requirements, Details, References, and Dependencies blocks on a task.
- Read the independent plan critique and its `Pass`, `Revise`, or `Blocked` disposition.
- Applied your own human review and amended a task's Requirements by hand.
- Reset the chat context in preparation for the Implement phase.

### You have successfully completed the exercise. Click **Next >>** to continue to the next exercise.

![Next](./media/afg10.png)
