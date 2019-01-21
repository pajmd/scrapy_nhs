# -*- coding: utf-8 -*-

import pymongo

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline

class DoNothingPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    collection_name = 'nhsCollection'

    def __init__(self, mongo_uri, mongo_db, file_store, validate=None, validation_schema=None):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.file_store = file_store
        self.validate = validate
        self.validation_schema = validation_schema

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            validate=crawler.settings.get('VALIDATE'),
            vaiadtion_schema=crawler.settings.get('VALIDATION_SCHEMA'),
            file_store=crawler.settings.get('FILES_STORE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if self.validate:
            self.apply_validation()

    def apply_validation(self):
        if self.collection_name in self.db.collection_names():
            self.db.runCommand({
                'collMod': self.collection_name,
                'validator': self.vaiadtion_schema
            }
            )
        else:
            self.db.createCollection(self.collection_name, **self.vaiadtion_schema)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 'files': [{'checksum': 'b619650372822a8362ff182728a0c6cd',
        #            'path': 'full/2e4f8f2529c3aa801b2c322f624897953445d9ea.xlsx',
        #            'url': 'https://www.nhsbsa.nhs
        for file in item['files']:
            documents = converttojson('%s/%s' % (self.file_store, file['path']))
            self.db[self.collection_name].insert(documents)
        return item
