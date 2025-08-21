import socketio
import MovementController
import Display
import time

# Create a Socket.IO client
sio = socketio.Client()

# Define the event handler for when the connection is established
@sio.event
def connect():
    print("Connected to server!")
    MovementController.setMovement(0,0, 0, 0)


# Define the event handler for receiving messages
@sio.event
def i_joystick(data):
    MovementController.setMovement(data['angle'], data['dist'], data['x'], data['y'])

@sio.event
def i_emoji(data):
    emoji_type = data['type']
    Display.onSelectAnimation(emoji_type)


# Define the event handler for errors
@sio.event
def disconnect():
    print("Disconnected from server")
    MovementController.setMovement(0,0, 0, 0)

@sio.event
def ext_disconnect(_):
    print("External client disconnected")
    MovementController.setMovement(0,0, 0, 0)

# Function to send data periodically or continuously in a loop
def main():
    Display.setupDisplay()
    MovementController.setupMovement()

    while True:
        try:
            # Connect to the Flask server
            sio.connect('http://localhost:80', transports=['websocket'])

            while True:
                Display.loopDisplay()
                MovementController.loopMovement()

                sio.sleep(0.1)

        except:
            print("Connection error, retrying...")
            time.sleep(1)

# Start the data-sending loop
main()
