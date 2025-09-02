// var socket = io();

// socket.on('connect', function() {
//     socket.emit('my event', {data: 'I\'m connected!'});
// });

// function sendCodeToServer() {
//   const userCode = document.getElementById("codeInput").value;
  
//   addUserMessage(userCode);

//   socket.emit('send_code', { code: userCode });

//   document.getElementById("codeInput").value = "";
// }

// socket.on('code_result', (data) => {
//   addBotMessage(data.result);
// });


// function addUserMessage(text) {
//   const messages = document.getElementById("messages");
//   const date = new Date();
//   const str_time = date.getHours() + ":" + String(date.getMinutes()).padStart(2, '0');

//   const userHtml = `
//     <div class="d-flex justify-content-end mb-4">
//       <div class="msg_cotainer_send">
//         ${text}
//         <span class="msg_time_send">${str_time}</span>
//       </div>
//       </div>
//     </div>`;
  
//   messages.insertAdjacentHTML("beforeend", userHtml);
//   scrollToBottom(messages);
// }
// function addBotMessage(text) {
//   const messages = document.getElementById("messages");
//   const date = new Date();
//   const str_time = date.getHours() + ":" + String(date.getMinutes()).padStart(2, '0');

//   const botHtml = `
//     <div class="d-flex justify-content-start mb-4">
//       <div class="img_cont_msg">
//         <img src="{{ url_for('static', filename='Airec.png') }}" class="rounded-circle user_img_msg">
//       </div>
//       <div class="msg_cotainer">
//         ${text}
//         <span class="msg_time">${str_time}</span>
//       </div>
//     </div>`;
  
//   messages.insertAdjacentHTML("beforeend", botHtml);
//   scrollToBottom(messages);
// }

// function scrollToBottom(container) {
//   container.scrollTop = container.scrollHeight;
// }


document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("chatForm").addEventListener("submit", function(e) {
        e.preventDefault();
        sendCodeToServer();
})});

let socket = null;
//Only if there is an active internet connection, the socket that connects to the backend will be opened, 
// otherwise the site will be operated in online mode
if (navigator.onLine) {
  try {
    socket = io();
    socket.on('connect', function() {
      console.log("Connection to server successful");
      socket.emit('my event', {data: 'I\'m connected!'});
     });

    socket.on('disconnect', function() {
      console.warn("You are disconnected from the server, you are taken offline.");
    });

    socket.on('connect_error', function(err) {
      console.warn("You are taken offline- error connecting to server:", err);
    });
    // socket.on('code_result', (data) => {
    //   document.getElementById("output").innerText = data.result;
    // });
    
    socket.on('code_result', (data) => {
      const container = document.getElementById("messages");   
      const newResult = document.createElement("div");       
      newResult.textContent = data.result;                  
      container.appendChild(newResult);
      container.scrollTop = container.scrollHeight; 
    });
  }
  catch (err) {
    console.error("Error connecting to Socket.IO:", err);
  }
} 
else {
  console.warn("No internet connection - socket will not run");
}


function sendCodeToServer() {
  const userCode = document.getElementById("codeInput").value;
   addUserMessage(userCode);
  if (!navigator.onLine|| !socket || !socket.connected) {
    // Offline mode → Local operation activation
    runLocalModel(userCode);
  } else {
    socket.emit('send_code', { code: userCode });
  }
  document.getElementById("codeInput").value = "";
};

function addUserMessage(text) {
  const container = document.getElementById("messages");
  const div = document.createElement("div");
  div.textContent = text;
  div.classList.add("user-message"); // אפשר להוסיף CSS אם רוצים
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
};

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

function runLocalModel(code) {
  // The actions that will be performed offline
  const container = document.getElementById("messages");
  const div = document.createElement("div");
  div.textContent = "You are offline.\n Local result for: " + code;
  // div.classList.add("offline-result");
  div.classList.add("user-message");
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}




// var socket = io();

// socket.on('connect', function() {
//     socket.emit('my event', {data: 'I\'m connected!'});
// });


// function sendCodeToServer() {
//   const userCode = document.getElementById("codeInput").value;
//   socket.emit('send_code', { code: userCode });
// }


// // socket.on('code_result', (data) => {
// //   document.getElementById("output").innerText = data.result;
// // });

// socket.on('code_result', (data) => {
//   const container = document.getElementById("output");   
//   const newResult = document.createElement("div");       
//   newResult.textContent = data.result;                  
//   container.appendChild(newResult);
// });