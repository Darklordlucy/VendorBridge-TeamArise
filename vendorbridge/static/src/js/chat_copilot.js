/** @odoo-module **/

export class CopilotChat {
    constructor(containerId, inputId, sendButtonId, messagesId) {
        this.container = document.getElementById(containerId);
        this.input = document.getElementById(inputId);
        this.sendButton = document.getElementById(sendButtonId);
        this.messagesContainer = document.getElementById(messagesId);
        
        if (this.sendButton && this.input) {
            this.sendButton.addEventListener("click", () => this.sendMessage());
            this.input.addEventListener("keypress", (e) => {
                if (e.key === "Enter") this.sendMessage();
            });
        }
    }

    sendMessage() {
        const text = this.input.value.trim();
        if (!text) return;

        this.addMessage(text, "user");
        this.input.value = "";

        // Show typing indicator
        const typingId = this.showTypingIndicator();

        // Simulate API call to Odoo backend
        setTimeout(() => {
            this.removeTypingIndicator(typingId);
            const response = this.getMockResponse(text);
            this.addMessage(response, "copilot");
        }, 1200);
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `chat-message ${sender}-message`;
        messageDiv.style.marginBottom = "12px";
        messageDiv.style.display = "flex";
        messageDiv.style.justifyContent = sender === "user" ? "flex-end" : "flex-start";

        const bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.style.padding = "8px 16px";
        bubble.style.borderRadius = "12px";
        bubble.style.maxWidth = "75%";
        bubble.style.fontSize = "14px";
        bubble.style.lineHeight = "1.4";

        if (sender === "user") {
            bubble.style.backgroundColor = "var(--cyprus, #004643)";
            bubble.style.color = "var(--sand, #F0EDE5)";
            bubble.style.borderBottomRightRadius = "2px";
        } else {
            bubble.style.backgroundColor = "var(--sand-dark, #E4DFD5)";
            bubble.style.color = "var(--text-primary, #001E1D)";
            bubble.style.borderBottomLeftRadius = "2px";
        }

        bubble.innerText = text;
        messageDiv.appendChild(bubble);
        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    showTypingIndicator() {
        const id = "typing-" + Date.now();
        const indicatorDiv = document.createElement("div");
        indicatorDiv.id = id;
        indicatorDiv.className = "chat-message copilot-message typing-indicator";
        indicatorDiv.style.marginBottom = "12px";
        indicatorDiv.style.display = "flex";
        indicatorDiv.style.justifyContent = "flex-start";

        const bubble = document.createElement("div");
        bubble.style.padding = "8px 16px";
        bubble.style.borderRadius = "12px";
        bubble.style.borderBottomLeftRadius = "2px";
        bubble.style.backgroundColor = "var(--sand-dark, #E4DFD5)";
        bubble.style.color = "var(--text-primary, #001E1D)";
        bubble.style.fontSize = "14px";
        bubble.innerText = "Copilot is typing...";

        indicatorDiv.appendChild(bubble);
        this.messagesContainer.appendChild(indicatorDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        return id;
    }

    removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    getMockResponse(query) {
        const lower = query.toLowerCase();
        if (lower.includes("pending approval") || lower.includes("approve")) {
            return "You have 2 pending purchase approvals:\n1. RFQ-2026-003: IT Equipment (₹1,25,000)\n2. RFQ-2026-004: Office Desks (₹45,000)";
        }
        if (lower.includes("spend") || lower.includes("cost")) {
            return "Acme Corp's total spend this month (MTD) is ₹3,24,000.00, which is 14% lower than last month's trend.";
        }
        if (lower.includes("vendor") || lower.includes("cheapest") || lower.includes("best")) {
            return "Our top performing vendor is Delhi Hardware Hub, with a rating of 4.8★ and 98% on-time delivery.";
        }
        return "I am the Procurement Copilot. Ask me about pending approvals, monthly spend, or top vendor performances!";
    }
}
