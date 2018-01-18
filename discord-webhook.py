import asyncio
import aiohttp

async def post_message(**params):
	session = aiohttp.ClientSession()
	async with session.post("https://discordapp.com/api/webhooks/403375654000656385/02oivqnUojFXCapa1Z_N0PjwheLl9WqPJpC4plGV0PhqOyZ9tnsiUUV1ZJ8noJYAvTPY", json=params) as resp:
		pass
	session.close()
