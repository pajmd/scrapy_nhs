#!/usr/bin/env bash

curl -X POST -H 'Content-type:application/json' --data-binary @one_solr_rec.json  http://localhost:8983/solr/nhsCollection/update?commit=true