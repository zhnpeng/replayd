# -*- encoding=utf-8 -*-
import json
from kafka import KafkaProducer
from .base import BaseOutput


class KafkaOutput(BaseOutput):

    def __init__(self, topics=None, kafka_params=None, **kwargs):
        if topics is None:
            raise Exception("topics is needed")
        if kafka_params is None:
            raise Exception("kafka_params is needed")
        self._topics = topics
        self._producer = self._make_producer(kafka_params)

    def _make_producer(self, kafka_params):
        return KafkaProducer(**kafka_params)

    def _encode(self, data):
        if type(data) in (bytes, bytearray, memoryview, type(None)):
            return data
        elif isinstance(data, str):
            return data.encode()
        try:
            return json.dumps(data, ensure_ascii=False).encode()
        except Exception as ex:
            print(ex)
        return data

    def output(self, data):
        data = self._encode(data)
        for topic in self._topics:
            self._producer.send(topic, value=data)

    def flush(self):
        self._producer.flush()

    def close(self):
        self._producer.flush()
        self._producer.close()
        self._producer = None
