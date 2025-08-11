var socket = io();
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});


function sendCodeToServer() {
  const userCode = document.getElementById("codeInput").value;
  socket.emit('send_code', { code: userCode });
}

socket.on('code_result', (data) => {
  document.getElementById("output").innerText = data.result;
});




