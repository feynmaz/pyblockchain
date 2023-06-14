from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field


def make_uuid() -> str:
    return str(uuid4()).replace('-', '')


class Settings(BaseModel):
    node_address: str = Field(description='', default_factory=make_uuid)


settings = Settings()
