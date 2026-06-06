/** @odoo-module **/

export function initQuoteReader(dropzoneId, fileInputId, formCallback) {
    const dropzone = document.getElementById(dropzoneId);
    const fileInput = document.getElementById(fileInputId);
    
    if (!dropzone || !fileInput) return;

    // Trigger input click when clicking the dropzone
    dropzone.addEventListener("click", () => {
        fileInput.click();
    });

    // Handle drag events
    dropzone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
    });

    dropzone.addEventListener("dragleave", () => {
        dropzone.classList.remove("dragover");
    });

    dropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0], dropzone, formCallback);
        }
    });

    fileInput.addEventListener("change", (e) => {
        const files = e.target.files;
        if (files.length > 0) {
            handleFileUpload(files[0], dropzone, formCallback);
        }
    });
}

function handleFileUpload(file, dropzone, callback) {
    if (!file.type.match('application/pdf') && !file.type.match('image.*')) {
        alert("Please upload a PDF or Image file.");
        return;
    }

    // Set loading state
    const originalContent = dropzone.innerHTML;
    dropzone.innerHTML = `
        <i class="fas fa-spinner fa-spin" style="font-size: 32px; color: var(--cyprus);"></i>
        <p style="margin-top:12px; font-weight: 500;">AI is reading your quotation PDF/Image...</p>
    `;
    
    // Simulate OCR + Gemini Extraction call
    setTimeout(() => {
        dropzone.innerHTML = originalContent;
        
        // Mock data response matching Gemini API extract structure
        const mockExtractedData = {
            vendor_name: "Delhi Hardware Hub",
            delivery_days: 5,
            items: [
                { name: "Dell Latitude 3440 Laptop", qty: 50, price: 42000 },
                { name: "Ergonomic Standing Office Desk", qty: 10, price: 15000 }
            ],
            tax_rate: 18,
            total_before_tax: 2250000,
            gst_amount: 405000,
            grand_total: 2655000
        };
        
        if (callback) {
            callback(mockExtractedData);
        }
    }, 2000);
}
