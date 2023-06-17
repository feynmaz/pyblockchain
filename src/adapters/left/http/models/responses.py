from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from src.app.models.block import Block
from src.app.models.transaction import Transaction


class MineBlock(BaseModel):
    message: str
    index: int
    timestamp: datetime = Field()
    proof: int
    previous_hash: str
    transactions: List[Transaction]


class GetChain(BaseModel):
    chain: list[Block]
    length: int

    def __init__(self, chain: list[Block]):
        super().__init__(chain=chain, length=len(chain))


class IsValid(BaseModel):
    is_valid: bool
    message: Optional[str] = None


class ConnectNodes(BaseModel):
    message: str
    total_nodes: int
