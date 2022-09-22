from typing import ByteString
import aio_pika
from aio_pika import Message


class Producer:
    @classmethod
    async def produce(cls, channel: aio_pika.channel.Channel, queue: aio_pika.queue.Queue, message: ByteString):
        await channel.default_exchange.publish(
            Message(body=message),
            routing_key=queue.name)
