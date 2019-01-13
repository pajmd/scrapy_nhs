# Setting up a pipeline:
https://groups.google.com/forum/#!topic/scrapy-users/kzGHFjXywuY

# Doc:
##. https://doc.scrapy.org/en/latest/topics/item-pipeline.html

##. https://doc.scrapy.org/en/latest/topics/media-pipeline.html


## Solr with separate zookeepers: 
https://docs.microfocus.com/UCMDB/2018.05/ucmdb-docs/docs/eng/doc_lib/Content/admin/ConfigSolrCloud_w_ZookeeperEnsemble.htm

## Core vs Collection
http://makble.com/solr-core-and-collection-whats-the-difference

Collections can be found under example/cloud/node1/solr/
Collection has its own schema, configuration and index data directory.

Create collection manually http://makble.com/how-to-create-new-collection-in-solr

## solr configsets creation, deletion
https://lucene.apache.org/solr/guide/7_6/config-sets.html
https://lucene.apache.org/solr/guide/7_6/configsets-api.html#configsets-api

curl "http://localhost:8983/solr/admin/configs?action=CREATE&name=nhsConfigSet&baseConfigSet=_default&configSetProp.immutable=false&wt=xml&omitHeader=true"

