import asyncio
import aiohttp
import json
import random

from utils.timer import Timer
from utils.EventHook import EventHook

#Create new exception to raise on multiple different types of connection errors
class ConnectionError(Exception):
    pass

class PubSub:

    def __init__(self):
        self.pong_received = False
        self.listens = []
        self.onMsg = EventHook()
        self.onListenError = EventHook()
        self.onError = EventHook()
        self.pingTimer = Timer(300, self._ping) #Timer to ping every 5 minutes
        self.pongTimer = Timer(10, self._pong) #Timer to check if pong received every 5 minutes

    async def connect(self, listens):
        """Function to handle auto reconnecting in case of connection failure"""
        self.reconnect_time = 1 #Set time to wait before connecting to 1 second
        self.active = True
        while True:
            try: #Try to connect
                await asyncio.sleep(self.reconnect_time)
                await self._connection(listens)
            except ConnectionError: #On connection error
                #Error report
                #If internet is still up, this will send, meaning Twitch is down
                #If internet is down, this will silently fail which means the internet connection on the bot is down
                self.onError("Twitch PubSub connection lost")
                #Close session
                await self.session.close()
                #Cancel timers for checking pings
                self.pongTimer.cancel()
                self.pingTimer.cancel()
                #Disable listen loop
                self.listening = False
                #Double reconnect timer, up to 2 minutes
                self.reconnect_time *= 2
                if self.reconnect_time > 120:
                    self.reconnect_time = 120

    async def _connection(self, listens):
        """Function to connect and call listen function"""
        try: #Try to connect
            self.session = aiohttp.ClientSession()
            self.ws = await self.session.ws_connect("wss://pubsub-edge.twitch.tv", verify_ssl=True) #Connect to PubSub WebSocket
            for i in listens: #For the topics to listen to, send to PubSub
                await self.add_listen(listens[i], i)
            self.pingTimer.start_loop() #Start timer for pinging every 5 minutes
            self.listening = True
            self.reconnect_time = 1 #Reset reconnect time
            #Report to Discord that connection was gained
            self.onError("Successful connection to Twitch PubSub")
            await self._listen()
        except aiohttp.client_exceptions.ClientConnectorError: #On connection error from initial connection attempt
            raise ConnectionError()

    async def _listen(self):
        """Function to listen for messages from PubSub, sending appropriate messages to parse_message"""
        try:
            while self.listening:
                msg = await self.ws.receive_json()
                if msg["type"] == "PONG":
                    self.pong_received = True
                elif msg["type"] == "RECONNECT":
                    raise ConnectionError()
                elif msg["type"] == "MESSAGE":
                    await self._parse_message(msg)
                elif msg["type"] == "RESPONSE" and msg["error"] != "": #if response to topic listens and there is an error
                    self.onListenError(msg["error"], msg["nonce"])
                else:
                    pass
        except TypeError: #On connection lost (connection lost in this stage raises a TypeError)
            raise ConnectionError()

    async def _ping(self):
        await asyncio.sleep(random.randint(1, 50) / 1000) #Wait for random time from 1ms to 50ms
        self.ws.send_json({"type": "PING"}) #Send ping
        self.pong_received = False
        self.pongTimer.start() #Start 10 second timer to see if PONG received

    async def _pong(self):
        if not self.pong_received:
            pass #TODO: code reconnect

    async def _parse_message(self, resp):
        """Function to parse messages and pass them to the discord webhook"""
        resp["data"]["message"] = json.loads(resp["data"]["message"])
        self.onMsg(resp)

    async def add_listen(self, listen, userid):
        """Function to add another topic to listen to"""
        if userid not in self.listens:
            await self.ws.send_json(listen)
            self.listens.append(userid)

    async def remove_listen(self, listen, userid):
        """Function to unlisten from a topic"""
        if userid in self.listens:
            await self.ws.send_json(listen)
            self.listens.remove(userid)
        