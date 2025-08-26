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

var socket = io();

socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});


function sendCodeToServer() {
  const userCode = document.getElementById("codeInput").value;
   addUserMessage(userCode);
  socket.emit('send_code', { code: userCode });
    document.getElementById("codeInput").value = "";
};


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

function addUserMessage(text) {
  const container = document.getElementById("messages");
  const div = document.createElement("div");
  div.textContent = text;
  div.classList.add("user-message"); // אפשר להוסיף CSS אם רוצים
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
};







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