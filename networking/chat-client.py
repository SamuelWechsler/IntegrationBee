import time
import websocket
import threading
import json
import sys

ID = None

if len(sys.argv) == 3:
    ip = sys.argv[1]
    username = sys.argv[2]
else:
    ip = input("ip: ")
    username = input("username: ")


def on_message(ws, message):
    global ID
    message = json.loads(message)
    if message["type"] == "init":
        ID = message["id"]
        print("connecton established")
    elif message["type"] == "broadcast":
        if message["sender"] == ID:
            return
        print(f"\r{message['username']}> {message['msg']}")
        print("> ", end="", flush=True)


def on_error(ws, error):
    print('error:', error)


def on_close(ws, close_status_code, close_msg):
    print("### connection closed ###")


def on_open(ws):
    event = {
        "type": "init",
        "username": username,
    }

    ws.send(json.dumps(event))
    print("connecting...")


websocket.enableTrace(False)
ws = websocket.WebSocketApp(f"ws://{ip}",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)


def send_message(msg):
    event = {
        "type": "send_message",
        "msg": msg,
    }
    ws.send(json.dumps(event))


threading.Thread(target=ws.run_forever).start()

time.sleep(1)

try:
    while True:
        send_message(input("> "))
except KeyboardInterrupt:
    ws.close()
