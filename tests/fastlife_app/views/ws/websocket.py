from fastlife import WebSocket, websocket_view


@websocket_view("ws", "/ws")
async def ws(sock: WebSocket):
    await sock.accept()
    await sock.send_json({"msg": "Hello WebSocket"})
    await sock.close()
