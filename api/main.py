from pprint import pprint

from fastapi import FastAPI
from models import SearchResponse
from database import object_to_entity, torrents

app = FastAPI()


@app.get("/", response_model=SearchResponse)
async def search(skip: int = 0, limit: int = 50, min_seeders: int = 0, max_seeders: int = 1_000_000,
                 min_leeches: int = 0, max_leeches: int = 1_000_000, name: str = None):
    await torrents.create_index([("name", "text")])

    q = {"$and": [
        {"seeders": {"$gte": min_seeders}},
        {"seeders": {"$lte": max_seeders}},
        {"leeches": {"$gte": min_leeches}},
        {"leeches": {"$lte": max_leeches}},
    ]}

    if name is not None:
        q["$and"].append({"$text": {"$search": name}})

    data = await torrents.find(q) \
        .skip(skip).limit(limit).to_list(length=limit + 1)

    return SearchResponse(data=list(map(object_to_entity, data)))
