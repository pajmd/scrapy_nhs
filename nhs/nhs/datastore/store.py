from datastore.fs_store import FSstore
from datastore.mongo_store import MongoStore
from config import (
FS,
MONGO,
SOURCE_DESTINATION
)


def get_source_destination(medium):
    return SOURCE_DESTINATION[medium]


def get_store(medium):
    if medium == FS:
        return FSstore(*get_source_destination(medium))
    elif medium == MONGO:
        return MongoStore(*get_source_destination(medium))


def store_docs(medium):
    store_engine = get_store(medium)
    store_engine.store()


def store_all_cvs_doc_to_fs():
    fs_store = get_store(FS)
    fs_store.store()


if __name__ == '__main__':
    store_all_cvs_doc_to_fs()