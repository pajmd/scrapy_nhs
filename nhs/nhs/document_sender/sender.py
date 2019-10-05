'''
Implement a Kafka producer
~/kafka_2.12-2.3.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic scrapy_nhs
'''
from kafka import KafkaProducer, errors
from json import dumps
from contextlib import contextmanager
import time
import logging


logger = logging.getLogger(__name__)


class NoBrokerAvailable(Exception):
    pass


class MessageProducer(object):

    def __init__(self, kafka_host, kafka_port, topic):
        self.topic = topic
        connected_to_broker = False
        for attempts in range(6):
            try:
                self.producer = KafkaProducer(bootstrap_servers=['%s:%s' % (kafka_host, kafka_port)],
                                         acks='all',
                                         client_id='producer_%s' % topic,
                                         value_serializer=lambda x:
                                         dumps(x).encode('utf-8'))
                logger.debug("Connected to Kafka")
                connected_to_broker = True
                break
            except errors.NoBrokersAvailable as ex:
                logger.exception(" Attempt %d - Failed finding a broker, wait 5 sec" % attempts)
                time.sleep(5)
        if not connected_to_broker:
            raise NoBrokerAvailable("Failed connecting to Kafka")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.producer.close()
        else:
            self.producer.close()
            raise

    def send(self, documents):
        logger.debug("Sending %d documments" % len(documents))
        print("Sending %d documments" % len(documents))
        for document in documents:
            # document.pop('digest')
            data = {'doc': document}
            self.producer.send(self.topic, value=data)

    def close(self):
        self.producer.close()