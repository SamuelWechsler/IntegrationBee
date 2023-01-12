import time
import websocket
import threading
import json
import sys

from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject


ID = None


class Signals(QObject):
    message = pyqtSignal(str, str)


class Client(QRunnable):
    def __init__(self,  ip, username):
        super(Client, self).__init__()

        self.signals = Signals()

        self.username = username
        self.ws = websocket.WebSocketApp(f"ws://{ip}",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def on_message(self, ws, message):
        global ID
        message = json.loads(message)
        if message["type"] == "init":
            ID = message["id"]
            print("connecton established")
        elif message["type"] == "broadcast":
            if message["sender"] == ID:
                return
            self.signals.message.emit(message['username'], message['msg'])

    def on_error(self, ws, error):
        print('error:', error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### connection closed ###")

    def on_open(self, ws):
        event = {
            "type": "init",
            "username": self.username,
        }

        ws.send(json.dumps(event))
        print("connecting...")

    def send(self, msg):
        event = {
            "type": "send_message",
            "msg": msg,
        }
        self.ws.send(json.dumps(event))

    @pyqtSlot()
    def run(self):
        self.ws.run_forever()
