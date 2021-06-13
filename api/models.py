from pydantic import BaseModel
from typing import List


class Entity(BaseModel):
    name: str
    reg: int  # UNIX Timestamp
    hash: str
    seeders: int
    leeches: int
    url: str
    last_updated: int  # UNIX Timestamp, last time parser found element


class SearchResponse(BaseModel):
    data: List[Entity]
