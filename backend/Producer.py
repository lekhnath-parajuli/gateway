from aio_pika import connect, Message

from config import config


class Producer:
    def __init__(self, service: str) -> None:
        self.service = service

    async def send(self, message: dict):
        producer = await connect(config.RABBITMQ_SERVER)
        async with producer:
            channel = await producer.channel()
            queue = await channel.declare_queue(self.service)
            await channel.default_exchange.publish(
                Message(body=await message),
                routing_key=queue.name
            )


