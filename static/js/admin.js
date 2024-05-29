const ROOMS = ["waiting", "room1", "room2", "room3"]

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

var users = { waiting: [], room1: [], room2: [], room3: [] };
var socket = io("/admin", { auth: { token: getCookie("auth_id") } });

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
    console.log("user connected:", data.user);
});

socket.on('userDisonnected', (data) => {
    console.log("user disconnected:", data.user);
});

socket.on('updateManifest', () => {
    console.log(users);
    refreshManifest();
});

//
// UI RENDERING
//
function renderRooms() {
    for (let room of ROOMS) {
        var ul = document.getElementById(room);
        if (ul == null) {
            continue;
        }

        // clear list
        ul.innerHTML = "";

        // re-populate list
        for (const [user, name] of users[room].entries()) {
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(name));
            li.setAttribute("id", `${room}-user${user}`);

            // clicking on a name auto-fills the name box
            li.addEventListener('click', (event) => {
                var text = event.target.textContent;
                console.log("selected user", text);
                document.getElementById("user").value = text;
            });

            ul.appendChild(li);
        }
    }
};


//
// USERS MANIFEST API
//
function refreshManifest() {
    fetch("/admin/user-manifest")
        .then(resp => resp.json())
        .then(data => users = data)
        .then(() => renderRooms())
        .catch(console.log);
}

//
// USER CONTROL (SOCKETS)
//
function moveUser(roomIndex) {
    let user = document.getElementById("user").value;
    if (user != "") {
        console.log(`moving ${user} to room ${roomIndex}`);
        socket.emit('move', { user: user, to: roomIndex });
        refreshManifest();
    }
};

function kickUser() {
    let user = document.getElementById("user").value;
    if (user != "") {
        console.log(`disconnecting ${user}`);
        socket.emit('kick', { user: user });
        refreshManifest();
    }
};

function pingRoom(roomIndex) {
    if (roomIndex < ROOMS.length) {
        console.log(`pinging room ${roomIndex}`);
        socket.emit("pingRoom", { room: roomIndex });
    }
};

addEventListener("DOMContentLoaded", () => {
    let copyButtons = document.querySelectorAll('.copy-invite-button')
    if (copyButtons) {
        copyButtons.forEach(function (button) {
            button.addEventListener('click', function (event) {
                navigator.clipboard.writeText(`${window.location.host}/login/${button.dataset.slug}`)
                    .then(() => {
                        alert(`Link copied to clipboard!\n\nDo not open this link yourself. Send it to ${button.dataset.guestname}.`);
                    })
                    .catch((err) => {
                        console.error('Error copying to clipboard:', err);
                    })
            });
        });
    }

    let move0 = document.getElementById("move0");
    if (move0) {
        move0.addEventListener("click", () => {
            moveUser(0);
        })
    }

    let move1 = document.getElementById("move1");
    if (move1) {
        move1.addEventListener("click", () => {
            moveUser(1);
        })
    }

    let move2 = document.getElementById("move2");
    if (move2) {
        move2.addEventListener("click", () => {
            moveUser(2);
        })
    }

    let move3 = document.getElementById("move3");
    if (move3) {
        move3.addEventListener("click", () => {
            moveUser(3);
        })
    }

    let kick = document.getElementById("kick");
    if (kick) {
        kick.addEventListener("click", () => {
            kickUser();
        })
    }

    let ping0 = document.getElementById("ping0");
    if (ping0) {
        ping0.addEventListener("click", () => {
            pingRoom(0);
        })
    }

    let ping1 = document.getElementById("ping1");
    if (ping1) {
        ping1.addEventListener("click", () => {
            pingRoom(1);
        })
    }

    let ping2 = document.getElementById("ping2");
    if (ping2) {
        ping2.addEventListener("click", () => {
            pingRoom(2);
        })
    }

    let ping3 = document.getElementById("ping3");
    if (ping3) {
        ping3.addEventListener("click", () => {
            pingRoom(3);
        })
    }

    refreshManifest();
});
