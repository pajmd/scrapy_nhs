from pipelines import KafkaPipeline
from . import utiltest
import settings


def test_feed_files_to_pipeline():
    folder = 'full'
    files = utiltest.get_listdir(settings.FILES_STORE, folder)
    item = {
        'files': [{'path': 'full/%s' % file, 'url': 'https://www.nhsbsa.nhs'} for file in files]
    }
    kafka_pipeline = KafkaPipeline(settings.KAFKA_HOST, settings.KAFKA_PORT, settings.TOPIC, settings.FILES_STORE)
    kafka_pipeline.open_spider(spider='dummy')
    rc_item = kafka_pipeline.process_item(item, spider='dummy')
    assert len(rc_item) == len(item)
