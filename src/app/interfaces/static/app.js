const fileInput = document.querySelector("#quotation-file");
const dropzone = document.querySelector(".dropzone");
const fileName = document.querySelector("[data-file-name]");
const form = document.querySelector("[data-upload-form]");

function showFile(file) {
  if (!file) return;
  fileName.textContent = file.name;
  dropzone.classList.remove("is-dragging");
}

fileInput?.addEventListener("change", () => showFile(fileInput.files[0]));
["dragenter", "dragover"].forEach((eventName) => {
  dropzone?.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.add("is-dragging");
  });
});
["dragleave", "drop"].forEach((eventName) => {
  dropzone?.addEventListener(eventName, (event) => {
    event.preventDefault();
    if (eventName === "drop") {
      const file = event.dataTransfer.files[0];
      if (file?.type === "application/pdf") {
        fileInput.files = event.dataTransfer.files;
        showFile(file);
      }
    } else {
      dropzone.classList.remove("is-dragging");
    }
  });
});
form?.addEventListener("submit", () => {
  const button = form.querySelector("button");
  button.disabled = true;
  button.querySelector("span").textContent = "Extracting quotation...";
});

const feedback = document.querySelector("[data-action-feedback]");
document.querySelectorAll("[data-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const fields = [...document.querySelectorAll("[data-review-field]")];
    const missing = fields.filter((field) => field.required && !field.value.trim());
    if (button.dataset.action === "validate" && missing.length) {
      feedback.textContent = "Add a cost center before validating this draft.";
      feedback.classList.add("is-warning");
      missing[0].focus();
      return;
    }
    const messages = {
      queue: "Draft queued for internal review.",
      validate: "Required review fields look complete.",
      prepare: "Draft prepared for the next approval step.",
    };
    feedback.textContent = `${messages[button.dataset.action]} Nothing has been sent.`;
    feedback.classList.remove("is-warning");
    button.classList.add("is-complete");
  });
});

document.querySelectorAll("[data-row-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const row = button.closest("[data-review-row]");
    const status = row.querySelector("[data-row-status]");
    const onboarded = row.querySelector("[data-onboarded]");
    const costCenter = row.querySelector(".table-input");
    const badge = row.querySelector(".queue-badge");
    const statusCell = row.querySelector("[data-request-status]");
    const emailFeedback = document.querySelector("[data-email-feedback]");
    if (button.dataset.rowAction === "validate") {
      if (onboarded && costCenter && (!onboarded.value || !costCenter.value.trim())) {
        status.textContent = "Needs data";
        status.classList.add("row-status--warning");
        return;
      }
      status.textContent = "Validated";
      status.classList.remove("row-status--warning", "row-status--rejected");
      status.classList.add("row-status--validated");
      if (badge) {
        badge.textContent = "Validated";
        badge.classList.remove("queue-badge--pending");
        badge.classList.add("queue-badge--validated");
      }
      if (statusCell) statusCell.dataset.requestStatus = "validated";
      if (emailFeedback) {
        emailFeedback.textContent = "Validated. Demo email prepared — no email was delivered.";
        emailFeedback.classList.remove("is-warning");
      }
    } else {
      status.textContent = "Rejected";
      status.classList.remove("row-status--warning", "row-status--validated");
      status.classList.add("row-status--rejected");
      if (badge) {
        badge.textContent = "Rejected";
        badge.classList.remove("queue-badge--pending", "queue-badge--validated");
        badge.classList.add("queue-badge--rejected");
      }
      if (statusCell) statusCell.dataset.requestStatus = "rejected";
      if (emailFeedback) {
        emailFeedback.textContent = "Request rejected. No email was prepared.";
        emailFeedback.classList.add("is-warning");
      }
    }
    applyQueueFilter();
  });
});

const queueRows = document.querySelector("[data-queue-rows]");
let activeQueueFilter = "all";
function applyQueueFilter() {
  queueRows?.querySelectorAll("[data-review-row]").forEach((row) => {
    const status = row.querySelector("[data-request-status]")?.dataset.requestStatus;
    row.hidden = activeQueueFilter !== "all" && status !== activeQueueFilter;
  });
  document.querySelectorAll("[data-queue-filter]").forEach((tab) => {
    const count = [...(queueRows?.querySelectorAll("[data-review-row]") || [])]
      .filter((row) => tab.dataset.queueFilter === "all" || row.querySelector("[data-request-status]")?.dataset.requestStatus === tab.dataset.queueFilter)
      .length;
    const countLabel = tab.querySelector("b");
    if (countLabel) countLabel.textContent = String(count).padStart(2, "0");
  });
}
document.querySelectorAll("[data-queue-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    activeQueueFilter = button.dataset.queueFilter;
    document.querySelectorAll("[data-queue-filter]").forEach((tab) => {
      const active = tab === button;
      tab.classList.toggle("queue-tab--active", active);
      tab.setAttribute("aria-selected", String(active));
    });
    applyQueueFilter();
  });
});
