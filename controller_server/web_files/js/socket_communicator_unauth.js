var loc = window.location.host;
var ws = new WebSocket("wss://"+loc +"/socket");
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


