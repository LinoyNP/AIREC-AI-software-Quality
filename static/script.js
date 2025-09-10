// ----------DOM ELEMENTS----------
let socket = null;
let chatBox;
let inputField;
let sendButton;
let welcomeScreen;

// ----------INITIALIZATION----------
document.addEventListener("DOMContentLoaded", function () {
    cacheDomElements();
    setupFormListener();
    initializeSocket();
    registerServiceWorker();
});

function cacheDomElements() {
    chatBox = document.getElementById("chat-box")
    inputField = document.getElementById("codeInput");
    sendButton = document.getElementById("send-btn")
    welcomeScreen = document.getElementById("welcome-screen");
}

// ----------FORM HANDLING----------
function setupFormListener() {
    sendButton.addEventListener("click", sendMessage);

    inputField.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    inputField.addEventListener("input", function () {
        autoGrow(this);
    });
}

// ----------SOCKET CONNECTION----------
function initializeSocket() {
    //Only if there is an active internet connection, the socket that connects to the backend will be opened, 
    // otherwise the site will be operated in online mode
    if (!navigator.onLine) {
        console.log("No internet connection - socket will not run");
        return;
    }

    try {
        socket = io();
        setupSocketEvents();
    } catch (err) {
        console.error("Error connecting to Socket.IO:", err);
    }
}

function setupSocketEvents() {
    socket.on('connect', handleSocketConnect);
    socket.on('disconnect', handleSocketDisconnect);
    socket.on('connect_error', handleSocketError);
    socket.on('code_result', handleServerResult);
}

function handleSocketConnect() {
    console.log("Connection to server successful");
    socket.emit('my event', { data: "I'm connected!" });//עדיין לא הבנתי למי ההודעה מיועדת
}

function handleSocketDisconnect() {
    console.log("You are disconnected from the server, you are taken offline.");
}

function handleSocketError(err) {
    console.warn("You are taken offline- error connecting to server:", err);
}

//----------MESSAGE HANDLING----------
function sendMessage() {
    const userMessage = inputField.value.trim();
    if (userMessage === "") return;

    addUserMessage(userMessage);

    if (!navigator.onLine || !socket || !socket.connected) {
        // Offline mode → Local operation activation
        runLocalModel(userMessage);
    } else {
        socket.emit("send_code", { code: userMessage });
    }

    inputField.value = "";
    autoGrow(inputField);
}

function addUserMessage(text) {
    appendMessage(text, "user");
}

function handleServerResult(data) {
    appendMessage(data.result, "bot");
}

function appendMessage(message, sender) {
    // If the welcome screen is visible, wait for it to disappear
    if (
        !chatBox.hasChildNodes() &&
        welcomeScreen &&
        !welcomeScreen.classList.contains("welcome-hidden")
    ) {
        welcomeScreen.classList.add("welcome-hidden");
        setTimeout(() => {
            welcomeScreen.style.display = "none";
            appendMessage(message, sender);
        }, 500);
        return;
    }

    // Create message bubble
    const msg = document.createElement("div");
    msg.classList.add("message", sender);

    // Render markdown instead of plain text
    if (typeof marked !== "undefined") {
        msg.innerHTML = marked.parse(message);
    } else {
        msg.textContent = message;
    }

    // Create copy button
    const copyBtn = document.createElement("button");
    copyBtn.classList.add("copy-btn");
    // Icon created by shin_icons - Flaticon
    // Link: https://www.flaticon.com/free-icons/ui
    copyBtn.innerHTML = `<img src="static/icons/copy.png" alt="Copy" />`;

    copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(message);
        copyBtn.style.opacity = "1";
        setTimeout(() => (copyBtn.style.opacity = "0.5"), 800);
    });

    msg.appendChild(copyBtn);

    // Append to chat box
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* Auto-growing textarea */
function autoGrow(element) {
    element.style.height = "auto";
    element.style.height = element.scrollHeight + "px";
}

// ----------OFFLINE MODE----------
function runLocalModel(code) {
    // The actions that will be performed offline
    // =========================
    // TODO:
    // ----------------------------------------------MODEL AI
    appendMessage("You are offline.\n Local result for: " + code, "bot");
}

// ----------SERVICE WORKER----------
function registerServiceWorker() {
    // Register the Service Worker
    // This code ensures the Service Worker (managing the logic of requests) is registered only after the entire page has fully loaded,
    // which is a best practice to avoid blocking the initial page load.
    // It's recommended to place this in main application JavaScript file.
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service_worker.js')
                .then(registration => {
                    // Service Worker registration successful
                    console.log('Service Worker registered with scope:', registration.scope);
                })
                .catch(error => {
                    // Service Worker registration failed
                    console.error('Service Worker registration failed:', error);
                });
        });
    }
}