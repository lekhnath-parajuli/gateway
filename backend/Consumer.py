from aio_pika import connect
import asyncio
from typing import Callable

from config import config


class Consumer:
    def __init__(self, service: str) -> None:
        self.service = service

    async def listen(self, callback: Callable):
        connection = await connect(config.RABBITMQ_SERVER)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.service)
            await queue.consume(callback=callback, no_ack=True)
