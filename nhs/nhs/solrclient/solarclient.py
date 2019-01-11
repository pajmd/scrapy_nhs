from solrclient import httpclient


# https://lucene.apache.org/solr/guide/7_3/collections-api.html

# https://lucene.apache.org/solr/guide/7_6/uploading-data-with-index-handlers.html#solr-style-json

class SolarClient(httpclient):

    def __init__(self, host, port, timeout):
        super(SolarClient, self).__init__(host, port, timeout)

    # curl -X POST -H 'Content-type:application/json'
    # --data-binary '{"add-field": {"name":"medicine", "type":"text_general", "multiValued":false, "stored":true}}'
    #  http://localhost:8983/solr/nhsdocs/schema
    def add_field(self):
        pass

    #  /admin/collections?action=CREATE&name=name
    # replicationFactor=2&numSahrdPerNode=2&wt=json"
    # curl "http://localhost:8983/solr/admin/collections?
    # action=CREATE&name=nhsdocs&numShards=2&replicationFactor=2&maxShardsPerNode=2&wt=json"
    def create_collection(self, name, numshards, replication_factor, max_shards_per_node):
        command = 'solr/admin/collections'
        payload = {
            'action': 'CREATE',
            'name': name,
            'numShards': numshards,
            'replicationFactor': replication_factor,
            'maxShardsPerNode': max_shards_per_node,
            'wt': 'json'
        }
        super().get(command,payload)
        pass

    # http://localhost:8983/solr/admin/collections?action=DELETE&name=newCollection&wt=xml
    def delete_collection(self, name):
        pass

    # curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/my_collection/update/json/docs' --data-binary '
    # {
    #   "id": "1",
    #   "title": "Doc 1"
    # }'
    def add_document(self):
        pass

    # curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/my_collection/update/json/docs' --data-binary '
    # [{
    #   "id": "1",
    #   "title": "Doc 1"
    # }, ]'
    def add_documents(self):
        pass

    # curl 'http://localhost:8983/solr/techproducts/update?
    # commit=true' --data-binary @example/exampledocs/books.json -H 'Content-type:application/json'
    def add_document_file(self):
        pass