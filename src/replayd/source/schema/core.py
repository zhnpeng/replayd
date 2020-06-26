from .strategy import (
    LiteralStrategy,
    DatetimeStrategy,
    DatetimeScopeStrategy,
    UUIDStrategy,
    UUIDScopeStrategy,
    IntegerStrategy,
    FloatStrategy,
    StringStrategy,
    ListStrategy,
    DictStrategy,
    JsonStrategy,
    XmlStrategy,
    EnumStrategy,
    BooleanStrategy,
    JoinStrategy,
    OneOfStrategy,
    AllOfStrategy,
)

class StrategyFactory:

    _strategies = {}

    @classmethod
    def register(cls, name):
        def _wrapper(func):
            cls._strategies[name] = func
            return func
        return _wrapper

    @classmethod
    def get(cls, name):
        return cls._strategies.get(name)


@StrategyFactory.register("literal")
def literals(**kwargs):
    return LiteralStrategy(kwargs.get("value"))


@StrategyFactory.register("datetime")
def datetimes(**kwargs):
    delta = kwargs.get("delta", 0)
    pattern = kwargs.get("pattern", "%Y-%m-%d %H:%M:%S")
    return DatetimeStrategy(delta=delta, pattern=pattern)


@StrategyFactory.register("datetime_scope")
def datetimes_scope(**kwargs):
    delta = kwargs.get("delta", 0)
    pattern = kwargs.get("pattern", "%Y-%m-%d %H:%M:%S")
    scope = kwargs.get("scope")
    return DatetimeScopeStrategy(pattern=pattern, delta=delta, scope=scope)


@StrategyFactory.register("uuid")
def uuids(**kwargs):
    return UUIDStrategy()


@StrategyFactory.register("uuid_scope")
def uuids_scope(**kwargs):
    scope = kwargs.get("scope")
    return UUIDScopeStrategy(scope=scope)


@StrategyFactory.register("integer")
def integers(**kwargs):
    min_value = kwargs.get("min_value", 0)
    max_value = kwargs.get("max_value", 9999)
    return IntegerStrategy(min_value=min_value, max_value=max_value)


@StrategyFactory.register("float")
def floats(**kwargs):
    min_value = kwargs.get("min_value", None)
    max_value = kwargs.get("max_value", None)
    return FloatStrategy(min_value=min_value, max_value=max_value)


@StrategyFactory.register("string")
def strings(**kwargs):
    min_size = kwargs.get("min_size", 0)
    max_size = kwargs.get("max_size", 10)
    pattern = kwargs.get('pattern')
    return StringStrategy(min_size=min_size, max_size=max_size, pattern=pattern)


@StrategyFactory.register("list")
def lists(**kwargs):
    min_size = kwargs.get("min_size", None)
    max_size = kwargs.get("max_size", None)
    schema = kwargs.get("schema")
    if schema:
        st = generate(schema)
        return ListStrategy(strategy=st, min_size=min_size, max_size=max_size)
    return ListStrategy(min_size=min_size, max_size=max_size)


@StrategyFactory.register("dict")
def dicts(**kwargs):
    strategies = {}
    schema = kwargs.get("schema")
    if schema:
        for key, schema in schema.items():
            strategies[key] = generate(schema)
    return DictStrategy(strategies)


@StrategyFactory.register("json")
def jsons(**kwargs):
    schema = kwargs.get("schema")
    if schema:
        st = generate(schema)
        return JsonStrategy(st)
    return JsonStrategy(None)


@StrategyFactory.register("xml")
def xmls(**kwargs):
    strategies = {}
    schema = kwargs.get("schema")
    if schema:
        for key, schema in schema.items():
            strategies[key] = generate(schema)
    return XmlStrategy(strategies)


@StrategyFactory.register("enum")
def enums(**kwargs):
    values = kwargs["choice"]
    return EnumStrategy(values)


@StrategyFactory.register("boolean")
def booleans(**kwargs):
    return BooleanStrategy()


def joins(**kwargs):
    sts = []
    joiner = kwargs.get("joiner")
    if joiner is None or not isinstance(joiner, str):
        joiner = " "
    for schema in kwargs.get("join", []):
        sts.append(generate(schema))
    return JoinStrategy(sts, joiner)


def oneofs(**kwargs):
    sts = []
    for schema in kwargs.get("oneof", []):
        sts.append(generate(schema))
    return OneOfStrategy(sts)


def allofs(**kwargs):
    sts = []
    for schema in kwargs.get("allof", []):
        sts.append(generate(schema))
    return AllOfStrategy(sts)


def generate(schema):
    oneof = schema.get("oneof")
    if oneof:
        return oneofs(**schema)
    allof = schema.get("allof")
    if allof:
        return allofs(**schema)
    join = schema.get("join")
    if join:
        return joins(**schema)
    typ = schema.get("type")
    st = StrategyFactory.get(typ)
    if st is None:
        raise TypeError("type %s is not supported" % typ)
    return st(**schema)


if __name__ == "__main__":
    schema = {
        "type": "dict",
        "schema": {
            "list_of_dict": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "field1": {
                            "type": "string"
                        }
                    }
                }
            },
            "all_of_list": {
                "allof": [
                    {
                        "type": "dict",
                        "schema": {
                            "field1": {
                                "type": "string"
                            }
                        }
                    },
                    {
                        "type": "dict",
                        "schema": {
                            "field2": {
                                "type": "string"
                            }
                        }
                    }
                ]
            },
            "list_of_integer": {
                "type": "list",
                "schema": {
                    "type": "integer"
                }
            },
            "one_of_field": {
                "oneof": [
                    {
                        "type": "string"
                    },
                    {
                        "type": "integer"
                    }
                ]
            },
            "string_pattern": {
                "type": "string",
                "pattern": "ABC",
            },
            "enum field": {
                "type": "enum",
                "choice": ["value", True, 0, 0.1, None]
            },
            "json_field": {
                "type": "json",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "field1": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
    strategy = generate(schema)
    strategy.validate()
    print(strategy.draw())
