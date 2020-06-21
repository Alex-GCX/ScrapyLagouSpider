# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json


class LagouPipeline:
    def process_item(self, item, spider):
        with open('jobs.json', 'a', encoding='utf-8') as f:
            item_json = json.dumps(dict(item), ensure_ascii=False, indent=2)
            f.write(item_json)
            f.write('\n')
