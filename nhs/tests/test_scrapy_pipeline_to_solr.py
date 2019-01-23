from pipelines import MongoPipeline
from nhs.tests import utiltest
import settings


def test_feed_files_to_pipeline():
    folder = 'full'
    files = utiltest.get_listdir(settings.FILES_STORE, folder)
    item = {
        'files': [{'path': 'full/%s' % file} for file in files]
    }
    mongo_pipeline = MongoPipeline(settings.MONGO_URI, settings.MONGO_DATABASE, settings.FILES_STORE,
                                   validate=None, validation_schema=None)
    mongo_pipeline.open_spider(spider='dummy')
    rc_item = mongo_pipeline.process_item(item, spider='dummy')
    assert len(rc_item) == len(item)
