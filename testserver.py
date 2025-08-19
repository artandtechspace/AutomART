from flask import Flask,render_template,request, send_from_directory
from flask_socketio import SocketIO, emit
import subprocess
import time

app = Flask(__name__)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*')


@app.route('/app/<path:filename>')
def access_webapp(filename):
    return send_from_directory("./webdir", filename)

@socketio.on("my_event")
def checkping():
    emit('server', { "yoink": time.time() })

@socketio.on('disconnect')
def test():
    print("Hi im disconnected")