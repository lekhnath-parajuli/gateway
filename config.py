from pydantic import BaseSettings


class Config(BaseSettings):
    HOST: str = 'localhost'
    PORT: int = 8080
    RABBITMQ_SERVER: str = 'amqp://guest:guest@localhost/'
    ALLOWED_TOPICS: list = [
        'user'
    ]


config = Config()
