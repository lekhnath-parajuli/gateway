import asyncio
import json
import aio_pika
from aio_pika.abc import AbstractIncomingMessage



class Consumer:
    response_: dict = None

    @classmethod
    async def listen(cls, queue: aio_pika.queue.Queue, timeout: float) -> dict:
        cls.response_ = {}
        await queue.consume(callback=cls.callback, no_ack=True)
        await asyncio.sleep(timeout)
        if cls.response_ == {}:
            return {"message": "please try to increase time out and see if it works"}
        return cls.response_
    
    @classmethod
    async def callback(cls, message: AbstractIncomingMessage):
        cls.response_ = json.loads(message.body)