from solrclient.solrclient import SolrClient
from solrclient.solrclientexceptions import CreateCollectionException
import pytest
import sys

def curlit(cmd):
    from subprocess import call
    try:
        retcode = call(["/usr/bin/curl", cmd])
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)


# need to add fixture to prepare the terrain (pre-delete, pre-create ...)

#scope should be module
@pytest.fixture()
def start_solr():
    from subprocess import call
    call(['~/solr-7.6.0/bin/solr', 'start', '-e', 'cloud'])


@pytest.fixture()
def predelete_collection():
    cmd = "http://localhost:8983/solr/admin/collections?action=DELETE&name=stuff&wt=json"
    curlit(cmd)

# fixture that can receive a parameter
@pytest.fixture()
def fixture_delete_collection():
    def fixture_delete_collection_(name):
        cmd = "http://localhost:8983/solr/admin/collections?action=DELETE&name=%s&wt=json" % name
        curlit(cmd)
    return fixture_delete_collection_

# fixture that can receive a parameter
@pytest.fixture()
def fixture_create_collection():
    def fixture_create_collection_(name):
        cmd = "http://localhost:8983/solr/admin/collections?action=CREATE&name=%s&numShards=2&replicationFactor=2&maxShardsPerNode=2&wt=json" % name
        curlit(cmd)
    return fixture_create_collection_


# this fixture works fine  and does a tear up and tera down but can't receive parameters
# so I just create 2 fixtures that can receive parameters one une as
# tear up and the other as teardown that must be call in the test case
@pytest.fixture()
def precreate_collection():
    cmd = "http://localhost:8983/solr/admin/collections?action=CREATE' \
    '&name=stuff&numShards=2&replicationFactor=2&maxShardsPerNode=2&wt=json"
    curlit(cmd)
    yield 'nothing to yield'
    # delete connection
    cmd = "http://localhost:8983/solr/admin/collections?action=DELETE&name=stuff&wt=json"
    curlit(cmd)


def test_create_collection(predelete_collection):
    slrclient = SolrClient(host='localhost', port=8983)
    slrclient.create_collection('stuff', 2, 2, 2)
    assert True


def test_param_create_collection(fixture_delete_collection):
    name = 'stuffy'
    fixture_delete_collection(name)
    slrclient = SolrClient(host='localhost', port=8983)
    slrclient.create_collection(name, 2, 2, 2)
    assert True


def test_create_collection_error(precreate_collection):
    with pytest.raises(CreateCollectionException):
        slrclient = SolrClient(host='localhost', port=8983)
        slrclient.create_collection('stuff', 2, 2, 2)


def test_create_collection_error_param(fixture_create_collection, fixture_delete_collection):
    name = 'stuffy3'
    fixture_create_collection(name)
    with pytest.raises(CreateCollectionException):
        slrclient = SolrClient(host='localhost', port=8983)
        slrclient.create_collection(name, 2, 2, 2)
        fixture_delete_collection(name)

def test_delete_collection():
    pass


def test_delete_collectio_error():
    pass