import sys
from .base import BaseOutput

class StdoutOutput(BaseOutput):

    def output(self, data):
        print(data, file=sys.stdout)

    def flush(self):
        pass

    def close(self):
        pass
