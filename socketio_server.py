import socketio

sio_server = socketio.AsyncServer(
    # Asynchronous Service Gateway Interface
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    # socketio_path='sockets' # default: 'socket.io'
)


@sio_server.event
async def connect(sid, environ, auth):
    print(f'{sid}: connected via socket.io')


@sio_server.event
async def session_request(sid, data):
    room = "room_id"
    # room = data['session_id']
    print("Joining room:", room)
    await sio_server.enter_room(sid, room)
    # sets the room_id/session_id
    await sio_server.emit("session_confirm", "room_id", room=sid)


@sio_server.event
async def user_uttered(sid, data):
    await sio_server.emit("bot_uttered", {'text': f"{data['message']}-response"}, room="room_id")

@sio_server.event
async def video_stream(sid, data):
    print(data)
    await sio_server.emit("bot_uttered", {'text': f"got image"}, room="room_id")


@sio_server.event
async def disconnect(sid):
    print(f'{sid}: disconnected from socket.io')
