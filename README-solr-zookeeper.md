## Zookeeper

Downloaded apache-zookeeper-3.5.5-bin.tgz and unpacked it as
$HOME/apache-zookeeper-3.5.5-bin

#### config for  n=1-3 zookeper
* created 3 conf/zoo-n.cfg
* /var/lib/zookeeper/data-n/myid
##### Example of zoo-1.cfg
```
tickTime=2000
initLimit=15
syncLimit=10
dataDir=/var/lib/zookeeper/data-1
clientPort=2181
server.1=localhost:2888:3888
server.2=localhost:2889:3889
server.3=localhost:2890:3890

# 4 letter word commands whitelisted for use with nc
4lw.commands.whitelist=stat, ruok, conf, isro
# jetty port for admin server
admin.serverPort=8081

```
#### ensemble commands
Start
```
bin$ ./zoo-ensemble.sh start
```
Stop
```
bin$ ./zoo-ensemble.sh stop
```
#### Zookeeper info commands
The followong commands must be whitelisted: see 4lw.commands.whitelist described in cluster configuration section. This commands will be deprecated.
* ```echo stat | nc localhost 2181 or ./zkServer.sh status```
* ```echo mntr | nc localhost 2181```  
* Instead use AdminServer (default port 8080)
```
http://localhost:808[1-3]/commands/stat
```
see zoo-n.cfg to check how the jetty port is set.  
Problem with ```zkServer.sh status```  I am not sure how to give it a specif zoo.cfg file

#### Zookeeper client interface
Tp start the client and have it connect to all instances:
```
bin/zkCli.sh -server "localhost:2181,localhost:2182,localhost:2183"
```

### Back to solr

#### Chroot: Znode
Create a chroot (folder hierarchy) i.e. config location dedicated to solr vs other possible apps
from solr folder:
```
bin/solr zk mkroot /my_solr_conf -z localhost:2181,localhost:2182,localhost:2183  
```

Znodes can be deleted from zookeeper withe the zookeeper client zkCli.sh
```
$ZK_HOME/bin/./zkCli.sh -server "localhost:2181,localhost:2182,localhost:2183"
Connecting to localhost:2181,localhost:2182,localhost:2183
deleteall /my_solr_conf
```

* Upload config
	* If solr was installed using the service installation script bin/install_solr_service.sh, add variable ZK_HOST to the inlude file: /etc/default/solr.in
	* else add it to bin/solr.in.sh
	```
	ZK_HOST=localhost:2181,localhost:2182,localhost:2183/my_solr_conf
	```
	* upload (without zk_HOST set in solr.in.sh)
	```
	./server/scripts/cloud-scripts/zkcli.sh -z localhost:2181,localhost:2182,localhost:2183/my_solr_conf -cmd upconfig -confname mongoConnectorBaseConfig -confdir /home/pjmd/python_workspace/PychramProjects/scrapy_nhs/nhs/resources/solr/configsets/mongoConnectorConfig/conf
	```
* to start 2 solr instances pointing to solr's znode, in solrCloud mode without ZH_HOST defined in solr.in.sh
	```
	./solr start -c -p 8983 -z localhost:2181,localhost:2182,localhost:2183/my_solr_conf && ./solr start -c -p 7574 -z localhost:2181,localhost:2182,localhost:2183/my_solr_conf
	```
	<span style="background-color: #FFFF00">
	<mark>If you see a message like: number of file open max 4096 change it to 65000  
	see ttps://docs.oracle.com/cd/E19623-01/820-6168/file-descriptor-requirements.html
	to fix it.</mark>
	</span>

* create the configset
	```
	curl "http://localhost:8983/solr/admin/configs?action=CREATE&name=mongoConnectorConfig&baseConfigSet=mongoConnectorBaseConfig&configSetProp.immutable=false&wt=json&omitHeader=true"
	```
* create the collection
	```
	curl "http://localhost:8983/solr/admin/collections?action=CREATE&name=nhsCollection&collection.configName=mongoConnectorConfig&numShards=2&replicationFactor=2&maxShardsPerNode=2&wt=json"
	```

* add mongo fields:
	```
	curl -X POST -H 'Content-type:application/json' --data-binary @/home/pjmd/python_workspace/PychramProjects/scrapy_nhs/nhs/resources/solr/resources/mongo_fields.json  http://localhost:8983/solr/nhsCollection/schema
	```
* start mongo connetcor in some temp folder  
	Starting from a clean slate:
	* delete the mongo connetor timestamp
	```
	rm oplog.timestamp
	```
	* in mongodb clear the nhsCollection
	```
	$ > mongo

	used nhsdb
	db.nhsCollection.count()
	db.nhsCollection.drop()
	```

	* start mongoconnector

	```
	~/tmp > source ../python_workspace/python-env/scrapy-nhs-env/bin/activate
	~/tmp > mongo-connector --unique-key=id --namespace-set=nhsdb.nhsCollection -m localhost:27017 -t http://localhost:8983/solr/nhsCollection -d solr_doc_manager -v
	```
	* start sacrpy-nhs mongo updater
	```
	python /home/pjmd/python_workspace/PychramProjects/scrapy_nhs/nhs/nhs/__main__.py
	```
