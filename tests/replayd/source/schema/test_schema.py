import json
import xmltodict
from cerberus import Validator
from replayd.source.schema import generate


def _validate(doc, schema):
    v = Validator()
    return v.validate({"doc": doc}, {"doc": schema})

def test_base_dict():
    schema = {
        "type": "dict",
        "schema": {
            "field1": {
                "type": "string",
                "required": True,
            }
        }
    }
    data = generate(schema).draw()
    assert _validate(data, schema)


def test_nest_dict():
    schema = {
        "type": "dict",
        "schema": {
            "nest_dict_field": {
                "type": "dict",
                "schema": {
                    "field1": {
                        "type": "string",
                        "required": True,
                    }
                }
            }
        }
    }
    data = generate(schema).draw()
    assert _validate(data, schema)


def test_base_list():
    schema = {
        "type": "list",
        "schema": {
            "type": "integer",
            "required": True,
        }
    }
    data = generate(schema).draw()
    assert _validate(data, schema)


def test_list_of_dict():
    schema = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "field": {
                    "type": "boolean",
                    "required": True,
                }
            }
        }
    }
    data = generate(schema).draw()
    assert _validate(data, schema)


def test_json():
    schema = {
        "type": "json",
        "schema": {
            "type": "dict",
            "schema": {
                "field1": {
                    "type": "string",
                    "required": True,
                }
            }
        }
    }
    vschema = {
        "type": "dict",
        "schema": {
            "field1": {
                "type": "string",
                "required": True,
            }
        }
    }
    data = generate(schema).draw()
    assert _validate(json.loads(data), vschema)


def test_xml():
    schema = {
        "type": "xml",
        "schema": {
            "field1": {
                "type": "string",
                "min_size": 1,
                "required": True,
            }
        }
    }
    vschema = {
        "type": "dict",
        "schema": {
            "field1": {
                "type": "string",
                "required": True,
            }
        }
    }
    data = generate(schema).draw()
    print(data)
    print(xmltodict.parse(data))
    assert _validate(xmltodict.parse(data), vschema)


def test_string_join_json():
    schema = {
        "join": [
            {
                "type": "string",
                "pattern": r"\d{4}-\d{2}-\d{2}"
            },
            {
                "type": "json",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "field1": {
                            "type": "string",
                        }
                    }
                }
            }
        ]
    }
    vschema = {
        "type": "dict",
        "schema": {
            "field1": {
                "type": "string",
                "required": True,
            }
        }
    }
    data = generate(schema).draw()
    print(data)
    _validate(json.loads(data[11:]), vschema)


def test_scope_field():
    schema1 = {
        "type": "datetime_scope",
        "scope": "s1",
    }
    schema2 = {
        "type": "datetime_scope",
        "scope": "s1",
        "delta": 1000
    }
    schema3 = {
        "type": "datetime_scope",
        "scope": "s1",
        "delta": 1000
    }
    schema4 = {
        "type": "datetime_scope",
        "scope": "s2",
        "delta": 2000
    }
    date1 = generate(schema1).draw()
    date2 = generate(schema2).draw()
    date3 = generate(schema3).draw(version=1)
    date4 = generate(schema4).draw()
    print("date1: {0}, date2: {1}, date3: {2}, date4: {3}".format(*[date1, date2, date3, date4]))
    assert date1 == date2
    assert date1 != date3
    assert date1 != date4
