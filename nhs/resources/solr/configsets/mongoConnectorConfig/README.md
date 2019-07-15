### NOTES:
I copied /home/pjmd/solr-7.6.0/server/solr/configsets/_default_conf under
/home/pjmd/python_workspace/PycharmProjects/scrapy_tuto/nhs/resources/solr/configsets/GoldenCopyConfig/conf
This config should not be modified as it's sole purpose is to be copied with the API to new names
derived from the new collection names.
Indeed whe the schema of a collection is updated. Deleting the collection will not
affect the schema so fields added to the schema will remain in the schema.
If one wants to start from a clean slate with a collection that is been worked on
one has to delete both collection and configset to get rid of previously added fields. 
Therefore to recreate the collection one would have to copy GoldenCopyConfig to
 a new config name and create a collection with this config name.
 
The _default config is schemaless which is not recommended:
If one has add-unknown-fields-to-the-schema configured in the update processor 
chain in solrconfig.xml, one is using schemaless mode.
I removed this update processeur from the chain

#### The purpose of GoldenCopyConfig 
is to have a custom soloarconfig.xml where
 the mutating field update processor is removed from the chain of update processor
 
#### command to copy the configset
curl "http://localhost:8983/solr/admin/configs?action=CREATE&name=testConfig&baseConfigSet=GoldenCopyConfig&configSetProp.immutable=false&wt=json&omitHeader=true"
 
#### command to upload the config:
from [pjmd@pjmd-ubuntu16 solr-7.6.0]$ 
./server/scripts/cloud-scripts/zkcli.sh -zkhost 127.0.0.1:9983 -cmd upconfig -confname GoldenCopyConfig -confdir /home/pjmd/python_workspace/PycharmProjects/scrapy_tuto/nhs/resources/solr/configsets/GoldenCopyConfig/conf