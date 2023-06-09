from datetime import datetime

from pydantic import BaseModel

from .transaction import Transaction


class Block(BaseModel):
    index: int
    timestamp: datetime
    proof: int
    previous_hash: str
    data: str
    transactions: list[Transaction]
