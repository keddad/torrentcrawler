import motor.motor_asyncio
from os import environ
from models import Entity

MONGO_URI = environ["MONGO_URI"]


def object_to_entity(obj: dict) -> Entity:
    return Entity(
        name=obj["name"],
        reg=obj["reg"],
        hash=obj["hash"],
        seeders=obj["seeders"],
        leeches=obj["leeches"],
        url=obj["url"],
        last_updated=obj["last_updated"]
    )


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.db
torrents = database["torrents"]
