import config
import datastore
from datastore.store import get_source_destination, get_store, store_docs
import pytest
import os


@pytest.mark.parametrize("medium, source_destination", [
    (
        config.FS,
        config.SOURCE_DESTINATION[config.FS]
    ),
    (
        config.MONGO,
        config.SOURCE_DESTINATION[config.MONGO]
    ),
])
def test_get_source_destination(medium, source_destination):
    s_d = get_source_destination(medium)
    assert s_d == source_destination


@pytest.mark.parametrize("medium, clazz", [
    (
        config.FS,
        datastore.fs_store.FSstore
    ),
    (
        config.MONGO,
        datastore.mongo_store.MongoStore
    ),
])
def test_get_store(medium, clazz):
    ds = get_store(medium)
    assert isinstance(ds, clazz)


@pytest.mark.parametrize("medium", [
    (
        config.FS
    )
])
def test_store_docs(monkeypatch, medium):
    def mock_get_source_destination(target):
        if target == config.FS:
            return 'resources/cvs', 'resources/json'

    monkeypatch.setattr(datastore.store, 'get_source_destination', mock_get_source_destination)
    store_docs(config.FS)
    assert os.path.exists('resources/json/test_drug_part_m.json')


def test_get_json_name():
    cvs_file = 'somefile.csv'
    json_file = datastore.fs_store.FSstore.get_json_name(cvs_file)
    assert json_file == 'somefile.json'
