from datetime import datetime

from pydantic import BaseModel


class Block(BaseModel):
    hash: str
    index: int
    timestamp: datetime
    proof: int
    previous_hash: str
    data: str
