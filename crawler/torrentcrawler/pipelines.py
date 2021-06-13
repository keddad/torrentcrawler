# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter
import json
from os import environ
from datetime import datetime
import pymongo
from pathlib import Path


class TorrentcrawlerPrintPipeline:
    def process_item(self, item, spider):
        e = environ.get("PRINT")
        if e and e == "1" or e.lower() == "true":
            print(item)
        return item


class TorrentJsonWriter:
    def process_item(self, item, spider):
        e = environ.get("JSON_PATH")
        if e:
            line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
            Path(e + item["hash"]).write_text(line)
        return item


class RegNormalizerPipeline:
    _months = {
        "Янв": 1,
        "Фев": 2,
        "Мар": 3,
        "Апр": 4,
        "Май": 5,
        "Июн": 6,
        "Июл": 7,
        "Авг": 8,
        "Сен": 9,
        "Окт": 10,
        "Ноя": 11,
        "Дек": 12
    }

    def process_item(self, item, spider):
        date, time = item["reg"].split(" ")
        day, month, year = date.split("-")
        h, m = time.split(":")
        month = self._months[month]
        year = "20" + year

        item["reg"] = datetime(year=int(year), month=month, day=int(day), hour=int(h), minute=int(m)).strftime('%s')
        return item


class MongoLoaderPipeline:
    collection_name = "torrents"

    def __init__(self):
        self.mongo = None
        self.collection = None

    def open_spider(self, spider):
        e = environ.get("MONGO_URI")
        if e:
            self.mongo = pymongo.MongoClient(e)
            self.collection = self.mongo.db[self.collection_name]

    def close_spider(self, spider):
        self.mongo.close()

    def process_item(self, item, spider):
        spider.log("Entered mongo pipeline!", logging.DEBUG)
        if self.mongo:
            data = ItemAdapter(item).asdict()
            existing = self.collection.find_one({"hash": data["hash"]})

            if not existing:
                id = self.collection.insert_one(data | {"last_updated": datetime.now().strftime('%s')})
                spider.log(f"Put something in mongo! {id}", logging.DEBUG)
            else:
                self.collection.update({"hash": data["hash"]},
                                       {
                                           "$set": {
                                               "last_updated": datetime.now().strftime('%s'),
                                               "seeders": data["seeders"],
                                               "leeches": data["leeches"]},
                                           "$min": {"reg": data["reg"]}})

        return item
