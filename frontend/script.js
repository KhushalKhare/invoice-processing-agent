const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const statusText = document.getElementById("statusText");
const uploadBtn = document.getElementById("uploadBtn");

fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
        fileName.textContent = fileInput.files[0].name;
        statusText.textContent = "";
    }
});

async function upload() {
    if (!fileInput.files.length) {
        statusText.textContent = "Please select a PDF invoice first.";
        statusText.className = "status error";
        return;
    }

    const file = fileInput.files[0];

    if (file.type !== "application/pdf") {
        statusText.textContent = "Only PDF files are supported.";
        statusText.className = "status error";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Processing...";
    statusText.textContent = "Extracting invoice data...";
    statusText.className = "status";

    try {
        const res = await fetch("http://127.0.0.1:8000/process", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (!res.ok || data.status === "error") {
            throw new Error(data.message || "Invoice processing failed.");
        }

        renderResult(data);

        statusText.textContent = "Invoice processed successfully.";
        statusText.className = "status success";

    } catch (error) {
        statusText.textContent = error.message;
        statusText.className = "status error";
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = "Process Invoice";
    }
}

function renderResult(data) {
    const extracted = data.extracted_data || {};

    document.getElementById("emptyState").classList.add("hidden");
    document.getElementById("resultView").classList.remove("hidden");

    document.getElementById("vendorName").textContent = extracted.vendor_name || "-";
    document.getElementById("invoiceNumber").textContent = extracted.invoice_number || "-";
    document.getElementById("invoiceDate").textContent = extracted.invoice_date || "-";
    document.getElementById("dueDate").textContent = extracted.due_date || "-";

    const amount = extracted.total_amount ?? "-";
    const currency = extracted.currency || "";
    document.getElementById("totalAmount").textContent =
        amount === "-" ? "-" : `${currency} ${amount}`;

    const issuesBox = document.getElementById("issuesBox");

    if (data.issues && data.issues.length > 0) {
        issuesBox.classList.remove("hidden");
        issuesBox.innerHTML = `
            <strong>Issues detected:</strong>
            <ul>
                ${data.issues.map(issue => `<li>${issue}</li>`).join("")}
            </ul>
        `;
    } else {
        issuesBox.classList.add("hidden");
        issuesBox.innerHTML = "";
    }
}