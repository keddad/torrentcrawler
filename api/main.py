from fastapi import FastAPI
from models import SearchResponse
from database import object_to_entity, torrents

app = FastAPI()


@app.get("/", response_model=SearchResponse)
async def search(skip: int = 0, limit: int = 50, min_peers: int = 0, max_peers: int = 1_000_000, min_leeches: int = 0,
                 max_leeches: int = 1_000_000):
    data = await torrents.find().skip(skip).limit(limit).to_list(length=limit + 1)  # TODO

    return SearchResponse(data=list(map(object_to_entity, data)))
