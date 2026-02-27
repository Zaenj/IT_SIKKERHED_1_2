from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    person_id: int
    first_name: str
    last_name: str
    address: str
    street_number: str
    password: str
    enabled: bool = True