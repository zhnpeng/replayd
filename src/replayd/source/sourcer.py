# -*- coding: utf-8 -*-
import time
import json
from .schema import generate
from .file.json import JsonFile


class BaseSourcer:

    def draw(self):
        raise NotImplementedError


class SchemaSourcer(BaseSourcer):

    def __init__(self, filename, interval=0, **kwargs):
        self._interval = interval
        self._strategies = []
        with open(filename, "r") as fp:
            _schemas = json.load(fp)
            for schema in _schemas:
                self._strategies.append(generate(schema))

    def draw(self, version=0, **kwargs):
        for st in self._strategies:
            yield st.draw(version=version)
            time.sleep(self._interval)


class SampleSourcer(BaseSourcer):

    def __init__(self, filename, interval=0, aware_datetime="", datetime_format="", encoding="utf-8", **kwargs):
        self._encoding = encoding
        self._interval = interval
        self._fp = open(filename, "r", encoding=encoding)
        try:
            self._fp = JsonFile(filename, aware_datetime=aware_datetime, datetime_format=datetime_format, encoding=encoding)
        except Exception:
            pass

    def draw(self, version=0, **kwargs):
        self._fp.seek(0)
        for line in self._fp:
            if isinstance(line, str):
                line = line.encode(self._encoding)
            yield line
            time.sleep(self._interval)
