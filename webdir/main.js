
function main() {
    const socket = io(); //socketio connection to server//
    socket.on("connect", () => {
        console.log("connected");
        document.getElementById("header").innerHTML = "<h3>" + "Websocket Connected" + "</h3";
    });

    socket.on("disconnect", () => {
        console.log("disconnected");
        document.getElementById("header").innerHTML = "<h3>" + "Websocket Disconnected" + "</h3>";
    });

    function myupdate() {
        //Event sent by Client
        socket.emit("my_event", function () {
        });
    }

    // Event sent by Server//
    socket.on("server", function (msg) {
        alert(JSON.stringify(msg));
    });

    const submitBtn = document.querySelector("#checkbutton")
    submitBtn.addEventListener("click", myupdate);

}


window.onload = main;