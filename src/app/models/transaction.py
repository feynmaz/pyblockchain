from pydantic import BaseModel


class Transaction(BaseModel):
    sender: str
    reveiver: str
    amount: float
