# -*- coding: utf-8 -*-

import pymongo
import base64
from parsers.parser import Parser, BasicParser
from document_sender.sender import MessageProducer
import logging


logger = logging.getLogger(__name__)


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


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
            validation_schema=crawler.settings.get('VALIDATION_SCHEMA'),
            file_store=crawler.settings.get('FILES_STORE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if self.validate:
            self.apply_validation()
        self.create_index("digest")

    def apply_validation(self):
        if self.collection_name in self.db.collection_names():
            self.db.runCommand({
                'collMod': self.collection_name,
                'validator': self.validation_schema
            }
            )
        else:
            self.db.createCollection(self.collection_name, **self.validation_schema)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 'files': [{'checksum': 'b619650372822a8362ff182728a0c6cd',
        #            'path': 'full/2e4f8f2529c3aa801b2c322f624897953445d9ea.xlsx',
        #            'url': 'https://www.nhsbsa.nhs
        for file in item['files']:
            filename = file['path']
            try:
                documents = self.converttojson(file)
                # rc = self.db[self.collection_name].insert_many(documents)
                operations = self.build_bulk_upsert(documents)
                logger.debug("Number of records to upsert: %d" % len(operations))
                rc = self.db[self.collection_name].bulk_write(operations)
            except Exception as ex:
                logger.debug("Failed proccessing file %s - %s" % (filename, ex))
        return item

    def converttojson(self, file):
        filename = file['path']
        parser = Parser(filename, self.file_store)
        specialized_parser = parser.get_parser()
        json_tariff = specialized_parser.parse(file)
        return json_tariff

    def build_bulk_upsert(self, documents):
        # UpdateOne({"field1": 11}, {"$set": {"field2": 12, "field3": 13 }}, upsert=True),
        operations = []
        for document in documents:
            mutating_document = document.copy()
            digest = mutating_document.pop("digest")
            if not self.mark_duplicate_document(document):
                operations.append(pymongo.UpdateOne({"digest": digest}, {"$set": mutating_document}, upsert=True))
        return operations

    def create_index(self, key):
        index_list = self.db[self.collection_name].list_indexes()
        truth = [index["key"].get(key) is None for index in index_list]
        if all(truth):
            self.db[self.collection_name].create_index(key)
            return True
        return False

    def mark_duplicate_document(self, document):
        digest = document['digest']
        b64digest = base64.b64encode(digest)
        docs = self.db[self.collection_name].find({"digest": digest})
        if docs.count():
            for doc in docs:
                if document['filename'] == 'full/2f307d3971227f3eaafcf9a6d5b7ca5b923be172.xlsx':
                    logger.debug('stop')
                if document['filename'] == doc['filename']:
                    logger.debug('there is a problem')

            file = {
                'url': document['url'],
                'filename': document['filename']
            }
            rc = self.db[self.collection_name].update_many(
                {"digest": digest},
                {"$push": {"dupes": file}})
            return True
        return False
        # docs = self.db[self.collection_name].find({"digest": digest})
        # if docs:
        #     digests = []
        #     for doc in docs:
        #         vals = []
        #         for k, v in doc.items():
        #             if k not in ["_id", "digest", 'filename', 'url']:
        #                 vals.append(v)
        #         actual = BasicParser.get_digest(vals)
        #         digests.append(actual)
        #         logger.debug(digests)



class KafkaPipeline(object):

    def __init__(self, kafka_host, kafka_port, topic, file_store):
        self.kafka_host = kafka_host
        self.kafka_port = kafka_port
        self.topic = topic
        self.file_store = file_store


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            kafka_host=crawler.settings.get('KAFKA_HOST'),
            kafka_port=crawler.settings.get('KAFKA_PORT'),
            topic=crawler.settings.get('TOPIC'),
            file_store=crawler.settings.get('FILE_STORE')
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # 'files': [{'checksum': 'b619650372822a8362ff182728a0c6cd',
        #            'path': 'full/2e4f8f2529c3aa801b2c322f624897953445d9ea.xlsx',
        #            'url': 'https://www.nhsbsa.nhs
        # producer = MessageProducer(self.kafka_host, self.kafka_port, self.topic)
        for file in item['files']:
            filename = file['path']
            try:
                documents = self.converttojson(file)
                print("sending %s with %d documents" % (filename, len(documents)))
                with MessageProducer(self.kafka_host, self.kafka_port, self.topic) as producer:
                    producer.send(documents)
            except Exception as ex:
                logger.exception("Failed proccessing file %s - %s" % (filename, ex))
                raise
        return item

    def converttojson(self, file):
        filename = file['path']
        parser = Parser(filename, self.file_store)
        specialized_parser = parser.get_parser()
        json_tariff = specialized_parser.parse(file)
        return json_tariff

