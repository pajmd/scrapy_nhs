
# Doc Scrapy and Solr Documentation:
## Setting up a pipeline:
https://groups.google.com/forum/#!topic/scrapy-users/kzGHFjXywuY

##item-pipeline:
https://doc.scrapy.org/en/latest/topics/item-pipeline.html
## The media pipeline (File ...)
https://doc.scrapy.org/en/latest/topics/media-pipeline.html

## scrapy architecture
https://doc.scrapy.org/en/latest/topics/architecture.html

## Solr with separate zookeepers: 
https://docs.microfocus.com/UCMDB/2018.05/ucmdb-docs/docs/eng/doc_lib/Content/admin/ConfigSolrCloud_w_ZookeeperEnsemble.htm

## Core vs Collection
http://makble.com/solr-core-and-collection-whats-the-difference

Collections can be found under example/cloud/node1/solr/
Collection has its own schema, configuration and index data directory.

Create collection manually http://makble.com/how-to-create-new-collection-in-solr

## solr configsets creation, deletion API
https://lucene.apache.org/solr/guide/7_6/config-sets.html
https://lucene.apache.org/solr/guide/7_6/configsets-api.html#configsets-api

curl "http://localhost:8983/solr/admin/configs?action=CREATE&name=nhsConfigSet&baseConfigSet=_default&configSetProp.immutable=false&wt=xml&omitHeader=true"

## Solr fields
https://lucene.apache.org/solr/guide/7_6/documents-fields-and-schema-design.html

## Solr field types use cases:
https://lucene.apache.org/solr/guide/7_6/field-properties-by-use-case.html#field-properties-by-use-case

<fieldType name="newFilter" class="solr.TextField" omitNorms="false" positionIncrementGap="100" multiValued="true">
    <analyzer type="index">
      <tokenizer class="solr.WhitespaceTokenizerFactory"/>
      <filter class="solr.LowerCaseFilterFactory"/>
    </analyzer>
    <analyzer type="query">
      <tokenizer class="solr.WhitespaceTokenizerFactory"/>
      <filter class="solr.StopFilterFactory" words="stopwords.txt" ignoreCase="true"/>
      <filter class="solr.LowerCaseFilterFactory"/>
    </analyzer>
  </fieldType>

####tokenizers:
https://lucene.apache.org/solr/guide/7_6/tokenizers.html#Tokenizers-LowerCaseTokenizer

## To retrieve the schema:
curl http://localhost:8983/solr/stuffy/schema?wt=json 
### All schema operations (add field types ....)
https://lucene.apache.org/solr/guide/7_6/schema-api.html
#### list all the fields
curl http://localhost:8983/solr/gettingstarted/schema/fields?wt=json
specific field GET /collection/schema/fields/fieldname
#### list all the field types
curl http://localhost:8983/solr/gettingstarted/schema/fieldtypes?wt=json

## Zookeeper - Configsets
https://chakrayel.wordpress.com/2017/11/08/updating-zookeeper-configuration-files-in-solrcloud-collection/
In SolrCloud configsets are stored under zookeeper trees structures.
See http://localhost:8983/solr/#/~cloud?view=tree
#### zkcli commands
https://lucene.apache.org/solr/guide/7_6/command-line-utilities.html
#### Only way to update solrconfig.xml
Upload a Configuration Directory
./server/scripts/cloud-scripts/zkcli.sh -zkhost 127.0.0.1:9983 -cmd upconfig -confname my_new_config -confdir server/solr/configsets/_default/conf
#### To check the new solrconfig.xml
http://localhost:8983/solr/#/~cloud?view=tree
##### for the particular collection stuffy
http://localhost:8983/solr/#/stuffy/files?file=solrconfig.xml

I appears the solrconfig.xml in the collection is updated right away when the configset solrconfig.xml is uploaded.

## Solr querying
#### field containing space
To query a fields containing space "This Is A Field" one needs to escapthe space i.e.: 
"This\ Is\ A\\ Field"
http://localhost:8983/solr/#/stuffy/queryselect?q"=Pack\ Size:5

#### field not null
Special\ Container:[* TO *]

# Note:
#### Indexing a document for a collection defined with the _default configset 
The _default configset is set with a solrconfig.xml containing an updateRequestProcessorChain.
This updateRequestProcessorChain chain is set with the field-name-mutating processor which will
transform fields so if a field contains a space it will be replace with a _
<updateProcessor class="solr.FieldNameMutatingUpdateProcessorFactory" name="field-name-mutating">
    <str name="pattern">[^\w-\.]</str>
    <str name="replacement">_</str>
</updateProcessor>

see https://lucene.apache.org/solr/guide/7_6/configuring-solrconfig-xml.html to mange solrconfig.xml
