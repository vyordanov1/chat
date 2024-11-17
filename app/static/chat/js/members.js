let location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;
const usernameBlockDate = JSON.parse(document.getElementById('user_block_date').textContent);
let chatButtons = document.querySelectorAll('#start-chat-btn');

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/members/'
);
function updateStatus(data){
    let membersDivs = document.getElementsByClassName('member-info');
    let logged_users = Object.values(data['logged_users']);
    for (const memberDiv of membersDivs ) {
        let currentUser = memberDiv.textContent.trim();
        memberDiv.innerHTML = currentUser;
        if (logged_users.includes(currentUser)) {
            memberDiv.innerHTML += ' <i class="fa-solid fa-check"></i>'
        } else {
            memberDiv.innerHTML += ' <i class="fa-solid fa-xmark" style="color:red"></i>'
        }
    }
}

for (let button of chatButtons) {
    if (usernameBlockDate !== '') {
        button.addEventListener('pointerdown', function (e) {
            alert("You have been blocked from entering chat rooms until: " + usernameBlockDate)
        })
    }
}


chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    updateStatus(data);
};
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

