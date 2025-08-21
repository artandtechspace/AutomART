
// #region Config

// Address of server
const SERVER_ADDR = "AUTO";

// #endregion

const ANIMATIONS = {
    'cry': '😭',
    'heartEye': '😍',
    'joy': '😂',
    'mindblow': '🤯',
    'scream': '😱',
    'star': '🤩',
    'tongue': '😝',
    'imp-smile': '😈',
    'melting': '🫠',
    'party-face': '🥳',
    'silently-happy': '🙂',
    'star-struck': '🤩'
}


// Socket-IO-Server
let socket;

// Object with references to all ui elements
let uiElements;

function onClickEmoji(evt) {
    // Sends the event to the server
    socket.emit("emoji", {type: evt.target.getAttribute("data-name")})
}

function onJoyStick(angle, dist, x, y) {
    if(dist > 500) dist = 500;

    angle += Math.PI/2
    if(angle > Math.PI)
        angle -= 2*Math.PI

    // Sends the data
    socket.emit("joystick", {angle, dist: dist/500, x, y});
}

function onSocketLoseConnect() {
    uiElements.status.textContent = "Reconnecting";
    uiElements.status.classList.remove("connected");
    uiElements.status.classList.add("disconnected");
}

function onSocketConnect() {
    uiElements.status.textContent = "Connected";
    uiElements.status.classList.add("connected");
    uiElements.status.classList.remove("disconnected");
}



function setupUI(){

    // Creates the joystick
    const joystick = new JoystickController.default(
    {
        maxRange: 500,
        level: 100,
        radius: 150,
        joystickRadius: 80,
        opacity: 0.5,
        distortion: false,
        dynamicPosition: true,
        dynamicPositionTarget: document.getElementById("joystick"),
        mouseClickButton: "ALL",
        hideContextMenu: true,
    },
    ({ x, y, leveledX, leveledY, distance, angle }) => {
        if(socket !== undefined) onJoyStick(angle, distance, leveledX, leveledY);
    });

    // Gets the emoji bar
    const bar = document.querySelector('#emoji-bar');

    // Creates the buttons
    for(let name in ANIMATIONS) {
        let emoji = ANIMATIONS[name];

        const btn = document.createElement("input");
        btn.type = "button";
        btn.classList.add("emoji");
        btn.setAttribute('data-name', name);
        btn.value = emoji;

        btn.addEventListener("click", onClickEmoji);

        bar.appendChild(btn);
    }

    uiElements = {
        status: document.querySelector("#status"),
        joystick
    }
}

function main() {
    let addr = SERVER_ADDR;
    if(addr == 'AUTO')
        addr = window.location.host;

    setupUI();
    socket = io(`http://${addr}/`, {
        transports: ['websocket']
    });
    socket.on('connect', onSocketConnect);
    socket.on('disconnect', onSocketLoseConnect);

    onSocketLoseConnect();
}

window.onload = main;
