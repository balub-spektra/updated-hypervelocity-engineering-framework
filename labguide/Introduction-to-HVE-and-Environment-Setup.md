# Exercise 01: Introduction to HVE and Environment Setup

### Estimated Duration: 30 Minutes

## 📘 Scenario

Before you can evaluate Hypervelocity Engineering for your team at Contoso Data Services, you need to understand what it actually is, and you need a working environment. In this exercise you will learn why the RPI lifecycle exists and what problem it solves, install HVE Core into Visual Studio Code, confirm the RPI entry surfaces are available in GitHub Copilot Chat, prepare the Contoso pipeline repository, and complete your first interaction with an RPI surface.

## 📖 Overview

This exercise establishes both the conceptual foundation and the working environment for the rest of the lab. You will read a short introduction to HVE and the RPI lifecycle, then install and validate the tooling. The final task has you use an RPI surface for the first time, so that you arrive at the Research phase already familiar with how RPI behaves.

By the end of this exercise, you will have a validated HVE Core installation, a prepared repository, and a clear mental model of what each RPI phase is for, including when a phase is deliberately skipped.

## 🎯 Objectives

In this exercise, you will complete the following tasks:

- Task 1: Understand Hypervelocity Engineering and the RPI lifecycle
- Task 2: Install the HVE Core extension
- Task 3: Validate the RPI entry surfaces in GitHub Copilot Chat
- Task 4: Prepare the Contoso pipeline repository
- Task 5: Your first interaction with an RPI surface

### Task 1: Understand Hypervelocity Engineering and the RPI Lifecycle

In this task, you will read a short introduction to HVE. There are no commands to run. Read it carefully, because every later exercise assumes you understand why the lifecycle is structured the way it is.

1. **The problem HVE solves.** AI coding assistants perform well on small, contained tasks and poorly on complex ones. The reason is not raw capability. The reason is that an assistant conflates investigation with implementation. Asked to add a feature, it starts writing code immediately, inventing patterns rather than discovering the ones your codebase already uses, and it has no durable record of what it assumed, what it decided, or how it verified the result.

1. **The insight behind RPI.** The fix is not a smarter model. The fix is giving each kind of work a clear contract and a durable output. **RPI** stands for **Research, Plan, Implement, Review**. Each phase has a defined scope, a defined set of permitted actions, and a dated artifact written to disk. Because state lives in those artifacts rather than in chat history, work stays inspectable, resumable, and reviewable.

1. **The lifecycle.** RPI is not a fixed four-step march. It is a pipeline that starts from what you already know:

    `Task context & evidence` ➔ `Research (only when a gap exists)` ➔ `Plan` ➔ `Implement` ➔ `Review` ➔ `Follow-up`

    Research is **conditional**. It runs only when the available evidence is inadequate for the requirements, acceptance criteria, dependencies, material risks, or architecture decisions the task depends on. If the evidence is already adequate, Research is satisfied and skipped, or an existing research document is reused, and the reason is logged.

    >**Note:** Skipping Research when evidence is adequate is correct behaviour, not a shortcut. In this lab, the backlog item is to add Azure Blob Storage output to the writers package, and nothing yet documents what `WriterBase` requires or how `LocalFileWriter` handles failures. That is an evidence gap, which is why you will run Research in Exercise 02.

1. **The entry surfaces.** You start RPI work through one of the following surfaces. Each has a behavioural contract:

    | Surface | Contract | Durable output |
    |---|---|---|
    | **RPI Agent** | User-selected lifecycle wrapper. Activates the applicable RPI skills under a single task identity. Manual by default, with "Full Auto" available on request. It is an entry surface, not an autonomous swarm of task workers. | Delegates to the artifacts below |
    | `/rpi-research` | Read-only. Runs only when evidence is inadequate. Never modifies source code. | `.copilot-tracking/research/YYYY-MM-DD/{task_slug}-research.md` |
    | `/rpi-plan` | Turns adequate evidence into a sequenced, verifiable implementation strategy without modifying source code. | `.copilot-tracking/plans/YYYY-MM-DD/{task_slug}-plan.md` and `.copilot-tracking/reviews/plans/YYYY-MM-DD/{task_slug}-plan-critique.md` |
    | `/rpi-implement` | Executes an approved `Pxx` phase or `Pxx-Txx` task scope. | `.copilot-tracking/changes/YYYY-MM-DD/{task_slug}-changes.md` |
    | `/rpi-review` | Read-only acceptance review of the finished work against the written requirements and plan. | `.copilot-tracking/reviews/logs/YYYY-MM-DD/{task_slug}-review.md` |
    | `/rpi-challenger` | Exposes assumptions before you act, using adaptive skeptical questions. | Conversational |
    | `/rpi-walkthrough` | Explains code or artifacts one segment at a time. | Conversational |

1. **Behavioural contracts, not personalities.** Four rules run through the lifecycle:

    - **Evidence before action.** Research and Plan never modify source code, so the plan is built from evidence rather than improvisation.
    - **Planning as a contract.** The plan uses stable `Pxx` phase and `Pxx-Txx` task identifiers, each with a checkable `Requirements:` record, and an independent critique records a `Pass`, `Revise`, or `Blocked` disposition.
    - **Evidence-based completion.** During Implement, a checkbox is updated only after evidence exists that the work is done. If reality departs materially from the plan, the discovery is recorded in the change log, the affected plan tasks are updated after a decision is made, and only the dependent work pauses.
    - **Acceptance review.** Review is read-only. It compares requirements, acceptance criteria, plan completion, critique dispositions, and change validation evidence.

1. **Two different questions at review time.** The review record deliberately separates **Execution Status** (`Complete`, `Partial`, or `Blocked`) from **Outcome** (`Conformant`, `Conformant with justified divergence`, `Defects found`, `Residual work`, or `Not accepted`). Work can be fully executed and still have defects, and work can be partially executed and still conform to what was accepted. Findings are recorded as severity-graded `RV-xxx` items, each routed to a designated destination.

1. **Follow-up routing.** Findings do not simply pile up in a list. They are routed by what kind of problem they are:

    | Finding type | Goes to |
    |---|---|
    | Defect in delivered work | Implementation |
    | Decision gap | Planning |
    | Evidence gap | Research |
    | Residual work | A distinct backlog item |

1. **Context hygiene.** Reset context with `/clear` or a fresh chat whenever you switch lifecycle concepts, for example from Research to Plan, or from Implement to Review. This is not housekeeping, it is the mechanism. Each phase writes its output to a dated file under `.copilot-tracking/`, so clearing context loses nothing. The handoff is the document, not the conversation.

1. **Durable artifacts and the tracking folder.** Every RPI phase writes to the `.copilot-tracking/` folder in the repository, in dated subfolders named with the task slug. These files are working documents for the current task, and they are how one phase hands off to the next.

    >**Note:** HVE is a framework in the sense of a process and a structural specification for packaging AI guidance. It is not a software framework. There is no SDK, no runtime and no library to import. This distinction matters when you explain HVE to your own team.

<question source="Questions/question-01.md" />

### Task 2: Install the HVE Core Extension

In this task, you will install the HVE Core extension into Visual Studio Code. HVE Core is the open-source agent and prompt library published by Microsoft at `github.com/microsoft/hve-core`.

1. In Visual Studio Code, open the **Extensions** view by pressing **Ctrl+Shift+X**, or by clicking the Extensions icon in the Activity Bar on the left.

    ![Open Extensions view](./media/hve-e1t2s1.png)

1. In the Extensions search box, type **HVE Core (1)**. From the results, select the **HVE Core (2)** extension.

    ![Search for HVE Core](./media/hve-e1t2s2.png)

    >**Note:** Select the extension whose publisher and repository link match the official `microsoft/hve-core` project. If more than one HVE Core variant appears, choose the standard **HVE Core** collection, which includes the RPI workflow this lab uses.

1. Click **Install**.

    ![Install HVE Core](./media/hve-e1t2s3.png)

1. Wait for the installation to complete. When prompted, click **Reload** to restart Visual Studio Code.

    ![Reload VS Code](./media/hve-e1t2s4.png)

    >**Note:** The extension requires a working GitHub Copilot installation with Copilot Chat enabled. Both are pre-configured on your lab virtual machine.

1. After the reload, return to the **Extensions** view and confirm that **HVE Core** now appears under **Installed** with no error badge.

    ![HVE Core installed](./media/hve-e1t2s5.png)

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000001" />

### Task 3: Validate the RPI Entry Surfaces in GitHub Copilot Chat

In this task, you will confirm that the RPI entry surfaces are registered and available inside GitHub Copilot Chat. If they do not appear here, nothing later in the lab will work, so do not skip this check.

1. Open **GitHub Copilot Chat** by pressing **Ctrl+Alt+I**.

    ![Open Copilot Chat](./media/hve-e1t3s1.png)

1. In the chat panel, open the **agent picker** (the mode dropdown next to the chat input box) and confirm that **RPI Agent** is listed.

    ![RPI Agent in the agent picker](./media/hve-e1t3s2.png)

    >**Note:** The RPI Agent is a **user-selected** lifecycle wrapper. Nothing activates it automatically. You choose it when you want one task identity carried across the lifecycle, and it works in manual mode by default. You will not select it in this lab, because you will drive each phase explicitly with its own prompt to see what each one does.

1. Press **Escape** to dismiss the picker without changing your selection.

1. Now confirm the RPI prompts are registered. In the Copilot Chat input box, type the **/** character. Scroll the list and confirm you can see all of the following:

    - **rpi-research**
    - **rpi-plan**
    - **rpi-implement**
    - **rpi-review**
    - **rpi-challenger**
    - **rpi-walkthrough**

    ![RPI prompts present](./media/hve-e1t3s3.png)

    >**Note:** If these entries do not appear, the extension has installed but Copilot has not picked it up. Reload Visual Studio Code with **Ctrl+Shift+P**, then **Developer: Reload Window**, and check again. If they are still missing, your Copilot organisation policy may be blocking custom agents or prompts. Contact CloudLabs support.

1. Press **Escape** to dismiss the list.

    >**Note:** The `/rpi-*` entries are the entry points you will type throughout the lab. The core four map to the phases of the lifecycle. `/rpi-challenger` and `/rpi-walkthrough` are specialised surfaces that support the lifecycle without being phases of it.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000002" />

### Task 4: Prepare the Contoso Pipeline Repository

In this task, you will open the sample repository, install its dependencies, confirm the test suite passes, and configure the workspace so RPI artifacts are kept out of version control.

1. In Visual Studio Code, click **File (1)** from the top left corner, then select **Open Folder (2)**.

    ![Open Folder](./media/hve-e1t4s1.png)

1. Navigate to **C:\Users\demouser\Downloads (1)**, press **Enter**, select **contoso-pipeline (2)**, and then click **Select Folder (3)**.

    ![Select contoso-pipeline](./media/hve-e1t4s2.png)

1. Click **Yes, I trust the authors**.

    ![Trust the authors](./media/hve-e1t4s3.png)

1. In the Explorer pane, expand **src (1)**, then **pipeline (2)**, then **writers (3)**. Select **base.py (4)** and read the `WriterBase` class.

    ![Explore the writers package](./media/hve-e1t4s4.png)

    >**Note:** `WriterBase` is the abstract class every output writer extends. `local_writer.py` next to it is the existing implementation. Your backlog item is to add a Blob Storage writer that follows the same pattern. Do not write it yourself, the RPI lifecycle will.

1. Open **docs/conventions.md** and skim it.

    ![Read team conventions](./media/hve-e1t4s5.png)

    >**Note:** This file documents the team's coding conventions. It is part of the task context and evidence that RPI draws on. The Research phase will discover it, the Plan phase will cite it, and the Review phase will check your implementation against it.

1. Right-click on the **contoso-pipeline (1)** folder in the Explorer, then select **Open in Integrated Terminal (2)**.

    ![Open integrated terminal](./media/hve-e1t4s6.png)

1. Install the project dependencies by running:

    ```
    pip install -r requirements.txt
    ```

    ![Install dependencies](./media/hve-e1t4s7.png)

    >**Note:** Wait for the installation to complete. It may take a few minutes.

1. Confirm the existing test suite passes by running:

    ```
    pytest -q
    ```

    ![Run the test suite](./media/hve-e1t4s8.png)

    >**Note:** All tests must pass before you continue. The Review phase later in this lab compares change validation evidence against this baseline, and it needs a clean starting point to do so.

1. Open the **.gitignore** file at the root of the repository and confirm it contains the following line. If it is not present, add it and press **Ctrl+S** to save.

    ```
    .copilot-tracking/
    ```

    ![Confirm gitignore entry](./media/hve-e1t4s9.png)

    >**Note:** `.copilot-tracking/` is where every RPI artifact is written. These are working documents for the current task and are deliberately kept out of source control.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000003" />

### Task 5: Your First Interaction with an RPI Surface

In this task, you will use an RPI surface for the first time. This is a deliberately small, read-only interaction so that you can see how RPI behaves before the real work begins.

1. Open **GitHub Copilot Chat** with **Ctrl+Alt+I**.

1. In the chat input box, type **/rpi-walkthrough** and select it from the list.

    ![Select rpi-walkthrough](./media/hve-e1t5s1.png)

1. After the prompt name, type the following and press **Enter**:

    ```
    src/pipeline/writers/base.py
    ```

    ![Ask for a walkthrough of base.py](./media/hve-e1t5s2.png)

1. Read the response. Note three things about how it answered:

    - It explains the file **one segment at a time**, rather than dumping a summary of the whole file at once.
    - It **did not modify any file**, even though it is looking at code.
    - It **grounded its explanation in what it actually found** in your repository, not in what a typical abstract writer class usually looks like.

    ![Walkthrough response](./media/hve-e1t5s3.png)

    >**Note:** The walkthrough surface exists so that you understand code or artifacts before you decide what to do with them. It is a good habit before a Plan review or a Review acceptance, and it is the same read-only discipline that Research and Review follow.

1. Now start a fresh chat by clicking the **+** icon at the top of the Copilot Chat panel, or by typing **/clear** in the chat input and pressing **Enter**.

    ![Clear the chat context](./media/hve-e1t5s4.png)

    >**Note:** Get into this habit now. You will reset context whenever you switch lifecycle concepts in this lab. This is the context hygiene rule from Task 1, and it is the single most commonly skipped step when teams adopt RPI.

<question source="Questions/question-02.md" />
<question source="Questions/question-03.md" />

## 🧾 Summary

In this exercise, you have successfully:

- Learned what Hypervelocity Engineering is, why the RPI lifecycle exists, and why Research runs only when an evidence gap exists.
- Understood the lifecycle from task context and evidence through Follow-up, the entry surfaces and their behavioural contracts, and the durable artifact each one writes.
- Understood how Review separates Execution Status from Outcome, and how findings are routed to implementation, planning, research, or the backlog.
- Installed the HVE Core extension in Visual Studio Code.
- Validated that the RPI Agent and the `/rpi-*` prompts are registered in GitHub Copilot Chat.
- Opened the Contoso pipeline repository, installed its dependencies, confirmed a clean test baseline, and excluded `.copilot-tracking/` from version control.
- Completed a first, read-only interaction with `/rpi-walkthrough` and practised resetting context.

### You have successfully completed the exercise. Click **Next >>** to continue to the next exercise.

![Next](./media/afg10.png)
