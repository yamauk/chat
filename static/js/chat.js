$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port+'/chat');
    socket.on('join',function(data){
        displayMessage(data)
    });

    socket.on('my response', function(data) {
        displayMessage(data)
    });

    $('#message-button').click(function(event) {
        if ($(':text[name=message-input]').val()!="" ){
            socket.emit('my broadcast event', {message: $('input[name=message-input]').val()});
            $(':text[name=message-input]').val('')
        }
        return false;
    });
});

//チャット画面にデータを表示
function displayMessage(data) {
    $("ul").prepend("<li>"+data.username+" > "+data.message+"</li>");
}
