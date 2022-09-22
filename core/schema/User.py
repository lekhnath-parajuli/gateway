from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    uid: Optional[int]
    firstname: str
    lastname: str
