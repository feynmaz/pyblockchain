from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from src.app.models.block import Block


class MineBlock(BaseModel):
    message: str
    index: int
    timestamp: datetime = Field()
    proof: int
    previous_hash: str


class GetChain(BaseModel):
    chain: list[Block]
    length: int

    def __init__(self, chain: list[Block]):
        super().__init__(chain=chain, length=len(chain))
