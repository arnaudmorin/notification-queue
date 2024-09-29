import socketio

# Create an instance of the SocketIO client
sio = socketio.Client()


# Define events the client should listen for
@sio.event
def connect():
    print("Connection established with the WebSocket server")
    # Send a request to connect to the queue
    sio.emit('connect_queue', {'queue': 'webex'})


@sio.event
def new_message(data):
    print(f"New message received: {data}")


@sio.event
def no_messages(data):
    print("No messages in the queue right now.")


@sio.event
def error(data):
    print(f"Error received: {data}")


@sio.event
def disconnect():
    print("Disconnected from the WebSocket server")


# Connect to the server
sio.connect('https://5.196.197.1:35800')  # Replace with your server's address
sio.wait()
