// Vendor Portal Interactions
document.addEventListener("DOMContentLoaded", () => {
    console.log("VendorBridge portal initialized");
    
    // Form submission validation
    const submitBtn = document.getElementById("submit_quotation_btn");
    const quoteForm = document.getElementById("vendor_quote_form");
    
    if (submitBtn && quoteForm) {
        submitBtn.addEventListener("click", (e) => {
            e.preventDefault();
            if (validateQuotationForm()) {
                submitQuotation();
            }
        });
    }
});

function validateQuotationForm() {
    const delivery = document.getElementById("delivery_days_input");
    if (!delivery || !delivery.value) {
        alert("Please enter the delivery days.");
        return false;
    }
    
    const itemRows = document.querySelectorAll(".quote-item-row");
    if (itemRows.length === 0) {
        alert("No items found in this Request for Quotation.");
        return false;
    }
    
    let allPricesFilled = true;
    itemRows.forEach(row => {
        const priceInput = row.querySelector(".item-price-input");
        if (!priceInput || !priceInput.value || parseFloat(priceInput.value) <= 0) {
            allPricesFilled = false;
        }
    });
    
    if (!allPricesFilled) {
        alert("Please fill in a valid unit price for all items.");
        return false;
    }
    
    return true;
}

function submitQuotation() {
    const formEl = document.getElementById("vendor_quote_form");
    if (!formEl) return;
    
    // Simulate successful submission
    const successModal = document.getElementById("portal_success_modal");
    if (successModal) {
        successModal.style.display = "flex";
    } else {
        alert("Quotation submitted successfully!");
    }
}
