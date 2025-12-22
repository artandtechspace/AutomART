import socketio
from client import Display, MovementController, Tank, Pump
import time
import Config

# Create a Socket.IO client
sio = socketio.Client()

# Time to wait until the next status
nextStatusAt = -1


# region Connect state events

# On: Self connected to server
@sio.event
def connect():
    print("Connected to server!")
    stop_all_systems()

# On: Self disconnected from server
@sio.event
def disconnect():
    print("Disconnected from server")
    stop_all_systems()

# On: External (Webpage) disconnected
@sio.event
def ext_disconnect(_):
    print("External client disconnected")
    stop_all_systems()

# endregion

# region Data sending

# Define the event handler for receiving messages
@sio.event
def i_joystick(data):
    MovementController.setMovement(data['angle'], data['dist'])

@sio.event
def i_emoji(data):
    emoji_type = data['type']
    Display.onSelectAnimation(emoji_type)
    notify_status()

@sio.event
def i_tank(data):
    Tank.turn_tank(data['state'])
    notify_status()

@sio.event
def i_pump(data):
    Pump.turn_pump(data['state'])
    notify_status()

# endregion



# Stops all systems
def stop_all_systems():
    MovementController.setMovement(0,0)
    Pump.turn_pump(False)
    Tank.turn_tank(False)

# Sends a status update to the frontend
def notify_status(force: bool = True):
    global nextStatusAt

    if time.time() > nextStatusAt or force:
        nextStatusAt = time.time() + 0.5

        # Collects information and sends the status
        sio.emit('status', {
            'emoji': Display.collect_status(),
            'tank': Tank.collect_status(),
            'pump': Pump.collect_status()
        })



# Function to send data periodically or continuously in a loop
def main():
    global nextStatusAt

    Display.setupDisplay()
    MovementController.setupMovement()
    Tank.setupTank()
    Pump.setupPump()

    while True:
        try:
            # Connect to the Flask server
            sio.connect(
                f'http://localhost:{Config.PORT}', transports=['websocket'],
                auth={'internal': True}
            )

            while True:
                Display.loopDisplay(notify_status)
                MovementController.loopMovement()
                Tank.loopTank()
                Pump.loopPump()

                notify_status(force=False)

                sio.sleep(0.1)

        except:
            print("Connection error, retrying...")
            time.sleep(1)

# Start the data-sending loop
main()
