from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field


class Settings(BaseModel):
    node_address: str = Field(description='', default_factory=str(uuid4()).replace('-', ''))


settings = Settings()
