function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function notifyConnectionSuccessful() {
    console.log("connected");
    // document.getElementById("chat").innerText = "Connection successful."
}

function notifyConnectionFailed() {
    console.log("connection failed");
    // document.getElementById("chat").innerText = "Connection failed."
}

var socket = io({
    auth: { token: getCookie("auth_id") || "unauthenticated" }
});

socket.on('connect', () => {
    notifyConnectionSuccessful();
    socket.emit('newUser', { user: getCookie("authId") });
});

socket.on('connect_error', (data) => {
    console.log(data)
    notifyConnectionFailed();
});

socket.on('move', (data) => {
    if (data) {
        window.location = "/pp"
    } else {
        window.location = "/"
    }
});

socket.on('kick', () => {
    window.location = "/logout";
});

socket.on('ping', () => {
    alert("received ping");
});

export function socketEmit(event, data) {
    socket.emit(event, data)
}