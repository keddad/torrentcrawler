# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from pathlib import Path


class TorrentcrawlerPipeline:
    def process_item(self, item, spider):
        print(item)
        return item


class TorrentJsonWriter:
    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
        Path("data/" + item["hash"]).write_text(line)
        return item
