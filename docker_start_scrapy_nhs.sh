#!/usr/bin/env bash

DB_HOST=$1

check_mongod_up() {
	attempts_left=5
	mongo_hostname=$1
	while (( attempts_left > 0 )); do

		(( attempts_left-- ))
		if (( attempts_left == 0 )); then
			echo "Mongo still not running. Giving up"
			exit 1
		fi
		mongo_session=`/usr/bin/mongo "mongodb://$mongo_hostname:27017" --eval "quit()" | grep "Implicit session"`
		echo "mongo_session= $mongo_session"
		if [ -z "$mongo_session" ]; then
			echo "Waiting for mongodb://$mongo_hostname:27017 another " $attempts_left " times"
			sleep 5
		else
			break
		fi
	done
	echo "$mongo_hostname is running!"
}

check_mongod_up $DB_HOST
# export needed because my pip was not install from source but apt-get
# as a consequence my libs go to dist-pacakges instead of site-packages
# I need to get the proper pip
cd /app/nhs/nhs
python __main__.py