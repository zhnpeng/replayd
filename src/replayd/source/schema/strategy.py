import json
import xmltodict
from faker import Faker
from xeger import Xeger
from random import randint, choice
from .providor import (
    UUIDProvider,
    UUIDScopeProvider,
    ProcessingDatetimeProvider,
    ProcessingDatetimeScopeProvider,
)
from .error import (
    InvalidType
)

fake = Faker()
fake.add_provider(UUIDProvider)
fake.add_provider(UUIDScopeProvider)
fake.add_provider(ProcessingDatetimeProvider)
fake.add_provider(ProcessingDatetimeScopeProvider)


class Strategy:

    def __init__(self):
        pass

    def validate(self):
        if not hasattr(self, 'already_validate'):
            self.already_validate = False
        if self.already_validate:
            return
        try:
            self.already_validate = True
            self.do_validate()
        except Exception:
            self.already_validate = False
            raise

    def do_validate(self):
        # return None or raise Exception
        pass

    def draw(self, **kwargs):
        return self.do_draw(**kwargs)

    def do_draw(self, **kwargs):
        raise NotImplementedError("%s.do_draw" % (type(self).__name__,))


class LiteralStrategy(Strategy):

    def __init__(self, value):
        self.value = value

    def do_draw(self, **kwargs):
        return self.value


class DatetimeStrategy(Strategy):

    def __init__(self, pattern="%Y-%m-%d %H:%M:%S", delta=0):
        self.pattern = pattern
        self.delta = delta

    def do_draw(self, **kwargs):
        return fake.processing_datetime(pattern=self.pattern, delta=self.delta)


class DatetimeScopeStrategy(Strategy):

    def __init__(self, scope="", pattern="%Y-%m-%d %H:%M:%S", delta=0):
        self.scope = scope
        self.pattern = pattern
        self.delta = delta

    def do_draw(self, **kwargs):
        version = kwargs.get("version")
        return fake.processing_datetime_scope(pattern=self.pattern, delta=self.delta, scope=self.scope, version=version)


class UUIDStrategy(Strategy):

    def do_draw(self, **kwargs):
        return fake.uuid()


class UUIDScopeStrategy(Strategy):

    def __init__(self, scope=""):
        self.scope = scope

    def do_draw(self, **kwargs):
        version = kwargs.get("version")
        return fake.uuid_scope(scope=self.scope, version=version)


class IntegerStrategy(Strategy):

    def __init__(self, min_value=0, max_value=9999):
        self.min_value = min_value
        self.max_value = max_value

    def do_validate(self):
        assert isinstance(self.min_value, int), InvalidType("min_value: %s", type(self.min_value).__name__)
        assert isinstance(self.max_value, int), InvalidType("max_value: %s", type(self.max_value).__name__)

    def do_draw(self, **kwargs):
        return fake.pyint(min_value=self.min_value, max_value=self.max_value)


class FloatStrategy(Strategy):

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def do_draw(self, **kwargs):
        return fake.pyint(min_value=self.min_value, max_value=self.max_value)


class StringStrategy(Strategy):

    def __init__(self, min_size=0, max_size=10, pattern=""):
        self.min_size = min_size
        self.max_size = max_size
        self.pattern = pattern

    def do_validate(self):
        assert isinstance(self.min_size, int), InvalidType("min_value: %s", type(self.min_size).__name__)
        assert isinstance(self.max_size, int), InvalidType("max_value: %s", type(self.max_size).__name__)

    def do_draw(self, **kwargs):
        x = Xeger(limit=self.max_size)
        if self.pattern and isinstance(self.pattern, str):
            return x.xeger(self.pattern)
        return fake.pystr(min_chars=self.min_size, max_chars=self.max_size)


def randomize_size(min_size, max_size):
    if min_size is None:
        min_size = 0
    if max_size is None:
        max_size = 10
    try:
        return randint(min_size, max_size)
    except Exception:
        return randint(0, 10)


class ListStrategy(Strategy):

    def __init__(self, strategy=None, min_size=None, max_size=None):
        self.strategy = strategy
        self.min_size = min_size
        self.max_size = max_size

    def do_draw(self, **kwargs):
        size = randomize_size(self.min_size, self.max_size)
        sts = []
        for _ in range(size):
            sts.append(self.strategy.do_draw(**kwargs))
            return sts
        return fake.pylist(nb_elements=size)


def any_dicts():
    return fake.pydict()


class DictStrategy(Strategy):

    def __init__(self, strategies):
        self._strategies = {}
        if isinstance(strategies, dict):
            self._strategies.update(strategies)

    def append(self, k, strategy):
        self._strategies[k] = strategy

    def do_draw(self, **kwargs):
        ret = {}
        for k, st in self._strategies.items():
            ret[k] = st.do_draw()
        if ret:
            return ret
        return any_dicts()


class JsonStrategy(Strategy):

    def __init__(self, strategy):
        self.strategy = strategy

    def do_draw(self, **kwargs):
        if isinstance(self.strategy, Strategy):
            return json.dumps(self.strategy.do_draw())
        return json.dumps(any_dicts())


class XmlStrategy(DictStrategy):

    def do_draw(self, **kwargs):
        data = super(XmlStrategy, self).do_draw()
        return xmltodict.unparse(data)


class EnumStrategy(Strategy):

    def __init__(self, values):
        self.values = values

    def do_draw(self):
        return choice(self.values)


class BooleanStrategy(Strategy):

    def do_draw(self):
        return fake.boolean()


class JoinStrategy(Strategy):

    def __init__(self, strategies, joiner=" "):
        self.strategies = strategies
        self.joiner = joiner

    def do_draw(self):
        return self.joiner.join(str(x.do_draw()) for x in self.strategies)


class OneOfStrategy(Strategy):

    def __init__(self, strategies):
        self.strategies = strategies

    def do_draw(self):
        st = choice(self.strategies)
        return st.do_draw()


class AllOfStrategy(OneOfStrategy):

    def do_draw(self):
        return [x.do_draw() for x in self.strategies]
