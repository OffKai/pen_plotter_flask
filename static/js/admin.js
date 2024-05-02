var socket = io("/admin", { auth: { token: "admin" }});
var users = { waiting: [], room1: "", room2: "", room3: "" };

socket.on('connect', () => {
    console.log("connected");
});

socket.on('connect_error', (data) => {
    console.log(data)
});

socket.on('userConnected', (data) => {
    console.log("User connected:", data.user);
    addUser(data.user, 0);
});

socket.on('userDisonnected', (data) => {
    console.log("User disconnected:", data.user);
    removeUser(data.user);
});

addUser = (user) => {
    users["waiting"].push(user);
    renderRooms();
};

/**
 * @param {string} room
 */
addUser = (user, room) => {
    if (room === 0)
        users["waiting"].push(user);
    else if (room >=1 && room <= 3)
        users["room" + room] = user;
    renderRooms();
};

removeUser = (user) => {
    users["waiting"] = users["waiting"].filter((value) => value !== user)
    if (users["room1"] === user) users["room1"] = "";
    if (users["room2"] === user) users["room2"] = "";
    if (users["room3"] === user) users["room3"] = "";
    renderRooms();
};

addUserToken = () => {
    let user = document.getElementById("user").value;
    socket.emit("addUserToken", { token: token, user: user });
};

addUserTokens = () => {
    for (let i=0; i < 10; i++)
    {
        let user = "user" + i;
        socket.emit("addUserToken", { token: user, user: user });
    }
};

moveUser = (room) => {
    let user = document.getElementById("user").value;
    socket.emit('move', { user: user, to: room });
    removeUser(user);
    addUser(user, room)
    renderRooms();
};

pingRoom = (room) => {
    socket.emit("pingRoom", { room: room });
};

renderRooms = () => {
    document.getElementById("waiting").innerHTML = users["waiting"].length === 0 ? "" : users["waiting"].reduce((acc, next) => acc + ", " + next);
    document.getElementById("users1").innerHTML = users["room1"];
    document.getElementById("users2").innerHTML = users["room2"];
    document.getElementById("users3").innerHTML = users["room3"];
};