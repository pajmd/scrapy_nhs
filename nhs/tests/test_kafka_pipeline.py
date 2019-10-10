from pipelines import KafkaPipeline
from . import utiltest
import settings
import logging
import pdb
import sys


# root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(filename)s: %(lineno)d  - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def test_feed_files_to_pipeline():
    logger.debug('Entering test')
    print('Entering test & print')
    folder = 'full'
    files = utiltest.get_listdir(settings.FILES_STORE, folder)
    item = {
        'files': [{'path': 'full/%s' % file, 'url': 'https://www.nhsbsa.nhs'} for file in files]
    }
    print('Testing with file: %s' % item)
    kafka_pipeline = KafkaPipeline(settings.KAFKA_HOST, settings.KAFKA_PORT, settings.TOPIC, settings.FILES_STORE)
    kafka_pipeline.open_spider(spider='dummy')
    # pdb.set_trace()
    rc_item = kafka_pipeline.process_item(item, spider='dummy')
    assert len(rc_item) == len(item)
