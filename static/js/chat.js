function sendMessage() {
    //ユーザデータを読み込み，メッセージを表示
    $.getJSON("/_json", function(data){
        var message = $(':text[name=message-input]').val();
        ws.send(message)
        $("ul").prepend("<li>"+data["username"]+" > "+message+"</li>");
        //値のクリア
        $(':text[name=message-input]').val('')
    });
}


function displayMessage(data) {
    $("ul").prepend("<li>"+data["username"]+" > "+data['message']+"</li>");
}

function sendMessage2(ws){
        var message = $(':text[name=message-input]').val();
        $.getJSON("/_json", function(user_info){
        ws.send({'username':user_info['username'],'message':message})
        });
}
function init() {

    ws = new WebSocket('ws://localhost:5000/chat');
    //メッセージの受信
    ws.onmessage = function(data) {
        displayMessage(data)
    };
    //メッセージの送信
    $('button[name=message-button]').click(sendMessage2(ws))
}

$(document).ready(function(){
    init()
    $('button[name=message-button]').click(sendMessage)
});

function DebugPrint(str)
{
    var out = document.getElementById("debug");
    if (!out) return;
    out.value += str;
}