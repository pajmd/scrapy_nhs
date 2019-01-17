from solrclient.solrclient import SolrClient
from solrclient.solrclientexceptions import (
    CreateCollectionException,
    DeleteCollectionException,
    AddFieldSchemaException
)
from nhs.tests.utiltest import get_resource, get_json_resource, get_bin_resource
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


################# tearup and teardown fixtures #################

#### I did not use the folowing 2 the pre... fixtures because the can't accept parameters

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


@pytest.fixture()
def predelete_collection():
    cmd = "http://localhost:8983/solr/admin/collections?action=DELETE&name=stuff&wt=json"
    curlit(cmd)


###


# fixture that can receive a parameter
def fixure_helper_delete_collection(collection):
    cmd = "http://localhost:8983/solr/admin/collections?action=DELETE&name=%s&wt=json" % collection
    curlit(cmd)
    cmd = "http://localhost:8983/solr/admin/configs?action=DELETE&name=%sConfig" % collection
    curlit(cmd)


@pytest.fixture()
def fixture_delete_collection():
    def fixture_delete_collection_(name):
        fixure_helper_delete_collection(name)
        # cmd = "http://localhost:8983/solr/admin/collections?action=DELETE&name=%s&wt=json" % name
        # curlit(cmd)
        # cmd =  "http://localhost:8983/solr/admin/configs?action=DELETE&name=%s.AUTOCREATED" % name
        # curlit(cmd)

    return fixture_delete_collection_


# fixture that can receive a parameter
@pytest.fixture()
def fixture_create_collection():
    def fixture_create_collection_(name):
        fixure_helper_delete_collection(name)
        cmd = "http://localhost:8983/solr/admin/configs?action=CREATE&name=%sConfig&baseConfigSet=GoldenCopyConfig&configSetProp.immutable=false&wt=json&omitHeader=true" % name
        curlit(cmd)
        cmd = "http://localhost:8983/solr/admin/collections?action=CREATE&name=%s&collection.configName=%sConfig&numShards=2&replicationFactor=2&maxShardsPerNode=2&wt=json" % (
        name, name)
        curlit(cmd)

    return fixture_create_collection_


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


def test_delete_collection(fixture_create_collection, fixture_delete_collection):
    name = 'stuffy'
    fixture_create_collection(name)
    slrclient = SolrClient(host='localhost', port=8983)
    slrclient.delete_collection(name)
    fixture_delete_collection(name)
    assert True


def test_delete_collectio_error(fixture_delete_collection):
    name = 'stuffy'
    fixture_delete_collection(name)
    with pytest.raises(DeleteCollectionException):
        slrclient = SolrClient(host='localhost', port=8983)
        slrclient.delete_collection(name)


def test_add_field(fixture_create_collection, fixture_delete_collection):
    collection = 'stuffy'
    fixture_create_collection(collection)
    slrclient = SolrClient(host='localhost', port=8983)
    slrclient.add_field(collection, name='a_field', fieldtype="text_general", multivalued=False, stored=True)
    with pytest.raises(AddFieldSchemaException):
        slrclient.add_field(collection, name='a_field', fieldtype="text_general", multivalued=False, stored=True)
    fixture_delete_collection(collection)
    assert True


@pytest.mark.parametrize("collection, files", [
    ('stuffy', get_resource('test_drug_part_m.json', 'json')),
    # ('stuffy', [get_resource('test_drug_part_m.json', 'json'), get_resource('test_drug_part_m.json', 'json')])
])
def test_add_document_file(fixture_create_collection, fixture_delete_collection, collection, files):
    fixture_create_collection(collection)
    slrclient = SolrClient(host='localhost', port=8983)
    options = {
        'stored': True,
        'indexed': True,
        'docValues': True
    }
    slrclient.add_field(collection, name='Pack Size', fieldtype="pfloat", multivalued=False, stored=True,
                        optional=options)

    slrclient.add_document_files(collection, files, commit=True)
    fixture_delete_collection(collection)


@pytest.mark.parametrize("collection, files", [
    ('stuffy', get_resource('test_drug_part_m.json', 'json')),
    # ('stuffy', [get_resource('test_drug_part_m.json', 'json'), get_resource('test_drug_part_m.json', 'json')])
])
def test_add_fields_and_document_file(fixture_create_collection, fixture_delete_collection, collection, files):
    fixture_create_collection(collection)
    slrclient = SolrClient(host='localhost', port=8983)
    fields = get_json_resource('nhs_field_list.json', 'json')
    slrclient.add_fields(collection, fields)

    slrclient.add_document_files(collection, files, commit=True)
    fixture_delete_collection(collection)


def test_adding_fields_to_del():
    slrclient = SolrClient(host='localhost', port=8983)
    fields = get_json_resource('nhs_field_list.json', 'json')
    slrclient.add_fields("stuffy", fields)

def test_indexing_to_del():
    slrclient = SolrClient(host='localhost', port=8983)
    slrclient.add_document_files("stuffy", [
        get_resource('test_drug_part_m.json', 'json'),
        get_resource('test_drug_part_m_may.json', 'json')
    ], commit=True)


def test_one_field_to_del():
    slrclient = SolrClient(host='localhost', port=8983)
    fields = [
        {
            "add-field": {
                "name": "Spec Cont Ind",
                "type": "text_general",
                "multiValued": False,
                "stored": True
            }
        }
    ]
    slrclient.add_fields("stuffy", fields)
