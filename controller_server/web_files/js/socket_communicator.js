var loc = window.location.host;
var ws = new WebSocket("ws://"+loc +":8765/");
var TOKEN = null;
ws.onopen = function (event) {
    ws.send(JSON.stringify({ cmd: "client_login", pass: "secret" }))
}


//============Websocket Code============

ws.onmessage = function (event) {
    var msg = JSON.parse(event.data)

    console.log(msg);

    if (msg['msgtype'] == "notify" && 'login' in msg) {
        TOKEN = msg['token'];
        updateAnimation(msg['POND_STATUS'])
    } else if (msg['msgtype'] == "cmd" && msg['cmd'] == 'update') {
        updateAnimation(msg['POND_STATUS'])
        console.log(msg["POND_STATUS"]);
    }

};

var set_flow = function (self) {
    var target = (self.target.id == "west_ctrl") ? "pondPiWest" : "pondPiEast";
    var flow_value = (self.target.innerHTML == "Stop Pump") ? "false" : "true";
    ws.send(JSON.stringify({ msgtype: "cmd", cmd: "set_flow", target: target, flow_value: flow_value, token: TOKEN }))
    return
}
document.addEventListener("onload", init(), false);

function init(){
    for (const btn of document.getElementsByClassName("pausebtn")) {
        btn.addEventListener('click', set_flow);
    }
}

