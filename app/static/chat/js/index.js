let location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port;
const indexSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/index/'
);


indexSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const containerDiv = document.getElementsByClassName('counter-container')[0];
    containerDiv.innerHTML = "";
    for (let object of Object.values(data)) {
        let infoContainer = document.createElement('div');
        infoContainer.className = 'info-container';
        let heading = document.createElement('h4');
        heading.textContent = object.count;
        let dividerDiv = document.createElement('div');
        dividerDiv.className = 'divider';
        let divider = document.createElement('hr');
        let infoText = document.createElement('div');
        infoText.className = 'info-text';
        infoText.textContent = object.title;

        dividerDiv.appendChild(divider);
        infoContainer.appendChild(heading);
        infoContainer.appendChild(dividerDiv);
        infoContainer.appendChild(infoText);
        containerDiv.appendChild(infoContainer);
    }
};

indexSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
