# replayd

replayd represent for replay data, replay data to stdout and kafka.

## support 2 type of source

* schema
* sample file

## requirement

Python3
faker
xmltodict
kafka-python
xeger

## download & install

```
git clone https://your_name@git.netisdev.com/scm/nc/replayd.git
pip install ./replayd
replayd -h
```

## parameters

param | required | default | description
--- | --- | --- | ---
--mode, -m | yes | | mode，sample or schema，schema means generate data according to schema
--loop, -l | no | 1 | how many times should replay，0 represent for infinite
--aware-datetime, -a | no | | whether should replace datetime field with processing time，work for sample data in json format
--datetime-format, -d | no | | datetime format，required when aware-datetime is true
--interval, -t | no | 0 | replay interval，in second，default is 0 represent for no interval
--input, -i | yes | | sample or schema file
--output, -o | no | | sinker config file，support kafka config file，if this is not set means sink to stdout
--encoding, -e | no | utf-8 | encoding


## replay data with schema to stdout

```
replayd -m schema -i examples/schema.json
output:
{"ID": "e487decb72ee4d419951334c1b74628f", "REQUEST_TIME": "2020-06-26 22:04:38", "TYPE": "Request", "TIME_COST": 706, "TRACE_ID": "c446f2465ed640409af71ed94e3aa5cb"}
{"ID": "0166c6e677e846d2bfe01577e540d8fb", "REQUEST_TIME": "2020-06-26 22:04:39", "TYPE": "Response", "TIME_COST": 338, "TRACE_ID": "c446f2465ed640409af71ed94e3aa5cb"}
```

## replay data with schema to kafka

```
replayd -m schema -i examples/schema.json -o config/kafka.json
```

## replay data with sample

```
replayd -m sample -i examples/sample.txt
or
replayd -m sample -i examples/sample.json
```

## use kafka docker

required[docker-compose](https://docs.docker.com/compose/install/)

make sure /ets/hosts has follow line:
```
127.0.0.1 host.docker.internal
```
or modify ```KAFKA_ADVERTISED_HOST_NAME``` in ```replayd/docker/kafka-docker-compose.yml``` to your host name

startup kafka docker
```
docker-compose -f replayd/docker/kafka-docker-compose.yml up -d
```