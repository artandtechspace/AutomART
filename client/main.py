import socketio
import MovementController
import Display
import time
import Config

# Create a Socket.IO client
sio = socketio.Client()

# Time to wait until the next status
nextStatusAt = -1


# Define the event handler for when the connection is established
@sio.event
def connect():
    print("Connected to server!")
    MovementController.setMovement(0,0)


# Define the event handler for receiving messages
@sio.event
def i_joystick(data):
    MovementController.setMovement(data['angle'], data['dist'])

@sio.event
def i_emoji(data):
    emoji_type = data['type']
    Display.onSelectAnimation(emoji_type)


# Define the event handler for errors
@sio.event
def disconnect():
    print("Disconnected from server")
    MovementController.setMovement(0,0)

@sio.event
def ext_disconnect(_):
    print("External client disconnected")
    MovementController.setMovement(0,0)

# Function to send data periodically or continuously in a loop
def main():
    global nextStatusAt

    Display.setupDisplay()
    MovementController.setupMovement()

    while True:
        try:
            # Connect to the Flask server
            sio.connect(
                f'http://localhost:{Config.PORT}', transports=['websocket'],
                auth={'internal': True}
            )

            while True:
                Display.loopDisplay()
                MovementController.loopMovement()

                if time.time() > nextStatusAt:
                    nextStatusAt = time.time() + 0.5

                    # Collects information and sends the status
                    sio.emit('status', {
                        'emoji': Display.get_selected_animation()
                    })


                sio.sleep(0.1)

        except:
            print("Connection error, retrying...")
            time.sleep(1)

# Start the data-sending loop
main()
