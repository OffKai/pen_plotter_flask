const ROOMS = ["waiting", "room1", "room2", "room3"]

getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

var socket = io("/admin", { auth: { token: getCookie("auth_id") }});
var users = { waiting: [], room1: "", room2: "", room3: "" };

//
// ADMIN SOCKETS
//
socket.on('connect', () => {
    console.log("connected");
});

socket.on('connect_error', (data) => {
    console.log(data)
});

socket.on('userConnected', (data) => {
    console.log("User connected:", data.user);
    refreshManifest();
});

socket.on('userDisonnected', (data) => {
    console.log("User disconnected:", data.user);
    refreshManifest();
});

socket.on('updateManifest', () => {
    refreshManifest();
});

//
// UI RENDERING
//
renderRooms = () => {
    for (let room of ROOMS) {
        document.getElementById(room).innerHTML = users[room].length === 0 ? "" : users[room].reduce((acc, next) => acc + ", " + next);
    }
};

//
// USERS MANIFEST API
//
refreshManifest = () => {
    fetch("/oke-pp-admin/user-manifest")
            .then(resp => resp.json())
            .then(data => users = data)
            .then(() => renderRooms())
            .catch(console.log);
}

//
// USER CONTROL (SOCKETS)
//
moveUser = (roomIndex) => {
    let user = document.getElementById("user").value;
    socket.emit('move', { user: user, to: roomIndex });
    renderRooms();
};

kickUser = () => {
    let user = document.getElementById("user").value;
    socket.emit('kick', { user: user });
    renderRooms();
};

pingRoom = (roomIndex) => {
    socket.emit("pingRoom", { room: roomIndex });
};

addEventListener("load", () => { refreshManifest() });
