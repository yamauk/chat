$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port+'/chat');
    socket.on('join',function(data){
        displayMessage(data)
    });

    socket.on('my response', function(data) {
        displayMessage(data)
    });

    socket.on('connect_proc',function(data){
        displayMessage(data)
        displayMembers(data)
    });
    socket.on('disconnect_proc',function(data){
        displayMessage(data)
        displayMembers(data)
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
    var str="<li class=\"message\">"+"<font color=\""+data.color+"\">"+data.username+"</font> > <font color=\""+data.color+"\">"+data.message+"</font></li>"
    $("#message").prepend(str);
}
function displayMembers(data) {
    $("#member li").remove()
    for (var i=0;i<data.userlist.length;i++){
        $("#member").prepend("<li><font color=\""+data.colors[i]+"\">"+data.userlist[i]+"</font></li>");
    }
}
