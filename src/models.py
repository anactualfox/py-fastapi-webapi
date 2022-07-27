from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    id: Optional[UUID]
    first_name: str
    last_name: str
    middle_name: Optional[str]
