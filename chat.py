# coding:utf-8

# エンコードをUTFにする
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# ロガー設定
import logging

logging.basicConfig()

import re
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'
socketio = SocketIO(app)


@socketio.on('join', namespace='/chat')
def join(data):
    username = data['username']
    room = "makalu_chat"
    join_room(room)
    emit('join', {'message': 'Hello ' + username, 'username': 'admin'},
         room=room, namespace='/chat', broadcast=True)


@socketio.on('my broadcast event', namespace='/chat')
def test_message(data):
    emit('my response',
         {'username': session['username'], 'message': link_it(data['message'])},
         broadcast=True)


@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response',
         {'message': 'Hello ' + session['username'] + ".",
          'username': 'admin'}, broadcast=True)


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    emit('my response',
         {'message': 'Bye ' + session['username'] + ".", 'username': 'admin'},
         broadcast=True)
    session.clear()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        # 入力値のバリデーションはJSで実行済み
        session['username'] = request.form['login-input']
        return render_template('chat.html')


def link_it(value):
    URL_PATTERN = r'([^"]|^)(https?)(://[\w:;/.?%#&=+-]+)'
    return re.compile(URL_PATTERN).sub(r'\1<a href="\2\3" target="_blank">\2\3</a>', value)
link_it.is_safe = True


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0')

    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app,
    # handler_class=WebSocketHandler)
    # server.serve_forever()
