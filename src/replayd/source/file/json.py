import json
import time
from datetime import datetime


default_datetime_formats = ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"]


def strptimestamp(string, format):
    st = time.strptime(string, format)
    return time.mktime(st)


def strfnow(format):
    return datetime.now().strftime(format)


def aware_datetime_format(dtstr, dtfmt=""):
    dtfmts = default_datetime_formats
    if dtfmt and dtfmt not in dtfmts:
        dtfmts.insert(0, dtfmt)
    for dtfmt in dtfmts:
        try:
            strptimestamp(dtstr, dtfmt)
            return dtfmt
        except Exception:
            pass
    return default_datetime_formats[0]


class JsonFile:

    def __init__(self, filename, aware_datetime="", datetime_format="", encoding="utf-8", **kwargs):
        self._i = 0
        self._aware_datetime = aware_datetime
        self._datetime_format = datetime_format
        self._datetime_foramts = []
        self._data = []
        with open(filename, "r", encoding=encoding) as fp:
            self._data = json.load(fp)
        if not isinstance(self._data, (tuple, list)):
            self._data = [self._data]
        self._length = len(self._data)

    def seek(self, p):
        self._i = 0

    def __iter__(self):
        i = self._i
        while i < self._length:
            record = self._data[i]
            if self._aware_datetime:
                if i < len(self._datetime_foramts):
                    dtfmt = self._datetime_foramts[i]
                else:
                    dtfmt = aware_datetime_format(self._aware_datetime, self._datetime_format)
                    self._datetime_foramts.append(dtfmt)
                record[self._aware_datetime] = strfnow(dtfmt)
            yield record
            i += 1
