# coding:utf-8

# エンコードをUTFにする
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# ロガー設定
import logging

logging.basicConfig()

import re
import redis
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'
socketio = SocketIO(app)
red = redis.Redis(host='localhost', port=6379, db=0)


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
         {'username': session['username'], 'color': session['color'],
          'message': link_it(data['message'])},
         broadcast=True)


@socketio.on('connect', namespace='/chat')
def test_connect():
    red.hmset(session['username'], session)
    userlist = red.keys()

    # ユーザ名の順番で色情報を配列に格納
    colors = []
    for key in userlist:
        colors.append(red.hgetall(key)['color'])

    emit('connect_proc',
         {'message': 'Hello ' + session['username'] + ".",
          'username': 'admin', 'color': session['color'],
          'userlist': userlist, 'colors': colors}, broadcast=True)


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    red.delete(session['username'])
    userlist = red.keys()

    # ユーザ名の順番で色情報を配列に格納
    colors = []
    for key in userlist:
        colors.append(red.hgetall(key)['color'])

    emit('disconnect_proc',
         {'message': 'Bye ' + session['username'] + ".", 'username': 'admin',
          'color': session['color'],
          'userlist': userlist},
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
        session['color'] = request.form['login-color']
        session['ip'] = request.remote_addr
        return render_template('chat.html')


def link_it(value):
    URL_PATTERN = r'([^"]|^)(https?)(://[\w:;/.?%#&=+-]+)'
    return re.compile(URL_PATTERN).sub(
        r'\1<a href="\2\3" target="_blank">\2\3</a>', value)


link_it.is_safe = True

if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    socketio.run(app, port=5555)
