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