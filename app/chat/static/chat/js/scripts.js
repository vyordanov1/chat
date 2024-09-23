const roomName = JSON.parse(document.getElementById('room-name').textContent);
const chatUser = JSON.parse(document.getElementById('chat_user').textContent);
const username = JSON.parse(document.getElementById('user').textContent);
let currentTime = new Date();
let time = currentTime.toLocaleTimeString();
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    let messageContainer = document.querySelector("#chat__message__container");
    let div = document.createElement("div");
    div.className = (data.username === chatUser) ? "chat-message right" : "chat-message left";
    if (data.message != '') {
        div.innerHTML = `<div class="message-content">
        <span class="message-username">${data.username.charAt(0).toUpperCase() + data.username.slice(1)}</span>
        <span class="message-text">${data.message}</span>
        <span class="message-timestamp">${data.time}</span>
        </div>`;
        document.querySelector("#chat-message-input").value = "";
        messageContainer.appendChild(div);
        // Scroll to the bottom of the chat container
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': username,
        'time': time
    }));
    messageInputDom.value = '';
};
