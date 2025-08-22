from flask import Flask, send_from_directory, redirect, request
from flask_socketio import SocketIO, send
import Config

app = Flask(__name__)
socketio = SocketIO(app, ping_interval=0.25, ping_timeout=1, async_mode='eventlet', cors_allowed_origins='*', transports=['websocket'])

# Stores connected internal clients
internal_clients = []

# Sends given data to all internal connections
def sendToInternals(channel: str, data):
    for sid in internal_clients:
        socketio.emit(channel, data, room=sid)


# Hosts webapp
@app.route("/")
def index_file():
    return access_webapp("index.html")

@app.route('/<path:filename>')
def access_webapp(filename):
    return send_from_directory("./rsc/webapp", filename)


@socketio.on('connect')
def on_connect():
    if request.remote_addr == '127.0.0.1':
        # Adds the address
        internal_clients.append(request.sid)

    print("Client connected: ",request.remote_addr)


@socketio.on('disconnect')
def on_disconnect(_ = None):
    if request.sid in internal_clients:
        internal_clients.remove(request.sid)
    else:
        sendToInternals('ext_disconnect', {})

    print("Client disconnected: ",request.remote_addr)


@socketio.on('joystick')
def handle_message_joystick(data):
    # Echos data to internal devices
    sendToInternals('i_joystick', data)

@socketio.on('emoji')
def handle_message_emoji(data):
    # Echos data to internal devices
    sendToInternals('i_emoji', data)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=Config.PORT, debug=True)
