from pydantic import BaseModel
from datetime import datetime

class Block(BaseModel):
    index: int
    timestamp: datetime
    proof: int
    previous_hash: str
    data: str
