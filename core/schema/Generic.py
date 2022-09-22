from socket import timeout
from pydantic import BaseModel

from .User import UserModel


class GeneticModel(BaseModel):
    service: str
    timeout: float = 0.1
    user: UserModel
