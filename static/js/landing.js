getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

notifyConnectionSuccessful = () => {
    console.log("connected");
    document.getElementById("chat").innerText = "Connection successful."
}

notifyConnectionFailed = () => {
    console.log("failed to connect");
    document.getElementById("chat").innerText = "Connection failed."
}

//
// SOCKETS
//
var socket = io({
    auth: {
        token: getCookie("auth_id") || "unauthenticated"
    }
});

socket.on('connect', () => {
    notifyConnectionSuccessful();
    socket.emit('newUser', { user: getCookie("authId") });
});

socket.on('connect_error', (data) => {
    notifyConnectionFailed();
});

socket.on('moveUser', (data) => {
    console.log(data);
    if (data) window.location = "/pp";
});
