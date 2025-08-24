from flask import Flask, send_from_directory, redirect, request
from flask_socketio import SocketIO, send
import Config

app = Flask(__name__)
socketio = SocketIO(app, ping_interval=0.25, ping_timeout=1, async_mode='eventlet', cors_allowed_origins='*', transports=['websocket'])

# Stores connected internal and external clients
internal_clients = []
external_clients = []

# Sends given data to all internal connections
def sendToInternals(channel: str, data):
    for sid in internal_clients:
        socketio.emit(channel, data, room=sid)

# Sends given data to all external connections
def sendToExternals(channel: str, data):
    for sid in external_clients:
        socketio.emit(channel, data, room=sid)

# Hosts webapp
@app.route("/")
def index_file():
    return access_webapp("index.html")

@app.route('/<path:filename>')
def access_webapp(filename):
    return send_from_directory("./rsc/webapp", filename)


@socketio.on('connect')
def on_connect(auth):
    is_internal_flag_set = isinstance(auth, dict) and auth['internal'] == True
    is_internal = request.remote_addr == '127.0.0.1' and is_internal_flag_set

    # Adds the address
    if is_internal:
        internal_clients.append(request.sid)
    else:
        external_clients.append(request.sid)

    print("Client connected: ",request.remote_addr, "Internal: ",is_internal)


@socketio.on('disconnect')
def on_disconnect(_ = None):
    if request.sid in internal_clients:
        internal_clients.remove(request.sid)
    if request.sid in external_clients:
        external_clients.remove(request.sid)
        sendToInternals('ext_disconnect', {})

    print("Client disconnected: ",request.remote_addr)


#region External 2 Internal

@socketio.on('joystick')
def handle_message_joystick(data):
    # Echos data to internal devices
    sendToInternals('i_joystick', data)

@socketio.on('emoji')
def handle_message_emoji(data):
    # Echos data to internal devices
    sendToInternals('i_emoji', data)

#endregion

#region Internal 2 External
@socketio.on('status')
def handle_message_status(data):
    # Echos data to external devices
    sendToExternals('e_status', data)

#endregion


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=Config.PORT, debug=True)
