from aio_pika import connect
import aio_pika
from core.backend.Producer import Producer
from core.backend.Consumer import Consumer


class ConnectionManager:
    connection: aio_pika.connection.Connection
    channel: aio_pika.channel.Channel
    queues: dict[str, aio_pika.queue.Queue] = {}

    @classmethod
    async def start(cls, services: str, server: str, suffixes: list[str]) -> None:
        cls.connection = await connect(server)
        cls.channel = await cls.connection.channel()
        for service in services:
            for suffix in suffixes:
                name = f'{service}-{suffix}'
                cls.queues[name] = await cls.channel.declare_queue(name)
    
    @classmethod
    async def send(cls, service: str, message: dict):
        await Producer.produce(cls.channel, cls.queues[service], message.json().encode('UTF-8'))
    
    @classmethod
    async def receive(cls, service: str, timeout: float = 0):
        return await Consumer.listen(cls.queues[service], timeout=timeout)

    @classmethod
    async def stop(cls):
        await cls.connection.close()
