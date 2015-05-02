# coding:utf-8

import sys

# エンコードをUTFにする
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi, sleep

ws_list = set()

def chat_handle(environ, start_response):
    web_socket = environ['wsgi.websocket']
    ws_list.add(web_socket)

    print 'enter:', len(ws_list), environ['REMOTE_ADDR'], environ[
        'REMOTE_PORT']

    while True:
        msg = web_socket.receive()
        if msg is None:
            break

        remove = set()
        for s in ws_list:
            try:
                s.send(msg)
                # エラー発生時はメッセージを消す
            except Exception:
                remove.add(s)

        for s in remove:
            ws_list.remove(s)

    print 'exit:', environ['REMOTE_ADDR'], environ['REMOTE_PORT']
    ws_list.remove(web_socket)

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'


# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "ようこそ"
    # index.html をレンダリングする
    return render_template('index.html',
                           title=title)

# /post にアクセスしたときの処理
@app.route('/login', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        # セッション変数に格納
        if len(request.form['name']) != 0:
            session['name'] = request.form['name']
            return redirect(url_for('chat'))
    return redirect(url_for('index'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html', name=session['name'])


# ユーザ情報のjsonを/_jsonに書き込み
@app.route('/_json')
def test_json():
    user_data = {'username':session['name']}
    return jsonify(user_data)

if __name__ == '__main__':
    #app.debug = True  # デバッグモード有効化
    # app.run()
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
