class BaseOutput(object):

    def output(self, data):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
