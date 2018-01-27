import asyncio

class Timer:

    def __init__(self, timeout, callback): #On initialization, store vars
        self._timeout = timeout
        self._callback = callback

    async def _job(self): #Job to run callback after timeout
        await asyncio.sleep(self._timeout)
        await self._callback()

    async def _loop(self): #Infinite loop that will run callback until task cancelled
        while True:
            await asyncio.sleep(self._timeout)
            await self._callback()

    def start_loop(self):
        """Function to start looping timer"""
        self._task = asyncio.ensure_future(self._loop())

    def start(self):
        """Function to start timer, running once"""
        self._task = asyncio.ensure_future(self._job())

    def cancel(self):
        """Function to cancel timer, both loop and normal"""
        try:
            self._task.cancel()
        except AttributeError:
            pass