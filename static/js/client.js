var socket = io();
var user = "user" + Math.floor(Math.random() * 10);
var currentRoom = "room1";

socket.on('connect', (sock) => {
    console.log("connected");
    socket.emit('newUser', { user: user });
});

socket.on('connect_error', (data) => {
    console.log(data)
});

socket.on('moveUser', (data) => {
    console.log(data)
    if (user === data.user)
    {
        const newRoom = "room" + data.to;
        console.log(newRoom);
        socket.emit("ackMove", { user: user, from: currentRoom, to: newRoom });
        currentRoom = newRoom;
    }
});

socket.on('ping', () => {
    console.log("ping");
});