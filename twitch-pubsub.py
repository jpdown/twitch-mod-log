import asyncio
import aiohttp
import json

listen = {}
listen["type"] = "LISTEN"
listen["nonce"] = "listen"
listen["data"] = {}
listen["data"]["topics"] = ["chat_moderator_actions.userid.roomid"]
listen["data"]["auth_token"] = "oauth"


async def connect(listens):
	"""Function to connect and listen for messages from PubSub"""
	session = aiohttp.ClientSession()
	async with session.ws_connect("wss://pubsub-edge.twitch.tv", verify_ssl=True) as ws: #Connect to PubSub WebSocket
		await ws.send_json(listens)
		while True:
			msg = await ws.receive_json()
			await parse_message(msg)

async def parse_message(json_msg):
	"""Function to parse messages and pass them to the discord webhook"""


asyncio.get_event_loop().create_task(connect(listen))
asyncio.get_event_loop().run_forever()
