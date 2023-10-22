from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from socketio_server import sio_app

app = FastAPI(
    title="FastAPI Chat Sockets",
    debug=True,
    # swagger_ui_oauth2_redirect_url='/docs/oauth2-redirect',
    swagger_ui_init_oauth={
        "appName": "ai_services_backend",
        "scopes": "openid",
        "useBasicAuthenticationWithAccessCodeGrant": True,
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # List of allowed origins. You can use ["*"] to allow all origins.
    allow_credentials=True,
    allow_methods=["*"],  # List of allowed methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # List of allowed headers, e.g., ["Content-Type"]
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://0.0.0.0:8000/websocket");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
        <h1>WebSocket Chat</h1>
        <div id="rasa-chat-widget" data-websocket-url="ws://0.0.0.0:8000/chatbot/socket.io"></div>
        <script src="https://unpkg.com/@rasahq/rasa-chat" type="application/javascript"></script>
    </body>
</html>
"""


@app.get("/", tags=["public"])
def root():
    return HTMLResponse(html)


app.mount('/chatbot', app=sio_app)


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

