# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from os import environ
from pathlib import Path


class TorrentcrawlerPipeline:
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
