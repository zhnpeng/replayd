import json
from .output import create_output


class Sinker:

    def __init__(self, filename=None, config=None):
        self._config = {"type": "stdout"}
        if config:
            self._config.update(config)
        elif filename:
            with open(filename, "r") as fp:
                self._config = json.loads(fp.read())
        self._output = self._make_output()

    def _make_output(self):
        typ = self._config.get("type")
        params = dict(self._config)
        params.pop("type", None)
        return create_output(typ, **params)

    def export(self, data):
        self._output.output(data)

    def flush(self):
        self._output.flush()

    def close(self):
        self._output.close()
