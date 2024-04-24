var socket = io();
var users = {};

socket.on('connect', () => {
    console.log("connected");
});

socket.on('connect_error', (data) => {
    console.log(data)
});

socket.on('userConnected', (data) => {
    console.log("User connected:", data.user);
    addUser(data.user);
});

socket.on('userDisonnected', (data) => {
    console.log("User disconnected:", data.user);
    removeUser(data.user);
});

addUser = (user) => {
    users[user] = 1;
};

removeUser = (user) => {
    delete users[user];
    resetRooms();
};

moveUser = (room) => {
    let user = document.getElementById("user").value;
    console.log(user);
    users[user] = room;
    socket.emit('move', { user: user, to: room });
    resetRooms();
    document.getElementById("users" + room).innerHTML = user;
};

pingRoom = (room) => {
    socket.emit("pingRoom", { room: room });
};

resetRooms = () => {
    document.getElementById("users1").innerHTML = "";
    document.getElementById("users2").innerHTML = "";
    document.getElementById("users3").innerHTML = "";
};