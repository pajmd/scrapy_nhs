# test

curl "http://localhost:8983/solr/admin/collections?action=DELETE&name=test"
curl "http://localhost:8983/solr/admin/configs?action=DELETE&name=test.AUTOCREATED"

curl "http://localhost:8983/solr/admin/collections?action=CREATE&name=test&numShards=2&replicationFactor=2&maxShardsPerNode=2&wt=json"


curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-copy-field" : {
    "source":"*",
    "dest":"_text_"
  },
  "add-field":{
     "name":"category",
     "type":"text_general",
     "multiValued":false,
     "stored":true },
  "add-field":{
     "name":"Formulations",
     "type":"text_general",
     "multiValued":true,
     "stored":true },
  "add-field":{
     "name":"Medicine",
     "type":"text_general",
     "multiValued":false,
     "stored":true },
  "add-field":{
     "name":"unit",
     "type":"text_general",
     "multiValued":false,
     "stored":true },
  "add-field":{
     "name":"period",
     "type":"text_general",
     "multiValued":false,
     "stored":true },
  "add-field":{
     "name":"Pack_Size",
     "type":"pfloat",
     "multiValued":false,
     "stored":true },
  "add-field":{
     "name":"VMPP_Snomed_Code",
     "type":"text_general",
     "multiValued":false,
     "stored":true },
  "add-field":{
     "name":"Basic_Price",
     "type":"pfloat",
     "multiValued":false,
     "stored":true }
}' http://localhost:8983/solr/test/schema


curl "http://localhost:8983/solr/test/update?commit=true"  --data-binary @/home/pjmd/python_workspace/PycharmProjects/scrapy_tuto/nhs/tests/resources/json/test_drug_part_m_todel.json -H 'Content-type:application/json'
