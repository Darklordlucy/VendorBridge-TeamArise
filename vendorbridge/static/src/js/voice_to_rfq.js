/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

// A template or vanilla helper function to initialize Voice-to-RFQ
export function initVoiceToRFQ(buttonId, transcriptCallback) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.warn("Speech Recognition not supported in this browser.");
        return null;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    const button = document.getElementById(buttonId);
    if (!button) return null;

    recognition.onstart = () => {
        button.classList.add("recording");
        button.innerHTML = '<i class="fas fa-microphone-slash"></i> Listening...';
    };

    recognition.onspeechend = () => {
        recognition.stop();
    };

    recognition.onend = () => {
        button.classList.remove("recording");
        button.innerHTML = '<i class="fas fa-microphone"></i> Start Voice-to-RFQ';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log("Voice Transcript:", transcript);
        
        // Simple extraction logic
        const data = parseTranscript(transcript);
        if (transcriptCallback) {
            transcriptCallback(transcript, data);
        }
    };

    button.addEventListener("click", () => {
        recognition.start();
    });

    return recognition;
}

function parseTranscript(text) {
    const data = {
        title: "",
        qty: 1,
        item: "",
        deadline: ""
    };
    
    // Parse Qty (e.g. "50 laptops")
    const qtyMatch = text.match(/(\d+)\s+([a-zA-Z\s]+)/);
    if (qtyMatch) {
        data.qty = parseInt(qtyMatch[1], 10);
        data.item = qtyMatch[2].trim();
    }
    
    // Parse deadline
    const deadlineMatch = text.match(/by\s+([a-zA-Z0-9\s]+)$/i);
    if (deadlineMatch) {
        data.deadline = deadlineMatch[1].trim();
    }
    
    data.title = text;
    return data;
}
