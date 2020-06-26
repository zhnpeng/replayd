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

## install

```
cd ./replayd
pip install ./
```

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