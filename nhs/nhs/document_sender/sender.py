'''
Implement a Kafka producer
~/kafka_2.12-2.3.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic scrapy_nhs
'''
from kafka import KafkaProducer
from json import dumps
from contextlib import contextmanager


class MessageProducer(object):

    def __init__(self, kafka_host, kafka_port, topic):
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=['%s:%s' % (kafka_host, kafka_port)],
                                 acks='all',
                                 client_id='producer_%s' % topic,
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.producer.close()
        else:
            self.producer.close()
            raise

    def send(self, documents):
        for document in documents:
            # document.pop('digest')
            data = {'doc': document}
            self.producer.send(self.topic, value=data)

    def close(self):
        self.producer.close()