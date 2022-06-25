# PubSub Handler Adapted from here: https://github.com/SlackingVeteran/twitch-pubsub

import asyncio
import json
import sqlite3
import uuid
import websockets

from camera import CameraMover


class PubSubHandler:

    def __init__(self):
        self.connection = None
        self.pubsub_topics = ["channel-points-channel-v1.71631229"]
        self.auth_token = None

    @staticmethod
    def get_auth_token():
        # DB connection for getting the auth_token
        db_con = sqlite3.connect('G:/sqlite3/test.db')
        auth = db_con.execute('SELECT access_token FROM twitch_auth;').fetchone()[0]
        db_con.close()
        return auth

    async def connect(self):
        self.auth_token = self.get_auth_token()
        self.connection = await websockets.connect('wss://pubsub-edge.twitch.tv')
        if self.connection.open:
            msg = {"type": "LISTEN", "nonce": str(self.generate_nonce()),
                   "data": {"topics": self.pubsub_topics, "auth_token": self.auth_token}}
            json_msg = json.dumps(msg)
            await self.send_msg(json_msg)
            return self.connection

    @staticmethod
    def generate_nonce():
        return uuid.uuid1().hex

    async def send_msg(self, msg):
        await self.connection.send(msg)

    @staticmethod
    async def recv_msg(connection):
        while True:
            try:
                msg = await connection.recv()
                msg = json.loads(msg)
                if msg['type'] == "MESSAGE":
                    meaty_potatos = json.loads(msg['data']['message'])
                    if meaty_potatos['data']['redemption']['reward']['title'] == 'Screen Saver Camera':
                        CameraMover.move_camera()
                    # print(json.dumps(meaty_potatos, indent=4))
            except websockets.WebSocketException:
                break

    @staticmethod
    async def pingus(connection):
        while True:
            try:
                json_req = json.dumps({"type": "PING"})
                await connection.send(json_req)
                await asyncio.sleep(60)
            except websockets.WebSocketException:
                break
