from .kafka import KafkaOutput
from .stdout import StdoutOutput

__all__ = ["create_output"]

all_outputs = {
    "kafka": KafkaOutput,
    "stdout": StdoutOutput,
}

def create_output(typ, *args, **kwargs):
    klass = all_outputs.get(typ)
    if klass is None:
        raise TypeError("type :%s is invalid" % typ)
    return klass(*args, **kwargs)
