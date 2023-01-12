#!/usr/bin/env python

# https://websockets.readthedocs.io/en/stable/intro/tutorial2.html

import asyncio
import json
import websockets

HOST = "0.0.0.0"
PORT = 8000


USERNAMES = []
CONNECTIONS = set()
COUNT = -1


async def error(websocket, message):
    """
    Send an error message.

    """
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def play(websocket, user_id):
    """
    Receive and process moves from a player.

    """
    async for message in websocket:
        # Parse a "play" event from the UI.
        message = json.loads(message)

        assert message["type"] == "send_message"

        event = {
            "type": "broadcast",
            "sender": user_id,
            "username": USERNAMES[user_id],
            "msg": message["msg"],
        }

        websockets.broadcast(CONNECTIONS, json.dumps(event))


async def handler(websocket):
    global COUNT, USERNAMES
    """
    Handle a connection and dispatch it according to who is connecting.

    """
    remote_ip = websocket.remote_address
    print(f"Connecton from {remote_ip[0]}:{remote_ip[1]}")

    # Receive and parse the "init" event from the UI.

    message = await websocket.recv()
    message = json.loads(message)
    assert message["type"] == "init"

    USERNAMES.append(message['username'])
    COUNT += 1
    event = {
        "type": "init",
        "id": COUNT,
    }
    await websocket.send(json.dumps(event))

    CONNECTIONS.add(websocket)
    try:
        await play(websocket, COUNT)
    finally:
        remote_ip = websocket.remote_address
        print(f"Closed connecton to {remote_ip[0]}:{remote_ip[1]}")
        CONNECTIONS.remove(websocket)


async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Serving on {HOST}:{PORT}")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
