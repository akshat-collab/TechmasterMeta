from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from support_inbox_env.environment import SupportInboxEnvironment
from support_inbox_env.models import (
    EnvironmentState,
    ResetRequest,
    StepRequest,
    StepResponse,
    SupportObservation,
)

app = FastAPI(
    title="Support Inbox OpenEnv",
    version="0.1.0",
    description="A deterministic OpenEnv-compatible customer support triage environment.",
)

ENVIRONMENT = SupportInboxEnvironment()


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Support Inbox OpenEnv</title>
        <style>
          :root {
            --bg: #08111f;
            --panel: rgba(10, 18, 32, 0.88);
            --panel-2: rgba(17, 24, 39, 0.92);
            --line: rgba(148, 163, 184, 0.2);
            --text: #e5eefc;
            --muted: #9cb0cc;
            --accent: #2dd4bf;
            --accent-2: #60a5fa;
            --danger: #f97316;
          }
          body {
            margin: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            background:
              radial-gradient(circle at top left, rgba(45, 212, 191, 0.16), transparent 28%),
              radial-gradient(circle at top right, rgba(96, 165, 250, 0.18), transparent 25%),
              linear-gradient(180deg, #07101c, #0b1327 48%, #09111e);
            color: var(--text);
            min-height: 100vh;
          }
          .wrap {
            max-width: 1240px;
            margin: 0 auto;
            padding: 32px 20px 48px;
          }
          .hero {
            display: grid;
            grid-template-columns: 1.3fr 0.9fr;
            gap: 20px;
            margin-bottom: 20px;
          }
          .card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 22px;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
          }
          h1 {
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 2.5rem;
            line-height: 1.05;
          }
          p, li, label {
            line-height: 1.6;
            color: var(--muted);
          }
          .grid {
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 20px;
          }
          .panel-title {
            margin: 0 0 12px;
            font-size: 1.05rem;
            color: var(--text);
          }
          .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(45, 212, 191, 0.12);
            color: #9af3e6;
            font-size: 0.85rem;
            margin-bottom: 14px;
          }
          .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
          }
          .stat {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 14px;
          }
          .stat strong {
            display: block;
            color: var(--text);
            font-size: 1.1rem;
            margin-top: 6px;
          }
          .toolbar,
          .actions {
            display: grid;
            gap: 12px;
          }
          .row {
            display: grid;
            gap: 10px;
          }
          input, select, textarea, button {
            width: 100%;
            box-sizing: border-box;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: rgba(15, 23, 42, 0.8);
            color: var(--text);
            padding: 12px 14px;
            font: inherit;
          }
          textarea {
            min-height: 100px;
            resize: vertical;
          }
          button {
            cursor: pointer;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            color: #04111e;
            font-weight: 700;
            border: none;
          }
          button.secondary {
            background: rgba(15, 23, 42, 0.9);
            color: var(--text);
            border: 1px solid var(--line);
          }
          .stack {
            display: grid;
            gap: 18px;
          }
          .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
          }
          .chip {
            display: inline-flex;
            align-items: center;
            padding: 7px 10px;
            border-radius: 999px;
            background: rgba(96, 165, 250, 0.12);
            color: #cfe0ff;
            border: 1px solid rgba(96, 165, 250, 0.18);
            font-size: 0.88rem;
          }
          .two-col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
          }
          .box {
            border: 1px solid var(--line);
            border-radius: 18px;
            background: var(--panel-2);
            padding: 16px;
          }
          .box h3 {
            margin: 0 0 10px;
            font-size: 0.98rem;
          }
          .mono {
            font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            font-size: 0.87rem;
            white-space: pre-wrap;
            word-break: break-word;
          }
          .history {
            display: grid;
            gap: 10px;
            max-height: 420px;
            overflow: auto;
          }
          .event {
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 12px;
            background: rgba(9, 14, 27, 0.78);
          }
          .event strong {
            color: var(--text);
          }
          .message {
            margin-top: 10px;
            padding: 12px 14px;
            border-radius: 14px;
            background: rgba(249, 115, 22, 0.1);
            border: 1px solid rgba(249, 115, 22, 0.18);
            color: #ffd8c2;
          }
          .ok {
            background: rgba(45, 212, 191, 0.1);
            border-color: rgba(45, 212, 191, 0.22);
            color: #c6fff7;
          }
          .small {
            font-size: 0.87rem;
          }
          @media (max-width: 960px) {
            .hero,
            .grid,
            .two-col,
            .stats {
              grid-template-columns: 1fr;
            }
            h1 {
              font-size: 2rem;
            }
          }
        </style>
      </head>
      <body>
        <div class="wrap">
          <section class="hero">
            <div class="card">
              <div class="eyebrow">Support Ops Simulator</div>
              <h1>Support Inbox OpenEnv</h1>
              <p>
                Explore the environment visually. Reset a task, inspect the ticket, track status changes,
                and send actions from the browser without using curl.
              </p>
              <div class="stats">
                <div class="stat">
                  <span class="small">Environment</span>
                  <strong>OpenEnv API</strong>
                </div>
                <div class="stat">
                  <span class="small">Modes</span>
                  <strong>4 tasks</strong>
                </div>
                <div class="stat">
                  <span class="small">Endpoints</span>
                  <strong>/reset /step /state</strong>
                </div>
              </div>
            </div>
            <div class="card">
              <h2 class="panel-title">Quick Endpoints</h2>
              <div class="chip-row">
                <span class="chip">GET /health</span>
                <span class="chip">GET /tasks</span>
                <span class="chip">POST /reset</span>
                <span class="chip">POST /step</span>
                <span class="chip">GET /state</span>
              </div>
              <div id="statusMessage" class="message ok small" style="margin-top:16px;">
                Loading tasks and current state...
              </div>
            </div>
          </section>

          <section class="grid">
            <aside class="stack">
              <div class="card toolbar">
                <h2 class="panel-title">Reset Task</h2>
                <div class="row">
                  <label for="taskSelect">Choose scenario</label>
                  <select id="taskSelect"></select>
                </div>
                <button id="resetButton">Reset Environment</button>
              </div>

              <div class="card actions">
                <h2 class="panel-title">Send Action</h2>
                <div class="row">
                  <label for="actionType">Action type</label>
                  <select id="actionType"></select>
                </div>
                <div class="row">
                  <label for="actionValue">Value</label>
                  <input id="actionValue" placeholder="billing / urgent / investigating / refund_started" />
                </div>
                <div class="row">
                  <label for="actionMessage">Message</label>
                  <textarea id="actionMessage" placeholder="Reply text, internal note, or escalation reason"></textarea>
                </div>
                <button id="stepButton">Submit Step</button>
                <button id="stateButton" class="secondary">Refresh State</button>
              </div>
            </aside>

            <main class="stack">
              <div class="card">
                <h2 class="panel-title">Current Ticket</h2>
                <div class="two-col">
                  <div class="box">
                    <h3>Summary</h3>
                    <div id="ticketSummary" class="mono small">Reset a task to load ticket details.</div>
                  </div>
                  <div class="box">
                    <h3>Progress</h3>
                    <div id="checklist" class="chip-row"></div>
                  </div>
                </div>
              </div>

              <div class="two-col">
                <div class="card">
                  <h2 class="panel-title">Workflow State</h2>
                  <div class="box">
                    <h3>Status History</h3>
                    <div id="statusHistory" class="chip-row"></div>
                  </div>
                  <div class="box" style="margin-top:16px;">
                    <h3>Internal Notes</h3>
                    <div id="internalNotes" class="mono small">No notes yet.</div>
                  </div>
                </div>

                <div class="card">
                  <h2 class="panel-title">Reward Snapshot</h2>
                  <div id="rewardBox" class="mono small">No step executed yet.</div>
                </div>
              </div>

              <div class="card">
                <h2 class="panel-title">Action History</h2>
                <div id="history" class="history"></div>
              </div>
            </main>
          </section>
        </div>

        <script>
          const actionTypes = [
            "classify_intent",
            "set_priority",
            "assign_team",
            "add_internal_note",
            "request_more_info",
            "change_status",
            "draft_reply",
            "apply_refund",
            "resolve",
            "escalate",
          ];

          const taskSelect = document.getElementById("taskSelect");
          const actionType = document.getElementById("actionType");
          const actionValue = document.getElementById("actionValue");
          const actionMessage = document.getElementById("actionMessage");
          const statusMessage = document.getElementById("statusMessage");

          actionTypes.forEach((type) => {
            const option = document.createElement("option");
            option.value = type;
            option.textContent = type;
            actionType.appendChild(option);
          });

          function setMessage(text, ok = false) {
            statusMessage.textContent = text;
            statusMessage.className = ok ? "message ok small" : "message small";
          }

          function renderObservation(observation, reward = null) {
            if (!observation) return;
            document.getElementById("ticketSummary").textContent = JSON.stringify({
              task_id: observation.task_id,
              title: observation.title,
              difficulty: observation.difficulty,
              current_status: observation.current_status,
              remaining_turns: observation.remaining_turns,
              ticket: observation.ticket
            }, null, 2);

            const checklist = document.getElementById("checklist");
            checklist.innerHTML = "";
            Object.entries(observation.checklist).forEach(([key, value]) => {
              const chip = document.createElement("span");
              chip.className = "chip";
              chip.textContent = `${key}: ${value ? "done" : "pending"}`;
              checklist.appendChild(chip);
            });

            const statusHistory = document.getElementById("statusHistory");
            statusHistory.innerHTML = "";
            (observation.status_history || []).forEach((status) => {
              const chip = document.createElement("span");
              chip.className = "chip";
              chip.textContent = status;
              statusHistory.appendChild(chip);
            });

            document.getElementById("internalNotes").textContent =
              (observation.internal_notes || []).length
                ? observation.internal_notes.join("\\n\\n")
                : "No notes yet.";

            const history = document.getElementById("history");
            history.innerHTML = "";
            (observation.action_history || []).forEach((item) => {
              const event = document.createElement("div");
              event.className = "event";
              event.innerHTML =
                `<strong>Step ${item.step_index}</strong><div class="small">${item.action_type}</div>` +
                `<div class="mono small">${JSON.stringify({ value: item.value, message: item.message }, null, 2)}</div>`;
              history.appendChild(event);
            });

            document.getElementById("rewardBox").textContent = reward
              ? JSON.stringify(reward, null, 2)
              : "No step executed yet.";
          }

          async function loadTasks() {
            const response = await fetch("/tasks");
            const data = await response.json();
            taskSelect.innerHTML = "";
            data.tasks.forEach((task) => {
              const option = document.createElement("option");
              option.value = task.task_id;
              option.textContent = `${task.title} (${task.difficulty})`;
              taskSelect.appendChild(option);
            });
          }

          async function resetEnvironment() {
            const response = await fetch("/reset", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ task_id: taskSelect.value }),
            });
            const observation = await response.json();
            renderObservation(observation);
            setMessage(`Loaded ${observation.task_id}.`, true);
          }

          async function refreshState() {
            const response = await fetch("/state");
            const data = await response.json();
            if (data.observation) {
              renderObservation(data.observation);
              setMessage(`State refreshed for ${data.active_task_id}.`, true);
            } else {
              setMessage("No active episode yet. Reset a task first.");
            }
          }

          async function sendStep() {
            const payload = {
              action: {
                action_type: actionType.value,
                value: actionValue.value,
                message: actionMessage.value,
              },
            };
            const response = await fetch("/step", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload),
            });
            const data = await response.json();
            renderObservation(data.observation, {
              reward: data.reward,
              done: data.done,
              info: data.info,
            });
            setMessage(
              `Action applied. Reward ${data.reward.value.toFixed(4)}. Done: ${data.done}.`,
              true
            );
          }

          document.getElementById("resetButton").addEventListener("click", resetEnvironment);
          document.getElementById("stateButton").addEventListener("click", refreshState);
          document.getElementById("stepButton").addEventListener("click", sendStep);

          (async () => {
            try {
              await loadTasks();
              await refreshState();
            } catch (error) {
              setMessage(`Failed to load frontend data: ${error}`);
            }
          })();
        </script>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/tasks")
def tasks() -> dict:
    return {"tasks": ENVIRONMENT.list_tasks()}


@app.post("/reset", response_model=SupportObservation)
def reset(request: Optional[ResetRequest] = None) -> SupportObservation:
    task_id = request.task_id if request else None
    return ENVIRONMENT.reset(task_id=task_id)


@app.post("/step", response_model=StepResponse)
def step(request: StepRequest) -> StepResponse:
    return ENVIRONMENT.step(request.action)


@app.get("/state", response_model=EnvironmentState)
def state() -> EnvironmentState:
    return ENVIRONMENT.state()


def main() -> None:
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
