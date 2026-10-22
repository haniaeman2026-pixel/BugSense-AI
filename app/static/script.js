const form = document.getElementById("bug-form");
const textarea = document.getElementById("bug-description");
const charCount = document.getElementById("char-count");
const analyzeButton = document.getElementById("analyze-button");
const buttonLabel = document.getElementById("button-label");
const formError = document.getElementById("form-error");
const workflowMessage = document.getElementById("workflow-message");
const resultsSection = document.getElementById("results-section");
const toast = document.getElementById("toast");
let lastReport = null;
let toastTimer = null;

textarea.addEventListener("input", () => { charCount.textContent = `${textarea.value.length} / 8000`; });
document.querySelectorAll("[data-example]").forEach(button => {
  button.addEventListener("click", () => {
    textarea.value = button.dataset.example;
    textarea.dispatchEvent(new Event("input"));
    textarea.focus();
  });
});

function setWorkflowState(index, state) {
  document.querySelectorAll(".workflow-step").forEach((step, i) => {
    step.classList.remove("running", "complete");
    const status = step.querySelector(".step-status");
    if (i < index || (state === "complete" && i === index)) {
      step.classList.add("complete"); status.textContent = "COMPLETE";
    } else if (i === index && state === "running") {
      step.classList.add("running"); status.textContent = "RUNNING";
    } else {
      status.textContent = "WAITING";
    }
  });
}
function resetWorkflow() {
  document.querySelectorAll(".workflow-step").forEach(step => {
    step.classList.remove("running", "complete");
    step.querySelector(".step-status").textContent = "WAITING";
  });
}
function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2800);
}
function text(id, value) { document.getElementById(id).textContent = value || "Not specified"; }
function renderReport(report) {
  lastReport = report;
  text("report-title", report.title);
  text("report-feature", report.affected_feature);
  text("report-severity-reason", report.severity_reason);
  text("report-summary", report.summary);
  text("report-original", report.original_description);
  text("investigation-notes", report.investigation_notes);
  const badge = document.getElementById("severity-badge");
  const severity = ["critical", "high", "medium", "low"].includes(String(report.severity).toLowerCase()) ? String(report.severity).toLowerCase() : "medium";
  badge.textContent = severity[0].toUpperCase() + severity.slice(1);
  badge.className = `severity-badge ${severity}`;
  const list = document.getElementById("root-causes");
  list.replaceChildren();
  (Array.isArray(report.possible_root_causes) ? report.possible_root_causes : []).forEach(cause => {
    const li = document.createElement("li"); li.textContent = cause; list.appendChild(li);
  });
  if (!list.children.length) { const li = document.createElement("li"); li.textContent = "No specific cause suggested. Gather logs and reproduction steps."; list.appendChild(li); }
  text("generated-at", `Generated ${new Date().toLocaleString()}`);
  resultsSection.hidden = false;
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}
form.addEventListener("submit", async event => {
  event.preventDefault();
  const description = textarea.value.trim();
  formError.hidden = true;
  if (description.length < 10) {
    formError.textContent = "Please enter at least 10 characters describing the issue.";
    formError.hidden = false; textarea.focus(); return;
  }
  analyzeButton.disabled = true;
  buttonLabel.textContent = "Analyzing issue…";
  workflowMessage.textContent = "Running the analysis workflow…";
  resultsSection.hidden = true;
  setWorkflowState(0, "running");
  try {
    const response = await fetch("/api/analyze", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Could not analyze this bug.");
    if (!data.report) throw new Error("The server returned an empty report.");
    setWorkflowState(3, "complete");
    workflowMessage.textContent = "Workflow completed successfully";
    renderReport(data.report);
  } catch (error) {
    resetWorkflow();
    workflowMessage.textContent = "Analysis needs attention";
    formError.textContent = error.message || "Something went wrong. Check the server terminal and try again.";
    formError.hidden = false;
    showToast("Analysis could not be completed.");
  } finally {
    analyzeButton.disabled = false;
    buttonLabel.textContent = "Analyze bug report";
  }
});
document.getElementById("copy-button").addEventListener("click", async () => {
  if (!lastReport) return;
  const report = lastReport;
  const output = [
    `BUG REPORT: ${report.title || ""}`,
    `Affected feature: ${report.affected_feature || ""}`,
    `Severity: ${report.severity || ""}`,
    `Severity reason: ${report.severity_reason || ""}`,
    `Summary: ${report.summary || ""}`,
    "Possible root causes:",
    ...(report.possible_root_causes || []).map((cause, i) => `${i + 1}. ${cause}`),
    `Original description: ${report.original_description || ""}`,
    `Investigation notes: ${report.investigation_notes || ""}`
  ].join("\n");
  try {
    await navigator.clipboard.writeText(output);
    showToast("Bug report copied to clipboard.");
  } catch {
    const area = document.createElement("textarea"); area.value = output; document.body.appendChild(area); area.select();
    const copied = document.execCommand("copy"); area.remove();
    showToast(copied ? "Bug report copied to clipboard." : "Copy failed. Please select and copy the report manually.");
  }
});
