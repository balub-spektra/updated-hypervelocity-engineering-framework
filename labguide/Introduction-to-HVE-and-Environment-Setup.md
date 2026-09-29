# Exercise 01: Introduction to HVE and Environment Setup

### Estimated Duration: 30 Minutes

## 📘 Scenario

Before you can evaluate Hypervelocity Engineering for your team at Contoso Data Services, you need to understand what it actually is, and you need a working environment. In this exercise you will learn why the RPI workflow exists and what problem it solves, install HVE Core into Visual Studio Code, confirm the specialised agents and prompts are available in GitHub Copilot Chat, prepare the Contoso pipeline repository, and complete your first interaction with an HVE agent.

## 📖 Overview

This exercise establishes both the conceptual foundation and the working environment for the rest of the lab. You will read a short introduction to HVE and the RPI workflow, then install and validate the tooling. The final task has you talk to an HVE agent for the first time so that you arrive at the Research phase already familiar with how the agents behave.

By the end of this exercise, you will have a validated HVE Core installation, a prepared repository, and a clear mental model of what each RPI phase is for.

## 🎯 Objectives

In this exercise, you will complete the following tasks:

- Task 1: Understand Hypervelocity Engineering and the RPI workflow
- Task 2: Install the HVE Core extension
- Task 3: Validate the HVE Core agents and prompts in GitHub Copilot Chat
- Task 4: Prepare the Contoso pipeline repository
- Task 5: Your first interaction with an HVE agent

### Task 1: Understand Hypervelocity Engineering and the RPI Workflow

In this task, you will read a short introduction to HVE. There are no commands to run. Read it carefully, because every later exercise assumes you understand why the phases are separated.

1. **The problem HVE solves.** AI coding assistants perform well on small, contained tasks and poorly on complex ones. The reason is not raw capability. The reason is that an AI assistant cannot tell the difference between investigating and implementing. Asked to add a feature, it starts writing code immediately, inventing patterns rather than discovering the ones your codebase already uses. Microsoft's own documentation puts it bluntly: AI writes first and thinks never, because that is the only mode it has when it has unrestricted access to both research and implementation.

1. **The insight behind RPI.** The fix is not a smarter model. The fix is preventing the AI from doing certain things at certain times. RPI separates the work into four phases, each handled by a specialised agent that is only permitted to do that phase's work. A researcher that knows it will never write the code has no choice but to cite evidence.

1. **The four phases.** The workflow moves you from uncertainty to validated code through four steps:

   | Phase | Prompt | Agent | What it does | What you get |
   |---|---|---|---|---|
   | Research | `/task-research` | Task Researcher | Investigates the codebase, docs and external sources. Does not write code. | A research document with evidence and sources |
   | Plan | `/task-plan` | Task Planner | Turns research into phased, checkable steps with success criteria | A plan, an implementation details file and a planning log |
   | Implement | `/task-implement` | Task Implementor | Executes the plan phase by phase against verified patterns | Working code and a change log |
   | Review | `/task-review` | Task Reviewer | Validates the result against the plan and research | A review log with severity-graded findings and follow-up items |

1. **The four principles.** Each phase enforces one principle:

   - **Research first, implementation never.** The researcher investigates and is barred from editing source code, which forces it to discover patterns rather than invent them.
   - **Planning as a contract.** The plan sequences work with clear dependencies and success criteria, so the implementer has no room to improvise.
   - **Constrained execution.** The implementer follows verified patterns instead of making fresh decisions mid-run.
   - **Validation closure.** The reviewer checks the implementation against the documented specification, surfacing discrepancies early rather than at pull request time.

1. **Context engineering.** RPI requires you to **clear the chat context between phases** with `/clear` or a new chat. This is not housekeeping, it is the mechanism. If the planner can still see the researcher's exploratory dead ends, those discarded assumptions contaminate the plan. Because each phase writes its output to a file, clearing context loses nothing. The handoff is the document, not the conversation.

1. **The RPI Agent.** HVE Core also ships **RPI Agent**, an autonomous orchestrator started with `/rpi`. It assesses how difficult a task is, runs Research, Plan, Implement and Review itself (using lightweight direct work for simple tasks and document-backed phases for hard ones), and finishes with a fifth step, **Discover**, which suggests follow-up work. In this lab you will drive each phase yourself with its own prompt so you can see exactly what each one does, and you will use the RPI Agent at the end to discover follow-up work.

1. **The four artifact types.** Everything HVE Core ships falls into one of four categories, and knowing them helps you read the extension's contents:

   - **Prompts** (`.prompt.md`) are entry points that capture your intent and route to an agent. These are the `/task-research`, `/task-plan` style commands you will use.
   - **Agents** (`.agent.md`) orchestrate multi-step work and declare which tools they are allowed to use.
   - **Instructions** (`.instructions.md`) encode coding standards and attach automatically. They are passive reference material.
   - **Skills** (`SKILL.md` plus scripts) are active, executable utilities rather than guidance.

   The delegation flow runs Prompt to Agent to Instructions plus Skills.

   >**Note:** HVE is a framework in the sense of a process and a structural specification. It is not a software framework. There is no SDK, no runtime and no library to import. This distinction matters when you explain HVE to your own team.

<question source="Questions/question-01.md" />

### Task 2: Install the HVE Core Extension

In this task, you will install the HVE Core extension into Visual Studio Code. HVE Core is published by Microsoft and distributed through the Visual Studio Code Marketplace.

1. In Visual Studio Code, open the **Extensions** view by pressing **Ctrl+Shift+X**, or by clicking the Extensions icon in the Activity Bar on the left.

    ![Open Extensions view](./media/hve-e1t2s1.png)

1. In the Extensions search box, type **HVE Core (1)**. From the results, select the extension published by **ise-hve-essentials (2)**.

    ![Search for HVE Core](./media/hve-e1t2s2.png)

    >**Note:** The extension identifier is `ise-hve-essentials.hve-core`. Make sure the publisher and the link to the `microsoft/hve-core` repository match before you install.

1. Click **Install**.

    ![Install HVE Core](./media/hve-e1t2s3.png)

1. Wait for the installation to complete. When prompted, click **Reload** to restart Visual Studio Code.

    ![Reload VS Code](./media/hve-e1t2s4.png)

    >**Note:** The extension requires Visual Studio Code version 1.106.1 or higher and a working GitHub Copilot installation. Both are pre-configured on your lab virtual machine.

1. After the reload, return to the **Extensions** view, select **HVE Core**, and check the version number shown on the extension page.

    ![HVE Core installed](./media/hve-e1t2s5.png)

    >**Note:** This lab was written and validated against **HVE Core 3.2.2**. HVE Core evolves quickly, and later versions may rename or replace prompts. If your version is different, click the **gear icon** on the extension, select **Install Specific Version...**, and choose **3.2.2**. You can also turn off **Auto Update** from the same menu so the version does not change during the lab.

1. Confirm that **HVE Core** appears under **Installed** with no error badge.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000001" />

### Task 3: Validate the HVE Core Agents and Prompts in GitHub Copilot Chat

In this task, you will confirm that the HVE Core agents and prompts are registered and available inside GitHub Copilot Chat. If they do not appear here, nothing later in the lab will work, so do not skip this check.

1. Open **GitHub Copilot Chat** by pressing **Ctrl+Alt+I**.

    ![Open Copilot Chat](./media/hve-e1t3s1.png)

1. In the Copilot Chat input area, click the **agent picker** (the dropdown at the bottom left of the input box, which shows the current agent or mode). A list of available agents will appear.

    ![List available agents](./media/hve-e1t3s2.png)

1. Scroll the list and confirm that the following agents are present:

    - **RPI Agent**
    - **Task Researcher**
    - **Task Planner**
    - **Task Implementor**
    - **Task Reviewer**

    ![HVE agents present](./media/hve-e1t3s3.png)

    >**Note:** If these agents do not appear, the extension has installed but Copilot has not picked it up. Reload Visual Studio Code with **Ctrl+Shift+P**, then **Developer: Reload Window**, and check again. If they are still missing, your Copilot organisation policy may be blocking custom agents. Contact CloudLabs support.

1. Press **Escape** to dismiss the agent list without changing your selection.

1. Now confirm the RPI prompts are registered. In the Copilot Chat input box, type **/task**. Confirm you can see **task-research**, **task-plan**, **task-implement** and **task-review**.

    ![RPI prompts present](./media/hve-e1t3s4.png)

    >**Note:** Type **/task** rather than **/rpi** to see the phase prompts. The list filters by the characters you type, so `/rpi` shows only the `/rpi` prompt.

1. Clear the input box, type **/rpi**, and confirm that the **rpi** prompt appears, described as the autonomous Research-Plan-Implement-Review-Discover workflow.

    ![The rpi prompt](./media/hve-e1t3s5.png)

    >**Note:** The `/task-*` entries are **prompts**, the entry points you will type. Each one routes to the matching **agent** (`/task-research` to Task Researcher, and so on), which is why you do not need to select the agent yourself. This is the Prompt to Agent delegation flow described in Task 1.

1. Clear the input box.

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

    >**Note:** `WriterBase` is the abstract class every output writer extends. `local_writer.py` next to it is the existing implementation. Your backlog item is to add a Blob Storage writer that follows the same pattern. Do not write it yourself, the RPI workflow will.

1. Open **docs/conventions.md** and skim it.

    ![Read team conventions](./media/hve-e1t4s5.png)

    >**Note:** This file documents the team's coding conventions. The Research phase will discover it, and the Review phase will check your implementation against it. This is how HVE keeps AI output aligned with a team's existing standards.

1. Open **.github/copilot-instructions.md**.

    ![Read the Copilot instructions](./media/hve-e1t4s6.png)

    >**Note:** This file points every agent at the architecture and conventions documents and states the rules that always apply. HVE Core agents follow the repository conventions in this file, which is why the workflow needs almost no repeated explanation from you.

1. Right-click on the **contoso-pipeline (1)** folder in the Explorer, then select **Open in Integrated Terminal (2)**.

    ![Open integrated terminal](./media/hve-e1t4s7.png)

1. Install the project dependencies by running:

    ```
    pip install -r requirements.txt
    ```

    ![Install dependencies](./media/hve-e1t4s8.png)

    >**Note:** Wait for the installation to complete. It may take a few minutes.

1. Confirm the existing test suite passes by running:

    ```
    pytest -q
    ```

    ![Run the test suite](./media/hve-e1t4s9.png)

    >**Note:** All tests must pass before you continue. The Review phase later in this lab runs the project's tests, and it needs a clean baseline to compare against.

1. Open the **.gitignore** file at the root of the repository and confirm it contains the following line. If it is not present, add it and press **Ctrl+S** to save.

    ```
    .copilot-tracking/
    ```

    ![Confirm gitignore entry](./media/hve-e1t4s10.png)

    >**Note:** `.copilot-tracking/` is where every RPI artifact is written. These are working documents for the current task and are deliberately kept out of source control.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000003" />

### Task 5: Your First Interaction with an HVE Agent

In this task, you will talk to an HVE agent for the first time. This is a deliberately small interaction so that you can see how the agents behave before the real work begins.

1. Open **GitHub Copilot Chat** with **Ctrl+Alt+I**.

1. Click the **agent picker** and select **Task Researcher**.

    ![Select Task Researcher](./media/hve-e1t5s1.png)

1. In the chat input box, type the following question and press **Enter**:

    ```
    What output writers does this pipeline currently support, and where are they defined?
    ```

    ![Ask the researcher a question](./media/hve-e1t5s2.png)

1. Read the response. Note three things about how it answered:

    - It **cited specific files and line references** rather than describing the code in general terms.
    - It **did not change any source code**, even though the question was about code.
    - It **grounded its answer in what it actually found** in your repository, not in what a typical pipeline usually looks like.

    ![Researcher response](./media/hve-e1t5s3.png)

    >**Note:** This is role specialisation in action. The researcher agent is constrained so that investigation is the only thing it can do, and it records what it finds in files under `.copilot-tracking/research/`. Compare this mentally with what plain Copilot Chat would have produced for the same question.

1. In the Explorer, expand **.copilot-tracking**. If the researcher created a **research** folder for this question, delete that folder now (right-click it, then select **Delete**).

    ![Remove the practice research files](./media/hve-e1t5s4.png)

    >**Note:** That research was only a warm-up. Removing it means Exercise 02 starts from a clean folder and the Plan phase cannot pick up the wrong document.

1. Now start a fresh chat by clicking the **+** icon at the top of the Copilot Chat panel, or by typing **/clear** in the chat input and pressing **Enter**.

    ![Clear the chat context](./media/hve-e1t5s5.png)

    >**Note:** Get into this habit now. You will clear context between every phase in this lab. This is the context engineering principle from Task 1, and it is the single most commonly skipped step when teams adopt RPI.

<question source="Questions/question-02.md" />
<question source="Questions/question-03.md" />

## 🧾 Summary

In this exercise, you have successfully:

- Learned what Hypervelocity Engineering is, why the RPI workflow exists, and what problem role specialisation and clearing context solve.
- Understood the four RPI phases, the four principles behind them, the RPI Agent, and the four artifact types that HVE Core ships.
- Installed the HVE Core extension from the Visual Studio Code Marketplace.
- Validated that the RPI agents and the `/task-*` and `/rpi` prompts are registered in GitHub Copilot Chat.
- Opened the Contoso pipeline repository, installed its dependencies, confirmed a clean test baseline, and excluded `.copilot-tracking/` from version control.
- Completed a first interaction with the Task Researcher agent and observed how a role-constrained agent responds.

### You have successfully completed the exercise. Click **Next >>** to continue to the next exercise.

![Next](./media/afg10.png)
