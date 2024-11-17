function getCSRFToken() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return csrfToken;
}
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const username = JSON.parse(document.getElementById('user').textContent);
const messages = JSON.parse(document.getElementById('messages').textContent);
const csrfToken = getCSRFToken();
let currentTime = new Date();
let time = currentTime.toLocaleTimeString();
let location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

function addMessage(data) {
    let messageContainer = document.querySelector("#chat__message__container");
    let div = document.createElement("div");
    div.className = (data.username === username) ? "chat-message left" : "chat-message right";
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

}

for (const [key, value] of Object.entries(messages)) {
    addMessage(value);
} // populate all messages from db to chat view window

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data); // Get message from socket
    addMessage(data); // add it to the current chat view
    if (data.message != '') { // hit the endpoint to write the message in the db
        if (data.username === username) {
            fetch(location + '/chat/api/send-message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    sender: data.username,
                    content: data.message,
                    room: roomName,
                })
            })
                .then(data => {
                    console.log('Message sent!');
                })
                .catch(error => {
                    console.log(error.message);
                });
        }
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
