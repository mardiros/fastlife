from starlette.responses import JSONResponse

from fastlife import websocket_view
from fastlife.adapters.fastapi.websocket import GenericWebSocket


@websocket_view("ws", "/ws/json")
async def ws_json(sock: GenericWebSocket):
    await sock.accept()
    await sock.send_json({"msg": f"Hello {sock.registry.settings.domain_name}"})
    new_message = await sock.receive_json()
    await sock.send_json(new_message)
    await sock.close()


@websocket_view("ws", "/ws/text")
async def ws_text(sock: GenericWebSocket):
    await sock.accept()
    await sock.send_text(f"Hello {sock.registry.settings.domain_name}")
    new_message = await sock.receive_text()
    await sock.send_text(new_message)
    await sock.close()


@websocket_view("ws", "/ws/bytes")
async def ws_bytes(sock: GenericWebSocket):
    await sock.accept()
    await sock.send_bytes(f"Hello {sock.registry.settings.domain_name}".encode())
    new_message = await sock.receive_bytes()
    await sock.send_bytes(new_message)
    await sock.close()


@websocket_view("ws", "/ws/denied")
async def ws_denied(sock: GenericWebSocket):
    await sock.accept()
    await sock.send_denial_response(
        JSONResponse({"error": "invalid_token"}, status_code=403)
    )
    await sock.close()
