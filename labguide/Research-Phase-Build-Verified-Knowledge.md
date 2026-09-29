# Exercise 02: Research Phase - Build Verified Knowledge

### Estimated Duration: 25 Minutes

## 📘 Scenario

Your backlog item is to add Azure Blob Storage output to the Contoso ingestion pipeline. An engineer under time pressure would open Copilot Chat and ask it to write a blob writer. That is exactly the failure mode HVE exists to prevent, because the AI does not yet know what `WriterBase` requires, how the existing `LocalFileWriter` handles errors, what the team's conventions document says, or which Azure SDK the project already depends on.

Those are evidence gaps, and RPI treats an evidence gap as the trigger for Research. In this exercise you will run the Research phase. `/rpi-research` will investigate all of that, read-only, and write down what it found, with evidence. No code will be written and no source file will be touched.

## 📖 Overview

In this exercise, you will execute the first phase of the RPI lifecycle. You will invoke `/rpi-research` against a real backlog item, observe it gathering evidence from the codebase and external documentation, and inspect the research artifact it produces. You will then refine the research with a follow-up question and read the recommended approach it settled on.

By the end of this exercise, you will have a research document that the Plan phase can consume, and you will understand why a phase that produces no code is worth twenty minutes of a two-hour delivery.

## 🎯 Objectives

In this exercise, you will complete the following tasks:

- Task 1: Run the Research phase
- Task 2: Inspect the research artifact
- Task 3: Read the evidence and the recommended approach
- Task 4: Refine the research with a follow-up

### Task 1: Run the Research Phase

In this task, you will invoke `/rpi-research` for the Azure Blob Storage backlog item.

1. Confirm you are working in the **contoso-pipeline** folder in Visual Studio Code.

1. Open **GitHub Copilot Chat** with **Ctrl+Alt+I**.

1. If the chat panel shows any earlier conversation, start a fresh one by clicking the **+** icon at the top of the panel, or by typing **/clear** and pressing **Enter**.

    ![Start a fresh chat](./media/hve-e2t1s3.png)

    >**Note:** Reset context whenever you switch lifecycle concepts. The dated artifacts in `.copilot-tracking/` carry all the state you need, so nothing is lost.

1. Before you run Research, decide whether it is warranted. Ask yourself whether the evidence you already have covers the requirements, acceptance criteria, dependencies, material risks, and architecture decisions for this task.

    >**Note:** Research runs **only when available evidence is inadequate**. You have a one-line backlog item and nothing that records what `WriterBase` requires, how `LocalFileWriter` fails, or which Azure SDK the project uses. That is an evidence gap, so Research is warranted here. On a task where the evidence was already adequate, RPI would record why Research was satisfied and skip it, or reuse an existing research document.

1. In the chat input box, type the following prompt and press **Enter**:

    ```
    /rpi-research Azure Blob Storage integration for the Contoso pipeline writers package
    ```

    ![Invoke rpi-research](./media/hve-e2t1s4.png)

    >**Note:** `/rpi-research` is a **read-only** surface. It can read files and consult external documentation, but it cannot modify source code. The task slug it derives from your prompt names every artifact for this task across the remaining phases.

1. Watch the agent work. You will see it read files from the repository, follow references between them, and consult external documentation. This takes a few minutes.

    ![Researcher gathering evidence](./media/hve-e2t1s5.png)

    >**Note:** Notice what it is doing and what it is not doing. It is reading `base.py`, `local_writer.py`, `requirements.txt` and `docs/conventions.md`. It is not creating or editing any file in `src/`. If you see it propose code at this stage, it has drifted from its contract, and you should tell it to continue researching rather than implementing.

1. Wait until the agent reports that the research document has been written. It will state the file path in its final message.

    ![Research complete](./media/hve-e2t1s6.png)

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000004" />

### Task 2: Inspect the Research Artifact

In this task, you will locate and open the research document the agent produced. The artifact, not the chat transcript, is the real output of this phase.

1. In the Visual Studio Code Explorer pane, expand the **.copilot-tracking (1)** folder, then **research (2)**, then the folder named with **today's date (3)**.

    ![Locate the research folder](./media/hve-e2t2s1.png)

    >**Note:** If `.copilot-tracking` is not visible, it is being hidden as an ignored folder. Open the Explorer's overflow menu (the **...** at the top of the pane) and ensure hidden files are shown, or open the file directly with **Ctrl+P** and type `research`.

1. Open the research file. It will be named following the pattern below:

    ```
    .copilot-tracking/research/YYYY-MM-DD/{task_slug}-research.md
    ```

    ![Open the research document](./media/hve-e2t2s2.png)

    >**Note:** The exact task slug depends on how the agent interpreted your prompt. It may be `blob-storage`, `azure-blob-storage` or similar, giving `blob-storage-research.md`, `azure-blob-storage-research.md` and so on. Any of these is correct. Note the slug, because you will use it in later exercises.

1. Read the document from top to bottom. Confirm it contains the following, and note where each appears:

    - A statement of what was investigated and which evidence gaps prompted the research.
    - Findings about the **existing writer pattern**, referencing `WriterBase` and `LocalFileWriter` by file and line.
    - Findings about the **team conventions** discovered in `docs/conventions.md`.
    - Findings about the **Azure SDK** approach for blob uploads, with external sources cited.
    - Any **material risks or open questions** it could not resolve.
    - A **recommended approach** at the end.

    ![Research document contents](./media/hve-e2t2s3.png)

1. Scroll to any finding that references your codebase. Hold **Ctrl** and click one of the file references to jump to the code it cites.

    ![Follow a citation](./media/hve-e2t2s4.png)

    >**Note:** Verify that the citation is accurate. This is the point of the Research phase. A finding you can trace back to a real line of code is knowledge. A finding you cannot trace is a guess, and if you find one, correct it now before it propagates into the plan.

   > **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
   - Hit the validate button for the corresponding task. If you receive a success message, you can proceed to the next task.
   - If not, carefully read the error message and retry the step, following the instructions in the exercise guide.
   - If you need any assistance, don't hesitate to get in touch with us at cloudlabs-support@spektrasystems.com. We are available 24/7 to assist you.

   <validation step="00000000-0000-0000-0000-000000000005" />

### Task 3: Read the Evidence and the Recommended Approach

In this task, you will focus on the two properties that make a research document useful downstream.

1. Scroll to the **sources** or **references** section of the research document.

    ![Sources section](./media/hve-e2t3s1.png)

    >**Note:** Every claim should be attributable. Internal claims point at files in this repository. External claims point at documentation URLs. A research document without sources is just a longer guess.

1. Scroll to the **recommended approach** section.

    ![Recommended approach](./media/hve-e2t3s2.png)

    >**Note:** Research converges on a recommendation rather than handing you a menu. This is deliberate. A plan built from several competing options is not a contract, and the Implement phase would have to make design decisions at execution time, which is exactly what RPI is designed to prevent.

1. Read the recommended approach and check it against what you saw in `base.py` during Exercise 01. Confirm that it proposes extending `WriterBase` rather than inventing a new abstraction.

    ![Approach aligns with existing pattern](./media/hve-e2t3s3.png)

    >**Note:** This is the difference between discovered patterns and invented ones. Plain Copilot, asked to write a blob writer, would commonly produce a standalone class with its own interface, because it never looked at what you already had.

### Task 4: Refine the Research with a Follow-up

In this task, you will deepen one area of the research. Research is iterative, and closing an evidence gap now is far cheaper than discovering it during implementation.

1. Return to **GitHub Copilot Chat**. Stay in the **same conversation**, do not clear it yet.

    >**Note:** You reset context *between* lifecycle concepts, not within one. Refining research is still the Research phase.

1. Type the following follow-up question and press **Enter**:

    ```
    How does LocalFileWriter handle write failures and partial writes? The blob writer needs to match that behaviour exactly. Add your findings to the research document.
    ```

    ![Follow-up question](./media/hve-e2t4s2.png)

    >**Note:** This is an evidence gap about a material risk: failure behaviour. You are asking Research to close it explicitly instead of hoping the implementer guesses correctly.

1. Wait for the agent to investigate and update the research document.

    ![Researcher updates the document](./media/hve-e2t4s3.png)

1. Return to the research file in the editor. Confirm the new findings about error handling have been added.

    ![Updated research document](./media/hve-e2t4s4.png)

    >**Note:** If the file appears unchanged, press **Ctrl+S** on the editor tab or close and reopen the file to pick up changes written on disk.

1. Start a fresh chat by clicking the **+** icon at the top of the Copilot Chat panel, or by typing **/clear** and pressing **Enter**.

    ![Clear context before the next phase](./media/hve-e2t4s5.png)

    >**Note:** The Research phase is complete and its output is on disk. Everything the Plan phase needs is in that file, so nothing is lost by discarding the conversation. This is what artifact-driven handoff means.

<question source="Questions/question-04.md" />

## 🧾 Summary

In this exercise, you have successfully:

- Decided that Research was warranted because a real evidence gap existed, and learned when RPI would skip or reuse Research instead.
- Invoked `/rpi-research` against a real backlog item.
- Observed a read-only surface gather evidence without writing code.
- Located and inspected the research artifact in `.copilot-tracking/research/`.
- Verified findings by tracing citations back to real lines in the codebase.
- Read the recommended approach and confirmed it aligns with the existing `WriterBase` pattern.
- Closed a failure-behaviour evidence gap with a follow-up question.
- Reset the chat context in preparation for the Plan phase.

### You have successfully completed the exercise. Click **Next >>** to continue to the next exercise.

![Next](./media/afg10.png)
