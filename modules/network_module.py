# modules/network_module.py
from .base_module import BaseModule
import aiohttp
import asyncio
from typing import List, Union

class NetworkModule(BaseModule):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Union[str, None]:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            self.log(f"Error: {e}")
            return None

    async def process_tasks(self, tasks: List) -> List:
        results = await asyncio.gather(*tasks)
        return results
