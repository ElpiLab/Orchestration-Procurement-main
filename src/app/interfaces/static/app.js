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
